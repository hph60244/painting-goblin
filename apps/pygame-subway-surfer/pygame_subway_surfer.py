import argparse
import logging
import sys
import random
import math

import pygame


WINDOW_TITLE = "Subway Surfer"
FPS = 60
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 500

LANE_COUNT = 3
LANE_HEIGHT = 80
LANE_GAP = 10
LANE_Y_START = 120

PLAYER_WIDTH = 35
PLAYER_HEIGHT = 45
PLAYER_X = 100

OBSTACLE_MIN_WIDTH = 30
OBSTACLE_MAX_WIDTH = 50
OBSTACLE_HEIGHT = 45
OBSTACLE_SPEED = 6
OBSTACLE_SPAWN_MIN = 0.8
OBSTACLE_SPAWN_MAX = 2.0

COIN_RADIUS = 8
COIN_SPEED = 6
COIN_SPAWN_INTERVAL = 0.8

POWERUP_SPAWN_INTERVAL = 5.0

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 50, 50)
DARK_RED = (180, 30, 30)
BLUE = (50, 100, 220)
DARK_BLUE = (30, 70, 180)
YELLOW = (255, 215, 0)
DARK_YELLOW = (200, 170, 0)
GRAY = (120, 120, 120)
DARK_GRAY = (60, 60, 60)
SKY_BLUE = (100, 180, 240)
GREEN = (50, 200, 50)
DARK_GREEN = (30, 150, 30)
ORANGE = (255, 165, 0)
PURPLE = (180, 50, 200)
BROWN = (139, 69, 19)
LIGHT_GRAY = (180, 180, 180)


