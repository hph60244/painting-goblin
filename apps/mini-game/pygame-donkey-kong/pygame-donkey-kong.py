"""
Donkey Kong Game Prototype
Problem: 製作Donkey Kong遊戲原型
Constraint: 使用Pygame - 適合製作2D遊戲原型，輕量化
Constraint: 用極簡風格呈現 - 強調玩法概念，節省製作時間
Constraint: 使用logger輸出訊息 - 用於人類跟AI除錯
"""

import sys
import math
import random
import logging
import argparse

import pygame

# ---------------------------------------------------------------------------
# Logger setup (Constraint: 使用logger輸出訊息)
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("donkey-kong")

# ---------------------------------------------------------------------------
# Constants (Constraint: 用極簡風格呈現)
# ---------------------------------------------------------------------------
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TITLE = "Donkey Kong - Prototype"

# Physics
GRAVITY = 0.5
JUMP_VELOCITY = -10
PLAYER_SPEED = 4
CLIMB_SPEED = 3

# Colors (極簡風格: flat colors, no textures)
COLOR_SKY = (30, 30, 40)
COLOR_PLATFORM = (140, 90, 50)
COLOR_LADDER = (200, 180, 60)
COLOR_PLAYER = (50, 130, 220)
COLOR_BARREL = (200, 50, 50)
COLOR_DK = (120, 80, 40)
COLOR_PAULINE = (220, 100, 150)
COLOR_TEXT = (255, 255, 255)
COLOR_GIRDER = (100, 100, 110)
COLOR_RIVET = (180, 180, 180)

# Player dimensions
PLAYER_W = 18
PLAYER_H = 24

# Barrel physics
BARREL_SPEED = 2
BARREL_GRAVITY = 0.3

# Scoring (Task: Platform physics, gravity, multi-screen levels)
SCORE_POINTS = 100
SCORE_BARREL_SKIP = 200
SCORE_LEVEL_CLEAR = 3000


