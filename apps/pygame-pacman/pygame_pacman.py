import argparse
import logging
import sys
from collections import deque

import pygame

WINDOW_TITLE = "Pac-Man"
FPS = 60
CELL_SIZE = 26
MAZE_COLS = 20
MAZE_ROWS = 20
WINDOW_WIDTH = MAZE_COLS * CELL_SIZE
WINDOW_HEIGHT = MAZE_ROWS * CELL_SIZE
GHOST_SPEED_FACTOR = 0.85
FRIGHTENED_DURATION = 8.0
SCATTER_DURATION = 7.0
CHASE_DURATION = 20.0

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
PINK = (255, 184, 255)
CYAN = (0, 255, 255)
ORANGE = (255, 184, 82)
BLUE = (0, 0, 255)
GRAY = (100, 100, 100)
DARK_GRAY = (50, 50, 50)
GHOST_COLORS = {"blinky": RED, "pinky": PINK, "inky": CYAN, "clyde": ORANGE}

MAZE_LAYOUT = [
    "WWWWWWWWWWWWWWWWWWWW",
    "W..................W",
    "W.WWWW.WWWW.WWWW.W.W",
    "W*WWWW.WWWW.WWWW*W.W",
    "W..................W",
    "W.WWWW..WW..WWWW.W.W",
    "W............W.....W",
    "WWWWW.WW.WW.WW.WWWWW",
    "WWWWW.W......W.WWWWW",
    "WWWWW.W......W.WWWWW",
    "WWWWW.WGGGGGGW.WWWWW",
    "WWWWW.W.DDDD.W.WWWWW",
    "WWWWW.W......W.WWWWW",
    "WWWWW.W......W.WWWWW",
    "W............W.....W",
    "W.WWWW..WW..WWWW.W.W",
    "W*................*W",
    "W.WWWW.WWWW.WWWW.W.W",
    "W..................W",
    "WWWWWWWWWWWWWWWWWWWW",
]

TILE_EMPTY = 0
TILE_WALL = 1
TILE_DOT = 2
TILE_POWER = 3
TILE_GHOST_HOUSE = 4
TILE_DOOR = 5

CHAR_MAP = {
    "W": TILE_WALL,
    ".": TILE_DOT,
    "*": TILE_POWER,
    "G": TILE_GHOST_HOUSE,
    "D": TILE_DOOR,
    " ": TILE_EMPTY,
}

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


def parse_maze(layout):
    grid = []
    dots = 0
    power_pellets = 0
    for row_idx, row_str in enumerate(layout):
        grid_row = []
        for col_idx, ch in enumerate(row_str):
            tile = CHAR_MAP.get(ch, TILE_EMPTY)
            grid_row.append(tile)
            if tile == TILE_DOT:
                dots += 1
            elif tile == TILE_POWER:
                power_pellets += 1
        grid.append(grid_row)
    return grid, dots + power_pellets


def is_walkable(tile, is_ghost=False, is_door_open=False):
    if tile == TILE_WALL:
        return False
    if tile == TILE_DOOR:
        return is_ghost
    if tile == TILE_GHOST_HOUSE:
        return is_ghost
    return True


def bfs_pathfind(grid, start, target, is_ghost=False, is_door_open=False):
    rows, cols = len(grid), len(grid[0])
    visited = [[False] * cols for _ in range(rows)]
    parent = [[None] * cols for _ in range(rows)]
    queue = deque()
    queue.append(start)
    visited[start[1]][start[0]] = True
    while queue:
        cx, cy = queue.popleft()
        if (cx, cy) == target:
            path = []
            while (cx, cy) != start:
                path.append((cx, cy))
                cx, cy = parent[cy][cx]
            path.reverse()
            return path
        for dx, dy in [RIGHT, LEFT, DOWN, UP]:
            nx, ny = cx + dx, cy + dy
            if 0 <= nx < cols and 0 <= ny < rows and not visited[ny][nx]:
                tile = grid[ny][nx]
                if is_walkable(tile, is_ghost, is_door_open) or (nx, ny) == target:
                    visited[ny][nx] = True
                    parent[ny][nx] = (cx, cy)
                    queue.append((nx, ny))
    return []


