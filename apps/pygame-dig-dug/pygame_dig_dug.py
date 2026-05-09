import argparse
import logging
import sys
from collections import deque

import pygame

WINDOW_TITLE = "Dig Dug"
FPS = 60
CELL_SIZE = 24
MAP_COLS = 26
MAP_ROWS = 22
WINDOW_WIDTH = MAP_COLS * CELL_SIZE
WINDOW_HEIGHT = MAP_ROWS * CELL_SIZE

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BROWN = (139, 90, 43)
DARK_BROWN = (101, 67, 33)
GRAY = (128, 128, 128)
DARK_GRAY = (60, 60, 60)
PLAYER_COLOR = (0, 200, 255)

TILE_WALL = 0
TILE_DIRT = 1
TILE_TUNNEL = 2
TILE_ROCK = 3

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

DIRECTION_KEYS = {
    pygame.K_UP: UP,
    pygame.K_DOWN: DOWN,
    pygame.K_LEFT: LEFT,
    pygame.K_RIGHT: RIGHT,
}

ROCK_FALL_TILES = {TILE_TUNNEL, TILE_DIRT}
ENEMY_MOVE_INTERVAL = 0.22

MAP_LAYOUT = [
    "WWWWWWWWWWWWWWWWWWWWWWWWWW",
    "W........................W",
    "W.DDDDD..DDDDDDD..DDDDDD.W",
    "W.DDDDD..DDDDDDD..DDDDDD.W",
    "W.DDDDD..DDDDDDD..DDDDDD.W",
    "W..RRR......RRR..........W",
    "W.DDDDD..DDDDDDD..DDDDDD.W",
    "W.DDDDD..DDDDDDD..DDDDDD.W",
    "W.DDDDD..DDDDDDD..DDDDDD.W",
    "W.....................R..W",
    "W.DDDDD..DDDDDDD..DDDDDD.W",
    "W.DDDDD..DDDDDDD..DDDDDD.W",
    "W.DDDDD..DDDDDDD..DDDDDD.W",
    "W.........RRR......RRR...W",
    "W.DDDDD..DDDDDDD..DDDDDD.W",
    "W.DDDDD..DDDDDDD..DDDDDD.W",
    "W.DDDDD..DDDDDDD..DDDDDD.W",
    "W...........RRR..........W",
    "W.DDDDD..DDDDDDD..DDDDDD.W",
    "W.DDDDD..DDDDDDD..DDDDDD.W",
    "W.DDDDD..DDDDDDD..DDDDDD.W",
    "WWWWWWWWWWWWWWWWWWWWWWWWWW",
]

TILE_CHARS = {
    "W": TILE_WALL,
    ".": TILE_TUNNEL,
    "D": TILE_DIRT,
    "R": TILE_ROCK,
}


def parse_map(layout):
    grid = []
    rocks = []
    for row_idx, row_str in enumerate(layout):
        grid_row = []
        for col_idx, ch in enumerate(row_str):
            tile = TILE_CHARS.get(ch, TILE_WALL)
            grid_row.append(tile)
            if tile == TILE_ROCK:
                rocks.append((col_idx, row_idx))
        grid.append(grid_row)
    return grid, rocks


def bfs_pathfind(grid, start, target, max_dist=50):
    rows = len(grid)
    cols = len(grid[0])
    tx, ty = target
    if not (0 <= tx < cols and 0 <= ty < rows):
        return []
    visited = [[False] * cols for _ in range(rows)]
    parent = [[None] * cols for _ in range(rows)]
    queue = deque()
    queue.append(start)
    visited[start[1]][start[0]] = True
    dist = {start: 0}
    while queue:
        cx, cy = queue.popleft()
        if (cx, cy) == target:
            path = []
            while (cx, cy) != start:
                path.append((cx, cy))
                cx, cy = parent[cy][cx]
            path.reverse()
            return path
        if dist.get((cx, cy), 0) >= max_dist:
            continue
        for dx, dy in [RIGHT, LEFT, DOWN, UP]:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < cols and 0 <= ny < rows and not visited[ny][nx]:
                tile = grid[ny][nx]
                if tile == TILE_TUNNEL or tile == TILE_DIRT:
                    visited[ny][nx] = True
                    parent[ny][nx] = (cx, cy)
                    dist[(nx, ny)] = dist.get((cx, cy), 0) + 1
                    queue.append((nx, ny))
    return []


