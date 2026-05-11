import argparse
import logging
import sys
import math
import random

import pygame

# Constraint: 使用Pygame - 適合製作2D遊戲原型, 輕量化
# Constraint: 用極簡風格呈現 - 強調玩法概念, 節省製作時間

WINDOW_TITLE = "Space Invaders"
FPS = 60
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

PLAYER_WIDTH = 50
PLAYER_HEIGHT = 20
PLAYER_SPEED = 5
PLAYER_MARGIN_BOTTOM = 30

ALIEN_COLS = 11
ALIEN_ROWS = 5
ALIEN_WIDTH = 40
ALIEN_HEIGHT = 30
ALIEN_PADDING = 10
ALIEN_TOP_OFFSET = 60
ALIEN_BASE_SPEED = 2
ALIEN_STEP_DOWN = 20

LASER_WIDTH = 3
LASER_HEIGHT = 12
LASER_SPEED = 8
PLAYER_FIRE_COOLDOWN = 0.3

ALIEN_SHOOT_CHANCE = 0.002

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (50, 255, 50)
RED = (255, 50, 50)
GRAY = (100, 100, 100)
YELLOW = (255, 255, 50)


class Player:
    # Constraint: 用極簡風格呈現 - 簡單矩形表示玩家
    def __init__(self, x, y, width, height, speed):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed
        self.direction = 0

    def move(self, dt, window_width):
        self.rect.x += self.direction * self.speed * dt
        self.rect.x = max(0, min(self.rect.x, window_width - self.rect.width))

    def reset(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def draw(self, surface):
        pygame.draw.rect(surface, GREEN, self.rect)
        tip_x = self.rect.centerx - 3
        tip_y = self.rect.top - 8
        pygame.draw.polygon(surface, GREEN, [
            (tip_x, self.rect.top),
            (tip_x + 6, self.rect.top),
            (self.rect.centerx, tip_y),
        ])


class Alien:
    # Constraint: 用極簡風格呈現 - 簡單矩形表示外星人
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)
        self.alive = True

    def draw(self, surface):
        if not self.alive:
            return
        color_map = {
            0: RED,
            1: YELLOW,
            2: GRAY,
            3: YELLOW,
            4: RED,
        }
        row = (self.rect.y - ALIEN_TOP_OFFSET) // (ALIEN_HEIGHT + ALIEN_PADDING)
        color = color_map.get(row, WHITE)
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 1)


class Laser:
    def __init__(self, x, y, width, height, speed):
        self.rect = pygame.Rect(x, y, width, height)
        self.speed = speed

    def move(self, dt):
        self.rect.y += self.speed * dt

    def is_out(self, window_height):
        return self.rect.bottom < 0 or self.rect.top > window_height

    def draw(self, surface):
        pygame.draw.rect(surface, RED, self.rect)