class Pacman:
    def __init__(self, col, row):
        self.x = col
        self.y = row
        self.direction = RIGHT
        self.next_direction = RIGHT
        self.speed = 1.0
        self.move_timer = 0.0
        self.move_interval = 0.12
        self.mouth_angle = 0
        self.mouth_open = True

    def set_direction(self, direction):
        self.next_direction = direction

    def can_move_to(self, grid, col, row):
        if row < 0 or row >= len(grid) or col < 0 or col >= len(grid[0]):
            return False
        tile = grid[row][col]
        return tile != TILE_WALL and tile != TILE_DOOR and tile != TILE_GHOST_HOUSE

    def update(self, dt, grid):
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
            return

        nx = self.x + self.direction[0]
        ny = self.y + self.direction[1]
        if self.can_move_to(grid, nx, ny):
            self.x = nx
            self.y = ny

    def eat_dot(self, grid):
        tile = grid[self.y][self.x]
        if tile == TILE_DOT:
            grid[self.y][self.x] = TILE_EMPTY
            return 10, False
        elif tile == TILE_POWER:
            grid[self.y][self.x] = TILE_EMPTY
            return 50, True
        return 0, False

    def draw(self, surface, cell_size, offset_x, offset_y):
        cx = offset_x + self.x * cell_size + cell_size // 2
        cy = offset_y + self.y * cell_size + cell_size // 2
        radius = cell_size // 2 - 1

        if self.direction == RIGHT:
            start_angle = 0.2
            end_angle = 2 * 3.14159 - 0.2
        elif self.direction == LEFT:
            start_angle = 3.14159 + 0.2
            end_angle = 3.14159 - 0.2
        elif self.direction == UP:
            start_angle = 1.5 * 3.14159 + 0.2
            end_angle = 1.5 * 3.14159 - 0.2
        else:
            start_angle = 0.5 * 3.14159 + 0.2
            end_angle = 0.5 * 3.14159 - 0.2

        pygame.draw.arc(
            surface, YELLOW,
            (cx - radius, cy - radius, radius * 2, radius * 2),
            min(start_angle, end_angle), max(start_angle, end_angle),
            radius,
        )
        eye_x = cx + (2 if self.direction == RIGHT else -2)
        eye_y = cy - radius // 2
        pygame.draw.circle(surface, BLACK, (eye_x, eye_y), 2)