class Player:
    def __init__(self, col, row):
        self.x = col
        self.y = row
        self.direction = RIGHT
        self.next_direction = RIGHT
        self.move_timer = 0.0
        self.move_interval = 0.1
        self.pump_active = False
        self.pump_timer = 0.0
        self.pump_duration = 0.3
        self.pump_reach = 3
        self.invincible_timer = 0.0
        self.invincible_duration = 1.5

    def set_direction(self, direction):
        self.next_direction = direction

    def can_move_to(self, grid, col, row):
        if row < 0 or row >= len(grid) or col < 0 or col >= len(grid[0]):
            return False
        return grid[row][col] not in (TILE_WALL, TILE_ROCK)

    def dig_tunnel(self, grid):
        if grid[self.y][self.x] == TILE_DIRT:
            grid[self.y][self.x] = TILE_TUNNEL
            return True
        return False

    def update(self, dt, grid):
        if self.invincible_timer > 0:
            self.invincible_timer -= dt
        self.move_timer += dt
        if self.move_timer < self.move_interval:
            return
        self.move_timer = 0.0

        nx = self.x + self.next_direction[0]
        ny = self.y + self.next_direction[1]
        if self.can_move_to(grid, nx, ny):
            self.direction = self.next_direction
            self.x = nx
            self.y = ny
            self.dig_tunnel(grid)
            return

        nx = self.x + self.direction[0]
        ny = self.y + self.direction[1]
        if self.can_move_to(grid, nx, ny):
            self.x = nx
            self.y = ny
            self.dig_tunnel(grid)

    def pump(self):
        self.pump_active = True
        self.pump_timer = self.pump_duration

    def update_pump(self, dt):
        if self.pump_active:
            self.pump_timer -= dt
            if self.pump_timer <= 0:
                self.pump_active = False
                self.pump_timer = 0.0

    def get_pump_cells(self):
        cells = []
        for i in range(1, self.pump_reach + 1):
            cells.append((
                self.x + self.direction[0] * i,
                self.y + self.direction[1] * i,
            ))
        return cells

    def draw(self, surface, cell_size):
        cx = self.x * cell_size + cell_size // 2
        cy = self.y * cell_size + cell_size // 2
        r = cell_size // 2 - 2

        if self.invincible_timer > 0 and int(self.invincible_timer * 10) % 2 == 0:
            return

        pygame.draw.circle(surface, PLAYER_COLOR, (cx, cy), r)
        pygame.draw.circle(surface, BLACK, (cx, cy), r, 1)

        eye_off_x = 3 if self.direction == RIGHT else -3 if self.direction == LEFT else 0
        eye_off_y = 3 if self.direction == DOWN else -3 if self.direction == UP else 0

        pygame.draw.circle(surface, WHITE, (cx + eye_off_x - 2, cy + eye_off_y - 1), 2)
        pygame.draw.circle(surface, WHITE, (cx + eye_off_x + 2, cy + eye_off_y - 1), 2)
        pygame.draw.circle(surface, BLACK, (cx + eye_off_x - 2, cy + eye_off_y - 1), 1)
        pygame.draw.circle(surface, BLACK, (cx + eye_off_x + 2, cy + eye_off_y - 1), 1)

        if self.pump_active:
            pump_cells = self.get_pump_cells()
            frac_done = 1.0 - (self.pump_timer / self.pump_duration)
            visible = int(len(pump_cells) * frac_done)
            for i in range(min(visible, len(pump_cells))):
                px, py = pump_cells[i]
                pcx = px * cell_size + cell_size // 2
                pcy = py * cell_size + cell_size // 2
                pr = 3 + i * 2
                pygame.draw.circle(surface, YELLOW, (pcx, pcy), pr, 2)