# ---------------------------------------------------------------------------
# Level definitions (Task: multi-screen levels - 4 classic style screens)
# ---------------------------------------------------------------------------
def make_levels():
    """
    Returns list of level dicts, each containing platforms, ladders,
    and the positions of DK and Pauline.
    """
    p = COLOR_PLATFORM
    g = COLOR_GIRDER
    return [
        {
            # Level 1: Classic angled platforms with ladders
            "name": "LEVEL 1 - 25m",
            "platforms": [
                # Ground
                pygame.Rect(0, 560, SCREEN_WIDTH, 20),
                # Row 1 (bottom)
                pygame.Rect(20, 460, 180, 16),
                pygame.Rect(260, 460, 280, 16),
                pygame.Rect(600, 460, 180, 16),
                # Row 2
                pygame.Rect(60, 360, 200, 16),
                pygame.Rect(320, 360, 160, 16),
                pygame.Rect(540, 360, 200, 16),
                # Row 3
                pygame.Rect(100, 260, 160, 16),
                pygame.Rect(340, 260, 120, 16),
                pygame.Rect(540, 260, 160, 16),
                # Row 4 (top)
                pygame.Rect(160, 160, 100, 16),
                pygame.Rect(400, 160, 100, 16),
                pygame.Rect(560, 160, 100, 16),
                # Top landing
                pygame.Rect(320, 80, 200, 16),
            ],
            "platform_colors": [p, p, p, p, p, p, p, p, p, p, p, p, p, g],
            "ladders": [
                (40, 460, 480),   # (x, bottom_y, top_y) connecting rows
                (240, 460, 360),
                (480, 460, 360),
                (620, 460, 360),
                (140, 360, 260),
                (380, 360, 260),
                (580, 360, 260),
                (220, 260, 160),
                (440, 260, 160),
                (360, 160, 80),
                (500, 160, 80),
            ],
            "dk_pos": (360, 30),
            "pauline_pos": (400, 40),
            "player_start": (40, 530),
        },
        {
            # Level 2: Different layout with more gaps
            "name": "LEVEL 2 - 50m",
            "platforms": [
                pygame.Rect(0, 560, SCREEN_WIDTH, 20),
                pygame.Rect(50, 460, 150, 16),
                pygame.Rect(300, 460, 200, 16),
                pygame.Rect(600, 460, 150, 16),
                pygame.Rect(100, 360, 120, 16),
                pygame.Rect(300, 360, 200, 16),
                pygame.Rect(580, 360, 120, 16),
                pygame.Rect(30, 260, 100, 16),
                pygame.Rect(240, 260, 160, 16),
                pygame.Rect(520, 260, 160, 16),
                pygame.Rect(700, 260, 100, 16),
                pygame.Rect(200, 160, 120, 16),
                pygame.Rect(480, 160, 120, 16),
                pygame.Rect(340, 70, 160, 16),
            ],
            "platform_colors": [p, p, p, p, p, p, p, p, p, p, p, p, p, g],
            "ladders": [
                (120, 460, 360),
                (380, 460, 360),
                (640, 460, 360),
                (180, 360, 260),
                (380, 360, 260),
                (620, 360, 260),
                (100, 260, 160),
                (340, 260, 160),
                (600, 260, 160),
                (420, 160, 70),
            ],
            "dk_pos": (360, 20),
            "pauline_pos": (400, 40),
            "player_start": (60, 530),
        },
        {
            # Level 3: Elevators / conveyor-like
            "name": "LEVEL 3 - 75m",
            "platforms": [
                pygame.Rect(0, 560, SCREEN_WIDTH, 20),
                pygame.Rect(40, 440, 200, 16),
                pygame.Rect(320, 440, 160, 16),
                pygame.Rect(560, 440, 200, 16),
                pygame.Rect(40, 320, 140, 16),
                pygame.Rect(280, 320, 240, 16),
                pygame.Rect(620, 320, 140, 16),
                pygame.Rect(120, 200, 120, 16),
                pygame.Rect(360, 200, 120, 16),
                pygame.Rect(560, 200, 120, 16),
                pygame.Rect(240, 90, 320, 16),
            ],
            "platform_colors": [p, p, p, p, p, p, p, p, p, p, g],
            "ladders": [
                (160, 440, 320),
                (380, 440, 320),
                (640, 440, 320),
                (120, 320, 200),
                (380, 320, 200),
                (660, 320, 200),
                (400, 200, 90),
            ],
            "dk_pos": (360, 30),
            "pauline_pos": (400, 50),
            "player_start": (50, 530),
        },
        {
            # Level 4: Final - rivet level
            "name": "LEVEL 4 - 100m",
            "platforms": [
                pygame.Rect(0, 560, SCREEN_WIDTH, 20),
                pygame.Rect(20, 450, 180, 16),
                pygame.Rect(250, 450, 100, 16),
                pygame.Rect(400, 450, 180, 16),
                pygame.Rect(630, 450, 150, 16),
                pygame.Rect(90, 340, 140, 16),
                pygame.Rect(290, 340, 220, 16),
                pygame.Rect(570, 340, 140, 16),
                pygame.Rect(40, 230, 120, 16),
                pygame.Rect(220, 230, 160, 16),
                pygame.Rect(460, 230, 160, 16),
                pygame.Rect(680, 230, 100, 16),
                pygame.Rect(150, 120, 140, 16),
                pygame.Rect(420, 120, 140, 16),
                pygame.Rect(300, 40, 200, 16),
            ],
            "platform_colors": [p, p, p, p, p, p, p, p, p, p, p, p, p, p, g],
            "ladders": [
                (110, 450, 340),
                (290, 450, 340),
                (480, 450, 340),
                (700, 450, 340),
                (160, 340, 230),
                (390, 340, 230),
                (610, 340, 230),
                (100, 230, 120),
                (300, 230, 120),
                (540, 230, 120),
                (500, 120, 40),
            ],
            "dk_pos": (360, 10),
            "pauline_pos": (320, 10),
            "player_start": (40, 530),
        },
    ]


