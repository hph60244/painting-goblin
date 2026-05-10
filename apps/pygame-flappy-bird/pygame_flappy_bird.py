import argparse
import logging
import sys
import random

import pygame

WINDOW_TITLE = "Flappy Bird"
FPS = 60
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 600

GROUND_HEIGHT = 80
BIRD_RADIUS = 12
PIPE_WIDTH = 60
PIPE_GAP = 160
PIPE_SPACING = 280
PIPE_SPEED = 3

GRAVITY = 0.5
FLAP_STRENGTH = -9

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 150, 0)
YELLOW = (255, 255, 0)
GRAY = (100, 100, 100)
SKY_BLUE = (135, 206, 235)


class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocity = 0.0
        self.radius = BIRD_RADIUS

    def flap(self, strength):
        self.velocity = strength

    def update(self, gravity):
        self.velocity += gravity
        self.y += self.velocity

    def get_rect(self):
        return pygame.Rect(
            self.x - self.radius,
            self.y - self.radius,
            self.radius * 2,
            self.radius * 2,
        )

    def draw(self, surface):
        pygame.draw.circle(surface, YELLOW, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(surface, BLACK, (int(self.x), int(self.y)), self.radius, 1)


class PipePair:
    def __init__(self, x, gap_y, gap_size, pipe_width):
        self.x = x
        self.gap_y = gap_y
        self.gap_size = gap_size
        self.width = pipe_width
        self.scored = False

    def move(self, speed):
        self.x -= speed

    def is_off_screen(self):
        return self.x + self.width < 0

    def get_top_rect(self):
        return pygame.Rect(self.x, 0, self.width, self.gap_y)

    def get_bottom_rect(self):
        return pygame.Rect(
            self.x,
            self.gap_y + self.gap_size,
            self.width,
            WINDOW_HEIGHT - GROUND_HEIGHT - self.gap_y - self.gap_size,
        )

    def collides_with(self, bird_rect):
        return bird_rect.colliderect(self.get_top_rect()) or bird_rect.colliderect(self.get_bottom_rect())

    def draw(self, surface):
        top_rect = self.get_top_rect()
        bottom_rect = self.get_bottom_rect()
        pygame.draw.rect(surface, GREEN, top_rect)
        pygame.draw.rect(surface, DARK_GREEN, top_rect, 2)
        pygame.draw.rect(surface, GREEN, bottom_rect)
        pygame.draw.rect(surface, DARK_GREEN, bottom_rect, 2)


class Game:
    def __init__(self, args):
        self.logger = logging.getLogger("FlappyBird")
        self.logger.setLevel(getattr(logging, args.log_level.upper(), logging.INFO))
        self.window_width = args.width
        self.window_height = args.height
        self.gravity = args.gravity
        self.flap_strength = args.flap_strength
        self.pipe_speed = args.pipe_speed
        self.pipe_gap = args.pipe_gap
        self.pipe_spacing = args.pipe_spacing
        self.score = 0
        self.game_over = False
        self.pipes = []
        self.pipe_timer = 0.0
        self.ground_scroll = 0.0
        self.flapped = False

        pygame.init()
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.running = True

        self.bird = Bird(self.window_width // 4, self.window_height // 2)

        self.logger.info(
            "Game initialized: %dx%d, gravity=%.2f, flap=%.1f, pipe_speed=%d, pipe_gap=%d",
            self.window_width, self.window_height,
            self.gravity, self.flap_strength,
            self.pipe_speed, self.pipe_gap,
        )

    def reset_game(self):
        self.logger.info("Game reset")
        self.bird = Bird(self.window_width // 4, self.window_height // 2)
        self.pipes.clear()
        self.pipe_timer = 0.0
        self.score = 0
        self.game_over = False
        self.flapped = False

    def spawn_pipe(self):
        min_gap_y = 60
        max_gap_y = self.window_height - GROUND_HEIGHT - self.pipe_gap - 60
        gap_y = random.randint(min_gap_y, max_gap_y)
        pipe = PipePair(self.window_width, gap_y, self.pipe_gap, PIPE_WIDTH)
        self.pipes.append(pipe)
        self.logger.debug("Pipe spawned at x=%d, gap_y=%d", pipe.x, pipe.gap_y)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_r and self.game_over:
                    self.reset_game()
                elif event.key == pygame.K_SPACE and not self.game_over:
                    self.bird.flap(self.flap_strength)
                    self.flapped = True

    def update(self, dt):
        if self.game_over:
            return

        self.bird.update(self.gravity)

        bird_rect = self.bird.get_rect()

        if bird_rect.top <= 0:
            self.logger.debug("Bird hit ceiling")
            self.game_over = True
            return

        if bird_rect.bottom >= self.window_height - GROUND_HEIGHT:
            self.logger.debug("Bird hit ground at y=%d", self.bird.y)
            self.game_over = True
            return

        self.pipe_timer += dt
        pipe_interval = self.pipe_spacing / (self.pipe_speed * FPS)
        if self.pipe_timer >= pipe_interval:
            self.pipe_timer -= pipe_interval
            self.spawn_pipe()

        for pipe in list(self.pipes):
            pipe.move(self.pipe_speed)
            if pipe.collides_with(bird_rect):
                self.logger.debug("Bird collided with pipe at x=%d", pipe.x)
                self.game_over = True
                return
            if not pipe.scored and pipe.x + pipe.width < bird_rect.left:
                pipe.scored = True
                self.score += 1
                self.logger.debug("Score increased to %d", self.score)
            if pipe.is_off_screen():
                self.pipes.remove(pipe)

    def draw(self):
        self.screen.fill(SKY_BLUE)

        for pipe in self.pipes:
            pipe.draw(self.screen)

        ground_rect = pygame.Rect(0, self.window_height - GROUND_HEIGHT, self.window_width, GROUND_HEIGHT)
        pygame.draw.rect(self.screen, GRAY, ground_rect)
        pygame.draw.rect(self.screen, BLACK, ground_rect, 2)

        self.bird.draw(self.screen)

        score_text = self.font.render(str(self.score), True, WHITE)
        score_rect = score_text.get_rect(center=(self.window_width // 2, 40))
        self.screen.blit(score_text, score_rect)

        if not self.flapped and not self.game_over:
            hint = self.font.render("Press SPACE to flap", True, WHITE)
            hint_rect = hint.get_rect(center=(self.window_width // 2, self.window_height // 2 - 60))
            self.screen.blit(hint, hint_rect)

        if self.game_over:
            game_over_text = self.font.render("Game Over! (R to restart, ESC to quit)", True, WHITE)
            game_over_rect = game_over_text.get_rect(
                center=(self.window_width // 2, self.window_height // 2 - 30)
            )
            self.screen.blit(game_over_text, game_over_rect)

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
    parser.add_argument("--width", type=int, default=WINDOW_WIDTH, help="Window width (default: %(default)s)")
    parser.add_argument("--height", type=int, default=WINDOW_HEIGHT, help="Window height (default: %(default)s)")
    parser.add_argument("--gravity", type=float, default=GRAVITY, help="Gravity strength (default: %(default)s)")
    parser.add_argument("--flap-strength", type=float, default=FLAP_STRENGTH, help="Flap upward velocity (default: %(default)s)")
    parser.add_argument("--pipe-speed", type=int, default=PIPE_SPEED, help="Pipe horizontal speed (default: %(default)s)")
    parser.add_argument("--pipe-gap", type=int, default=PIPE_GAP, help="Gap between top and bottom pipes (default: %(default)s)")
    parser.add_argument("--pipe-spacing", type=int, default=PIPE_SPACING, help="Horizontal space between pipe pairs (default: %(default)s)")
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
