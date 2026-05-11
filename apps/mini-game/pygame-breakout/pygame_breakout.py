import argparse
import logging
import sys
import math
import random

import pygame

# Constraint: 使用Pygame - 適合製作2D遊戲原型, 輕量化
# Constraint: 用極簡風格呈現 - 強調玩法概念, 節省製作時間

WINDOW_TITLE = "Breakout"
FPS = 60
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

PADDLE_WIDTH = 100
PADDLE_HEIGHT = 14
PADDLE_MARGIN_BOTTOM = 30
PADDLE_SPEED = 7

BALL_SIZE = 8
BALL_SPEED_INIT = 5

BRICK_ROWS = 6
BRICK_COLS = 10
BRICK_WIDTH = 70
BRICK_HEIGHT = 20
BRICK_PADDING = 4
BRICK_TOP_OFFSET = 60

LIVES = 3

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
BLUE = (50, 50, 255)
YELLOW = (255, 255, 50)
ORANGE = (255, 165, 0)
PURPLE = (200, 50, 255)

BRICK_COLORS = [RED, ORANGE, YELLOW, GREEN, BLUE, PURPLE]

POWERUP_TYPES = ["wide", "multi", "fast", "slow"]
POWERUP_SIZE = 12
POWERUP_SPEED = 3
POWERUP_DROP_CHANCE = 0.25
WIDE_PADDLE_DURATION = 8.0
WIDE_PADDLE_WIDTH = 160


class Paddle:
    def __init__(self, x, y, width, height, speed):
        self.base_width = width
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed
        self.direction = 0
        self.wide_timer = 0.0

    def move(self, dt, window_width):
        self.rect.x += self.direction * self.speed * dt
        self.rect.x = max(0, min(self.rect.x, window_width - self.rect.width))

    def widen(self, duration):
        self.wide_timer = duration
        center_x = self.rect.centerx
        self.rect.width = WIDE_PADDLE_WIDTH
        self.rect.centerx = center_x

    def update_timers(self, dt, window_width):
        if self.wide_timer > 0:
            self.wide_timer -= dt
            if self.wide_timer <= 0:
                self.wide_timer = 0.0
                center_x = self.rect.centerx
                self.rect.width = self.base_width
                self.rect.centerx = min(max(center_x, self.rect.width // 2), window_width - self.rect.width // 2)

    def reset(self, x, y):
        self.rect.x = x
        self.rect.y = y
        self.rect.width = self.base_width
        self.wide_timer = 0.0

    def draw(self, surface):
        pygame.draw.rect(surface, WHITE, self.rect)


class Ball:
    def __init__(self, x, y, size, speed):
        self.rect = pygame.Rect(x, y, size, size)
        self.speed = speed
        self.dx = speed * random.choice([-1, 1])
        self.dy = -speed
        self.stuck = True

    def move(self, dt):
        self.rect.x += self.dx * dt
        self.rect.y += self.dy * dt

    def bounce_wall(self, window_width, window_height):
        bounced = False
        if self.rect.left <= 0:
            self.rect.left = 0
            self.dx = abs(self.dx)
            bounced = True
        if self.rect.right >= window_width:
            self.rect.right = window_width
            self.dx = -abs(self.dx)
            bounced = True
        if self.rect.top <= 0:
            self.rect.top = 0
            self.dy = abs(self.dy)
            bounced = True
        return bounced

    def is_out_bottom(self, window_height):
        return self.rect.top >= window_height

    # Contract: Breakout/Arkanoid - Angled ball deflection
    def bounce_paddle(self, paddle_rect):
        if self.rect.colliderect(paddle_rect) and self.dy > 0:
            paddle_center = paddle_rect.centerx
            ball_center = self.rect.centerx
            offset = (ball_center - paddle_center) / (paddle_rect.width / 2)
            offset = max(-1.0, min(1.0, offset))
            angle = offset * (math.pi / 3)
            speed = math.sqrt(self.dx**2 + self.dy**2)
            self.dx = speed * math.sin(angle)
            self.dy = -speed * math.cos(angle)
            self.rect.bottom = paddle_rect.top
            return True
        return False

    def bounce_brick(self, brick_rect):
        if not self.rect.colliderect(brick_rect):
            return False
        overlap_left = self.rect.right - brick_rect.left
        overlap_right = brick_rect.right - self.rect.left
        overlap_top = self.rect.bottom - brick_rect.top
        overlap_bottom = brick_rect.bottom - self.rect.top
        min_overlap = min(overlap_left, overlap_right, overlap_top, overlap_bottom)
        if min_overlap == overlap_left or min_overlap == overlap_right:
            self.dx = -self.dx
        else:
            self.dy = -self.dy
        return True

    def launch(self):
        if self.stuck:
            self.stuck = False

    def reset(self, x, y, paddle_rect):
        self.stuck = True
        self.rect.x = x
        self.rect.y = y
        self.dx = self.speed * random.choice([-1, 1])
        self.dy = -self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, WHITE, self.rect)


class Brick:
    def __init__(self, x, y, width, height, color, hp=1):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hp = hp
        self.alive = True

    def hit(self):
        self.hp -= 1
        if self.hp <= 0:
            self.alive = False
            return True
        return False

    def draw(self, surface):
        if not self.alive:
            return
        pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 1)