# ---------------------------------------------------------------------------
# Game classes (Task: Platform physics, gravity)
# ---------------------------------------------------------------------------
class Player:
    """Player character with platform physics and gravity."""

    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PLAYER_W, PLAYER_H)
        self.vx = 0
        self.vy = 0
        self.on_ground = False
        self.on_ladder = False
        self.climbing = False
        self.facing_right = True
        self.alive = True
        logger.debug(f"Player created at ({x}, {y})")

    def update(self, platforms, ladders, barrels):
        if not self.alive:
            return

        keys = pygame.key.get_pressed()
        self.vx = 0
        self.climbing = False

        # Horizontal movement (Constraint: 用極簡風格呈現)
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vx = -PLAYER_SPEED
            self.facing_right = False
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vx = PLAYER_SPEED
            self.facing_right = True

        # Ladder detection & climbing (Task: multi-screen levels)
        self.on_ladder = False
        for ladder in ladders:
            lx, by, ty = ladder
            if (self.rect.centerx > lx - 10 and self.rect.centerx < lx + 10 and
                    ty < self.rect.centery < by):
                self.on_ladder = True
                break

        if self.on_ladder and (keys[pygame.K_UP] or keys[pygame.K_w] or
                               keys[pygame.K_DOWN] or keys[pygame.K_s]):
            self.climbing = True
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.vy = -CLIMB_SPEED
            elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.vy = CLIMB_SPEED
            else:
                self.vy = 0
            self.vx = 0
        elif self.on_ladder and (keys[pygame.K_UP] or keys[pygame.K_w]):
            # Grab ladder even without vertical key held
            self.climbing = True
            self.vy = -CLIMB_SPEED
            self.vx = 0
        else:
            # Gravity (Constraint: Platform physics)
            self.vy += GRAVITY
            if self.vy > 15:
                self.vy = 15

        # Jump
        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]):
            if self.on_ground:
                self.vy = JUMP_VELOCITY
                self.on_ground = False
                logger.debug("Player jumped")

        # Apply horizontal movement
        self.rect.x += self.vx
        # Collision with platforms (horizontal)
        for p_idx, platform in enumerate(platforms):
            if self.rect.colliderect(platform):
                if self.vx > 0:
                    self.rect.right = platform.left
                elif self.vx < 0:
                    self.rect.left = platform.right

        # Apply vertical movement
        self.rect.y += self.vy
        self.on_ground = False

        # Collision with platforms (vertical)
        for p_idx, platform in enumerate(platforms):
            if self.rect.colliderect(platform):
                if self.vy > 0:
                    self.rect.bottom = platform.top
                    self.vy = 0
                    self.on_ground = True
                elif self.vy < 0:
                    self.rect.top = platform.bottom
                    self.vy = 0
                self.climbing = False

        # Climbing - snap to ladder x
        if self.climbing:
            for ladder in ladders:
                lx, by, ty = ladder
                if (self.rect.centerx > lx - 15 and self.rect.centerx < lx + 15 and
                        ty <= self.rect.centery <= by):
                    self.rect.centerx = lx
                    self.vy = 0
                    break

        # Keep within screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

        # Fall off screen
        if self.rect.top > SCREEN_HEIGHT:
            self.alive = False
            logger.info("Player fell off screen")

        # Barrel collision
        for barrel in barrels:
            if self.rect.colliderect(barrel.rect):
                self.alive = False
                logger.info("Player hit by barrel")

    def draw(self, surface):
        # Player body (Constraint: 用極簡風格呈現)
        pygame.draw.rect(surface, COLOR_PLAYER, self.rect)
        # Simple face direction indicator
        eye_x = self.rect.right - 6 if self.facing_right else self.rect.left + 2
        pygame.draw.circle(surface, (255, 255, 255), (eye_x, self.rect.top + 6), 3)
        pygame.draw.circle(surface, (0, 0, 0), (eye_x, self.rect.top + 6), 1)

    def reset(self, x, y):
        self.rect.topleft = (x, y)
        self.vx = 0
        self.vy = 0
        self.on_ground = False
        self.alive = True
        logger.debug(f"Player reset to ({x}, {y})")


