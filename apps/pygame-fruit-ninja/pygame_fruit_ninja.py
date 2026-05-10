import argparse
import logging
import math
import random
import sys

import pygame

WINDOW_TITLE = "Fruit Ninja"
FPS = 60
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

FRUIT_RADIUS = 20
GRAVITY = 600.0
FRUIT_SPAWN_INTERVAL = 1.2
MAX_FRUITS = 15
MAX_LIVES = 3

SWIPE_MIN_DIST = 30
SWIPE_MAX_GAP = 100

PARTICLE_COUNT = 12
PARTICLE_LIFETIME = 1.0
PARTICLE_SPEED = 200.0

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
BLUE = (50, 150, 255)
YELLOW = (255, 255, 50)
ORANGE = (255, 165, 50)
PURPLE = (200, 50, 255)
GRAY = (100, 100, 100)
DARK = (30, 30, 30)

FRUIT_COLORS = [RED, GREEN, YELLOW, ORANGE, PURPLE, BLUE]


class Particle:
    def __init__(self, x, y, color):
        angle = random.uniform(0, math.tau)
        speed = random.uniform(PARTICLE_SPEED * 0.5, PARTICLE_SPEED * 1.5)
        self.x = float(x)
        self.y = float(y)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.color = color
        self.lifetime = PARTICLE_LIFETIME
        self.age = 0.0
        self.radius = random.uniform(2, 5)

    def update(self, dt):
        self.age += dt
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.vy += GRAVITY * 0.3 * dt

    @property
    def alive(self):
        return self.age < self.lifetime

    def draw(self, surface):
        alpha = max(0, 1.0 - self.age / self.lifetime)
        radius = int(self.radius * alpha)
        if radius < 1:
            return
        color = tuple(int(c * alpha) for c in self.color)
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), radius)


class Fruit:
    def __init__(self, x, y, window_width):
        self.x = float(x)
        self.y = float(y)
        self.vx = random.uniform(-80, 80)
        self.vy = random.uniform(-500, -350)
        self.radius = FRUIT_RADIUS
        self.color = random.choice(FRUIT_COLORS)
        self.sliced = False
        self.window_width = window_width

    def update(self, dt):
        self.vy += GRAVITY * dt
        self.x += self.vx * dt
        self.y += self.vy * dt

    def is_off_screen(self, height):
        return self.y - self.radius > height

    def get_rect(self):
        return pygame.Rect(
            self.x - self.radius,
            self.y - self.radius,
            self.radius * 2,
            self.radius * 2,
        )

    def contains_point(self, px, py):
        dx = self.x - px
        dy = self.y - py
        return dx * dx + dy * dy <= self.radius * self.radius

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)
        pygame.draw.circle(surface, BLACK, (int(self.x), int(self.y)), self.radius, 2)


