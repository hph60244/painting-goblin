#!/usr/bin/env python3
# Problem: 製作Galaga遊戲原型

import argparse
import logging
import math
import random
import sys

import pygame


# Constraint: 使用logger輸出訊息
logger = logging.getLogger(__name__)


# ----
# Constraint: 使用Pygame - constants
# ----
SCREEN_WIDTH = 480
SCREEN_HEIGHT = 640
FPS = 60

PLAYER_SPEED = 5
BULLET_SPEED = 8
ENEMY_BULLET_SPEED = 4

FORMATION_COLS = 8
FORMATION_ROWS = 4
FORMATION_TOP = 60
FORMATION_SPACING_X = 48
FORMATION_SPACING_Y = 40

DIVE_INTERVAL_MIN = 180
DIVE_INTERVAL_MAX = 360

WAVE_ENTER_SPEED = 2
FORMATION_AMPLITUDE = 8
FORMATION_FREQUENCY = 0.02

COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)
COLOR_GREEN = (0, 255, 0)
COLOR_RED = (255, 50, 50)
COLOR_CYAN = (0, 200, 255)
COLOR_YELLOW = (255, 255, 0)


# ----
# Task: 使腳本接收輸入參數
# ----
def parse_args():
    parser = argparse.ArgumentParser(description="Galaga game prototype")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging")
    parser.add_argument("--fps", type=int, default=FPS, help=f"Target FPS (default: {FPS})")
    parser.add_argument("--width", type=int, default=SCREEN_WIDTH, help=f"Screen width (default: {SCREEN_WIDTH})")
    parser.add_argument("--height", type=int, default=SCREEN_HEIGHT, help=f"Screen height (default: {SCREEN_HEIGHT})")
    return parser.parse_args()