class Building:
    def __init__(self, x, height, width, color):
        self.x = x
        self.height = height
        self.width = width
        self.color = color
        self.window_color = (random.randint(200, 255), random.randint(200, 255), random.randint(100, 200))

    def draw(self, surface, offset_x, screen_width, ground_y):
        draw_x = (self.x - offset_x) % (screen_width + 200) - 100
        rect = pygame.Rect(draw_x, ground_y - self.height, self.width, self.height)
        pygame.draw.rect(surface, self.color, rect)
        win_w = max(4, self.width // 5)
        win_h = max(4, self.height // 6)
        for wy in range(ground_y - self.height + 8, ground_y - 4, win_h + 4):
            for wx in range(int(draw_x) + 4, int(draw_x + self.width) - 4, win_w + 4):
                wr = pygame.Rect(wx, wy, win_w, win_h)
                brightness = random.randint(180, 255) if random.random() > 0.3 else 50
                win_color = (brightness, brightness, brightness // 2)
                pygame.draw.rect(surface, win_color, wr)


class ParallaxBackground:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.ground_y = height - 80

        buildings = []
        x = -50
        while x < width + 300:
            bw = random.randint(40, 90)
            bh = random.randint(100, 200)
            brightness = random.randint(80, 140)
            color = (brightness, brightness, brightness + 20)
            buildings.append(Building(x, bh, bw, color))
            x += bw + random.randint(5, 20)
        self.buildings = buildings
        self.city_scroll = 0.0
        self.city_speed = 0.5

        self.track_scroll = 0.0
        self.track_speed = 2.0

        self.foreground_scroll = 0.0
        self.foreground_speed = 4.0

    def update(self, speed_multiplier=1.0):
        self.city_scroll += self.city_speed * speed_multiplier
        self.track_scroll += self.track_speed * speed_multiplier
        self.foreground_scroll += self.foreground_speed * speed_multiplier

    def draw(self, surface):
        surface.fill(SKY_BLUE)

        for b in self.buildings:
            b.draw(surface, self.city_scroll, self.width, self.ground_y)

        base_y = self.ground_y
        for i in range(3):
            track_offset = (self.track_scroll + i * 50) % 100
            for x in range(-50, self.width + 50, 10):
                if (x + track_offset) % 20 < 10:
                    pygame.draw.line(
                        surface, DARK_GRAY,
                        (x, base_y + i * 30 + 15),
                        (x + 8, base_y + i * 30 + 15), 2
                    )

        rail_offset = (self.foreground_scroll * 1.5) % 40
        rail_y = self.ground_y + 85
        for x in range(-40, self.width + 40, 40):
            rx = x + rail_offset
            pygame.draw.rect(surface, GRAY, (rx, rail_y, 20, 8))
            pygame.draw.rect(surface, DARK_GRAY, (rx, rail_y, 20, 8), 1)

        ground_rect = pygame.Rect(0, self.ground_y, self.width, self.height - self.ground_y)
        pygame.draw.rect(surface, GRAY, ground_rect)
        pygame.draw.rect(surface, DARK_GRAY, ground_rect, 2)
        for gy in range(self.ground_y, self.height, 4):
            pygame.draw.line(surface, DARK_GRAY, (0, gy), (self.width, gy), 1)

    def get_ground_y(self):
        return self.ground_y


class Player:
    def __init__(self, lane_count, lane_y_start, lane_height, lane_gap):
        self.lane_count = lane_count
        self.lane_y_start = lane_y_start
        self.lane_height = lane_height
        self.lane_gap = lane_gap
        self.current_lane = 1
        self.target_y = self._lane_y(1)
        self.y = self.target_y
        self.x = PLAYER_X
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.switch_cooldown = 0.0
        self.animation_offset = 0.0
        self.invincible = False
        self.invincible_timer = 0.0

    def _lane_y(self, lane):
        return self.lane_y_start + lane * (self.lane_height + self.lane_gap)

    def switch_lane(self, direction):
        new_lane = self.current_lane + direction
        if 0 <= new_lane < self.lane_count:
            self.current_lane = new_lane
            self.target_y = self._lane_y(new_lane)
            self.switch_cooldown = 0.15

    def update(self, dt):
        if self.switch_cooldown > 0:
            self.switch_cooldown -= dt
        diff = self.target_y - self.y
        if abs(diff) > 1:
            self.y += diff * 10 * dt
        else:
            self.y = self.target_y
        self.animation_offset += dt * 5

    def set_invincible(self, duration):
        self.invincible = True
        self.invincible_timer = duration

    def update_invincible(self, dt):
        if self.invincible:
            self.invincible_timer -= dt
            if self.invincible_timer <= 0:
                self.invincible = False

    def get_rect(self):
        return pygame.Rect(self.x, self.y - self.height // 2, self.width, self.height)

    def draw(self, surface):
        bob = math.sin(self.animation_offset) * 2
        draw_y = self.y + bob
        rect = pygame.Rect(self.x, draw_y - self.height // 2, self.width, self.height)

        if self.invincible:
            blink = int(self.invincible_timer * 10) % 2 == 0
            if blink:
                color = YELLOW
            else:
                color = BLUE
        else:
            color = BLUE

        pygame.draw.rect(surface, color, rect)
        pygame.draw.rect(surface, DARK_BLUE, rect, 2)

        head_rect = pygame.Rect(self.x + 8, draw_y - self.height // 2 - 8, 19, 12)
        pygame.draw.ellipse(surface, (255, 220, 180), head_rect)
        pygame.draw.ellipse(surface, BLACK, head_rect, 1)

        eye_x = self.x + 22
        eye_y = draw_y - self.height // 2 - 4
        pygame.draw.circle(surface, BLACK, (eye_x, eye_y), 2)

        arm_y = draw_y
        pygame.draw.line(surface, (255, 220, 180), (self.x, arm_y), (self.x - 10, arm_y + 5), 3)
        pygame.draw.line(surface, (255, 220, 180), (self.x + self.width, arm_y), (self.x + self.width + 10, arm_y - 3), 3)

        leg_offset = math.sin(self.animation_offset * 2) * 4
        pygame.draw.line(surface, DARK_BLUE,
                         (self.x + 8, draw_y + self.height // 2),
                         (self.x + 4 + leg_offset, draw_y + self.height // 2 + 12), 4)
        pygame.draw.line(surface, DARK_BLUE,
                         (self.x + self.width - 8, draw_y + self.height // 2),
                         (self.x + self.width - 4 - leg_offset, draw_y + self.height // 2 + 12), 4)


class Game:
    def __init__(self, args):
        self.logger = logging.getLogger("SubwaySurfer")
        self.logger.setLevel(getattr(logging, args.log_level.upper(), logging.INFO))
        self.window_width = args.width
        self.window_height = args.height
        self.obstacle_speed = args.obstacle_speed
        self.lane_count = args.lanes
        self.score = 0
        self.coin_count = 0
        self.max_score = 0
        self.game_over = False
        self.paused = False
        self.obstacles = []
        self.coins = []
        self.powerups = []
        self.obstacle_timer = 0.0
        self.coin_timer = 0.0
        self.powerup_timer = 0.0
        self.distance = 0.0
        self.speed_multiplier = 1.0

        lane_height = (self.window_height - LANE_Y_START - 100) // self.lane_count - LANE_GAP
        self.lane_height_actual = max(40, min(lane_height, 100))

        pygame.init()
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 32)
        self.small_font = pygame.font.Font(None, 24)
        self.large_font = pygame.font.Font(None, 48)
        self.running = True

        self.background = ParallaxBackground(self.window_width, self.window_height)
        self.player = Player(self.lane_count, LANE_Y_START, self.lane_height_actual, LANE_GAP)

        self.logger.info(
            "Game initialized: %dx%d, lanes=%d, obstacle_speed=%d",
            self.window_width, self.window_height,
            self.lane_count, self.obstacle_speed,
        )

    def reset_game(self):
        self.logger.info("Game reset")
        self.player = Player(self.lane_count, LANE_Y_START, self.lane_height_actual, LANE_GAP)
        self.obstacles.clear()
        self.coins.clear()
        self.powerups.clear()
        self.obstacle_timer = 0.0
        self.coin_timer = 0.0
        self.powerup_timer = 0.0
        self.distance = 0.0
        self.score = 0
        self.coin_count = 0
        self.game_over = False
        self.speed_multiplier = 1.0

    def spawn_obstacle(self):
        lane = random.randint(0, self.lane_count - 1)
        for obs in self.obstacles:
            if obs.lane == lane and obs.x > self.window_width - 150:
                return
        obstacle = Obstacle(
            self.window_width + 20, lane,
            LANE_Y_START, self.lane_height_actual, LANE_GAP
        )
        self.obstacles.append(obstacle)
        self.logger.debug("Obstacle spawned in lane %d at x=%.0f", lane, obstacle.x)

    def spawn_coins(self):
        lane = random.randint(0, self.lane_count - 1)
        pattern = random.choice(["single", "triple"])
        if pattern == "single":
            coin = Coin(
                self.window_width + 20, lane,
                LANE_Y_START, self.lane_height_actual, LANE_GAP
            )
            self.coins.append(coin)
        else:
            for i in range(3):
                coin = Coin(
                    self.window_width + 20 + i * 30, lane,
                    LANE_Y_START, self.lane_height_actual, LANE_GAP
                )
                self.coins.append(coin)

    def spawn_powerup(self):
        lane = random.randint(0, self.lane_count - 1)
        powerup = PowerUp(
            self.window_width + 20, lane,
            LANE_Y_START, self.lane_height_actual, LANE_GAP
        )
        self.powerups.append(powerup)
        self.logger.debug("PowerUp spawned in lane %d", lane)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_r and self.game_over:
                    self.reset_game()
                elif event.key == pygame.K_p and not self.game_over:
                    self.paused = not self.paused
                elif not self.game_over and not self.paused:
                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        self.player.switch_lane(-1)
                        self.logger.debug("Player switched up to lane %d", self.player.current_lane)
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        self.player.switch_lane(1)
                        self.logger.debug("Player switched down to lane %d", self.player.current_lane)

    def update(self, dt):
        if self.game_over or self.paused:
            return

        self.speed_multiplier = 1.0 + self.distance / 5000.0
        self.player.update(dt)
        self.player.update_invincible(dt)
        self.background.update(self.speed_multiplier)

        self.distance += self.obstacle_speed * self.speed_multiplier * dt * 10

        current_speed = self.obstacle_speed * self.speed_multiplier

        self.obstacle_timer += dt
        spawn_interval = random.uniform(OBSTACLE_SPAWN_MIN, OBSTACLE_SPAWN_MAX) / self.speed_multiplier
        if self.obstacle_timer >= spawn_interval:
            self.obstacle_timer -= spawn_interval
            self.spawn_obstacle()

        self.coin_timer += dt
        if self.coin_timer >= COIN_SPAWN_INTERVAL:
            self.coin_timer -= COIN_SPAWN_INTERVAL
            self.spawn_coins()

        self.powerup_timer += dt
        if self.powerup_timer >= POWERUP_SPAWN_INTERVAL:
            self.powerup_timer -= POWERUP_SPAWN_INTERVAL
            self.spawn_powerup()

        player_rect = self.player.get_rect()

        for obs in list(self.obstacles):
            obs.move(current_speed)
            if obs.collides_with(player_rect) and not self.player.invincible:
                self.logger.debug("Player collided with obstacle in lane %d", obs.lane)
                self.game_over = True
                if self.score > self.max_score:
                    self.max_score = self.score
                return
            if obs.is_off_screen():
                self.obstacles.remove(obs)
                self.score += 10
                self.logger.debug("Score increased to %d (obstacle dodged)", self.score)

        for coin in list(self.coins):
            coin.move(current_speed)
            if coin.collects(player_rect):
                coin.collected = True
                self.coin_count += 1
                self.score += 50
                self.logger.debug("Coin collected! Total: %d", self.coin_count)
            if coin.is_off_screen() or coin.collected:
                self.coins.remove(coin)

        for powerup in list(self.powerups):
            powerup.move(current_speed)
            if powerup.collects(player_rect):
                powerup.collected = True
                self.player.set_invincible(5.0)
                self.score += 100
                self.logger.debug("PowerUp collected! Invincible for 5s")
            if powerup.is_off_screen() or powerup.collected:
                self.powerups.remove(powerup)

    def draw(self):
        self.background.draw(self.screen)

        lane_w = self.window_width
        for i in range(self.lane_count):
            y = LANE_Y_START + i * (self.lane_height_actual + LANE_GAP)
            lane_rect = pygame.Rect(0, y - self.lane_height_actual // 2, lane_w, self.lane_height_actual)
            pygame.draw.rect(self.screen, (60, 60, 70, 128), lane_rect, 0)
            pygame.draw.rect(self.screen, DARK_GRAY, lane_rect, 1)
            label = self.small_font.render(f"Lane {i + 1}", True, LIGHT_GRAY)
            self.screen.blit(label, (5, y - self.lane_height_actual // 2 + 2))

        for obs in self.obstacles:
            obs.draw(self.screen)

        for coin in self.coins:
            coin.draw(self.screen)

        for powerup in self.powerups:
            powerup.draw(self.screen)

        self.player.draw(self.screen)

        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (self.window_width - 180, 10))

        coin_text = self.font.render(f"Coins: {self.coin_count}", True, YELLOW)
        self.screen.blit(coin_text, (self.window_width - 180, 40))

        dist_text = self.small_font.render(f"Dist: {int(self.distance)}m", True, WHITE)
        self.screen.blit(dist_text, (self.window_width - 180, 70))

        high_text = self.small_font.render(f"Best: {self.max_score}", True, WHITE)
        self.screen.blit(high_text, (self.window_width - 180, 95))

        if self.paused:
            overlay = pygame.Surface((self.window_width, self.window_height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))
            self.screen.blit(overlay, (0, 0))
            pause_text = self.large_font.render("PAUSED", True, WHITE)
            pause_rect = pause_text.get_rect(center=(self.window_width // 2, self.window_height // 2 - 20))
            self.screen.blit(pause_text, pause_rect)
            unpause_hint = self.small_font.render("Press P to resume", True, WHITE)
            unhint_rect = unpause_hint.get_rect(center=(self.window_width // 2, self.window_height // 2 + 20))
            self.screen.blit(unpause_hint, unhint_rect)

        if self.game_over:
            overlay = pygame.Surface((self.window_width, self.window_height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))
            self.screen.blit(overlay, (0, 0))
            go_text = self.large_font.render("GAME OVER", True, RED)
            go_rect = go_text.get_rect(center=(self.window_width // 2, self.window_height // 2 - 50))
            self.screen.blit(go_text, go_rect)
            final_score = self.font.render(f"Score: {self.score}", True, WHITE)
            fs_rect = final_score.get_rect(center=(self.window_width // 2, self.window_height // 2))
            self.screen.blit(final_score, fs_rect)
            restart_hint = self.small_font.render("Press R to restart, ESC to quit", True, WHITE)
            rh_rect = restart_hint.get_rect(center=(self.window_width // 2, self.window_height // 2 + 40))
            self.screen.blit(restart_hint, rh_rect)

        controls_hint = self.small_font.render("Up/Down: Switch lane | P: Pause | ESC: Quit", True, WHITE)
        ch_rect = controls_hint.get_rect(center=(self.window_width // 2, self.window_height - 10))
        self.screen.blit(controls_hint, ch_rect)

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


class Obstacle:
    def __init__(self, x, lane, lane_y, lane_height, lane_gap):
        self.x = x
        self.lane = lane
        self.width = random.randint(OBSTACLE_MIN_WIDTH, OBSTACLE_MAX_WIDTH)
        self.height = OBSTACLE_HEIGHT
        self.lane_y = lane_y + lane * (lane_height + lane_gap)
        self.scored = False
        self.obstacle_type = random.choice(["train", "barrier"])

    def move(self, speed):
        self.x -= speed

    def is_off_screen(self):
        return self.x + self.width < -50

    def collides_with(self, player_rect):
        rect = self.get_rect()
        return player_rect.colliderect(rect)

    def get_rect(self):
        return pygame.Rect(self.x, self.lane_y - self.height // 2, self.width, self.height)

    def draw(self, surface):
        rect = self.get_rect()
        if self.obstacle_type == "train":
            pygame.draw.rect(surface, RED, rect)
            pygame.draw.rect(surface, DARK_RED, rect, 2)
            for wx in range(int(self.x) + 5, int(self.x + self.width) - 5, 12):
                pygame.draw.rect(surface, DARK_YELLOW, (wx, self.lane_y - self.height // 2 + 5, 8, 8))
                pygame.draw.rect(surface, DARK_YELLOW, (wx, self.lane_y + self.height // 2 - 13, 8, 8))
        else:
            pygame.draw.rect(surface, ORANGE, rect)
            pygame.draw.rect(surface, BROWN, rect, 2)
            for i in range(self.width // 8):
                hx = self.x + i * 8 + 4
                pygame.draw.line(surface, BROWN, (hx, self.lane_y - self.height // 2),
                                 (hx, self.lane_y + self.height // 2), 2)


class Coin:
    def __init__(self, x, lane, lane_y, lane_height, lane_gap):
        self.x = x
        self.lane = lane
        self.y = lane_y + lane * (lane_height + lane_gap)
        self.radius = COIN_RADIUS
        self.collected = False
        self.angle = random.random() * math.pi * 2

    def move(self, speed):
        self.x -= speed
        self.angle += 0.05

    def is_off_screen(self):
        return self.x + self.radius < -20

    def collects(self, player_rect):
        return player_rect.colliderect(self.get_rect())

    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius,
                           self.radius * 2, self.radius * 2)

    def draw(self, surface):
        scale = abs(math.cos(self.angle))
        if scale < 0.1:
            return
        draw_radius = max(2, int(self.radius * scale))
        pygame.draw.circle(surface, YELLOW, (int(self.x), int(self.y)), draw_radius)
        pygame.draw.circle(surface, DARK_YELLOW, (int(self.x), int(self.y)), draw_radius, 1)
        if scale > 0.5:
            inner_r = max(1, int(draw_radius * 0.4))
            pygame.draw.circle(surface, DARK_YELLOW, (int(self.x), int(self.y)), inner_r)


class PowerUp:
    def __init__(self, x, lane, lane_y, lane_height, lane_gap):
        self.x = x
        self.lane = lane
        self.y = lane_y + lane * (lane_height + lane_gap)
        self.radius = 14
        self.collected = False
        self.pulse = 0.0
        self.power_type = "invincible"

    def move(self, speed):
        self.x -= speed
        self.pulse += 0.05

    def is_off_screen(self):
        return self.x + self.radius < -20

    def collects(self, player_rect):
        return player_rect.colliderect(self.get_rect())

    def get_rect(self):
        return pygame.Rect(self.x - self.radius, self.y - self.radius,
                           self.radius * 2, self.radius * 2)

    def draw(self, surface):
        pulse_radius = self.radius + int(math.sin(self.pulse) * 3)
        glow_radius = pulse_radius + 4
        pygame.draw.circle(surface, PURPLE, (int(self.x), int(self.y)), pulse_radius)
        pygame.draw.circle(surface, (200, 80, 220), (int(self.x), int(self.y)), pulse_radius, 2)
        for i in range(4):
            angle = self.pulse + i * math.pi / 2
            sx = self.x + int(math.cos(angle) * 5)
            sy = self.y + int(math.sin(angle) * 5)
            pygame.draw.circle(surface, WHITE, (sx, sy), 2)


def parse_args(argv):
    parser = argparse.ArgumentParser(description=WINDOW_TITLE)
    parser.add_argument("--width", type=int, default=WINDOW_WIDTH, help="Window width (default: %(default)s)")
    parser.add_argument("--height", type=int, default=WINDOW_HEIGHT, help="Window height (default: %(default)s)")
    parser.add_argument("--lanes", type=int, default=LANE_COUNT, help="Number of lanes (default: %(default)s)")
    parser.add_argument("--obstacle-speed", type=int, default=OBSTACLE_SPEED, help="Obstacle scroll speed (default: %(default)s)")
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
