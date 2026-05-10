import argparse
import logging
import sys
import random

import pygame

WINDOW_TITLE = "Doodle Jump"
FPS = 60
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 700

PLAYER_WIDTH = 24
PLAYER_HEIGHT = 28

PLATFORM_WIDTH = 60
PLATFORM_HEIGHT = 12

GRAVITY = 0.4
JUMP_VELOCITY = -10
MOVE_SPEED = 5

CAMERA_SMOOTH = 0.1

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (100, 149, 237)
RED = (220, 60, 60)
GREEN = (80, 200, 80)
SKY_BLUE = (135, 206, 235)


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.velocity_y = 0.0
        self.velocity_x = 0.0

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def update(self, gravity):
        self.velocity_y += gravity
        self.y += self.velocity_y
        self.x += self.velocity_x

    def move_left(self):
        self.velocity_x = -MOVE_SPEED

    def move_right(self):
        self.velocity_x = MOVE_SPEED

    def stop_x(self):
        self.velocity_x = 0.0

    def wrap_x(self, screen_width):
        if self.x + self.width < 0:
            self.x = screen_width
        elif self.x > screen_width:
            self.x = -self.width

    def bounce(self, platform_y):
        self.y = platform_y - self.height
        self.velocity_y = JUMP_VELOCITY

    def draw(self, surface, camera_y):
        draw_y = int(self.y - camera_y)
        pygame.draw.ellipse(surface, BLUE, (int(self.x), draw_y, self.width, self.height))
        eye_center_x = int(self.x) + self.width // 2
        eye_y = draw_y + 6
        pygame.draw.circle(surface, WHITE, (eye_center_x - 4, eye_y), 3)
        pygame.draw.circle(surface, WHITE, (eye_center_x + 4, eye_y), 3)
        pygame.draw.circle(surface, BLACK, (eye_center_x - 4, eye_y), 1)
        pygame.draw.circle(surface, BLACK, (eye_center_x + 4, eye_y), 1)


class Platform:
    def __init__(self, x, y, width=PLATFORM_WIDTH):
        self.x = x
        self.y = y
        self.width = width
        self.height = PLATFORM_HEIGHT
        self.rect = pygame.Rect(x, y, width, PLATFORM_HEIGHT)

    def update_rect(self):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

    def draw(self, surface, camera_y):
        draw_y = int(self.y - camera_y)
        pygame.draw.rect(surface, GREEN, (int(self.x), draw_y, self.width, self.height))
        pygame.draw.rect(surface, BLACK, (int(self.x), draw_y, self.width, self.height), 1)


