import argparse
import logging
import sys
import random

import pygame

WINDOW_TITLE = "Snake"
FPS = 60
CELL_SIZE = 30
GRID_COLS = 20
GRID_ROWS = 15
WINDOW_WIDTH = GRID_COLS * CELL_SIZE
WINDOW_HEIGHT = GRID_ROWS * CELL_SIZE
MOVE_INTERVAL = 0.15

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
GRAY = (40, 40, 40)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)


class Snake:
    def __init__(self, cols, rows):
        start_x = cols // 2
        start_y = rows // 2
        self.segments = [(start_x, start_y)]
        self.direction = RIGHT
        self.next_direction = RIGHT
        self.growing = False
        self.cols = cols
        self.rows = rows

    def set_direction(self, direction):
        opposite = (direction[0] * -1, direction[1] * -1)
        if opposite != self.direction:
            self.next_direction = direction

    def move(self):
        self.direction = self.next_direction
        head = self.segments[0]
        new_head = (
            head[0] + self.direction[0],
            head[1] + self.direction[1],
        )

        if self.growing:
            self.segments.insert(0, new_head)
            self.growing = False
        else:
            self.segments.insert(0, new_head)
            self.segments.pop()

    def grow(self):
        self.growing = True

    def check_wall_collision(self):
        head = self.segments[0]
        return head[0] < 0 or head[0] >= self.cols or head[1] < 0 or head[1] >= self.rows

    def check_self_collision(self):
        head = self.segments[0]
        return head in self.segments[1:]

    def get_head(self):
        return self.segments[0]

    def draw(self, surface, cell_size):
        for i, segment in enumerate(self.segments):
            rect = pygame.Rect(
                segment[0] * cell_size,
                segment[1] * cell_size,
                cell_size,
                cell_size,
            )
            if i == 0:
                pygame.draw.rect(surface, (0, 255, 0), rect)
            else:
                pygame.draw.rect(surface, GREEN, rect)
            pygame.draw.rect(surface, BLACK, rect, 1)


class Food:
    def __init__(self, cols, rows):
        self.cols = cols
        self.rows = rows
        self.position = (0, 0)

    def spawn(self, snake_segments):
        available = []
        for x in range(self.cols):
            for y in range(self.rows):
                if (x, y) not in snake_segments:
                    available.append((x, y))
        if available:
            self.position = random.choice(available)
            return True
        return False

    def draw(self, surface, cell_size):
        rect = pygame.Rect(
            self.position[0] * cell_size,
            self.position[1] * cell_size,
            cell_size,
            cell_size,
        )
        pygame.draw.rect(surface, RED, rect)
        pygame.draw.rect(surface, BLACK, rect, 1)


class Game:
    def __init__(self, args):
        self.logger = logging.getLogger("Snake")
        self.logger.setLevel(getattr(logging, args.log_level.upper(), logging.INFO))
        self.cell_size = args.cell_size
        self.cols = args.cols
        self.rows = args.rows
        self.window_width = self.cols * self.cell_size
        self.window_height = self.rows * self.cell_size
        self.move_interval = args.speed
        self.move_timer = 0.0
        self.score = 0
        self.game_over = False

        pygame.init()
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 28)
        self.running = True

        self.snake = Snake(self.cols, self.rows)
        self.food = Food(self.cols, self.rows)
        if not self.food.spawn(self.snake.segments):
            self.logger.warning("No space to spawn food")

        self.logger.info(
            "Game initialized: %dx%d grid, cell=%dpx, speed=%.2fs per move",
            self.cols, self.rows, self.cell_size, self.move_interval,
        )

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_r and self.game_over:
                    self.reset_game()
                elif event.key == pygame.K_UP:
                    self.snake.set_direction(UP)
                elif event.key == pygame.K_DOWN:
                    self.snake.set_direction(DOWN)
                elif event.key == pygame.K_LEFT:
                    self.snake.set_direction(LEFT)
                elif event.key == pygame.K_RIGHT:
                    self.snake.set_direction(RIGHT)

    def reset_game(self):
        self.logger.info("Game reset")
        self.snake = Snake(self.cols, self.rows)
        self.food.spawn(self.snake.segments)
        self.score = 0
        self.game_over = False
        self.move_timer = 0.0

    def update(self, dt):
        if self.game_over:
            return

        self.move_timer += dt
        if self.move_timer < self.move_interval:
            return
        self.move_timer = 0.0

        self.snake.move()

        if self.snake.check_wall_collision():
            self.logger.debug("Snake hit wall at head=%s", self.snake.get_head())
            self.game_over = True
            return

        if self.snake.check_self_collision():
            self.logger.debug("Snake hit itself at head=%s", self.snake.get_head())
            self.game_over = True
            return

        if self.snake.get_head() == self.food.position:
            self.snake.grow()
            self.score += 1
            self.logger.debug("Food eaten. Score=%d", self.score)
            if not self.food.spawn(self.snake.segments):
                self.logger.info("No space left for food. Player wins!")
                self.game_over = True

    def draw_grid(self):
        for x in range(0, self.window_width, self.cell_size):
            pygame.draw.line(self.screen, GRAY, (x, 0), (x, self.window_height))
        for y in range(0, self.window_height, self.cell_size):
            pygame.draw.line(self.screen, GRAY, (0, y), (self.window_width, y))

    def draw(self):
        self.screen.fill(BLACK)
        self.draw_grid()
        self.snake.draw(self.screen, self.cell_size)
        self.food.draw(self.screen, self.cell_size)

        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))

        if self.game_over:
            text = self.font.render("Game Over! (R to restart, ESC to quit)", True, WHITE)
            text_rect = text.get_rect(center=(self.window_width // 2, self.window_height // 2))
            self.screen.blit(text, text_rect)

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
    parser.add_argument("--cell-size", type=int, default=CELL_SIZE, help="Cell size in pixels (default: %(default)s)")
    parser.add_argument("--cols", type=int, default=GRID_COLS, help="Number of grid columns (default: %(default)s)")
    parser.add_argument("--rows", type=int, default=GRID_ROWS, help="Number of grid rows (default: %(default)s)")
    parser.add_argument(
        "--speed", type=float, default=MOVE_INTERVAL,
        help="Time in seconds between snake moves (default: %(default)s). Lower = faster.",
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
