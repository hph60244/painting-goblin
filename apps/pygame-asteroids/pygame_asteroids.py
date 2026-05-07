import argparse
import logging
import sys
import math
import random

import pygame

# Constraint: 使用Pygame
# Constraint: 極簡風格 - minimal constants, no bloat
WINDOW_TITLE = "Asteroids"
FPS = 60
WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 768

# Ship params
SHIP_SIZE = 20
SHIP_ROTATION_SPEED = 270
SHIP_THRUST_POWER = 300.0
SHIP_FRICTION = 0.98
SHIP_MAX_SPEED = 400.0

# Bullet params
BULLET_SPEED = 500.0
BULLET_LIFETIME = 1.5
SHOOT_COOLDOWN = 0.25

# Asteroid params - Task: Splitting
ASTEROID_SIZES = {
    3: {"radius": 60, "speed_range": (40, 80), "points": 20},
    2: {"radius": 35, "speed_range": (60, 120), "points": 50},
    1: {"radius": 18, "speed_range": (80, 180), "points": 100},
}
ASTEROID_SPAWN_COUNT = 4
INITIAL_LIVES = 3
INVINCIBLE_TIME = 3.0

# Constraint: 極簡呈現 - monochrome palette
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


def wrap_position(pos, width, height):
    # Constraint: Screen wrapping
    x, y = pos
    if x < 0:
        x += width
    elif x > width:
        x -= width
    if y < 0:
        y += height
    elif y > height:
        y -= height
    return x, y


def random_polygon_points(radius):
    num_points = random.randint(8, 12)
    points = []
    for i in range(num_points):
        angle = (2 * math.pi / num_points) * i
        r = radius * random.uniform(0.65, 1.0)
        x = r * math.cos(angle)
        y = r * math.sin(angle)
        points.append((x, y))
    return points


class Ship:
    # Task: Vector rotation, thrust
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angle = -math.pi / 2
        self.vel_x = 0.0
        self.vel_y = 0.0
        self.radius = SHIP_SIZE
        self.thrusting = False
        self.invincible = False
        self.invincible_timer = 0.0
        self.alive = True

    # Task: Vector rotation
    def rotate_left(self):
        self.angle -= math.radians(SHIP_ROTATION_SPEED * 1 / 60)

    def rotate_right(self):
        self.angle += math.radians(SHIP_ROTATION_SPEED * 1 / 60)

    # Task: Thrust
    def thrust(self, dt):
        self.vel_x += math.cos(self.angle) * SHIP_THRUST_POWER * dt
        self.vel_y += math.sin(self.angle) * SHIP_THRUST_POWER * dt

    def update(self, dt, width, height):
        if not self.alive:
            return

        self.vel_x *= SHIP_FRICTION
        self.vel_y *= SHIP_FRICTION

        speed = math.hypot(self.vel_x, self.vel_y)
        if speed > SHIP_MAX_SPEED:
            scale = SHIP_MAX_SPEED / speed
            self.vel_x *= scale
            self.vel_y *= scale

        self.x += self.vel_x * dt
        self.y += self.vel_y * dt

        # Constraint: Screen wrapping
        self.x, self.y = wrap_position((self.x, self.y), width, height)

        if self.invincible:
            self.invincible_timer -= dt
            if self.invincible_timer <= 0:
                self.invincible = False

    def get_vertices(self):
        tip_x = self.x + SHIP_SIZE * math.cos(self.angle)
        tip_y = self.y + SHIP_SIZE * math.sin(self.angle)
        left_x = self.x + SHIP_SIZE * 0.6 * math.cos(self.angle + 2.5)
        left_y = self.y + SHIP_SIZE * 0.6 * math.sin(self.angle + 2.5)
        right_x = self.x + SHIP_SIZE * 0.6 * math.cos(self.angle - 2.5)
        right_y = self.y + SHIP_SIZE * 0.6 * math.sin(self.angle - 2.5)
        return [(tip_x, tip_y), (left_x, left_y), (right_x, right_y)]

    def draw(self, surface):
        if not self.alive:
            return
        if self.invincible:
            if int(self.invincible_timer * 10) % 2 == 0:
                return
        vertices = self.get_vertices()
        pygame.draw.polygon(surface, WHITE, vertices, 2)


class Bullet:
    def __init__(self, x, y, angle):
        self.x = x
        self.y = y
        self.vel_x = math.cos(angle) * BULLET_SPEED
        self.vel_y = math.sin(angle) * BULLET_SPEED
        self.radius = 2
        self.lifetime = BULLET_LIFETIME
        self.alive = True

    def update(self, dt, width, height):
        self.x += self.vel_x * dt
        self.y += self.vel_y * dt

        # Constraint: Screen wrapping
        self.x, self.y = wrap_position((self.x, self.y), width, height)

        self.lifetime -= dt
        if self.lifetime <= 0:
            self.alive = False

    def draw(self, surface):
        pygame.draw.circle(surface, WHITE, (int(self.x), int(self.y)), self.radius)