def setup_logging(debug: bool):
    level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(level=level, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    logger.debug("Debug logging enabled")


# ----
# Constraint: 用極簡風格呈現 - simple shape-based entities
# ----
class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 24
        self.height = 24
        self.speed = PLAYER_SPEED
        self.alive = True
        self.shoot_cooldown = 0
        logger.debug(f"Player created at ({x}, {y})")

    def update(self, keys, screen_width):
        # Constraint: 用極簡風格呈現 - simple left/right movement
        if keys[pygame.K_LEFT] and self.x > self.width // 2:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < screen_width - self.width // 2:
            self.x += self.speed
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def shoot(self):
        if self.shoot_cooldown == 0:
            self.shoot_cooldown = 12
            return Bullet(self.x, self.y - self.height // 2, 0, -BULLET_SPEED, is_player=True)
        return None

    # Constraint: 用極簡風格呈現 - draw as triangle
    def draw(self, screen):
        if not self.alive:
            return
        color = COLOR_GREEN if self.alive else COLOR_RED
        half_w = self.width // 2
        half_h = self.height // 2
        points = [
            (self.x, self.y - half_h),
            (self.x - half_w, self.y + half_h),
            (self.x + half_w, self.y + half_h),
        ]
        pygame.draw.polygon(screen, color, points)

    def get_rect(self):
        return pygame.Rect(self.x - self.width // 2, self.y - self.height // 2, self.width, self.height)


class Bullet:
    def __init__(self, x, y, vx, vy, is_player=True):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.is_player = is_player
        self.radius = 3
        self.alive = True

    def update(self):
        self.x += self.vx
        self.y += self.vy

    # Constraint: 用極簡風格呈現 - draw as small circles
    def draw(self, screen):
        if not self.alive:
            return
        color = COLOR_CYAN if self.is_player else COLOR_RED
        pygame.draw.circle(screen, color, (int(self.x), int(self.y)), self.radius)

    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius, self.radius * 2, self.radius * 2)


# ----
# Contract: Formation patterns
# Contract: dive-bomb AI
# ----
class Enemy:
    # States for enemy behavior
    STATE_ENTERING = "entering"
    STATE_FORMATION = "formation"
    STATE_DIVING = "diving"
    STATE_RETURNING = "returning"

    def __init__(self, col, row, target_x, target_y):
        self.col = col
        self.row = row
        self.target_x = target_x
        self.target_y = target_y
        self.start_x = target_x + (col - FORMATION_COLS // 2) * 100
        self.start_y = -40
        self.x = self.start_x
        self.y = self.start_y
        self.width = 28
        self.height = 28
        self.state = Enemy.STATE_ENTERING
        self.alive = True
        self.enter_progress = 0.0
        self.dive_timer = 0
        self.dive_phase = 0.0
        self.dive_start_x = 0
        self.dive_start_y = 0
        self.dive_target_x = 0
        self.dive_target_y = 0
        self.shoot_cooldown = 0
        self.formation_offset = random.uniform(0, math.pi * 2)
        logger.debug(f"Enemy created at col={col} row={row} target=({target_x},{target_y})")

    def update(self, player_x, player_y):
        if not self.alive:
            return None

        bullet = None

        # Constraint: 用極簡風格呈現 - simple state machine
        if self.state == Enemy.STATE_ENTERING:
            self.enter_progress += 0.02
            progress = min(self.enter_progress, 1.0)
            eased = 1 - (1 - progress) ** 3
            self.x = self.start_x + (self.target_x - self.start_x) * eased
            self.y = self.start_y + (self.target_y - self.start_y) * eased
            if progress >= 1.0:
                self.state = Enemy.STATE_FORMATION
                logger.debug(f"Enemy ({self.col},{self.row}) reached formation")

        elif self.state == Enemy.STATE_FORMATION:
            # Floating oscillation
            self.x = self.target_x + math.sin(self.formation_offset + pygame.time.get_ticks() * FORMATION_FREQUENCY) * FORMATION_AMPLITUDE
            self.y = self.target_y

        elif self.state == Enemy.STATE_DIVING:
            # Contract: dive-bomb AI - sinusoidal dive path toward player
            self.dive_phase += 0.03
            progress = min(self.dive_phase, 1.0)
            # Bezier-like swoop
            cx = (self.dive_start_x + self.dive_target_x) / 2
            cy = min(self.dive_start_y, self.dive_target_y) - 100
            t = progress
            self.x = (1 - t) ** 2 * self.dive_start_x + 2 * (1 - t) * t * cx + t ** 2 * self.dive_target_x
            self.y = (1 - t) ** 2 * self.dive_start_y + 2 * (1 - t) * t * cy + t ** 2 * self.dive_target_y

            # Contract: bullet-hell - shoot during dive
            if self.shoot_cooldown <= 0 and progress > 0.2:
                bullet = Bullet(self.x, self.y + self.height // 2, 0, ENEMY_BULLET_SPEED, is_player=False)
                self.shoot_cooldown = 60
                logger.debug(f"Enemy ({self.col},{self.row}) fired bullet during dive")
            if self.shoot_cooldown > 0:
                self.shoot_cooldown -= 1

            if progress >= 1.0:
                self.state = Enemy.STATE_RETURNING
                logger.debug(f"Enemy ({self.col},{self.row}) returning to formation")

        elif self.state == Enemy.STATE_RETURNING:
            dx = self.target_x - self.x
            dy = self.target_y - self.y
            dist = math.sqrt(dx * dx + dy * dy)
            if dist < 4:
                self.x = self.target_x
                self.y = self.target_y
                self.state = Enemy.STATE_FORMATION
                logger.debug(f"Enemy ({self.col},{self.row}) back in formation")
            else:
                speed = 3
                self.x += (dx / dist) * speed
                self.y += (dy / dist) * speed

        return bullet if bullet and bullet.alive else None

    # Constraint: 用極簡風格呈現 - draw as simple bug shape
    def draw(self, screen):
        if not self.alive:
            return
        if self.state == Enemy.STATE_ENTERING:
            alpha = max(0, min(255, int(255 * self.enter_progress)))
            color = (alpha // 2, alpha, alpha // 2)
        else:
            color = COLOR_RED
        half_w = self.width // 2
        half_h = self.height // 2
        # Body
        pygame.draw.ellipse(screen, color, (self.x - half_w, self.y - half_h, self.width, self.height))
        # Wings
        wing_color = (color[0] // 2, color[1] // 2, color[2] // 2)
        pygame.draw.ellipse(screen, wing_color, (self.x - half_w - 6, self.y - half_h + 4, 8, self.height - 8))
        pygame.draw.ellipse(screen, wing_color, (self.x + half_w - 2, self.y - half_h + 4, 8, self.height - 8))

    def get_rect(self):
        return pygame.Rect(self.x - self.width // 2, self.y - self.height // 2, self.width, self.height)

    def start_dive(self, target_x, target_y):
        # Contract: dive-bomb AI - initiate dive toward player
        self.state = Enemy.STATE_DIVING
        self.dive_phase = 0.0
        self.dive_start_x = self.x
        self.dive_start_y = self.y
        self.dive_target_x = target_x
        self.dive_target_y = target_y
        self.shoot_cooldown = 30
        logger.debug(f"Enemy ({self.col},{self.row}) started dive toward ({target_x},{target_y})")


class Game:
    def __init__(self, args):
        self.args = args
        self.screen_width = args.width
        self.screen_height = args.height
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Galaga Prototype")
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)

        # Game objects
        self.player = Player(self.screen_width // 2, self.screen_height - 60)
        self.player_bullets = []
        self.enemy_bullets = []
        self.enemies = []
        self.score = 0
        self.wave = 0
        self.state = "playing"

        # Contract: Formation patterns - create initial formation
        self.spawn_wave()
        logger.info(f"Game initialized - screen: {self.screen_width}x{self.screen_height}")

    def spawn_wave(self):
        # Contract: Formation patterns - staggered arrival
        self.wave += 1
        self.enemies.clear()
        logger.info(f"Wave {self.wave} starting")

        base_x = self.screen_width // 2 - (FORMATION_COLS - 1) * FORMATION_SPACING_X // 2
        base_y = FORMATION_TOP

        for row in range(FORMATION_ROWS):
            for col in range(FORMATION_COLS):
                # Stagger: every other column offset slightly
                stagger_x = FORMATION_SPACING_X // 2 if row % 2 == 1 else 0
                tx = base_x + col * FORMATION_SPACING_X + stagger_x
                ty = base_y + row * FORMATION_SPACING_Y
                enemy = Enemy(col, row, tx, ty)
                # Stagger entry
                enemy.enter_progress = -(col + row * FORMATION_COLS) * 0.04
                self.enemies.append(enemy)

        logger.debug(f"Spawned {len(self.enemies)} enemies")

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                # Task: 使腳本接收輸入參數 - space to shoot
                if event.key == pygame.K_SPACE and self.player.alive:
                    bullet = self.player.shoot()
                    if bullet:
                        self.player_bullets.append(bullet)
                        logger.debug("Player fired bullet")

        # Continuous shooting with space held
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.player.alive:
            bullet = self.player.shoot()
            if bullet:
                self.player_bullets.append(bullet)

    def update(self):
        if self.state != "playing":
            return

        # Update player
        keys = pygame.key.get_pressed()
        self.player.update(keys, self.screen_width)

        # Update player bullets
        for b in self.player_bullets:
            b.update()
            if b.y < -10 or b.y > self.screen_height + 10:
                b.alive = False
        self.player_bullets = [b for b in self.player_bullets if b.alive]

        # Update enemy bullets
        for b in self.enemy_bullets:
            b.update()
            if b.y < -10 or b.y > self.screen_height + 10:
                b.alive = False
        self.enemy_bullets = [b for b in self.enemy_bullets if b.alive]

        # Contract: dive-bomb AI - pick enemies to dive
        formation_enemies = [e for e in self.enemies if e.alive and e.state == Enemy.STATE_FORMATION]
        if formation_enemies and random.random() < 0.005:
            diver = random.choice(formation_enemies)
            # Slight random offset from player position
            target_x = self.player.x + random.randint(-60, 60)
            target_y = self.screen_height - 100
            diver.start_dive(target_x, target_y)
            logger.debug(f"Dive started by enemy ({diver.col},{diver.row})")

        # Update enemies
        for e in self.enemies:
            bullet = e.update(self.player.x, self.player.y)
            if bullet:
                self.enemy_bullets.append(bullet)

        # Problem: 製作Galaga遊戲原型 - collision detection
        self.check_collisions()

        # Check wave complete
        alive = [e for e in self.enemies if e.alive]
        if not alive:
            logger.info(f"Wave {self.wave} cleared!")
            self.spawn_wave()

    def check_collisions(self):
        player_rect = self.player.get_rect()

        # Player bullets hit enemies
        for b in self.player_bullets:
            if not b.alive:
                continue
            b_rect = b.get_rect()
            for e in self.enemies:
                if not e.alive:
                    continue
                if b_rect.colliderect(e.get_rect()):
                    b.alive = False
                    e.alive = False
                    self.score += 100
                    logger.debug(f"Enemy ({e.col},{e.row}) destroyed")
                    break

        # Enemy bullets hit player
        for b in self.enemy_bullets:
            if not b.alive or not self.player.alive:
                continue
            if b.get_rect().colliderect(player_rect):
                b.alive = False
                self.player.alive = False
                logger.info("Player hit!")
                break

        # Diving enemies hit player
        for e in self.enemies:
            if not e.alive or not self.player.alive:
                continue
            if e.state == Enemy.STATE_DIVING and e.get_rect().colliderect(player_rect):
                self.player.alive = False
                logger.info("Player destroyed by diving enemy!")
                break

        # Player respawn (simple: respawn on key press)
        if not self.player.alive:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                self.player.alive = True
                self.player.x = self.screen_width // 2
                self.player_bullets.clear()
                self.enemy_bullets.clear()
                logger.info("Player respawned")

    def draw(self):
        self.screen.fill(COLOR_BLACK)

        # Draw game objects
        self.player.draw(self.screen)
        for b in self.player_bullets:
            b.draw(self.screen)
        for b in self.enemy_bullets:
            b.draw(self.screen)
        for e in self.enemies:
            e.draw(self.screen)

        # Constraint: 用極簡風格呈現 - minimal HUD
        score_text = self.font.render(f"Score: {self.score}", True, COLOR_WHITE)
        wave_text = self.small_font.render(f"Wave: {self.wave}", True, COLOR_WHITE)
        enemies_text = self.small_font.render(
            f"Enemies: {len([e for e in self.enemies if e.alive])}", True, COLOR_WHITE
        )
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(wave_text, (10, 50))
        self.screen.blit(enemies_text, (10, 75))

        if not self.player.alive:
            # Constraint: 用極簡風格呈現 - simple game over / respawn prompt
            go_text = self.font.render("GAME OVER - Press R to Respawn", True, COLOR_RED)
            go_rect = go_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
            self.screen.blit(go_text, go_rect)

        # Constraint: 用極簡風格呈現 - FPS counter
        fps_text = self.small_font.render(f"FPS: {int(self.clock.get_fps())}", True, COLOR_YELLOW)
        self.screen.blit(fps_text, (self.screen_width - 80, 10))

        pygame.display.flip()

    def run(self):
        logger.info("Game loop started")
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.args.fps)
        logger.info("Game loop ended")
        pygame.quit()


def main():
    # Task: 使腳本接收輸入參數
    args = parse_args()
    setup_logging(args.debug)
    logger.info("Galaga prototype starting...")

    # Constraint: 使用Pygame
    pygame.init()
    logger.info(f"Pygame version: {pygame.ver}")

    game = Game(args)
    game.run()
    logger.info("Galaga prototype exited")
    return 0


if __name__ == "__main__":
    sys.exit(main())