class PowerUp:
    def __init__(self, x, y, ptype):
        self.rect = pygame.Rect(x, y, POWERUP_SIZE, POWERUP_SIZE)
        self.ptype = ptype
        self.speed = POWERUP_SPEED

    def move(self, dt):
        self.rect.y += self.speed * dt

    def is_out_bottom(self, window_height):
        return self.rect.top >= window_height

    def draw(self, surface):
        color_map = {
            "wide": GREEN,
            "multi": BLUE,
            "fast": RED,
            "slow": PURPLE,
        }
        color = color_map.get(self.ptype, WHITE)
        pygame.draw.rect(surface, color, self.rect)
        font = pygame.font.Font(None, 14)
        label = font.render(self.ptype[0].upper(), True, BLACK)
        label_rect = label.get_rect(center=self.rect.center)
        surface.blit(label, label_rect)


class Game:
    def __init__(self, args):
        # Constraint: 使用logger輸出訊息 - 用於人類跟AI除錯
        self.logger = logging.getLogger("Breakout")
        self.logger.setLevel(getattr(logging, args.log_level.upper(), logging.INFO))
        self.window_width = args.width
        self.window_height = args.height
        self.fps = args.fps
        self.ball_speed_init = args.ball_speed
        self.lives = LIVES
        self.score = 0
        self.powerups_active = []

        pygame.init()
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 28)
        self.big_font = pygame.font.Font(None, 48)
        self.running = True

        paddle_x = self.window_width // 2 - PADDLE_WIDTH // 2
        paddle_y = self.window_height - PADDLE_MARGIN_BOTTOM - PADDLE_HEIGHT
        self.paddle = Paddle(paddle_x, paddle_y, PADDLE_WIDTH, PADDLE_HEIGHT, PADDLE_SPEED)

        ball_x = self.paddle.rect.centerx - BALL_SIZE // 2
        ball_y = self.paddle.rect.top - BALL_SIZE
        self.ball = Ball(ball_x, ball_y, BALL_SIZE, self.ball_speed_init)

        self.bricks = []
        self.powerups = []
        self._build_bricks()

        self.logger.info(
            "Game initialized: %dx%d, fps=%d, bricks=%d",
            self.window_width, self.window_height, self.fps,
            BRICK_ROWS * BRICK_COLS,
        )

    # Contract: Breakout/Arkanoid - Brick grid
    def _build_bricks(self):
        self.bricks = []
        for row in range(BRICK_ROWS):
            for col in range(BRICK_COLS):
                x = col * (BRICK_WIDTH + BRICK_PADDING) + BRICK_PADDING
                y = row * (BRICK_HEIGHT + BRICK_PADDING) + BRICK_TOP_OFFSET
                color = BRICK_COLORS[row % len(BRICK_COLORS)]
                hp = 1
                if row == 0:
                    hp = 2
                brick = Brick(x, y, BRICK_WIDTH, BRICK_HEIGHT, color, hp)
                self.bricks.append(brick)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE and self.ball.stuck:
                    self.ball.launch()
                    self.logger.debug("Ball launched")
                elif event.key == pygame.K_r and self.lives <= 0:
                    self.reset_game()

    def handle_input(self, dt):
        keys = pygame.key.get_pressed()
        self.paddle.direction = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.paddle.direction = -1
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.paddle.direction = 1

    def reset_ball(self):
        self.lives -= 1
        self.logger.info("Ball lost. Lives remaining: %d", self.lives)
        ball_x = self.paddle.rect.centerx - BALL_SIZE // 2
        ball_y = self.paddle.rect.top - BALL_SIZE
        self.ball.reset(ball_x, ball_y, self.paddle.rect)

    def reset_game(self):
        self.logger.info("Game reset")
        self.lives = LIVES
        self.score = 0
        self.powerups_active = []
        self.powerups.clear()
        paddle_x = self.window_width // 2 - PADDLE_WIDTH // 2
        paddle_y = self.window_height - PADDLE_MARGIN_BOTTOM - PADDLE_HEIGHT
        self.paddle.reset(paddle_x, paddle_y)
        ball_x = self.paddle.rect.centerx - BALL_SIZE // 2
        ball_y = self.paddle.rect.top - BALL_SIZE
        self.ball.reset(ball_x, ball_y, self.paddle.rect)
        self._build_bricks()

    def _apply_powerup(self, powerup):
        self.logger.info("Powerup collected: %s", powerup.ptype)
        if powerup.ptype == "wide":
            self.paddle.widen(WIDE_PADDLE_DURATION)
        elif powerup.ptype == "multi":
            # Not implementing multi-ball for minimal style
            pass
        elif powerup.ptype == "fast":
            speed = math.sqrt(self.ball.dx**2 + self.ball.dy**2)
            new_speed = speed * 1.5
            if self.ball.dx != 0:
                self.ball.dx = (self.ball.dx / abs(self.ball.dx)) * new_speed * abs(self.ball.dx) / speed
            if self.ball.dy != 0:
                self.ball.dy = (self.ball.dy / abs(self.ball.dy)) * new_speed * abs(self.ball.dy) / speed
        elif powerup.ptype == "slow":
            speed = math.sqrt(self.ball.dx**2 + self.ball.dy**2)
            new_speed = max(speed * 0.7, 2.0)
            if self.ball.dx != 0:
                self.ball.dx = (self.ball.dx / abs(self.ball.dx)) * new_speed * abs(self.ball.dx) / speed
            if self.ball.dy != 0:
                self.ball.dy = (self.ball.dy / abs(self.ball.dy)) * new_speed * abs(self.ball.dy) / speed

    def update(self, dt):
        self.paddle.update_timers(dt, self.window_width)
        self.paddle.move(dt, self.window_width)

        if self.ball.stuck:
            self.ball.rect.x = self.paddle.rect.centerx - BALL_SIZE // 2
            self.ball.rect.y = self.paddle.rect.top - BALL_SIZE
        else:
            old_pos = (self.ball.rect.x, self.ball.rect.y, self.ball.dx, self.ball.dy)
            self.ball.move(dt)
            if self.ball.bounce_wall(self.window_width, self.window_height):
                self.logger.debug("Ball bounced off wall at pos=(%d,%d)", self.ball.rect.x, self.ball.rect.y)
            if self.ball.bounce_paddle(self.paddle.rect):
                self.logger.debug("Ball bounced off paddle. dir=(%.2f,%.2f)", self.ball.dx, self.ball.dy)

            for brick in self.bricks:
                if not brick.alive:
                    continue
                if self.ball.bounce_brick(brick.rect):
                    destroyed = brick.hit()
                    if destroyed:
                        self.score += 10 * (BRICK_ROWS - (brick.rect.y - BRICK_TOP_OFFSET) // (BRICK_HEIGHT + BRICK_PADDING))
                        self.logger.debug("Brick destroyed at (%d,%d). Score=%d", brick.rect.x, brick.rect.y, self.score)
                        if random.random() < POWERUP_DROP_CHANCE:
                            ptype = random.choice(POWERUP_TYPES)
                            pu = PowerUp(brick.rect.centerx - POWERUP_SIZE // 2, brick.rect.centery, ptype)
                            self.powerups.append(pu)
                            self.logger.debug("PowerUp spawned: %s at (%d,%d)", ptype, pu.rect.x, pu.rect.y)
                    break

            if self.ball.is_out_bottom(self.window_height):
                self.reset_ball()

        for pu in self.powerups[:]:
            pu.move(dt)
            if pu.is_out_bottom(self.window_height):
                self.powerups.remove(pu)
            elif pu.rect.colliderect(self.paddle.rect):
                self._apply_powerup(pu)
                self.powerups.remove(pu)

        if all(not b.alive for b in self.bricks):
            self.logger.info("All bricks destroyed! Rebuilding...")
            self._build_bricks()

    def draw_hud(self):
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        lives_text = self.font.render(f"Lives: {self.lives}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(lives_text, (self.window_width - 100, 10))
        if self.ball.stuck:
            hint = self.font.render("Press SPACE to launch", True, GRAY)
            hint_rect = hint.get_rect(center=(self.window_width // 2, self.window_height // 2))
            self.screen.blit(hint, hint_rect)

    def draw_game_over(self):
        if self.lives <= 0:
            text = self.big_font.render("GAME OVER", True, RED)
            text_rect = text.get_rect(center=(self.window_width // 2, self.window_height // 2 - 30))
            self.screen.blit(text, text_rect)
            restart = self.font.render("Press R to restart, ESC to quit", True, WHITE)
            restart_rect = restart.get_rect(center=(self.window_width // 2, self.window_height // 2 + 20))
            self.screen.blit(restart, restart_rect)

    def draw(self):
        self.screen.fill(BLACK)
        for brick in self.bricks:
            brick.draw(self.screen)
        self.paddle.draw(self.screen)
        self.ball.draw(self.screen)
        for pu in self.powerups:
            pu.draw(self.screen)
        self.draw_hud()
        self.draw_game_over()
        pygame.display.flip()

    def run(self):
        self.logger.info("Game started")
        while self.running:
            dt = self.clock.tick(self.fps) / 16.667
            self.handle_events()
            if self.lives > 0:
                self.handle_input(dt)
                self.update(dt)
            else:
                self.handle_input(dt)
            self.draw()
        self.logger.info("Game ended")
        pygame.quit()
        sys.exit()


def parse_args(argv):
    parser = argparse.ArgumentParser(description=WINDOW_TITLE)
    parser.add_argument("--fps", type=int, default=FPS, help="Frame rate (default: %(default)s)")
    parser.add_argument("--width", type=int, default=WINDOW_WIDTH, help="Window width (default: %(default)s)")
    parser.add_argument("--height", type=int, default=WINDOW_HEIGHT, help="Window height (default: %(default)s)")
    parser.add_argument("--ball-speed", type=int, default=BALL_SPEED_INIT, help="Initial ball speed (default: %(default)s)")
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
