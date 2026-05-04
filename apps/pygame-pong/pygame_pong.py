import argparse
import logging
import sys
import math
import random

import pygame

WINDOW_TITLE = "Pong"
FPS = 60
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

PADDLE_WIDTH = 10
PADDLE_HEIGHT = 80
PADDLE_MARGIN = 20
PADDLE_SPEED = 5
AI_SPEED = 4

BALL_SIZE = 10
BALL_SPEED_X = 5
BALL_SPEED_Y = 3

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)

WINNING_SCORE = 5


class Paddle:
    def __init__(self, x, y, width, height, speed):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed
        self.direction = 0

    def move(self, dt, window_height):
        self.rect.y += self.direction * self.speed * dt
        self.rect.y = max(0, min(self.rect.y, window_height - self.rect.height))

    def reset(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def draw(self, surface):
        pygame.draw.rect(surface, WHITE, self.rect)


class Ball:
    def __init__(self, x, y, size, speed_x, speed_y):
        self.rect = pygame.Rect(x, y, size, size)
        self.speed_x_init = speed_x
        self.speed_y_init = speed_y
        self.speed_x = speed_x * random.choice([-1, 1])
        self.speed_y = speed_y * random.choice([-1, 1])

    def move(self, dt):
        self.rect.x += self.speed_x * dt
        self.rect.y += self.speed_y * dt

    def bounce_wall(self, window_height):
        if self.rect.top <= 0 or self.rect.bottom >= window_height:
            self.speed_y = -self.speed_y
            self.rect.y = max(0, min(self.rect.y, window_height - self.rect.height))
            return True
        return False

    def bounce_paddle(self, paddle_rect):
        if self.rect.colliderect(paddle_rect):
            paddle_center = paddle_rect.centery
            ball_center = self.rect.centery
            offset = (ball_center - paddle_center) / (paddle_rect.height / 2)
            offset = max(-1.0, min(1.0, offset))
            angle = offset * (math.pi / 3)
            speed = math.sqrt(self.speed_x**2 + self.speed_y**2)
            self.speed_x = speed * math.cos(angle)
            self.speed_y = speed * math.sin(angle)
            if self.rect.centerx < paddle_rect.centerx:
                self.speed_x = -abs(self.speed_x)
            else:
                self.speed_x = abs(self.speed_x)
            return True
        return False

    def is_out_left(self):
        return self.rect.right <= 0

    def is_out_right(self, window_width):
        return self.rect.left >= window_width

    def reset(self, x, y):
        self.rect.x = x
        self.rect.y = y
        self.speed_x = self.speed_x_init * random.choice([-1, 1])
        self.speed_y = self.speed_y_init * random.choice([-1, 1])

    def draw(self, surface):
        pygame.draw.rect(surface, WHITE, self.rect)


class AI:
    def __init__(self, paddle, speed, reaction_delay=0.15):
        self.paddle = paddle
        self.speed = speed
        self.reaction_delay = reaction_delay
        self.timer = 0.0
        self.target_y = paddle.rect.centery

    def update(self, ball, dt):
        self.timer += dt
        if self.timer >= self.reaction_delay:
            self.timer = 0.0
            self.target_y = ball.rect.centery
        diff = self.target_y - self.paddle.rect.centery
        if abs(diff) > self.speed * dt:
            self.paddle.direction = 1 if diff > 0 else -1
        else:
            self.paddle.direction = 0


class Game:
    def __init__(self, args):
        self.logger = logging.getLogger("Pong")
        self.logger.setLevel(getattr(logging, args.log_level.upper(), logging.INFO))
        self.window_width = args.width
        self.window_height = args.height
        self.fps = args.fps
        self.ai_speed = args.ai_speed
        self.ball_speed_x = args.ball_speed
        self.player_score = 0
        self.ai_score = 0

        pygame.init()
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.running = True

        paddle_x_left = PADDLE_MARGIN
        paddle_x_right = self.window_width - PADDLE_MARGIN - PADDLE_WIDTH
        paddle_y_center = self.window_height // 2 - PADDLE_HEIGHT // 2

        self.player_paddle = Paddle(
            paddle_x_left, paddle_y_center, PADDLE_WIDTH, PADDLE_HEIGHT, PADDLE_SPEED
        )
        self.ai_paddle = Paddle(
            paddle_x_right, paddle_y_center, PADDLE_WIDTH, PADDLE_HEIGHT, PADDLE_SPEED
        )
        self.ai_controller = AI(self.ai_paddle, self.ai_speed)

        ball_x = self.window_width // 2 - BALL_SIZE // 2
        ball_y = self.window_height // 2 - BALL_SIZE // 2
        self.ball = Ball(ball_x, ball_y, BALL_SIZE, self.ball_speed_x, BALL_SPEED_Y)

        self.logger.info("Game initialized: %dx%d, fps=%d", self.window_width, self.window_height, self.fps)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_r and (self.player_score >= WINNING_SCORE or self.ai_score >= WINNING_SCORE):
                    self.reset_game()

    def handle_input(self, dt):
        keys = pygame.key.get_pressed()
        self.player_paddle.direction = 0
        if keys[pygame.K_w]:
            self.player_paddle.direction = -1
        elif keys[pygame.K_s]:
            self.player_paddle.direction = 1

    def reset_round(self, scorer):
        self.logger.info("Point scored by %s. Score: Player %d - AI %d", scorer, self.player_score, self.ai_score)
        ball_x = self.window_width // 2 - BALL_SIZE // 2
        ball_y = self.window_height // 2 - BALL_SIZE // 2
        self.ball.reset(ball_x, ball_y)
        paddle_y_center = self.window_height // 2 - PADDLE_HEIGHT // 2
        self.player_paddle.reset(PADDLE_MARGIN, paddle_y_center)
        self.ai_paddle.reset(
            self.window_width - PADDLE_MARGIN - PADDLE_WIDTH,
            paddle_y_center,
        )

    def reset_game(self):
        self.logger.info("Game reset")
        self.player_score = 0
        self.ai_score = 0
        self.reset_round("none")

    def update(self, dt):
        self.player_paddle.move(dt, self.window_height)
        self.ai_controller.update(self.ball, dt)
        self.ai_paddle.move(dt, self.window_height)

        old_pos = (self.ball.rect.x, self.ball.rect.y, self.ball.speed_x, self.ball.speed_y)
        self.ball.move(dt)
        if self.ball.bounce_wall(self.window_height):
            self.logger.debug("Ball bounced off wall at pos=(%d,%d)", self.ball.rect.x, self.ball.rect.y)

        if self.ball.bounce_paddle(self.player_paddle.rect):
            self.logger.debug("Ball bounced off player paddle. speed=(%.1f,%.1f)", self.ball.speed_x, self.ball.speed_y)
        if self.ball.bounce_paddle(self.ai_paddle.rect):
            self.logger.debug("Ball bounced off AI paddle. speed=(%.1f,%.1f)", self.ball.speed_x, self.ball.speed_y)

        if self.ball.is_out_left():
            self.ai_score += 1
            self.reset_round("AI")
        elif self.ball.is_out_right(self.window_width):
            self.player_score += 1
            self.reset_round("Player")

    def draw_center_line(self):
        for y in range(0, self.window_height, 30):
            pygame.draw.rect(self.screen, GRAY, (self.window_width // 2 - 1, y, 2, 15))

    def draw_score(self):
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        self.screen.blit(player_text, (self.window_width // 2 - 60, 30))
        self.screen.blit(ai_text, (self.window_width // 2 + 50, 30))

    def draw_game_over(self):
        if self.player_score >= WINNING_SCORE:
            text = self.font.render("Player Wins! (R to restart, ESC to quit)", True, WHITE)
        elif self.ai_score >= WINNING_SCORE:
            text = self.font.render("AI Wins! (R to restart, ESC to quit)", True, WHITE)
        else:
            return
        text_rect = text.get_rect(center=(self.window_width // 2, self.window_height // 2 - 50))
        self.screen.blit(text, text_rect)
        self.running = False

    def draw(self):
        self.screen.fill(BLACK)
        self.draw_center_line()
        self.player_paddle.draw(self.screen)
        self.ai_paddle.draw(self.screen)
        self.ball.draw(self.screen)
        self.draw_score()
        self.draw_game_over()
        pygame.display.flip()

    def run(self):
        self.logger.info("Game started")
        while self.running or (self.player_score >= WINNING_SCORE or self.ai_score >= WINNING_SCORE):
            if self.running:
                dt = self.clock.tick(self.fps) / 16.667
                self.handle_events()
                self.handle_input(dt)
                self.update(dt)
                self.draw()
            else:
                self.clock.tick(self.fps)
                self.handle_events()
        self.logger.info("Game ended")
        pygame.quit()
        sys.exit()


def parse_args(argv):
    parser = argparse.ArgumentParser(description=WINDOW_TITLE)
    parser.add_argument("--fps", type=int, default=FPS, help="Frame rate (default: %(default)s)")
    parser.add_argument("--width", type=int, default=WINDOW_WIDTH, help="Window width (default: %(default)s)")
    parser.add_argument("--height", type=int, default=WINDOW_HEIGHT, help="Window height (default: %(default)s)")
    parser.add_argument("--ball-speed", type=int, default=BALL_SPEED_X, help="Initial ball speed (default: %(default)s)")
    parser.add_argument("--ai-speed", type=int, default=AI_SPEED, help="AI paddle speed (default: %(default)s)")
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