class Barrel:
    """Barrel that rolls down platforms."""

    def __init__(self, x, y, direction=1):
        self.rect = pygame.Rect(x - 8, y - 8, 16, 16)
        self.vx = BARREL_SPEED * direction
        self.vy = 0
        self.direction = direction
        self.bounce_count = 0
        self.alive = True
        logger.debug(f"Barrel created at ({x}, {y})")

    def update(self, platforms):
        if not self.alive:
            return

        # Gravity
        self.vy += BARREL_GRAVITY
        if self.vy > 10:
            self.vy = 10

        # Horizontal movement
        self.rect.x += self.vx

        # Horizontal collision
        for platform in platforms:
            if self.rect.colliderect(platform):
                if self.vx > 0:
                    self.rect.right = platform.left
                    self.direction = -1
                elif self.vx < 0:
                    self.rect.left = platform.right
                    self.direction = 1
                self.vx = BARREL_SPEED * self.direction
                self.bounce_count += 1

        # Vertical movement
        self.rect.y += self.vy

        on_platform = False
        for platform in platforms:
            if self.rect.colliderect(platform):
                if self.vy > 0:
                    self.rect.bottom = platform.top
                    self.vy = 0
                    on_platform = True
                elif self.vy < 0:
                    self.rect.top = platform.bottom
                    self.vy = 0

        # Roll along platform surface
        if on_platform:
            self.rect.x += self.vx

        # Off screen
        if self.rect.top > SCREEN_HEIGHT + 20 or self.rect.right < -20 or self.rect.left > SCREEN_WIDTH + 20:
            self.alive = False

    def draw(self, surface):
        pygame.draw.circle(surface, COLOR_BARREL, self.rect.center, 8)
        pygame.draw.circle(surface, (150, 30, 30), self.rect.center, 5)
        # Spinning effect
        angle = (self.bounce_count * 45) % 360
        end_x = self.rect.centerx + int(6 * math.cos(math.radians(angle)))
        end_y = self.rect.centery + int(6 * math.sin(math.radians(angle)))
        pygame.draw.line(surface, (255, 200, 200), self.rect.center, (end_x, end_y), 2)