class Asteroid:
    # Task: Splitting
    def __init__(self, x, y, size):
        self.x = x
        self.y = y
        self.size = size
        config = ASTEROID_SIZES[size]
        self.radius = config["radius"]

        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(*config["speed_range"])
        self.vel_x = math.cos(angle) * speed
        self.vel_y = math.sin(angle) * speed

        self.rotation_speed = random.uniform(-1.5, 1.5)
        self.rot_angle = 0.0
        self.base_shape = random_polygon_points(self.radius)
        self.alive = True

    def update(self, dt, width, height):
        self.x += self.vel_x * dt
        self.y += self.vel_y * dt
        self.rot_angle += self.rotation_speed * dt

        # Constraint: Screen wrapping
        self.x, self.y = wrap_position((self.x, self.y), width, height)

    def get_vertices(self):
        cos_a = math.cos(math.radians(self.rot_angle))
        sin_a = math.sin(math.radians(self.rot_angle))
        vertices = []
        for dx, dy in self.base_shape:
            rx = dx * cos_a - dy * sin_a
            ry = dx * sin_a + dy * cos_a
            vertices.append((self.x + rx, self.y + ry))
        return vertices

    # Task: Splitting
    def split(self):
        if not self.alive:
            return []
        self.alive = False
        new_size = self.size - 1
        if new_size < 1:
            return []
        asteroids = []
        for _ in range(2):
            new_ast = Asteroid(self.x, self.y, new_size)
            new_ast.x += random.uniform(-10, 10)
            new_ast.y += random.uniform(-10, 10)
            asteroids.append(new_ast)
        return asteroids

    def draw(self, surface):
        if not self.alive:
            return
        vertices = self.get_vertices()
        pygame.draw.polygon(surface, WHITE, vertices, 2)


