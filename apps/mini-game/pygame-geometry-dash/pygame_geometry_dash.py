import argparse
import logging
import sys
import math

import pygame


WINDOW_TITLE = "Geometry Dash"
FPS = 60
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 400

GROUND_HEIGHT = 40
PLAYER_SIZE = 30
GRAVITY = 1800
JUMP_STRENGTH = -600
SCROLL_SPEED = 300
MIN_OBSTACLE_GAP = 200
MAX_OBSTACLE_GAP = 350
OBSTACLE_WIDTH = 30

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARK_GRAY = (20, 20, 30)
GRAY = (60, 60, 80)
PLAYER_COLOR = (255, 200, 50)
OBSTACLE_COLOR = (200, 60, 60)
GROUND_COLOR = (40, 40, 60)


class Player:
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        self.velocity_y = 0.0
        self.on_ground = False

    def jump(self, strength):
        if self.on_ground:
            self.velocity_y = strength
            self.on_ground = False

    def update(self, dt, gravity, ground_y):
        self.velocity_y += gravity * dt
        self.y += self.velocity_y * dt

        if self.y + self.size >= ground_y:
            self.y = ground_y - self.size
            self.velocity_y = 0.0
            self.on_ground = True
        else:
            self.on_ground = False

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.size, self.size)

    def draw(self, surface):
        rect = self.get_rect()
        pygame.draw.rect(surface, PLAYER_COLOR, rect)
        pygame.draw.rect(surface, WHITE, rect, 2)


class Obstacle:
    def __init__(self, x, ground_y, obstacle_type="block"):
        self.x = x
        self.obstacle_type = obstacle_type
        self.width = OBSTACLE_WIDTH

        if obstacle_type == "spike":
            self.height = 30
            self.y = ground_y - self.height
        else:
            self.height = 30
            self.y = ground_y - self.height

    def move(self, speed, dt):
        self.x -= speed * dt

    def is_off_screen(self):
        return self.x + self.width < 0

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

    def collides_with(self, player_rect):
        if self.obstacle_type == "spike":
            spike_rect = self.get_rect()
            if not player_rect.colliderect(spike_rect):
                return False
            cx = self.x + self.width / 2
            cy = self.y + self.height
            half_w = self.width / 2
            px = player_rect.centerx
            py = player_rect.centery
            dx = abs(px - cx) / half_w
            dy = abs(py - cy) / self.height
            return (dx + dy * 0.5) <= 1.0
        return player_rect.colliderect(self.get_rect())

    def draw(self, surface):
        if self.obstacle_type == "spike":
            points = [
                (self.x, self.y + self.height),
                (self.x + self.width / 2, self.y),
                (self.x + self.width, self.y + self.height),
            ]
            pygame.draw.polygon(surface, OBSTACLE_COLOR, points)
            pygame.draw.polygon(surface, WHITE, points, 2)
        else:
            rect = self.get_rect()
            pygame.draw.rect(surface, OBSTACLE_COLOR, rect)
            pygame.draw.rect(surface, WHITE, rect, 2)