class FruitNinjaGame:
    def __init__(self, args):
        self.logger = logging.getLogger("FruitNinja")
        self.logger.setLevel(getattr(logging, args.log_level.upper(), logging.INFO))
        self.window_width = args.width
        self.window_height = args.height
        self.gravity = args.gravity
        self.spawn_interval = args.spawn_interval
        self.score = 0
        self.lives = MAX_LIVES
        self.game_over = False
        self.fruits = []
        self.particles = []
        self.spawn_timer = 0.0
        self.last_mouse_pos = None
        self.swipe_points = []
        self.swipe_age = 0.0

        pygame.init()
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 60)
        self.running = True

        self.logger.info(
            "Game initialized: %dx%d, gravity=%.1f, spawn_interval=%.2f",
            self.window_width, self.window_height,
            self.gravity, self.spawn_interval,
        )

    def reset_game(self):
        self.logger.info("Game reset")
        self.fruits.clear()
        self.particles.clear()
        self.score = 0
        self.lives = MAX_LIVES
        self.game_over = False
        self.spawn_timer = 0.0
        self.swipe_points.clear()
        self.last_mouse_pos = None

    def spawn_fruit(self):
        if len(self.fruits) >= MAX_FRUITS:
            return
        x = random.randint(FRUIT_RADIUS * 2, self.window_width - FRUIT_RADIUS * 2)
        fruit = Fruit(x, self.window_height + FRUIT_RADIUS, self.window_width)
        self.fruits.append(fruit)
        self.logger.debug("Fruit spawned at x=%d", x)

    def slice_fruit(self, fruit):
        fruit.sliced = True
        self.score += 1
        self.logger.debug("Fruit sliced! Score: %d", self.score)
        for _ in range(PARTICLE_COUNT):
            self.particles.append(Particle(fruit.x, fruit.y, fruit.color))

    def check_swipe(self):
        if len(self.swipe_points) < 2:
            return
        p1 = self.swipe_points[-2]
        p2 = self.swipe_points[-1]
        for fruit in self.fruits:
            if fruit.sliced:
                continue
            if line_circle_intersect(p1, p2, (fruit.x, fruit.y), fruit.radius):
                self.slice_fruit(fruit)
                return

    def handle_events(self):
        mouse_buttons = pygame.mouse.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_r and self.game_over:
                    self.reset_game()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.last_mouse_pos = event.pos
                    self.swipe_points.clear()
                    self.swipe_points.append(event.pos)
                    self.swipe_age = 0.0
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    self.last_mouse_pos = None
                    self.swipe_points.clear()
        if mouse_buttons[0]:
            mouse_pos = pygame.mouse.get_pos()
            if self.last_mouse_pos:
                dx = mouse_pos[0] - self.last_mouse_pos[0]
                dy = mouse_pos[1] - self.last_mouse_pos[1]
                dist = math.sqrt(dx * dx + dy * dy)
                if dist > SWIPE_MIN_DIST:
                    self.swipe_points.append(mouse_pos)
                    if len(self.swipe_points) > 10:
                        self.swipe_points.pop(0)
                    self.check_swipe()
            self.last_mouse_pos = mouse_pos

    def update(self, dt):
        if self.game_over:
            return

        self.spawn_timer += dt
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_timer -= self.spawn_interval
            self.spawn_fruit()

        for fruit in list(self.fruits):
            fruit.update(dt)
            if fruit.is_off_screen(self.window_height + 50):
                if not fruit.sliced:
                    self.lives -= 1
                    self.logger.debug("Fruit missed! Lives: %d", self.lives)
                    if self.lives <= 0:
                        self.game_over = True
                        self.logger.info("Game Over! Final score: %d", self.score)
                self.fruits.remove(fruit)

        self.fruits = [f for f in self.fruits if not f.sliced]

        for p in list(self.particles):
            p.update(dt)
            if not p.alive:
                self.particles.remove(p)

    def draw(self):
        self.screen.fill(DARK)

        for fruit in self.fruits:
            fruit.draw(self.screen)

        for p in self.particles:
            p.draw(self.screen)

        if self.swipe_points and len(self.swipe_points) > 1:
            for i in range(1, len(self.swipe_points)):
                alpha = i / len(self.swipe_points)
                width = max(1, int(4 * alpha))
                color = tuple(int(200 * alpha) for _ in range(3))
                pygame.draw.line(
                    self.screen, color,
                    self.swipe_points[i - 1], self.swipe_points[i], width,
                )

        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))

        lives_text = self.font.render(f"Lives: {self.lives}", True, WHITE)
        self.screen.blit(lives_text, (10, 50))

        if self.game_over:
            game_over_text = self.big_font.render("GAME OVER", True, RED)
            game_over_rect = game_over_text.get_rect(
                center=(self.window_width // 2, self.window_height // 2 - 30)
            )
            self.screen.blit(game_over_text, game_over_rect)
            restart_text = self.font.render("Press R to restart, ESC to quit", True, WHITE)
            restart_rect = restart_text.get_rect(
                center=(self.window_width // 2, self.window_height // 2 + 20)
            )
            self.screen.blit(restart_text, restart_rect)

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


def line_circle_intersect(p1, p2, center, radius):
    x1, y1 = p1
    x2, y2 = p2
    cx, cy = center

    dx = x2 - x1
    dy = y2 - y1
    fx = x1 - cx
    fy = y1 - cy

    a = dx * dx + dy * dy
    b = 2 * (fx * dx + fy * dy)
    c = fx * fx + fy * fy - radius * radius

    discriminant = b * b - 4 * a * c
    if discriminant <= 0:
        return False

    sqrt_disc = math.sqrt(discriminant)
    t1 = (-b - sqrt_disc) / (2 * a)
    t2 = (-b + sqrt_disc) / (2 * a)

    return (0 <= t1 <= 1) or (0 <= t2 <= 1)


def parse_args(argv):
    parser = argparse.ArgumentParser(description=WINDOW_TITLE)
    parser.add_argument("--width", type=int, default=WINDOW_WIDTH, help="Window width (default: %(default)s)")
    parser.add_argument("--height", type=int, default=WINDOW_HEIGHT, help="Window height (default: %(default)s)")
    parser.add_argument("--gravity", type=float, default=GRAVITY, help="Gravity strength (default: %(default)s)")
    parser.add_argument("--spawn-interval", type=float, default=FRUIT_SPAWN_INTERVAL, help="Seconds between fruit spawns (default: %(default)s)")
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
    game = FruitNinjaGame(args)
    game.run()


if __name__ == "__main__":
    main()