class Ghost:
    # pacman_problem: Ghost pathfinding AI with state machine for classic chase/scatter/frightened behavior
    def __init__(self, name, col, row, scatter_target):
        self.name = name
        self.x = col
        self.y = row
        self.start_x = col
        self.start_y = row
        self.color = GHOST_COLORS[name]
        self.direction = UP
        self.scatter_target = scatter_target
        self.speed = GHOST_SPEED_FACTOR
        self.move_timer = 0.0
        self.move_interval = 0.15
        self.state = "SCATTER"
        self.frightened_timer = 0.0
        self.eaten = False
        self.returning = False
        self.in_house = True
        self.leave_timer = 0.0

    def get_target(self, pacman, blinky_pos):
        # pacman_problem: Ghost pathfinding AI with distinct personalities
        if self.returning:
            return (self.start_x, self.start_y - 2)
        if self.state == "CHASE":
            if self.name == "blinky":
                return (pacman.x, pacman.y)
            elif self.name == "pinky":
                return (pacman.x + pacman.direction[0] * 4, pacman.y + pacman.direction[1] * 4)
            elif self.name == "inky":
                ahead = (pacman.x + pacman.direction[0] * 2, pacman.y + pacman.direction[1] * 2)
                if blinky_pos:
                    dx = ahead[0] - blinky_pos[0]
                    dy = ahead[1] - blinky_pos[1]
                    return (ahead[0] + dx, ahead[1] + dy)
                return ahead
            elif self.name == "clyde":
                dist = abs(self.x - pacman.x) + abs(self.y - pacman.y)
                if dist > 8:
                    return (pacman.x, pacman.y)
                return self.scatter_target
        elif self.state == "FRIGHTENED":
            return None
        return self.scatter_target

    def update(self, dt, grid, pacman, blinky_pos):
        if self.state == "FRIGHTENED":
            self.frightened_timer -= dt
            if self.frightened_timer <= 0:
                self.state = "CHASE"
                self.frightened_timer = 0.0

        if self.eaten:
            self.move_timer += dt
            if self.move_timer < self.move_interval * 0.5:
                return
            self.move_timer = 0.0
            target = (self.start_x, self.start_y - 1)
            if (self.x, self.y) == target:
                self.eaten = False
                self.returning = False
                self.state = "CHASE"
                self.in_house = True
                self.leave_timer = 0.0
                return
            path = bfs_pathfind(grid, (self.x, self.y), target, is_ghost=True, is_door_open=True)
            if path:
                self.x, self.y = path[0]
            return

        if self.in_house:
            self.leave_timer += dt
            if self.leave_timer < 1.0:
                return
            for dy in range(-1, 0):
                ny = self.y + dy
                if 0 <= ny < len(grid) and is_walkable(grid[ny][self.x], True, True):
                    self.y = ny
                    if ny <= 9:
                        self.in_house = False
                    return
            self.in_house = False
            return

        self.move_timer += dt
        if self.move_timer < self.move_interval:
            return
        self.move_timer = 0.0

        if self.state == "FRIGHTENED":
            directions = [UP, DOWN, LEFT, RIGHT]
            opposite = (-self.direction[0], -self.direction[1])
            candidates = []
            for d in directions:
                if d == opposite:
                    continue
                nx, ny = self.x + d[0], self.y + d[1]
                if 0 <= ny < len(grid) and 0 <= nx < len(grid[0]):
                    tile = grid[ny][nx]
                    if is_walkable(tile, True, True):
                        candidates.append(d)
            if candidates:
                import random
                self.direction = random.choice(candidates)
                self.x += self.direction[0]
                self.y += self.direction[1]
            return

        target = self.get_target(pacman, blinky_pos)
        if target:
            path = bfs_pathfind(grid, (self.x, self.y), target, is_ghost=True, is_door_open=True)
            if path:
                nx, ny = path[0]
                self.direction = (nx - self.x, ny - self.y)
                self.x = nx
                self.y = ny

    def draw(self, surface, cell_size, offset_x, offset_y):
        cx = offset_x + self.x * cell_size + cell_size // 2
        cy = offset_y + self.y * cell_size + cell_size // 2
        radius = cell_size // 2 - 2

        color = BLUE if self.state == "FRIGHTENED" else self.color
        if self.eaten:
            return

        pygame.draw.circle(surface, color, (cx, cy), radius)
        pygame.draw.circle(surface, BLACK, (cx, cy), radius, 1)

        eye_offsets = [(-3, -3), (3, -3)]
        for eo in eye_offsets:
            eye_x = cx + eo[0]
            eye_y = cy + eo[1]
            pygame.draw.circle(surface, WHITE, (eye_x, eye_y), 3)
            pygame.draw.circle(surface, BLACK, (eye_x, eye_y), 1)