class Game:
    def __init__(self, args):
        self.logger = logging.getLogger("GeometryDash")
        self.logger.setLevel(getattr(logging, args.log_level.upper(), logging.INFO))
        self.window_width = args.width
        self.window_height = args.height
        self.gravity = args.gravity
        self.jump_strength = args.jump_strength
        self.scroll_speed = args.scroll_speed

        self.ground_y = self.window_height - GROUND_HEIGHT
        self.score = 0.0
        self.game_over = False
        self.obstacles = []
        self.obstacle_timer = 0.0
        self.next_gap = MIN_OBSTACLE_GAP
        self.player_x = self.window_width // 4

        pygame.init()
        self.screen = pygame.display.set_mode(
            (self.window_width, self.window_height)
        )
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        self.running = True

        self.player = Player(
            self.player_x,
            self.ground_y - PLAYER_SIZE,
            PLAYER_SIZE,
        )

        self.logger.info(
            "Game initialized: %dx%d, gravity=%.0f, jump=%.0f, scroll_speed=%.0f",
            self.window_width, self.window_height,
            self.gravity, self.jump_strength, self.scroll_speed,
        )

    def reset_game(self):
        self.logger.info("Game reset")
        self.player = Player(
            self.player_x,
            self.ground_y - PLAYER_SIZE,
            PLAYER_SIZE,
        )
        self.obstacles.clear()
        self.obstacle_timer = 0.0
        self.score = 0.0
        self.next_gap = MIN_OBSTACLE_GAP
        self.game_over = False

    def spawn_obstacle(self):
        obs_type = "spike" if self.score < 500 else ("block" if self.score < 1500 else "spike")
        obstacle = Obstacle(self.window_width, self.ground_y, obs_type)
        self.obstacles.append(obstacle)
        self.logger.debug("Obstacle spawned at x=%d, type=%s", obstacle.x, obstacle.obstacle_type)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_r:
                    self.reset_game()
                elif event.key == pygame.K_SPACE:
                    if self.game_over:
                        self.reset_game()
                    else:
                        self.player.jump(self.jump_strength)

    def update(self, dt):
        if self.game_over:
            return

        self.player.update(dt, self.gravity, self.ground_y)

        if self.player.y <= -self.player.size:
            self.logger.debug("Player fell off top")
            self.game_over = True
            return

        self.obstacle_timer += self.scroll_speed * dt
        if self.obstacle_timer >= self.next_gap:
            self.obstacle_timer -= self.next_gap
            self.spawn_obstacle()
            self.next_gap = max(
                MIN_OBSTACLE_GAP,
                MAX_OBSTACLE_GAP - int(self.score / 20) * 10,
            )

        player_rect = self.player.get_rect()
        for obstacle in list(self.obstacles):
            obstacle.move(self.scroll_speed, dt)
            if obstacle.collides_with(player_rect):
                self.logger.debug("Player collided with obstacle at x=%d", obstacle.x)
                self.game_over = True
                return
            if obstacle.is_off_screen():
                self.obstacles.remove(obstacle)

        self.score += self.scroll_speed * dt / 10

    def draw(self):
        self.screen.fill(DARK_GRAY)

        ground_rect = pygame.Rect(0, self.ground_y, self.window_width, GROUND_HEIGHT)
        pygame.draw.rect(self.screen, GROUND_COLOR, ground_rect)
        pygame.draw.line(
            self.screen, WHITE,
            (0, self.ground_y),
            (self.window_width, self.ground_y),
            2,
        )

        for obstacle in self.obstacles:
            obstacle.draw(self.screen)

        self.player.draw(self.screen)

        score_text = self.font.render(f"{int(self.score)}", True, WHITE)
        score_rect = score_text.get_rect(topright=(self.window_width - 20, 20))
        self.screen.blit(score_text, score_rect)

        if self.game_over:
            go_text = self.font.render("Game Over", True, OBSTACLE_COLOR)
            go_rect = go_text.get_rect(center=(self.window_width // 2, self.window_height // 2 - 20))
            self.screen.blit(go_text, go_rect)

            restart_text = self.small_font.render("Press R or SPACE to restart, ESC to quit", True, WHITE)
            restart_rect = restart_text.get_rect(center=(self.window_width // 2, self.window_height // 2 + 20))
            self.screen.blit(restart_text, restart_rect)
        else:
            hint_text = self.small_font.render("SPACE to jump | R to restart", True, WHITE)
            hint_rect = hint_text.get_rect(bottomleft=(10, self.window_height - 10))
            self.screen.blit(hint_text, hint_rect)

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
        "--width", type=int, default=WINDOW_WIDTH,
        help="Window width (default: %(default)s)",
    )
    parser.add_argument(
        "--height", type=int, default=WINDOW_HEIGHT,
        help="Window height (default: %(default)s)",
    )
    parser.add_argument(
        "--gravity", type=float, default=GRAVITY,
        help="Gravity strength in px/s^2 (default: %(default)s)",
    )
    parser.add_argument(
        "--jump-strength", type=float, default=JUMP_STRENGTH,
        help="Jump initial velocity in px/s (default: %(default)s)",
    )
    parser.add_argument(
        "--scroll-speed", type=float, default=SCROLL_SPEED,
        help="Level scroll speed in px/s (default: %(default)s)",
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