class Game:
    """Main game controller (Task: Platform physics, gravity, multi-screen levels)."""

    def __init__(self, screen):
        # Constraint: 使用logger輸出訊息
        logger.info("Initializing Donkey Kong game")
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("monospace", 20, bold=True)
        self.big_font = pygame.font.SysFont("monospace", 32, bold=True)

        self.levels = make_levels()
        self.current_level = 0
        self.score = 0
        self.lives = 3
        self.state = "title"  # title, playing, game_over, victory, level_clear

        # Game objects
        self.barrels = []
        self.platforms = []
        self.platform_colors = []
        self.ladders = []
        self.dk_pos = (0, 0)
        self.pauline_pos = (0, 0)
        self.player_start = (0, 0)

        self.barrel_timer = 0
        self.barrel_interval = 90  # frames between barrel spawns
        self.level_clear_timer = 0
        self.invincible_timer = 0

        self.load_level(self.current_level)
        logger.info("Game initialized successfully")

    def load_level(self, level_idx):
        level = self.levels[level_idx]
        logger.info(f"Loading {level['name']}")

        self.platforms = level["platforms"]
        self.platform_colors = level.get("platform_colors", [COLOR_PLATFORM] * len(level["platforms"]))
        self.ladders = level["ladders"]
        self.dk_pos = level["dk_pos"]
        self.pauline_pos = level["pauline_pos"]
        self.player_start = level["player_start"]

        self.player = Player(*self.player_start)
        self.barrels = []
        self.barrel_timer = 0
        self.barrel_interval = max(30, 90 - level_idx * 15)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if self.state == "title" and event.key == pygame.K_RETURN:
                    self.state = "playing"
                    logger.info("Game started")
                elif self.state == "game_over" and event.key == pygame.K_RETURN:
                    self.__init__(self.screen)
                    return True
                elif self.state == "victory" and event.key == pygame.K_RETURN:
                    self.__init__(self.screen)
                    return True
                elif self.state == "level_clear" and event.key == pygame.K_RETURN:
                    self.current_level += 1
                    if self.current_level >= len(self.levels):
                        self.state = "victory"
                        logger.info("All levels cleared! Victory!")
                    else:
                        self.load_level(self.current_level)
                        self.state = "playing"
                if event.key == pygame.K_ESCAPE:
                    return False
        return True

    def update(self):
        if self.state != "playing":
            return

        if self.invincible_timer > 0:
            self.invincible_timer -= 1

        # Spawn barrels
        self.barrel_timer += 1
        if self.barrel_timer >= self.barrel_interval:
            self.barrel_timer = 0
            direction = random.choice([-1, 1])
            new_barrel = Barrel(self.dk_pos[0], self.dk_pos[1] + 20, direction)
            self.barrels.append(new_barrel)
            logger.debug(f"Barrel spawned, total barrels: {len(self.barrels)}")

        # Update barrels
        for barrel in self.barrels[:]:
            barrel.update(self.platforms)
            if not barrel.alive:
                self.barrels.remove(barrel)
                self.score += SCORE_BARREL_SKIP

        # Update player
        self.player.update(self.platforms, self.ladders, self.barrels)

        # Check player death
        if not self.player.alive and self.invincible_timer <= 0:
            self.lives -= 1
            logger.info(f"Player died. Lives remaining: {self.lives}")
            if self.lives <= 0:
                self.state = "game_over"
                logger.info("Game Over")
            else:
                self.player.reset(*self.player_start)
                self.invincible_timer = 60  # 1 second invincibility

        # Check level clear: player reaches DK/Pauline area
        if self.player.rect.top < 100 and self.player.rect.centerx > 300 and self.player.rect.centerx < 420:
            self.score += SCORE_LEVEL_CLEAR
            self.state = "level_clear"
            self.level_clear_timer = 120
            logger.info(f"Level {self.current_level + 1} cleared!")

    def draw(self):
        self.screen.fill(COLOR_SKY)

        if self.state == "title":
            self._draw_title()
            return

        # Draw platforms
        for i, platform in enumerate(self.platforms):
            color = self.platform_colors[i] if i < len(self.platform_colors) else COLOR_PLATFORM
            pygame.draw.rect(self.screen, color, platform)
            # Girder lines for last platform (top)
            if color == COLOR_GIRDER:
                for rx in range(platform.left, platform.right, 40):
                    pygame.draw.circle(self.screen, COLOR_RIVET, (rx + 4, platform.top + 8), 4)

        # Draw ladders
        for lx, by, ty in self.ladders:
            for y in range(ty, by, 16):
                pygame.draw.rect(self.screen, COLOR_LADDER, (lx - 3, y, 6, 8))
                pygame.draw.line(self.screen, (100, 80, 20), (lx - 5, y + 4), (lx + 5, y + 4), 1)

        # Draw DK
        dk_rect = pygame.Rect(self.dk_pos[0] - 25, self.dk_pos[1], 50, 40)
        pygame.draw.rect(self.screen, COLOR_DK, dk_rect)
        pygame.draw.circle(self.screen, COLOR_DK, (self.dk_pos[0], self.dk_pos[1] - 10), 16)
        # DK eyes
        pygame.draw.circle(self.screen, (255, 255, 255), (self.dk_pos[0] - 6, self.dk_pos[1] - 12), 5)
        pygame.draw.circle(self.screen, (255, 255, 255), (self.dk_pos[0] + 6, self.dk_pos[1] - 12), 5)
        pygame.draw.circle(self.screen, (0, 0, 0), (self.dk_pos[0] - 6, self.dk_pos[1] - 12), 2)
        pygame.draw.circle(self.screen, (0, 0, 0), (self.dk_pos[0] + 6, self.dk_pos[1] - 12), 2)
        # Label
        label = self.font.render("DK", True, (255, 255, 200))
        self.screen.blit(label, (self.dk_pos[0] - 15, self.dk_pos[1] + 35))

        # Draw Pauline
        pauline_rect = pygame.Rect(self.pauline_pos[0] - 10, self.pauline_pos[1], 20, 30)
        pygame.draw.rect(self.screen, COLOR_PAULINE, pauline_rect)
        pygame.draw.circle(self.screen, COLOR_PAULINE, (self.pauline_pos[0], self.pauline_pos[1] - 4), 10)
        label = self.font.render("PAULINE", True, (255, 200, 200))
        self.screen.blit(label, (self.pauline_pos[0] - 30, self.pauline_pos[1] - 40))

        # Draw barrels
        for barrel in self.barrels:
            barrel.draw(self.screen)

        # Draw player (blink if invincible)
        if self.player.alive:
            if self.invincible_timer <= 0 or self.invincible_timer % 6 < 3:
                self.player.draw(self.screen)

        # Draw UI
        self._draw_ui()

        # Draw level clear overlay
        if self.state == "level_clear":
            self._draw_overlay(f"{self.levels[self.current_level]['name']} CLEAR!", "Press ENTER to continue")

        # Draw game over
        if self.state == "game_over":
            self._draw_overlay("GAME OVER", f"Score: {self.score} - Press ENTER to restart")

        # Draw victory
        if self.state == "victory":
            self._draw_overlay("YOU WIN!", f"Final Score: {self.score} - Press ENTER to restart")

    def _draw_title(self):
        title = self.big_font.render("DONKEY KONG", True, (255, 220, 50))
        subtitle = self.font.render("Pygame Prototype", True, COLOR_TEXT)
        start = self.font.render("Press ENTER to Start", True, COLOR_TEXT)
        controls = self.font.render("Arrows/WASD: Move & Climb  SPACE: Jump", True, COLOR_TEXT)
        info = self.font.render("Use the ladders to reach Donkey Kong!", True, (200, 200, 200))

        self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 150))
        self.screen.blit(subtitle, (SCREEN_WIDTH // 2 - subtitle.get_width() // 2, 200))
        self.screen.blit(start, (SCREEN_WIDTH // 2 - start.get_width() // 2, 300))
        self.screen.blit(controls, (SCREEN_WIDTH // 2 - controls.get_width() // 2, 360))
        self.screen.blit(info, (SCREEN_WIDTH // 2 - info.get_width() // 2, 400))

    def _draw_ui(self):
        level_name = self.levels[self.current_level]["name"]
        score_text = self.font.render(f"SCORE: {self.score}", True, COLOR_TEXT)
        lives_text = self.font.render(f"LIVES: {self.lives}", True, COLOR_TEXT)
        level_text = self.font.render(level_name, True, COLOR_TEXT)

        self.screen.blit(score_text, (10, 10))
        self.screen.blit(lives_text, (SCREEN_WIDTH - 120, 10))
        self.screen.blit(level_text, (SCREEN_WIDTH // 2 - level_text.get_width() // 2, 10))

    def _draw_overlay(self, main_text, sub_text):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        main = self.big_font.render(main_text, True, (255, 220, 50))
        sub = self.font.render(sub_text, True, COLOR_TEXT)
        self.screen.blit(main, (SCREEN_WIDTH // 2 - main.get_width() // 2, SCREEN_HEIGHT // 2 - 40))
        self.screen.blit(sub, (SCREEN_WIDTH // 2 - sub.get_width() // 2, SCREEN_HEIGHT // 2 + 10))

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()
        logger.info("Game closed")


# ---------------------------------------------------------------------------
# Entry point (Task: 使腳本接收輸入參數)
# ---------------------------------------------------------------------------
def parse_args():
    parser = argparse.ArgumentParser(
        description="Donkey Kong Game Prototype - Pygame Edition"
    )
    parser.add_argument(
        "--fps", type=int, default=FPS,
        help=f"Target FPS (default: {FPS})"
    )
    parser.add_argument(
        "--fullscreen", action="store_true",
        help="Launch in fullscreen mode"
    )
    parser.add_argument(
        "--level", type=int, default=1, choices=range(1, 5),
        help="Start at a specific level 1-4 (default: 1)"
    )
    parser.add_argument(
        "--lives", type=int, default=3,
        help="Number of lives (default: 3)"
    )
    parser.add_argument(
        "--debug", action="store_true",
        help="Enable debug logging"
    )
    return parser.parse_args()


def main():
    args = parse_args()

    if args.debug:
        logger.setLevel(logging.DEBUG)
        logger.debug("Debug logging enabled")

    # Constraint: 使用Pygame
    logger.info(f"Starting Donkey Kong prototype (FPS: {args.fps})")
    pygame.init()

    flags = pygame.FULLSCREEN if args.fullscreen else 0
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), flags)
    pygame.display.set_caption(TITLE)

    game = Game(screen)
    game.current_level = args.level - 1
    game.lives = args.lives
    game.load_level(game.current_level)

    game.run()


if __name__ == "__main__":
    main()