class Game:
    def __init__(self, args):
        self.logger = logging.getLogger("PacMan")
        self.logger.setLevel(getattr(logging, args.log_level.upper(), logging.INFO))
        self.cell_size = args.cell_size
        self.cols = MAZE_COLS
        self.rows = MAZE_ROWS
        self.window_width = self.cols * self.cell_size
        self.window_height = self.rows * self.cell_size
        self.move_interval = args.speed
        self.score = 0
        self.lives = 3
        self.game_over = False
        self.won = False
        self.paused = False
        self.phase_timer = 0.0
        self.is_chase_mode = False
        self.total_dots = 0
        self.ghost_combo = 0

        # pacman_constraint: use logger for human/AI debugging
        self.logger.info("Initializing Pac-Man game: %dx%d grid, cell=%dpx", self.cols, self.rows, self.cell_size)

        pygame.init()
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 22)
        self.big_font = pygame.font.Font(None, 36)
        self.running = True

        self.grid, self.total_dots = parse_maze(MAZE_LAYOUT)
        self.logger.debug("Total dots in maze: %d", self.total_dots)

        self.pacman = Pacman(10, 18)

        # pacman_problem: Ghost pathfinding AI with distinct scatter corners
        scatter_targets = {
            "blinky": (18, 1),
            "pinky": (1, 1),
            "inky": (18, 18),
            "clyde": (1, 18),
        }
        self.ghosts = [
            Ghost("blinky", 9, 10, scatter_targets["blinky"]),
            Ghost("pinky", 10, 10, scatter_targets["pinky"]),
            Ghost("inky", 11, 10, scatter_targets["inky"]),
            Ghost("clyde", 12, 10, scatter_targets["clyde"]),
        ]
        self.ghosts[0].in_house = False
        self.ghosts[0].leave_timer = 999.0

        self.logger.info("Game initialized. Dots: %d, Lives: %d", self.total_dots, self.lives)

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
                elif event.key in DIRECTION_KEYS and not self.game_over and not self.won:
                    self.pacman.set_direction(DIRECTION_KEYS[event.key])

    def reset_game(self):
        self.logger.info("Game reset")
        self.grid, self.total_dots = parse_maze(MAZE_LAYOUT)
        self.pacman = Pacman(10, 18)
        scatter_targets = {
            "blinky": (18, 1),
            "pinky": (1, 1),
            "inky": (18, 18),
            "clyde": (1, 18),
        }
        self.ghosts = [
            Ghost("blinky", 9, 10, scatter_targets["blinky"]),
            Ghost("pinky", 10, 10, scatter_targets["pinky"]),
            Ghost("inky", 11, 10, scatter_targets["inky"]),
            Ghost("clyde", 12, 10, scatter_targets["clyde"]),
        ]
        self.ghosts[0].in_house = False
        self.ghosts[0].leave_timer = 999.0
        self.score = 0
        self.lives = 3
        self.game_over = False
        self.won = False
        self.phase_timer = 0.0
        self.is_chase_mode = False
        self.ghost_combo = 0

    def check_ghost_collisions(self):
        px, py = self.pacman.x, self.pacman.y
        for ghost in self.ghosts:
            if ghost.eaten or ghost.in_house:
                continue
            if (ghost.x, ghost.y) == (px, py):
                if ghost.state == "FRIGHTENED":
                    ghost.eaten = True
                    ghost.returning = True
                    self.ghost_combo += 1
                    points = 200 * (2 ** (self.ghost_combo - 1))
                    self.score += points
                    self.logger.debug("Ate ghost %s! +%d points", ghost.name, points)
                else:
                    self.lives -= 1
                    self.logger.debug("Pac-Man caught by %s! Lives left: %d", ghost.name, self.lives)
                    if self.lives <= 0:
                        self.game_over = True
                    else:
                        self.respawn()

    def respawn(self):
        self.pacman = Pacman(10, 18)
        scatter_targets = {
            "blinky": (18, 1),
            "pinky": (1, 1),
            "inky": (18, 18),
            "clyde": (1, 18),
        }
        self.ghosts = [
            Ghost("blinky", 9, 10, scatter_targets["blinky"]),
            Ghost("pinky", 10, 10, scatter_targets["pinky"]),
            Ghost("inky", 11, 10, scatter_targets["inky"]),
            Ghost("clyde", 12, 10, scatter_targets["clyde"]),
        ]
        self.ghosts[0].in_house = False
        self.ghosts[0].leave_timer = 999.0
        self.ghost_combo = 0
        self.phase_timer = 0.0
        self.is_chase_mode = False
        self.logger.info("Pac-Man respawned")

    # pacman_problem: state machine for ghost mode cycling between scatter/chase
    def update_ghost_phase(self, dt):
        if any(g.state == "FRIGHTENED" for g in self.ghosts):
            return
        self.phase_timer += dt
        phase_duration = CHASE_DURATION if self.is_chase_mode else SCATTER_DURATION
        if self.phase_timer >= phase_duration:
            self.is_chase_mode = not self.is_chase_mode
            self.phase_timer = 0.0
            new_state = "CHASE" if self.is_chase_mode else "SCATTER"
            for ghost in self.ghosts:
                if ghost.state != "FRIGHTENED" and not ghost.eaten:
                    ghost.state = new_state
            self.logger.debug("Ghost mode switched to: %s", new_state)

    def update(self, dt):
        if self.game_over or self.won or self.paused:
            return

        self.pacman.update(dt, self.grid)
        self.update_ghost_phase(dt)

        score_gained, is_power = self.pacman.eat_dot(self.grid)
        if score_gained > 0:
            self.score += score_gained
            self.logger.debug("Score: %d, Ate: %s", self.score,
                              "power pellet" if is_power else "dot")
            if is_power:
                for ghost in self.ghosts:
                    if not ghost.eaten:
                        ghost.state = "FRIGHTENED"
                        ghost.frightened_timer = FRIGHTENED_DURATION
                self.ghost_combo = 0

        remaining = sum(row.count(TILE_DOT) + row.count(TILE_POWER) for row in self.grid)
        if remaining == 0:
            self.won = True
            self.logger.info("All dots eaten! Player wins!")

        blinky_pos = (self.ghosts[0].x, self.ghosts[0].y) if not self.ghosts[0].eaten else None
        for ghost in self.ghosts:
            ghost.update(dt, self.grid, self.pacman, blinky_pos)

        self.check_ghost_collisions()

    def draw_grid(self):
        for row_idx, row in enumerate(self.grid):
            for col_idx, tile in enumerate(row):
                x = col_idx * self.cell_size
                y = row_idx * self.cell_size
                if tile == TILE_WALL:
                    pygame.draw.rect(self.screen, DARK_GRAY, (x, y, self.cell_size, self.cell_size))
                elif tile == TILE_DOT:
                    center = (x + self.cell_size // 2, y + self.cell_size // 2)
                    pygame.draw.circle(self.screen, WHITE, center, 2)
                elif tile == TILE_POWER:
                    center = (x + self.cell_size // 2, y + self.cell_size // 2)
                    pygame.draw.circle(self.screen, WHITE, center, 5)
                elif tile == TILE_GHOST_HOUSE:
                    pygame.draw.rect(self.screen, (30, 30, 30), (x, y, self.cell_size, self.cell_size))
                elif tile == TILE_DOOR:
                    pygame.draw.rect(self.screen, PINK, (x, y, self.cell_size, self.cell_size // 3))

    def draw(self):
        self.screen.fill(BLACK)
        self.draw_grid()
        self.pacman.draw(self.screen, self.cell_size, 0, 0)
        for ghost in self.ghosts:
            ghost.draw(self.screen, self.cell_size, 0, 0)

        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (5, 5))

        lives_text = self.font.render(f"Lives: {self.lives}", True, WHITE)
        self.screen.blit(lives_text, (self.window_width - 80, 5))

        if self.game_over:
            text = self.big_font.render("GAME OVER", True, RED)
            text_rect = text.get_rect(center=(self.window_width // 2, self.window_height // 2 - 20))
            self.screen.blit(text, text_rect)
            restart = self.font.render("Press R to restart, ESC to quit", True, WHITE)
            restart_rect = restart.get_rect(center=(self.window_width // 2, self.window_height // 2 + 10))
            self.screen.blit(restart, restart_rect)

        if self.won:
            text = self.big_font.render("YOU WIN!", True, YELLOW)
            text_rect = text.get_rect(center=(self.window_width // 2, self.window_height // 2 - 20))
            self.screen.blit(text, text_rect)
            restart = self.font.render("Press R to restart, ESC to quit", True, WHITE)
            restart_rect = restart.get_rect(center=(self.window_width // 2, self.window_height // 2 + 10))
            self.screen.blit(restart, restart_rect)

        if self.paused:
            pause = self.big_font.render("PAUSED", True, WHITE)
            pause_rect = pause.get_rect(center=(self.window_width // 2, self.window_height // 2))
            self.screen.blit(pause, pause_rect)

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
    parser.add_argument("--cell-size", type=int, default=CELL_SIZE,
                        help="Cell size in pixels (default: %(default)s)")
    parser.add_argument("--speed", type=float, default=0.12,
                        help="Time in seconds between Pac-Man moves (default: %(default)s)")
    parser.add_argument("--ghost-speed", type=float, default=0.15,
                        help="Time in seconds between ghost moves (default: %(default)s)")
    parser.add_argument("--frightened-duration", type=float, default=FRIGHTENED_DURATION,
                        help="Duration of frightened mode in seconds (default: %(default)s)")
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