class Game:
    def __init__(self, args):
        # Constraint: 使用logger輸出訊息 - 用於人類跟AI除錯
        self.logger = logging.getLogger("SpaceInvaders")
        self.logger.setLevel(getattr(logging, args.log_level.upper(), logging.INFO))
        self.window_width = args.width
        self.window_height = args.height
        self.fps = args.fps
        self.alien_base_speed = args.alien_speed
        self.lives = 3
        self.score = 0
        self.level = 1
        self.game_over = False

        pygame.init()
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 28)
        self.big_font = pygame.font.Font(None, 48)
        self.running = True

        player_x = self.window_width // 2 - PLAYER_WIDTH // 2
        player_y = self.window_height - PLAYER_MARGIN_BOTTOM - PLAYER_HEIGHT
        self.player = Player(player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT, PLAYER_SPEED)

        self.aliens = []
        self.player_lasers = []
        self.alien_lasers = []
        self.fire_timer = 0.0
        self.alien_direction = 1
        self.alien_move_timer = 0.0
        self.alien_move_interval = 1.0

        self._build_formation()

        self.logger.info(
            "Game initialized: %dx%d, fps=%d, aliens=%d",
            self.window_width, self.window_height, self.fps,
            ALIEN_ROWS * ALIEN_COLS,
        )

    # Problem: 製作Space Invaders遊戲原型 - Alien formation
    def _build_formation(self):
        self.aliens = []
        for row in range(ALIEN_ROWS):
            for col in range(ALIEN_COLS):
                x = col * (ALIEN_WIDTH + ALIEN_PADDING) + ALIEN_PADDING + 50
                y = row * (ALIEN_HEIGHT + ALIEN_PADDING) + ALIEN_TOP_OFFSET
                alien = Alien(x, y, ALIEN_WIDTH, ALIEN_HEIGHT)
                self.aliens.append(alien)
        self._update_move_interval()

    def _update_move_interval(self):
        alive_count = sum(1 for a in self.aliens if a.alive)
        total = ALIEN_ROWS * ALIEN_COLS
        if alive_count == 0:
            return
        # Problem: Increasing difficulty - speed increases as aliens are destroyed
        ratio = alive_count / total
        min_interval = 0.2
        max_interval = 1.0
        self.alien_move_interval = max_interval - (max_interval - min_interval) * (1 - ratio)
        self.logger.debug("Move interval updated: %.3f (aliens alive: %d/%d)", self.alien_move_interval, alive_count, total)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE and self.game_over:
                    self.reset_game()
                elif event.key == pygame.K_r and self.game_over:
                    self.reset_game()

    def handle_input(self, dt):
        if self.game_over:
            return
        keys = pygame.key.get_pressed()
        self.player.direction = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.player.direction = -1
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.player.direction = 1

        if keys[pygame.K_SPACE] and self.fire_timer <= 0:
            self._player_shoot()
            self.fire_timer = PLAYER_FIRE_COOLDOWN

    def _player_shoot(self):
        laser = Laser(
            self.player.rect.centerx - LASER_WIDTH // 2,
            self.player.rect.top - LASER_HEIGHT,
            LASER_WIDTH,
            LASER_HEIGHT,
            -LASER_SPEED,
        )
        self.player_lasers.append(laser)
        self.logger.debug("Player fired at x=%d", self.player.rect.centerx)

    # Problem: Space Invaders - Alien shooting
    def _alien_shoot(self):
        alive_aliens = [a for a in self.aliens if a.alive]
        if not alive_aliens:
            return
        shooter = random.choice(alive_aliens)
        laser = Laser(
            shooter.rect.centerx - LASER_WIDTH // 2,
            shooter.rect.bottom,
            LASER_WIDTH,
            LASER_HEIGHT,
            LASER_SPEED,
        )
        self.alien_lasers.append(laser)

    # Problem: Space Invaders - Formation movement
    def _move_aliens(self):
        if not any(a.alive for a in self.aliens):
            return

        edge_reached = False
        for alien in self.aliens:
            if not alien.alive:
                continue
            alien.rect.x += self.alien_direction * self.alien_base_speed
            if alien.rect.right >= self.window_width or alien.rect.left <= 0:
                edge_reached = True

        if edge_reached:
            self.alien_direction *= -1
            for alien in self.aliens:
                if not alien.alive:
                    continue
                alien.rect.y += ALIEN_STEP_DOWN
                alien.rect.x += self.alien_direction * self.alien_base_speed
                if alien.rect.bottom >= self.window_height:
                    self.logger.info("Aliens reached the bottom")
                    self.game_over = True

    def _check_collisions(self):
        for laser in self.player_lasers[:]:
            for alien in self.aliens:
                if not alien.alive:
                    continue
                if laser.rect.colliderect(alien.rect):
                    alien.alive = False
                    self.score += 10
                    self.logger.debug("Alien destroyed at (%d,%d). Score=%d", alien.rect.x, alien.rect.y, self.score)
                    if laser in self.player_lasers:
                        self.player_lasers.remove(laser)
                    self._update_move_interval()
                    break

        for laser in self.alien_lasers[:]:
            if laser.rect.colliderect(self.player.rect):
                self.lives -= 1
                self.logger.info("Player hit. Lives remaining: %d", self.lives)
                if laser in self.alien_lasers:
                    self.alien_lasers.remove(laser)
                if self.lives <= 0:
                    self.game_over = True

    def _check_level_clear(self):
        if all(not a.alive for a in self.aliens):
            self.level += 1
            self.logger.info("Level %d cleared!", self.level - 1)
            self.alien_base_speed = ALIEN_BASE_SPEED + (self.level - 1) * 0.5
            self._build_formation()
            self.player_lasers.clear()
            self.alien_lasers.clear()

    def reset_game(self):
        self.logger.info("Game reset")
        self.lives = 3
        self.score = 0
        self.level = 1
        self.game_over = False
        self.alien_base_speed = ALIEN_BASE_SPEED
        self.alien_direction = 1
        self.alien_move_timer = 0.0
        self.player_lasers.clear()
        self.alien_lasers.clear()
        player_x = self.window_width // 2 - PLAYER_WIDTH // 2
        player_y = self.window_height - PLAYER_MARGIN_BOTTOM - PLAYER_HEIGHT
        self.player.reset(player_x, player_y)
        self._build_formation()

    def update(self, dt):
        if self.game_over:
            return

        self.fire_timer = max(0, self.fire_timer - dt)

        self.player.move(dt, self.window_width)

        self.alien_move_timer += dt
        if self.alien_move_timer >= self.alien_move_interval:
            self.alien_move_timer = 0.0
            self._move_aliens()

        for laser in self.player_lasers[:]:
            laser.move(dt)
            if laser.is_out(self.window_height):
                self.player_lasers.remove(laser)

        for laser in self.alien_lasers[:]:
            laser.move(dt)
            if laser.is_out(self.window_height):
                self.alien_lasers.remove(laser)

        if random.random() < ALIEN_SHOOT_CHANCE:
            self._alien_shoot()

        self._check_collisions()
        self._check_level_clear()

    def draw_hud(self):
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        lives_text = self.font.render(f"Lives: {self.lives}", True, WHITE)
        level_text = self.font.render(f"Level: {self.level}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(lives_text, (self.window_width - 100, 10))
        self.screen.blit(level_text, (self.window_width // 2 - 40, 10))

    def draw_game_over(self):
        if self.game_over:
            text = self.big_font.render("GAME OVER", True, RED)
            text_rect = text.get_rect(center=(self.window_width // 2, self.window_height // 2 - 30))
            self.screen.blit(text, text_rect)
            restart = self.font.render("Press R to restart, ESC to quit", True, WHITE)
            restart_rect = restart.get_rect(center=(self.window_width // 2, self.window_height // 2 + 20))
            self.screen.blit(restart, restart_rect)

    def draw(self):
        self.screen.fill(BLACK)
        for alien in self.aliens:
            alien.draw(self.screen)
        self.player.draw(self.screen)
        for laser in self.player_lasers:
            laser.draw(self.screen)
        for laser in self.alien_lasers:
            laser.draw(self.screen)
        self.draw_hud()
        self.draw_game_over()
        pygame.display.flip()

    def run(self):
        self.logger.info("Game started")
        while self.running:
            dt = self.clock.tick(self.fps) / 16.667
            self.handle_events()
            if self.lives > 0 and not self.game_over:
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
    parser.add_argument(
        "--alien-speed", type=float, default=ALIEN_BASE_SPEED,
        help="Alien movement base speed in pixels per move (default: %(default)s)",
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
