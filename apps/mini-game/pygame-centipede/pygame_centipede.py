import argparse
import logging
import sys
import random

import pygame

# Constraint: 極簡風格 - minimal constants, no bloat
WINDOW_TITLE = "Centipede"
FPS = 60
CELL_SIZE = 20
GRID_COLS = 40
GRID_ROWS = 28
WINDOW_WIDTH = GRID_COLS * CELL_SIZE
WINDOW_HEIGHT = (GRID_ROWS + 3) * CELL_SIZE  # extra rows for player area
PLAYER_Y = (GRID_ROWS + 1) * CELL_SIZE
PLAYER_SPEED = 300.0
BULLET_SPEED = 400.0
SHOOT_COOLDOWN = 0.25
CENTIPEDE_MOVE_INTERVAL = 0.08
INITIAL_MUSHROOM_COUNT = 24
INITIAL_LIVES = 3
INITIAL_CENTIPEDE_LENGTH = 12
INVINCIBLE_TIME = 2.0
SEGMENT_SCORE = 10
MUSHROOM_SCORE = 5

# Constraint: 極簡呈現 - minimal palette
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (60, 60, 60)
DARK_GREEN = (0, 120, 0)
RED = (200, 0, 0)


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.alive = True
        self.invincible = False
        self.invincible_timer = 0.0

    def move_left(self, dt):
        self.x -= PLAYER_SPEED * dt
        if self.x < 10:
            self.x = 10

    def move_right(self, dt):
        self.x += PLAYER_SPEED * dt
        if self.x > WINDOW_WIDTH - 10:
            self.x = WINDOW_WIDTH - 10

    def update(self, dt):
        if self.invincible:
            self.invincible_timer -= dt
            if self.invincible_timer <= 0:
                self.invincible = False

    # Task: Segmented enemies - player shoots upward at centipede
    def draw(self, surface):
        if not self.alive:
            return
        if self.invincible and int(self.invincible_timer * 10) % 2 == 0:
            return
        half = 10
        points = [
            (self.x, self.y - half),
            (self.x - half, self.y + half),
            (self.x + half, self.y + half),
        ]
        pygame.draw.polygon(surface, WHITE, points, 2)


class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.alive = True

    def update(self, dt):
        self.y -= BULLET_SPEED * dt
        if self.y < 0:
            self.alive = False

    def draw(self, surface):
        pygame.draw.rect(surface, WHITE, (self.x - 2, self.y - 5, 4, 10))


# Task: Segmented enemies, Terrain interaction, Splitting
class Centipede:
    def __init__(self, col, row, length, direction):
        # head-first list of (col, row) grid positions
        self.positions = [(col - i, row) for i in range(length)]
        self.direction = direction  # 1 = right, -1 = left
        self.move_timer = CENTIPEDE_MOVE_INTERVAL
        self.alive = True

    # Task: Terrain interaction - centipede dodges mushrooms
    def update(self, dt, mushrooms):
        if not self.alive:
            return
        self.move_timer -= dt
        if self.move_timer > 0:
            return
        self.move_timer += CENTIPEDE_MOVE_INTERVAL

        col, row = self.positions[0]
        next_col = col + self.direction

        # Check edge collision
        if next_col < 0 or next_col >= GRID_COLS:
            new_pos = (col, row + 1)
            self.direction *= -1
        # Check mushroom collision
        elif (next_col, row) in mushrooms:
            new_pos = (col, row + 1)
            self.direction *= -1
        else:
            new_pos = (next_col, row)

        self.positions.insert(0, new_pos)
        self.positions.pop()

        # Wrap centipede to top if it goes below play area
        if self.positions[0][1] >= GRID_ROWS:
            offset = self.positions[0][1] - 0
            self.positions = [(c, max(0, r - GRID_ROWS)) for c, r in self.positions]

    # Task: Splitting - centipede splits at hit segment
    def split(self, index):
        if not self.alive:
            return [], None
        self.alive = False

        mushroom_pos = self.positions[index]
        new_centipedes = []

        # Head part (segments before hit)
        if index > 0:
            first = Centipede(0, 0, index, self.direction)
            first.positions = list(self.positions[:index])
            first.direction = self.direction
            new_centipedes.append(first)

        # Tail part (segments after hit)
        if index < len(self.positions) - 1:
            second = Centipede(0, 0, len(self.positions) - index - 1, self.direction)
            second.positions = list(self.positions[index + 1:])
            # Tail part reverses direction
            second.direction = self.direction * -1
            new_centipedes.append(second)

        return new_centipedes, mushroom_pos

    # Task: Segmented enemies - draw each segment
    def draw(self, surface):
        if not self.alive:
            return
        for i, (col, row) in enumerate(self.positions):
            cx = col * CELL_SIZE + CELL_SIZE // 2
            cy = row * CELL_SIZE + CELL_SIZE // 2
            if i == 0:
                r = CELL_SIZE // 2 - 1
            else:
                r = CELL_SIZE // 2 - 3
            # Draw connecting line to next segment
            if i < len(self.positions) - 1:
                ncol, nrow = self.positions[i + 1]
                nx = ncol * CELL_SIZE + CELL_SIZE // 2
                ny = nrow * CELL_SIZE + CELL_SIZE // 2
                pygame.draw.line(surface, WHITE, (cx, cy), (nx, ny), 2)
            pygame.draw.circle(surface, WHITE, (cx, cy), r, 1 if i > 0 else 0)