class Game:
    def __init__(self, args):
        self.logger = logging.getLogger("DoodleJump")
        self.logger.setLevel(getattr(logging, args.log_level.upper(), logging.INFO))
        self.window_width = args.width
        self.window_height = args.height
        self.gravity = args.gravity
        self.jump_velocity = args.jump_velocity
        self.move_speed = args.move_speed
        self.score = 0
        self.highest_y = 0.0
        self.camera_y = 0.0
        self.game_over = False
        self.platforms = []
        self.started = False

        pygame.init()
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 24)
        self.running = True

        start_x = self.window_width // 2 - PLAYER_WIDTH // 2
        start_y = self.window_height - 150
        self.player = Player(start_x, start_y)

        self._init_platforms()

        self.logger.info(
            "Game initialized: %dx%d, gravity=%.2f, jump=%.1f, move_speed=%d",
            self.window_width, self.window_height,
            self.gravity, self.jump_velocity, self.move_speed,
        )

    def _init_platforms(self):
        ground = Platform(0, self.window_height - PLATFORM_HEIGHT, self.window_width)
        self.platforms.append(ground)
        for i in range(10):
            x = random.randint(0, self.window_width - PLATFORM_WIDTH)
            y = self.window_height - 80 - i * 60
            self.platforms.append(Platform(x, y))

    def reset_game(self):
        self.logger.info("Game reset")
        self.score = 0
        self.highest_y = 0.0
        self.camera_y = 0.0
        self.game_over = False
        self.started = False
        self.platforms.clear()
        start_x = self.window_width // 2 - PLAYER_WIDTH // 2
        start_y = self.window_height - 150
        self.player = Player(start_x, start_y)
        self._init_platforms()

    def spawn_platform_above(self):
        max_y = min(p.y for p in self.platforms) if self.platforms else 0
        top = max_y - random.randint(40, 80)
        x = random.randint(0, self.window_width - PLATFORM_WIDTH)
        platform = Platform(x, top)
        self.platforms.append(platform)
        self.logger.debug("Platform spawned at (%.0f, %.0f)", platform.x, platform.y)

    def trim_platforms_below(self):
        cutoff = self.camera_y + self.window_height + 100
        before = len(self.platforms)
        self.platforms = [p for p in self.platforms if p.y < cutoff]
        removed = before - len(self.platforms)
        if removed > 0:
            self.logger.debug("Removed %d platforms below camera", removed)

    def handle_events(self):
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_r and self.game_over:
                    self.reset_game()
                elif event.key in (pygame.K_SPACE, pygame.K_UP) and not self.game_over:
                    if not self.started:
                        self.started = True
                        self.player.velocity_y = self.jump_velocity

        if self.game_over:
            return
        if not self.started:
            return

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player.move_left()
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player.move_right()
        else:
            self.player.stop_x()

    def update(self, dt):
        if self.game_over or not self.started:
            return

        self.player.update(self.gravity)
        self.player.wrap_x(self.window_width)

        player_rect = self.player.get_rect()

        if self.player.velocity_y >= 0:
            for platform in self.platforms:
                if platform.rect.colliderect(player_rect):
                    player_bottom = self.player.y + self.player.height
                    platform_top = platform.y
                    prev_bottom = player_bottom - self.player.velocity_y
                    if prev_bottom <= platform_top + 4:
                        self.player.bounce(platform.y)
                        self.logger.debug("Player bounced on platform at (%.0f, %.0f)", platform.x, platform.y)
                        break

        if self.player.y < self.highest_y:
            self.highest_y = self.player.y
            self.score = int(-self.highest_y // 10)
            self.logger.debug("Score increased to %d", self.score)

        target_camera = self.player.y - self.window_height * 0.35
        self.camera_y += (target_camera - self.camera_y) * CAMERA_SMOOTH
        if self.camera_y < 0:
            self.camera_y = 0

        lowest_platform_y = max(p.y for p in self.platforms)
        highest_platform_y = min(p.y for p in self.platforms)
        if self.camera_y < highest_platform_y + 200:
            self.spawn_platform_above()
        if self.camera_y > lowest_platform_y - self.window_height:
            ground = Platform(0, lowest_platform_y + 60, self.window_width)
            self.platforms.append(ground)

        self.trim_platforms_below()

        for p in self.platforms:
            p.update_rect()

        if self.player.y > self.camera_y + self.window_height + 50:
            self.logger.debug("Player fell off screen at y=%.0f", self.player.y)
            self.game_over = True

    def draw(self):
        self.screen.fill(SKY_BLUE)

        for platform in self.platforms:
            platform.draw(self.screen, self.camera_y)

        self.player.draw(self.screen, self.camera_y)

        score_text = self.font.render(f"Score: {self.score}", True, BLACK)
        self.screen.blit(score_text, (10, 10))

        if not self.started:
            title = self.font.render("Doodle Jump", True, BLACK)
            title_rect = title.get_rect(center=(self.window_width // 2, self.window_height // 3))
            self.screen.blit(title, title_rect)
            hint = self.small_font.render("Press SPACE to start", True, BLACK)
            hint_rect = hint.get_rect(center=(self.window_width // 2, self.window_height // 3 + 40))
            self.screen.blit(hint, hint_rect)

        if self.game_over:
            overlay = pygame.Surface((self.window_width, self.window_height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))
            self.screen.blit(overlay, (0, 0))
            go_text = self.font.render("Game Over!", True, WHITE)
            go_rect = go_text.get_rect(center=(self.window_width // 2, self.window_height // 2 - 30))
            self.screen.blit(go_text, go_rect)
            final_score = self.small_font.render(f"Score: {self.score}", True, WHITE)
            fs_rect = final_score.get_rect(center=(self.window_width // 2, self.window_height // 2 + 10))
            self.screen.blit(final_score, fs_rect)
            restart = self.small_font.render("Press R to restart, ESC to quit", True, WHITE)
            restart_rect = restart.get_rect(center=(self.window_width // 2, self.window_height // 2 + 50))
            self.screen.blit(restart, restart_rect)

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
    parser.add_argument("--jump-velocity", type=float, default=JUMP_VELOCITY, help="Jump upward velocity (default: %(default)s)")
    parser.add_argument("--move-speed", type=int, default=MOVE_SPEED, help="Horizontal movement speed (default: %(default)s)")
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