class Game:
    def __init__(self, args):
        # Constraint: 使用logger輸出訊息
        self.logger = logging.getLogger("Asteroids")
        self.logger.setLevel(getattr(logging, args.log_level.upper(), logging.INFO))
        self.window_width = args.width
        self.window_height = args.height
        self.fps = args.fps
        self.asteroid_count = args.asteroids
        self.lives = args.lives
        self.score = 0
        self.level = 1
        self.shoot_timer = 0.0
        self.respawning = False
        self.respawn_timer = 0.0

        # Constraint: 使用Pygame
        pygame.init()
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 28)
        self.big_font = pygame.font.Font(None, 48)
        self.running = True

        self.ship = Ship(self.window_width // 2, self.window_height // 2)
        self.bullets = []
        self.asteroids = []

        self.spawn_asteroids(self.asteroid_count)

        self.logger.info(
            "Game initialized: %dx%d, fps=%d, asteroids=%d, lives=%d",
            self.window_width, self.window_height, self.fps, self.asteroid_count, self.lives,
        )

    def spawn_asteroids(self, count, size=3):
        for _ in range(count):
            while True:
                x = random.uniform(50, self.window_width - 50)
                y = random.uniform(50, self.window_height - 50)
                if math.hypot(x - self.ship.x, y - self.ship.y) > 150:
                    break
            self.asteroids.append(Asteroid(x, y, size))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_r and not self.ship.alive and self.lives <= 0:
                    self.reset_game()
                elif event.key == pygame.K_SPACE:
                    self.try_shoot()

    def handle_input(self, dt):
        if not self.ship.alive:
            return
        keys = pygame.key.get_pressed()

        # Task: Vector rotation
        if keys[pygame.K_LEFT]:
            self.ship.rotate_left()
        if keys[pygame.K_RIGHT]:
            self.ship.rotate_right()
        # Task: Thrust
        if keys[pygame.K_UP]:
            self.ship.thrust(dt)
            self.ship.thrusting = True
        else:
            self.ship.thrusting = False

        if keys[pygame.K_SPACE]:
            self.try_shoot()

    def try_shoot(self):
        if self.shoot_timer > 0:
            return
        if not self.ship.alive:
            return
        bullet = Bullet(self.ship.x, self.ship.y, self.ship.angle)
        self.bullets.append(bullet)
        self.shoot_timer = SHOOT_COOLDOWN
        self.logger.debug("Bullet fired at angle=%.1f", math.degrees(self.ship.angle))

    def reset_game(self):
        self.logger.info("Game reset")
        self.score = 0
        self.level = 1
        self.lives = INITIAL_LIVES
        self.ship = Ship(self.window_width // 2, self.window_height // 2)
        self.bullets.clear()
        self.asteroids.clear()
        self.spawn_asteroids(self.asteroid_count)
        self.respawning = False
        self.respawn_timer = 0.0

    def respawn_ship(self):
        self.ship = Ship(self.window_width // 2, self.window_height // 2)
        self.ship.invincible = True
        self.ship.invincible_timer = INVINCIBLE_TIME
        self.respawning = False
        self.logger.debug("Ship respawned, lives=%d", self.lives)

    def update(self, dt):
        self.shoot_timer = max(0, self.shoot_timer - dt)

        if self.respawning:
            self.respawn_timer -= dt
            if self.respawn_timer <= 0:
                self.respawn_ship()
            else:
                for asteroid in self.asteroids:
                    asteroid.update(dt, self.window_width, self.window_height)
                return

        self.ship.update(dt, self.window_width, self.window_height)
        for bullet in self.bullets:
            bullet.update(dt, self.window_width, self.window_height)
        self.bullets = [b for b in self.bullets if b.alive]
        for asteroid in self.asteroids:
            asteroid.update(dt, self.window_width, self.window_height)

        # Task: Splitting - bullet hits asteroid
        new_asteroids = []
        for bullet in self.bullets:
            for asteroid in self.asteroids:
                if not asteroid.alive or not bullet.alive:
                    continue
                dist = math.hypot(bullet.x - asteroid.x, bullet.y - asteroid.y)
                if dist < asteroid.radius:
                    bullet.alive = False
                    score_gain = ASTEROID_SIZES[asteroid.size]["points"]
                    self.score += score_gain
                    self.logger.debug(
                        "Asteroid hit! size=%d, +%d pts, total=%d",
                        asteroid.size, score_gain, self.score,
                    )
                    new_asteroids.extend(asteroid.split())
                    break
        self.bullets = [b for b in self.bullets if b.alive]
        self.asteroids = [a for a in self.asteroids if a.alive]
        self.asteroids.extend(new_asteroids)

        # Ship hit by asteroid
        if self.ship.alive and not self.ship.invincible:
            for asteroid in self.asteroids:
                if not asteroid.alive:
                    continue
                for vx, vy in self.ship.get_vertices():
                    dist = math.hypot(vx - asteroid.x, vy - asteroid.y)
                    if dist < asteroid.radius:
                        self.ship.alive = False
                        self.lives -= 1
                        self.logger.info("Ship destroyed! lives=%d", self.lives)
                        if self.lives > 0:
                            self.respawning = True
                            self.respawn_timer = 1.5
                        break
                if not self.ship.alive:
                    break

        # Level progression
        remaining = [a for a in self.asteroids if a.alive]
        if len(remaining) == 0:
            self.level += 1
            self.logger.info("Level %d started", self.level)
            self.spawn_asteroids(self.asteroid_count + self.level - 1)

    def draw_hud(self):
        score_surf = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_surf, (10, 10))
        level_surf = self.font.render(f"Level: {self.level}", True, WHITE)
        self.screen.blit(level_surf, (10, 35))
        lives_surf = self.font.render(f"Lives: {self.lives}", True, WHITE)
        self.screen.blit(lives_surf, (10, 60))

    def draw_game_over(self):
        if not self.ship.alive and self.lives <= 0 and not self.respawning:
            text = self.big_font.render("GAME OVER", True, WHITE)
            rect = text.get_rect(center=(self.window_width // 2, self.window_height // 2 - 30))
            self.screen.blit(text, rect)
            restart = self.font.render("Press R to restart, ESC to quit", True, WHITE)
            r_rect = restart.get_rect(center=(self.window_width // 2, self.window_height // 2 + 20))
            self.screen.blit(restart, r_rect)

    def draw(self):
        self.screen.fill(BLACK)

        self.ship.draw(self.screen)
        for bullet in self.bullets:
            bullet.draw(self.screen)
        for asteroid in self.asteroids:
            asteroid.draw(self.screen)

        self.draw_hud()
        self.draw_game_over()

        pygame.display.flip()

    def run(self):
        self.logger.info("Game started")
        while self.running:
            dt = self.clock.tick(self.fps) / 1000.0
            self.handle_events()
            self.handle_input(dt)
            self.update(dt)
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
        "--asteroids", type=int, default=ASTEROID_SPAWN_COUNT,
        help="Asteroids per level (default: %(default)s)",
    )
    parser.add_argument(
        "--lives", type=int, default=INITIAL_LIVES,
        help="Number of lives (default: %(default)s)",
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