class Game:
    def __init__(self, args):
        # Constraint: 使用logger輸出訊息
        self.logger = logging.getLogger("Centipede")
        self.logger.setLevel(getattr(logging, args.log_level.upper(), logging.INFO))
        self.fps = args.fps
        self.score = 0
        self.lives = INITIAL_LIVES
        self.centipede_length = INITIAL_CENTIPEDE_LENGTH

        # Constraint: 使用Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        self.big_font = pygame.font.Font(None, 48)
        self.running = True

        self.player = Player(WINDOW_WIDTH // 2, PLAYER_Y)
        self.bullets = []
        self.centipedes = []
        self.mushrooms = set()
        self.centipede_spawn_timer = 0.0

        self.spawn_mushrooms()
        self.spawn_centipede()
        self.logger.info(
            "Game initialized: %dx%d, fps=%d, mushrooms=%d, centipede_len=%d",
            WINDOW_WIDTH, WINDOW_HEIGHT, self.fps,
            len(self.mushrooms), self.centipede_length,
        )

    def spawn_mushrooms(self):
        for _ in range(INITIAL_MUSHROOM_COUNT):
            col = random.randint(2, GRID_COLS - 3)
            row = random.randint(2, GRID_ROWS - 4)
            self.mushrooms.add((col, row))

    def spawn_centipede(self):
        col = random.randint(10, GRID_COLS - 10)
        self.centipedes.append(Centipede(col, 0, self.centipede_length, 1))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_r and self.lives <= 0:
                    self.reset_game()

    def handle_input(self, dt):
        if not self.player.alive:
            return
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player.move_left(dt)
        if keys[pygame.K_RIGHT]:
            self.player.move_right(dt)
        if keys[pygame.K_SPACE]:
            self.try_shoot()

    def try_shoot(self):
        if not self.player.alive:
            return
        for b in self.bullets:
            if not b.alive:
                b.x = self.player.x
                b.y = self.player.y
                b.alive = True
                self.logger.debug("Bullet fired from (%.0f, %.0f)", self.player.x, self.player.y)
                return
        self.bullets.append(Bullet(self.player.x, self.player.y))
        self.logger.debug("Bullet fired from (%.0f, %.0f)", self.player.x, self.player.y)

    def reset_game(self):
        self.logger.info("Game reset")
        self.score = 0
        self.lives = INITIAL_LIVES
        self.centipede_length = INITIAL_CENTIPEDE_LENGTH
        self.player = Player(WINDOW_WIDTH // 2, PLAYER_Y)
        self.bullets.clear()
        self.centipedes.clear()
        self.mushrooms.clear()
        self.spawn_mushrooms()
        self.spawn_centipede()
        self.centipede_spawn_timer = 0.0

    def update(self, dt):
        if self.lives <= 0 and not self.centipedes:
            return

        self.player.update(dt)
        for bullet in self.bullets:
            bullet.update(dt)
        self.bullets = [b for b in self.bullets if b.alive]

        # Update centipedes
        for centipede in self.centipedes:
            centipede.update(dt, self.mushrooms)
        self.centipedes = [c for c in self.centipedes if c.alive]

        # Task: Splitting - bullet hits centipede segment
        for bullet in self.bullets:
            bx, by = bullet.x, bullet.y
            bcol = int(bx // CELL_SIZE)
            brow = int(by // CELL_SIZE)
            for centipede in self.centipedes:
                if not centipede.alive:
                    continue
                for i, (col, row) in enumerate(centipede.positions):
                    if col == bcol and row == brow:
                        bullet.alive = False
                        self.score += SEGMENT_SCORE
                        self.logger.debug(
                            "Centipede segment hit! index=%d, score=%d",
                            i, self.score,
                        )
                        new_centipedes, mush_pos = centipede.split(i)
                        if mush_pos:
                            self.mushrooms.add(mush_pos)
                        self.centipedes.extend(new_centipedes)
                        break
                if not bullet.alive:
                    break
        self.bullets = [b for b in self.bullets if b.alive]
        self.centipedes = [c for c in self.centipedes if c.alive]

        # Spawn new centipede when all gone
        if not self.centipedes and self.lives > 0:
            self.centipede_spawn_timer += dt
            if self.centipede_spawn_timer >= 1.0:
                self.centipede_length = max(4, self.centipede_length - 1)
                self.spawn_centipede()
                self.centipede_spawn_timer = 0.0
                self.logger.debug("New centipede spawned, length=%d", self.centipede_length)

        # Player hit by centipede
        if self.player.alive and not self.player.invincible:
            pcol = int(self.player.x // CELL_SIZE)
            prow = int(self.player.y // CELL_SIZE)
            for centipede in self.centipedes:
                for col, row in centipede.positions:
                    if abs(col - pcol) <= 1 and abs(row - prow) <= 1:
                        self.player.alive = False
                        self.lives -= 1
                        self.logger.info("Player hit! lives=%d", self.lives)
                        if self.lives > 0:
                            self.player.invincible = True
                            self.player.invincible_timer = INVINCIBLE_TIME
                            self.player.alive = True
                        break
                if not self.player.alive and self.lives <= 0:
                    break

    def draw_grid(self):
        for x in range(0, WINDOW_WIDTH, CELL_SIZE):
            pygame.draw.line(self.screen, GRAY, (x, 0), (x, GRID_ROWS * CELL_SIZE))
        for y in range(0, GRID_ROWS * CELL_SIZE, CELL_SIZE):
            pygame.draw.line(self.screen, GRAY, (0, y), (WINDOW_WIDTH, y))

    def draw(self):
        self.screen.fill(BLACK)
        self.draw_grid()

        # Draw mushrooms
        for col, row in self.mushrooms:
            rect = pygame.Rect(col * CELL_SIZE + 2, row * CELL_SIZE + 2, CELL_SIZE - 4, CELL_SIZE - 4)
            pygame.draw.rect(self.screen, DARK_GREEN, rect)
            pygame.draw.rect(self.screen, WHITE, rect, 1)

        # Draw centipedes
        for centipede in self.centipedes:
            centipede.draw(self.screen)

        # Draw bullets
        for bullet in self.bullets:
            bullet.draw(self.screen)

        # Draw player
        self.player.draw(self.screen)

        # HUD
        score_surf = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_surf, (10, GRID_ROWS * CELL_SIZE + 5))
        lives_surf = self.font.render(f"Lives: {self.lives}", True, WHITE)
        self.screen.blit(lives_surf, (10, GRID_ROWS * CELL_SIZE + 25))

        # Game over
        if self.lives <= 0 and not self.centipedes:
            text = self.big_font.render("GAME OVER", True, WHITE)
            rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 20))
            self.screen.blit(text, rect)
            restart = self.font.render("Press R to restart, ESC to quit", True, WHITE)
            rrect = restart.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 20))
            self.screen.blit(restart, rrect)

        pygame.display.flip()

    def run(self):
        self.logger.info("Game started")
        while self.running:
            dt = self.clock.tick(self.fps) / 1000.0
            self.handle_events()
            self.handle_input(dt)
            self.update(dt)
            self.draw()
        self.logger.info("Game ended")
        pygame.quit()
        sys.exit()


def parse_args(argv):
    parser = argparse.ArgumentParser(description=WINDOW_TITLE)
    parser.add_argument("--fps", type=int, default=FPS, help="Frame rate (default: %(default)s)")
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
