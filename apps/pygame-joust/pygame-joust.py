import argparse
import logging
import math
import random
import sys

import pygame

# Constraint: 使用Pygame - 2D遊戲原型框架
WINDOW_TITLE = "Joust"

# Constraint: 極簡風格 - minimal geometric style
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLUE = (50, 100, 255)
BROWN = (139, 69, 19)
GRAY = (100, 100, 100)
DARK_GRAY = (40, 40, 40)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
SKY_BLUE = (100, 150, 230)
GROUND_COLOR = (80, 160, 60)

# Problem: 製作Joust遊戲原型 - default settings
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60
GRAVITY = 800.0
FLAP_FORCE = 350.0
PLAYER_SPEED = 250.0
ENEMY_SPEED_MIN = 80.0
ENEMY_SPEED_MAX = 180.0
ENEMY_FLAP_INTERVAL_MIN = 0.8
ENEMY_FLAP_INTERVAL_MAX = 2.0
PLATFORM_HEIGHT = 16
DEFAULT_LIVES = 3
DEFAULT_ENEMIES = 3
GROUND_Y = 560


class Bird:
    def __init__(self, x, y, color, is_player=False):
        self.x = x
        self.y = y
        self.vx = 0.0
        self.vy = 0.0
        self.color = color
        self.is_player = is_player
        self.alive = True
        self.width = 36
        self.height = 24
        self.flap_cooldown = 0.0
        self.facing = 1

    # Problem: Flight physics - apply gravity and flap
    def flap(self, force):
        self.vy = -force
        self.flap_cooldown = 0.15

    def get_rect(self):
        return pygame.Rect(
            int(self.x - self.width // 2),
            int(self.y - self.height // 2),
            self.width,
            self.height,
        )

    def update(self, dt, gravity, platforms, ground_y, window_width, window_height):
        self.flap_cooldown = max(0.0, self.flap_cooldown - dt)

        # Problem: Flight physics - apply gravity
        self.vy += gravity * dt

        # Problem: Flight physics - apply horizontal velocity
        self.x += self.vx * dt
        self.y += self.vy * dt

        # Constraint: 極簡風格 - simple horizontal wrapping
        if self.x < -self.width:
            self.x = window_width + self.width
        elif self.x > window_width + self.width:
            self.x = -self.width

        # Problem: Flight physics - ground collision
        bird_bottom = self.y + self.height // 2
        if bird_bottom >= ground_y:
            self.y = ground_y - self.height // 2
            self.vy = 0.0

        # Problem: Flight physics - ceiling collision
        bird_top = self.y - self.height // 2
        if bird_top < 0:
            self.y = self.height // 2
            self.vy = 0.0

        # Platform collision
        for plat in platforms:
            if plat.collide(self):
                break

    def draw(self, surface):
        rect = self.get_rect()
        # Problem: 極簡風格 - bird as simple body + beak + wing
        body_color = self.color
        body_rect = pygame.Rect(rect.x + 2, rect.y + 4, rect.width - 4, rect.height - 8)
        pygame.draw.ellipse(surface, body_color, body_rect)

        head_radius = 6
        head_cx = rect.right - head_radius - 2 if self.facing > 0 else rect.left + head_radius + 2
        head_cy = rect.centery - 4
        pygame.draw.circle(surface, body_color, (int(head_cx), int(head_cy)), head_radius)

        beak_points = []
        if self.facing > 0:
            beak_points = [
                (rect.right - 2, head_cy - 2),
                (rect.right + 8, head_cy),
                (rect.right - 2, head_cy + 2),
            ]
        else:
            beak_points = [
                (rect.left + 2, head_cy - 2),
                (rect.left - 8, head_cy),
                (rect.left + 2, head_cy + 2),
            ]
        pygame.draw.polygon(surface, YELLOW, beak_points)

        eye_cx = head_cx + (2 if self.facing > 0 else -2)
        eye_cy = head_cy - 2
        pygame.draw.circle(surface, WHITE, (int(eye_cx), int(eye_cy)), 3)
        pygame.draw.circle(surface, BLACK, (int(eye_cx), int(eye_cy)), 1)

        # Constraint: 極簡風格 - wing flap indicator
        wing_y_offset = 2 * math.sin(pygame.time.get_ticks() * 0.008)
        wing_rect = pygame.Rect(
            rect.centerx - 6, rect.centery - 6 + int(wing_y_offset), 12, 12,
        )
        pygame.draw.ellipse(surface, self._darken(body_color), wing_rect)

        # Legs (only when on ground)
        if abs(self.vy) < 5 and self.y + self.height // 2 >= GROUND_Y - 2:
            leg_color = (200, 160, 80)
            leg_spacing = 8
            for lx in (rect.centerx - leg_spacing, rect.centerx + leg_spacing):
                pygame.draw.line(
                    surface, leg_color,
                    (lx, rect.bottom - 2),
                    (lx, rect.bottom + 4), 2,
                )

    def _darken(self, color):
        return tuple(max(0, c - 60) for c in color)


class Platform:
    def __init__(self, x, y, width):
        self.rect = pygame.Rect(x, y, width, PLATFORM_HEIGHT)

    def collide(self, bird):
        # Problem: Flight physics - platform collision (only from above)
        bird_rect = bird.get_rect()
        if not bird_rect.colliderect(self.rect):
            return False
        bird_bottom = bird_rect.bottom
        bird_prev_bottom = bird_bottom - bird.vy * 0.02 if bird.vy else bird_bottom
        if bird.vy >= 0 and bird_prev_bottom <= self.rect.top + 8:
            bird.y = self.rect.top - bird.height // 2
            bird.vy = 0.0
            return True
        return False

    def draw(self, surface):
        pygame.draw.rect(surface, BROWN, self.rect)
        pygame.draw.rect(surface, DARK_GRAY, self.rect, 2)


class Enemy(Bird):
    def __init__(self, x, y, color, speed):
        super().__init__(x, y, color, is_player=False)
        self.speed = speed
        self.move_timer = 0.0
        self.move_dir = random.choice([-1, 1])
        self.flap_timer = random.uniform(ENEMY_FLAP_INTERVAL_MIN, ENEMY_FLAP_INTERVAL_MAX)
        self.vx = self.speed * self.move_dir

    def update(self, dt, gravity, platforms, ground_y, window_width, window_height):
        self.flap_timer -= dt
        if self.flap_timer <= 0:
            self.flap(FLAP_FORCE * random.uniform(0.7, 1.2))
            self.flap_timer = random.uniform(ENEMY_FLAP_INTERVAL_MIN, ENEMY_FLAP_INTERVAL_MAX)

        self.move_timer -= dt
        if self.move_timer <= 0:
            self.move_dir = random.choice([-1, 1])
            self.vx = self.speed * self.move_dir
            self.move_timer = random.uniform(1.0, 3.0)

        self.facing = self.move_dir

        super().update(dt, gravity, platforms, ground_y, window_width, window_height)


class Game:
    def __init__(self, args):
        # Constraint: 使用logger輸出訊息
        self.logger = logging.getLogger("Joust")
        self.logger.setLevel(getattr(logging, args.log_level.upper(), logging.INFO))

        self.window_width = args.width
        self.window_height = args.height
        self.gravity = args.gravity
        self.flap_force = args.flap_force
        self.player_speed = args.player_speed
        self.lives = args.lives
        self.enemy_count = args.enemies

        self.score = 0
        self.game_over = False
        self.won = False
        self.level = 1

        pygame.init()
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        self.big_font = pygame.font.Font(None, 36)
        self.running = True

        self.ground_y = self.window_height - 40

        # Constraint: 極簡風格 - platforms as simple rectangles
        self.platforms = [
            Platform(100, 400, 120),
            Platform(300, 320, 100),
            Platform(500, 380, 140),
            Platform(200, 220, 100),
            Platform(450, 240, 120),
            Platform(100, 140, 80),
            Platform(600, 160, 120),
        ]

        # Problem: 製作Joust遊戲原型 - player bird
        self.player = Bird(
            self.window_width // 2, self.ground_y - 20, GREEN, is_player=True,
        )

        # Problem: 製作Joust遊戲原型 - enemy birds
        self.enemies = []
        self._spawn_enemies()

        # Constraint: 使用logger輸出訊息
        self.logger.info(
            "Game initialized: %dx%d, gravity=%.1f, flap=%.1f, enemies=%d, lives=%d",
            self.window_width, self.window_height, self.gravity, self.flap_force,
            self.enemy_count, self.lives,
        )

    def _spawn_enemies(self):
        self.enemies.clear()
        for _ in range(self.enemy_count):
            x = random.randint(100, self.window_width - 100)
            y = random.randint(80, self.ground_y - 100)
            speed = random.uniform(ENEMY_SPEED_MIN, ENEMY_SPEED_MAX)
            colors = [RED, ORANGE, (200, 50, 200), (50, 200, 200)]
            enemy = Enemy(x, y, random.choice(colors), speed)
            self.enemies.append(enemy)

    # Task: Flight physics, vertical collision priority
    def _check_collisions(self):
        player_rect = self.player.get_rect()
        for enemy in list(self.enemies):
            if not enemy.alive:
                continue
            enemy_rect = enemy.get_rect()
            if not player_rect.colliderect(enemy_rect):
                continue

            # Problem: Vertical collision priority
            # If player center is above enemy center by enough margin, kill enemy
            player_bottom = player_rect.centery
            enemy_top = enemy_rect.centery
            margin = 10

            if player_bottom < enemy_top - margin:
                # Constraint: Vertical collision priority - player above kills enemy
                self.logger.debug("Enemy killed by player at (%.0f, %.0f)", enemy.x, enemy.y)
                enemy.alive = False
                self.score += 100
                self.player.vy = -self.flap_force * 0.6
                self.logger.info("Enemy killed! Score: %d", self.score)
            else:
                # Constraint: Vertical collision priority - player hit from below dies
                self.logger.debug("Player hit by enemy at (%.0f, %.0f)", enemy.x, enemy.y)
                self._player_die()
                return

        # Respawn enemies when all are dead
        if self.enemies and all(not e.alive for e in self.enemies):
            self.logger.info("All enemies defeated! Level %d complete", self.level)
            self.level += 1
            self.enemy_count = min(self.enemy_count + 1, 8)
            self._spawn_enemies()

    def _player_die(self):
        self.lives -= 1
        self.logger.debug("Player died. Lives left: %d", self.lives)
        if self.lives <= 0:
            self.game_over = True
            self.logger.info("Game over - no lives remaining")
        else:
            self.player.x = self.window_width // 2
            self.player.y = self.ground_y - 20
            self.player.vy = 0.0
            self.player.vx = 0.0
            self.player.alive = True

    def handle_events(self):
        # Task: 使腳本接收輸入參數 - keyboard input handled via key states
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_r and self.game_over:
                    self.reset_game()

        keys = pygame.key.get_pressed()
        if not self.game_over:
            # Constraint: Flight physics - horizontal movement
            if keys[pygame.K_LEFT]:
                self.player.vx = -self.player_speed
                self.player.facing = -1
            elif keys[pygame.K_RIGHT]:
                self.player.vx = self.player_speed
                self.player.facing = 1
            else:
                self.player.vx = 0.0

            # Problem: Flight physics - flap on space
            if keys[pygame.K_SPACE] and self.player.flap_cooldown <= 0:
                self.player.flap(self.flap_force)
                self.logger.debug("Player flapped at y=%.0f", self.player.y)

    def reset_game(self):
        self.logger.info("Game reset")
        self.lives = DEFAULT_LIVES
        self.score = 0
        self.level = 1
        self.game_over = False
        self.enemy_count = DEFAULT_ENEMIES
        self.player.x = self.window_width // 2
        self.player.y = self.ground_y - 20
        self.player.vy = 0.0
        self.player.vx = 0.0
        self.player.alive = True
        self._spawn_enemies()

    def update(self, dt):
        if self.game_over:
            return

        # Problem: Flight physics - update player
        self.player.update(dt, self.gravity, self.platforms, self.ground_y, self.window_width, self.window_height)

        # Problem: Flight physics - update enemies
        for enemy in self.enemies:
            if enemy.alive:
                enemy.update(dt, self.gravity, self.platforms, self.ground_y, self.window_width, self.window_height)

        # Problem: Vertical collision priority
        self._check_collisions()

    def draw(self):
        self.screen.fill(SKY_BLUE)

        # Draw ground
        ground_rect = pygame.Rect(0, self.ground_y, self.window_width, self.window_height - self.ground_y)
        pygame.draw.rect(self.screen, GROUND_COLOR, ground_rect)
        pygame.draw.rect(self.screen, DARK_GRAY, (0, self.ground_y, self.window_width, 2))

        # Constraint: 極簡風格 - draw platforms
        for plat in self.platforms:
            plat.draw(self.screen)

        # Draw enemies
        for enemy in self.enemies:
            if enemy.alive:
                enemy.draw(self.screen)

        # Draw player
        if not self.game_over:
            self.player.draw(self.screen)

        # HUD
        score_surf = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_surf, (10, 10))
        lives_surf = self.font.render(f"Lives: {self.lives}", True, WHITE)
        self.screen.blit(lives_surf, (10, 30))
        level_surf = self.font.render(f"Level: {self.level}", True, WHITE)
        self.screen.blit(level_surf, (10, 50))

        # Help text
        help_surf = self.font.render("Arrow keys: move | Space: flap | ESC: quit", True, WHITE)
        self.screen.blit(help_surf, (10, self.window_height - 20))

        if self.game_over:
            msg = self.big_font.render("Game Over! (R to restart, ESC to quit)", True, RED)
            msg_rect = msg.get_rect(center=(self.window_width // 2, self.window_height // 2))
            self.screen.blit(msg, msg_rect)

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


# Task: 使腳本接收輸入參數
def parse_args(argv):
    parser = argparse.ArgumentParser(description=WINDOW_TITLE)
    parser.add_argument("--width", type=int, default=WINDOW_WIDTH, help="Window width (default: %(default)s)")
    parser.add_argument("--height", type=int, default=WINDOW_HEIGHT, help="Window height (default: %(default)s)")
    parser.add_argument("--gravity", type=float, default=GRAVITY, help="Gravity strength (default: %(default)s)")
    parser.add_argument("--flap-force", type=float, default=FLAP_FORCE, help="Flap upward force (default: %(default)s)")
    parser.add_argument("--player-speed", type=float, default=PLAYER_SPEED, help="Player horizontal speed (default: %(default)s)")
    parser.add_argument("--lives", type=int, default=DEFAULT_LIVES, help="Number of lives (default: %(default)s)")
    parser.add_argument("--enemies", type=int, default=DEFAULT_ENEMIES, help="Initial enemy count (default: %(default)s)")
    parser.add_argument(
        "--log-level", type=str, default="INFO",
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