class Enemy:
    def __init__(self, col, row, enemy_type="pooka"):
        self.x = col
        self.y = row
        self.start_x = col
        self.start_y = row
        self.enemy_type = enemy_type
        self.direction = DOWN
        self.move_timer = 0.0
        self.move_interval = ENEMY_MOVE_INTERVAL
        self.inflation = 0.0
        self.inflating = False
        self.dead = False
        self.death_timer = 0.0
        self.dig_cooldown = 0.0
        self.spawn_delay = 0.5
        self.spawn_timer = 0.0

    def reset(self):
        self.x = self.start_x
        self.y = self.start_y
        self.direction = DOWN
        self.move_timer = 0.0
        self.inflation = 0.0
        self.inflating = False
        self.dead = False
        self.death_timer = 0.0
        self.spawn_timer = 0.0
        self.dig_cooldown = 0.0

    def update(self, dt, grid, player_pos):
        if self.dead:
            self.death_timer += dt
            return

        self.spawn_timer += dt
        if self.spawn_timer < self.spawn_delay:
            return

        if self.inflating:
            self.inflation += dt * 0.5
            if self.inflation >= 1.0:
                self.dead = True
                self.death_timer = 0.0
            return

        if self.dig_cooldown > 0:
            self.dig_cooldown -= dt

        self.move_timer += dt
        if self.move_timer < self.move_interval:
            return
        self.move_timer = 0.0

        px, py = player_pos
        target = (px, py)
        path = bfs_pathfind(grid, (self.x, self.y), target, max_dist=30)
        if path:
            self.x, self.y = path[0]
            self.direction = (path[0][0] - self.x, path[0][1] - self.y)
            return

        if self.dig_cooldown <= 0:
            for dx, dy in [RIGHT, LEFT, DOWN, UP]:
                nx, ny = self.x + dx, self.y + dy
                if 0 <= ny < len(grid) and 0 <= nx < len(grid[0]):
                    if grid[ny][nx] == TILE_DIRT:
                        grid[ny][nx] = TILE_TUNNEL
                        self.x = nx
                        self.y = ny
                        self.direction = (dx, dy)
                        self.dig_cooldown = 0.5
                        return

        for dx, dy in [RIGHT, LEFT, DOWN, UP]:
            nx, ny = self.x + dx, self.y + dy
            if 0 <= ny < len(grid) and 0 <= nx < len(grid[0]):
                if grid[ny][nx] == TILE_TUNNEL:
                    self.x = nx
                    self.y = ny
                    self.direction = (dx, dy)
                    return

    def start_inflate(self):
        if not self.dead and not self.inflating:
            self.inflating = True
            self.inflation = 0.0

    def draw(self, surface, cell_size):
        if self.dead and self.death_timer > 0.8:
            return

        cx = self.x * cell_size + cell_size // 2
        cy = self.y * cell_size + cell_size // 2

        if self.dead:
            if int(self.death_timer * 10) % 3 == 0:
                text = pygame.font.Font(None, cell_size).render("POP!", True, YELLOW)
                text_rect = text.get_rect(center=(cx, cy))
                surface.blit(text, text_rect)
            return

        base_r = cell_size // 2 - 2
        if self.inflating:
            base_r = int((cell_size // 2 - 2) * (1 + self.inflation * 1.5))

        color = RED
        pygame.draw.circle(surface, color, (cx, cy), base_r)
        pygame.draw.circle(surface, BLACK, (cx, cy), base_r, 1)

        if not self.inflating:
            eye_y = cy - 3
            pygame.draw.circle(surface, WHITE, (cx - 3, eye_y), 3)
            pygame.draw.circle(surface, WHITE, (cx + 3, eye_y), 3)
            pygame.draw.circle(surface, BLACK, (cx - 3, eye_y), 1)
            pygame.draw.circle(surface, BLACK, (cx + 3, eye_y), 1)


class Game:
    def __init__(self, args):
        self.logger = logging.getLogger("DigDug")
        self.logger.setLevel(getattr(logging, args.log_level.upper(), logging.INFO))
        self.cell_size = args.cell_size
        self.score = 0
        self.lives = 3
        self.game_over = False
        self.won = False
        self.paused = False
        self.level = 1
        self.enemies_per_level = args.enemies

        self.logger.info(
            "Initializing Dig Dug: %dx%d grid, cell=%dpx, enemies=%d",
            MAP_COLS, MAP_ROWS, self.cell_size, self.enemies_per_level,
        )

        pygame.init()
        pygame.display.set_caption(WINDOW_TITLE)
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 20)
        self.big_font = pygame.font.Font(None, 36)
        self.running = True

        self.reset_level()

    def reset_level(self):
        self.grid, self.rocks = parse_map(MAP_LAYOUT)
        self.player = Player(13, 9)
        self.enemies = []
        spawn_points = [(2, 1), (13, 1), (23, 1)]
        for i in range(min(self.enemies_per_level, len(spawn_points))):
            self.enemies.append(Enemy(spawn_points[i][0], spawn_points[i][1], "pooka"))
        self.rocks_data = []
        for rx, ry in self.rocks:
            self.rocks_data.append({"x": rx, "y": ry, "falling": False})
        self.logger.info(
            "Level %d: %d enemies, %d rocks",
            self.level, len(self.enemies), len(self.rocks_data),
        )

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_r and (self.game_over or self.won):
                    self.reset_game()
                elif event.key == pygame.K_p:
                    self.paused = not self.paused
                elif event.key == pygame.K_SPACE and not self.game_over and not self.won:
                    self.player.pump()
                elif event.key in DIRECTION_KEYS and not self.game_over and not self.won:
                    self.player.set_direction(DIRECTION_KEYS[event.key])

    def reset_game(self):
        self.logger.info("Game reset")
        self.score = 0
        self.lives = 3
        self.level = 1
        self.game_over = False
        self.won = False
        self.reset_level()

    def check_pump_hits(self):
        if not self.player.pump_active:
            return
        pump_cells = self.player.get_pump_cells()
        for enemy in self.enemies:
            if enemy.dead:
                continue
            if (enemy.x, enemy.y) in pump_cells and not enemy.inflating:
                enemy.start_inflate()
                self.logger.debug("Pump hit enemy at (%d,%d)", enemy.x, enemy.y)

    def update_rocks(self, dt):
        rows = len(self.grid)
        for rock in self.rocks_data:
            rx, ry = rock["x"], rock["y"]
            below = ry + 1
            if below >= rows:
                continue
            below_tile = self.grid[below][rx]
            if below_tile == TILE_TUNNEL:
                rock["falling"] = True
            if rock["falling"]:
                if below_tile not in ROCK_FALL_TILES:
                    rock["falling"] = False
                    continue
                self.grid[ry][rx] = TILE_TUNNEL
                rock["y"] = below
                self.grid[below][rx] = TILE_ROCK
                for enemy in self.enemies:
                    if not enemy.dead and (enemy.x, enemy.y) == (rx, below):
                        enemy.dead = True
                        enemy.death_timer = 0.0
                        self.score += 2000
                        self.logger.debug("Rock crushed enemy! +2000")
                self.logger.debug("Rock fell (%d,%d)->(%d,%d)", rx, ry, rx, below)

    def check_enemies_cleared(self):
        alive = sum(1 for e in self.enemies if not e.dead)
        if alive == 0 and not self.won:
            self.won = True
            self.logger.info("All enemies cleared!")

    def update(self, dt):
        if self.game_over or self.won or self.paused:
            return

        self.player.update(dt, self.grid)
        self.player.update_pump(dt)
        self.check_pump_hits()
        self.update_rocks(dt)

        player_pos = (self.player.x, self.player.y)
        for enemy in self.enemies:
            enemy.update(dt, self.grid, player_pos)

        if self.player.invincible_timer <= 0:
            for enemy in self.enemies:
                if enemy.dead:
                    continue
                if (enemy.x, enemy.y) == player_pos:
                    self.lives -= 1
                    self.logger.debug("Player caught! Lives: %d", self.lives)
                    if self.lives <= 0:
                        self.game_over = True
                    else:
                        self.respawn()
                    break

        self.check_enemies_cleared()

    def respawn(self):
        self.player = Player(13, 9)
        self.player.invincible_timer = self.player.invincible_duration
        for enemy in self.enemies:
            enemy.reset()
        self.logger.info("Player respawned")

    def draw_grid(self):
        for row_idx, row in enumerate(self.grid):
            for col_idx, tile in enumerate(row):
                x = col_idx * self.cell_size
                y = row_idx * self.cell_size
                if tile == TILE_WALL:
                    pygame.draw.rect(self.screen, DARK_GRAY, (x, y, self.cell_size, self.cell_size))
                elif tile == TILE_DIRT:
                    pygame.draw.rect(self.screen, BROWN, (x, y, self.cell_size, self.cell_size))
                    dot_x = x + self.cell_size // 2
                    dot_y = y + self.cell_size // 2
                    pygame.draw.circle(self.screen, DARK_BROWN, (dot_x, dot_y), 2)
                elif tile == TILE_TUNNEL:
                    pygame.draw.rect(self.screen, (20, 20, 20), (x, y, self.cell_size, self.cell_size))
                elif tile == TILE_ROCK:
                    pygame.draw.rect(self.screen, GRAY, (x, y, self.cell_size, self.cell_size))
                    inner = 2
                    pygame.draw.rect(
                        self.screen, DARK_GRAY,
                        (x + inner, y + inner, self.cell_size - inner * 2, self.cell_size - inner * 2),
                    )

    def draw_hud(self):
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (5, 5))
        lives_text = self.font.render(f"Lives: {self.lives}", True, WHITE)
        self.screen.blit(lives_text, (WINDOW_WIDTH - 80, 5))
        alive = sum(1 for e in self.enemies if not e.dead)
        enemies_text = self.font.render(f"Enemies: {alive}", True, WHITE)
        self.screen.blit(enemies_text, (WINDOW_WIDTH // 2 - 40, 5))
        controls = self.font.render("Arrows: Move | Space: Pump | P: Pause | ESC: Quit", True, GRAY)
        self.screen.blit(controls, (5, WINDOW_HEIGHT - 16))

    def draw_overlay(self):
        if self.game_over:
            text = self.big_font.render("GAME OVER", True, RED)
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 20))
            self.screen.blit(text, text_rect)
            restart = self.font.render("Press R to restart, ESC to quit", True, WHITE)
            restart_rect = restart.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 10))
            self.screen.blit(restart, restart_rect)
        elif self.won:
            text = self.big_font.render("LEVEL CLEAR!", True, GREEN)
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 20))
            self.screen.blit(text, text_rect)
            msg = self.font.render("Press R to continue, ESC to quit", True, WHITE)
            msg_rect = msg.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 10))
            self.screen.blit(msg, msg_rect)
        elif self.paused:
            pause = self.big_font.render("PAUSED", True, WHITE)
            pause_rect = pause.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            self.screen.blit(pause, pause_rect)

    def draw(self):
        self.screen.fill(BLACK)
        self.draw_grid()
        self.player.draw(self.screen, self.cell_size)
        for enemy in self.enemies:
            enemy.draw(self.screen, self.cell_size)
        self.draw_hud()
        self.draw_overlay()
        pygame.display.flip()

    def run(self):
        self.logger.info("Game started")
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            self.handle_events()
            self.update(dt)
            self.draw()
        self.logger.info("Game ended")
        pygame.quit()
        sys.exit()


def parse_args(argv):
    parser = argparse.ArgumentParser(description=WINDOW_TITLE)
    parser.add_argument(
        "--cell-size", type=int, default=CELL_SIZE,
        help="Cell size in pixels (default: %(default)s)",
    )
    parser.add_argument(
        "--speed", type=float, default=0.1,
        help="Time in seconds between player moves (default: %(default)s)",
    )
    parser.add_argument(
        "--enemies", type=int, default=3,
        help="Number of enemies per level (default: %(default)s)",
    )
    parser.add_argument(
        "--log-level",
        type=str,
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help="Logging level (default: %(default)s)",
    )
    return parser.parse_args(argv)


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    args = parse_args(argv)
    logging.basicConfig(
        format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
        level=getattr(logging, args.log_level.upper(), logging.INFO),
        datefmt="%H:%M:%S",
    )
    game = Game(args)
    game.run()


if __name__ == "__main__":
    main()
