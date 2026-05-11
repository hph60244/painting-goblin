import argparse
import logging
import sys
import math
import random

import pygame
import pymunk

# Constraint: 使用Pygame - 適合製作2D遊戲原型, 輕量化
# Constraint: 用極簡風格呈現 - 強調玩法概念, 節省製作時間
# Contract: Physics simulation (Pymunk), destructible

WINDOW_TITLE = "Angry Birds"
FPS = 60
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 600

GROUND_HEIGHT = 40
GRAVITY = (0.0, 900.0)

BIRD_RADIUS = 12
BIRD_MASS = 5.0
PIG_RADIUS = 14
PIG_MASS = 2.0

BLOCK_W = 20
BLOCK_H = 50

SLING_X = 150
SLING_Y = WINDOW_HEIGHT - GROUND_HEIGHT - 60
MAX_BIRDS = 3
LAUNCH_POWER_SCALE = 10000
MAX_DRAG_DIST = 200

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)
RED = (255, 50, 50)
GREEN = (50, 200, 50)
YELLOW = (255, 255, 50)
SKY_COLOR = (135, 206, 235)
GROUND_COLOR = (100, 180, 80)
WOOD_COLOR = (180, 130, 60)
WOOD_DAMAGED = (220, 180, 120)
STONE_COLOR = (120, 120, 120)
STONE_DAMAGED = (170, 170, 170)
SLING_COLOR = (80, 40, 20)
DARK_GREEN = (0, 100, 0)

CT_BIRD = 1
CT_PIG = 2
CT_BLOCK = 3
CT_GROUND = 4
CT_WALL = 5
CT_SENSOR = 6


class Bird:
    def __init__(self, space, x, y):
        self.body = pymunk.Body(BIRD_MASS, pymunk.moment_for_circle(BIRD_MASS, 0, BIRD_RADIUS))
        self.body.position = x, y
        self.shape = pymunk.Circle(self.body, BIRD_RADIUS)
        self.shape.elasticity = 0.3
        self.shape.friction = 0.5
        self.shape.collision_type = CT_BIRD
        space.add(self.body, self.shape)
        self.launched = False

    def launch(self, vx, vy):
        self.body.velocity = (vx, vy)
        self.launched = True

    def should_remove(self):
        vel = self.body.velocity
        x, y = self.body.position
        speed = math.hypot(vel.x, vel.y)
        ground_top = WINDOW_HEIGHT - GROUND_HEIGHT * 2
        on_ground = y > ground_top - BIRD_RADIUS
        return (speed < 3 and on_ground) or x > WINDOW_WIDTH + 100 or y > WINDOW_HEIGHT + 100

    def draw(self, surface):
        x, y = int(self.body.position.x), int(self.body.position.y)
        pygame.draw.circle(surface, RED, (x, y), BIRD_RADIUS)
        pygame.draw.circle(surface, BLACK, (x, y), BIRD_RADIUS, 1)
        eye_off = BIRD_RADIUS * 0.3
        pygame.draw.circle(surface, WHITE, (int(x - eye_off), int(y - eye_off)), 4)
        pygame.draw.circle(surface, WHITE, (int(x + eye_off), int(y - eye_off)), 4)
        pygame.draw.circle(surface, BLACK, (int(x - eye_off), int(y - eye_off)), 2)
        pygame.draw.circle(surface, BLACK, (int(x + eye_off), int(y - eye_off)), 2)
        brow_y = y - eye_off - 5
        pygame.draw.line(surface, BLACK, (x - eye_off - 4, brow_y - 2), (x - eye_off + 2, brow_y + 1), 2)
        pygame.draw.line(surface, BLACK, (x + eye_off + 4, brow_y - 2), (x + eye_off - 2, brow_y + 1), 2)


class Pig:
    def __init__(self, space, x, y):
        self.body = pymunk.Body(PIG_MASS, pymunk.moment_for_circle(PIG_MASS, 0, PIG_RADIUS))
        self.body.position = x, y
        self.shape = pymunk.Circle(self.body, PIG_RADIUS)
        self.shape.elasticity = 0.1
        self.shape.friction = 0.8
        self.shape.collision_type = CT_PIG
        space.add(self.body, self.shape)
        self.alive = True
        self.hp = 3

    def hit(self, impulse):
        dmg = max(1, int(abs(impulse) / 200))
        self.hp -= dmg
        if self.hp <= 0:
            self.hp = 0
            self.alive = False
            return True
        return False

    def draw(self, surface):
        if not self.alive:
            return
        x, y = int(self.body.position.x), int(self.body.position.y)
        color = GREEN if self.hp > 1 else YELLOW
        pygame.draw.circle(surface, color, (x, y), PIG_RADIUS)
        pygame.draw.circle(surface, BLACK, (x, y), PIG_RADIUS, 1)
        pygame.draw.circle(surface, DARK_GREEN, (x, y), 5)
        pygame.draw.circle(surface, BLACK, (x - 5, y - 4), 3)
        pygame.draw.circle(surface, BLACK, (x + 5, y - 4), 3)


class Block:
    def __init__(self, space, x, y, w, h, block_type="wood"):
        self.w = w
        self.h = h
        self.block_type = block_type
        if block_type == "stone":
            mass = 10.0
            self.max_hp = 6
        else:
            mass = 3.0
            self.max_hp = 2
        moment = pymunk.moment_for_box(mass, (w, h))
        self.body = pymunk.Body(mass, moment)
        self.body.position = x, y
        self.shape = pymunk.Poly.create_box(self.body, (w, h))
        self.shape.elasticity = 0.1
        self.shape.friction = 0.7
        self.shape.collision_type = CT_BLOCK
        space.add(self.body, self.shape)
        self.alive = True
        self.hp = self.max_hp

    def hit(self, impulse):
        dmg = max(1, int(abs(impulse) / 150))
        self.hp -= dmg
        if self.hp <= 0:
            self.hp = 0
            self.alive = False
            return True
        return False

    def draw(self, surface):
        if not self.alive:
            return
        x, y = int(self.body.position.x), int(self.body.position.y)
        a = self.body.angle
        cos_a, sin_a = math.cos(a), math.sin(a)
        hw, hh = self.w / 2, self.h / 2
        corners = [(-hw, -hh), (hw, -hh), (hw, hh), (-hw, hh)]
        pts = []
        for dx, dy in corners:
            rx = x + dx * cos_a - dy * sin_a
            ry = y + dx * sin_a + dy * cos_a
            pts.append((int(rx), int(ry)))

        if self.block_type == "stone":
            color = STONE_DAMAGED if self.hp <= self.max_hp // 2 else STONE_COLOR
        else:
            color = WOOD_DAMAGED if self.hp <= self.max_hp // 2 else WOOD_COLOR
        pygame.draw.polygon(surface, color, pts)
        pygame.draw.polygon(surface, BLACK, pts, 1)


class Game:
    def __init__(self, args):
        self.logger = logging.getLogger("AngryBirds")
        self.logger.setLevel(getattr(logging, args.log_level.upper(), logging.INFO))
        self.window_width = args.width
        self.window_height = args.height
        self.fps = args.fps
        self.max_birds = args.birds

        pygame.init()
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 28)
        self.big_font = pygame.font.Font(None, 48)
        self.running = True

        self.space = pymunk.Space()
        self.space.gravity = GRAVITY
        self.dt_accum = 0.0
        self.physics_dt = 1.0 / 60.0

        self.blocks = []
        self.pigs = []
        self.score = 0
        self.birds_used = 0
        self.current_bird = None
        self.dragging = False
        self.drag_start = (0, 0)
        self.drag_end = (0, 0)
        self.game_over = False
        self.level_clear = False

        self._setup_collision_handlers()
        self._create_boundaries()
        self._build_structure()
        self._spawn_bird()

        self.logger.info(
            "Game initialized: %dx%d, fps=%d, birds=%d",
            self.window_width, self.window_height, self.fps, self.max_birds,
        )

    def _setup_collision_handlers(self):
        self.space.on_collision(CT_BIRD, CT_PIG, post_solve=self._on_bird_pig_collision)
        self.space.on_collision(CT_BIRD, CT_BLOCK, post_solve=self._on_bird_block_collision)
        self.space.on_collision(CT_PIG, CT_GROUND, post_solve=self._on_ground_collision)
        self.space.on_collision(CT_BLOCK, CT_GROUND, post_solve=self._on_ground_collision)

    def _on_bird_pig_collision(self, arbiter, space, data):
        impulse = arbiter.total_impulse
        impulse_mag = math.hypot(impulse.x, impulse.y)
        pig_shape = arbiter.shapes[1]
        pig = self._find_pig(pig_shape)
        if pig and pig.alive:
            destroyed = pig.hit(impulse_mag)
            if destroyed:
                self.score += 500
                self.logger.debug("Pig destroyed! Score=%d", self.score)
        return True

    def _on_bird_block_collision(self, arbiter, space, data):
        impulse = arbiter.total_impulse
        impulse_mag = math.hypot(impulse.x, impulse.y)
        block_shape = arbiter.shapes[1]
        block = self._find_block(block_shape)
        if block and block.alive:
            destroyed = block.hit(impulse_mag)
            if destroyed:
                self.logger.debug("Block destroyed")
        return True

    def _on_ground_collision(self, arbiter, space, data):
        shape = arbiter.shapes[0]
        body = shape.body
        speed = body.velocity.length
        if speed < 30:
            return True
        impulse = arbiter.total_impulse
        impulse_mag = math.hypot(impulse.x, impulse.y)
        if shape.collision_type == CT_PIG:
            pig = self._find_pig(shape)
            if pig and pig.alive:
                destroyed = pig.hit(impulse_mag)
                if destroyed:
                    self.score += 500
                    self.logger.debug("Pig destroyed by fall! Score=%d", self.score)
        elif shape.collision_type == CT_BLOCK:
            block = self._find_block(shape)
            if block and block.alive:
                destroyed = block.hit(impulse_mag)
                if destroyed:
                    self.logger.debug("Block destroyed by fall")
        return True

    def _find_pig(self, shape):
        for pig in self.pigs:
            if pig.shape == shape:
                return pig
        return None

    def _find_block(self, shape):
        for block in self.blocks:
            if block.shape == shape:
                return block
        return None

    def _create_boundaries(self):
        ground_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        ground_shape = pymunk.Segment(
            ground_body, (0, self.window_height - GROUND_HEIGHT),
            (self.window_width, self.window_height - GROUND_HEIGHT), GROUND_HEIGHT
        )
        ground_shape.elasticity = 0.2
        ground_shape.friction = 0.9
        ground_shape.collision_type = CT_GROUND
        self.space.add(ground_body, ground_shape)

        wall_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        wall_shape = pymunk.Segment(
            wall_body, (0, 0), (0, self.window_height), 5
        )
        wall_shape.collision_type = CT_WALL
        self.space.add(wall_body, wall_shape)

        wall_body2 = pymunk.Body(body_type=pymunk.Body.STATIC)
        wall_shape2 = pymunk.Segment(
            wall_body2, (self.window_width, 0), (self.window_width, self.window_height), 5
        )
        wall_shape2.collision_type = CT_WALL
        self.space.add(wall_body2, wall_shape2)

        ceiling_body = pymunk.Body(body_type=pymunk.Body.STATIC)
        ceiling_shape = pymunk.Segment(
            ceiling_body, (0, 0), (self.window_width, 0), 5
        )
        ceiling_shape.collision_type = CT_WALL
        self.space.add(ceiling_body, ceiling_shape)

    def _build_structure(self):
        ground_y = self.window_height - GROUND_HEIGHT
        cx = self.window_width // 2

        col_spacing = 60
        cols = [
            ("left", cx - col_spacing),
            ("right", cx + col_spacing),
        ]
        hog = BLOCK_H
        for _, col_x in cols:
            for i in range(3):
                y = ground_y - hog * i - hog // 2
                block = Block(self.space, col_x, y, BLOCK_W, hog, "wood")
                self.blocks.append(block)

        beam_y = ground_y - 3 * hog - 7
        beam = Block(self.space, cx, beam_y, col_spacing * 2 + BLOCK_W, 14, "wood")
        self.blocks.append(beam)

        pig_positions = [
            (cx - 20, ground_y - hog - PIG_RADIUS),
            (cx + 20, ground_y - hog - PIG_RADIUS),
        ]
        for px, py in pig_positions:
            pig = Pig(self.space, px, py)
            self.pigs.append(pig)

    def reset_game(self):
        self.logger.info("Game reset")
        for b in self.blocks:
            try:
                self.space.remove(b.shape, b.body)
            except Exception:
                pass
        for p in self.pigs:
            try:
                self.space.remove(p.shape, p.body)
            except Exception:
                pass
        if self.current_bird:
            try:
                self.space.remove(self.current_bird.shape, self.current_bird.body)
            except Exception:
                pass
            self.current_bird = None

        self.blocks = []
        self.pigs = []
        self.score = 0
        self.birds_used = 0
        self.current_bird = None
        self.dragging = False
        self.drag_start = (0, 0)
        self.drag_end = (0, 0)
        self.game_over = False
        self.level_clear = False
        self._build_structure()
        self._spawn_bird()

    def _spawn_bird(self):
        if self.current_bird:
            self.space.remove(self.current_bird.shape, self.current_bird.body)
            self.current_bird = None
        if self.birds_used < self.max_birds:
            self.current_bird = Bird(self.space, SLING_X, SLING_Y)
            self.dragging = True
            self.drag_start = (SLING_X, SLING_Y)
            self.drag_end = (SLING_X, SLING_Y)

    def _launch_bird(self):
        if not self.current_bird or self.current_bird.launched:
            return
        dx = self.drag_end[0] - self.drag_start[0]
        dy = self.drag_end[1] - self.drag_start[1]
        dist = math.hypot(dx, dy)
        if dist < 5:
            self.dragging = False
            return
        power = min(dist / MAX_DRAG_DIST, 1.0) * LAUNCH_POWER_SCALE / BIRD_MASS
        vx = -dx / dist * power
        vy = -dy / dist * power
        self.current_bird.launch(vx, vy)
        self.birds_used += 1
        self.dragging = False
        self.logger.debug("Bird launched! velocity=(%.0f, %.0f) bird=%d/%d",
                          vx, vy, self.birds_used, self.max_birds)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_r and (self.game_over or self.level_clear):
                    self._cleanup_objects()
                    self.reset_game()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.dragging and self.current_bird and not self.current_bird.launched:
                    mx, my = event.pos
                    bx, by = self.current_bird.body.position
                    if math.hypot(mx - bx, my - by) < BIRD_RADIUS + 20:
                        self.drag_start = (bx, by)
                        self.drag_end = (mx, my)
            elif event.type == pygame.MOUSEMOTION:
                if self.dragging and self.current_bird and not self.current_bird.launched:
                    mx, my = event.pos
                    dx = mx - SLING_X
                    dy = my - SLING_Y
                    dist = math.hypot(dx, dy)
                    if dist > MAX_DRAG_DIST:
                        mx = SLING_X + dx / dist * MAX_DRAG_DIST
                        my = SLING_Y + dy / dist * MAX_DRAG_DIST
                    self.drag_end = (mx, my)
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.dragging and self.current_bird and not self.current_bird.launched:
                    self._launch_bird()

    def _cleanup_objects(self):
        for b in self.blocks:
            try:
                self.space.remove(b.shape, b.body)
            except Exception:
                pass
        for p in self.pigs:
            try:
                self.space.remove(p.shape, p.body)
            except Exception:
                pass
        if self.current_bird:
            try:
                self.space.remove(self.current_bird.shape, self.current_bird.body)
            except Exception:
                pass
            self.current_bird = None

    def update(self):
        self.dt_accum += self.clock.get_time() / 1000.0
        while self.dt_accum >= self.physics_dt:
            self.space.step(self.physics_dt)
            self.dt_accum -= self.physics_dt

        self.space.step(self.physics_dt)

        if self.current_bird and self.current_bird.launched:
            if self.current_bird.should_remove():
                self.logger.debug("Bird removed")
                try:
                    self.space.remove(self.current_bird.shape, self.current_bird.body)
                except Exception:
                    pass
                self.current_bird = None
                if self.birds_used < self.max_birds:
                    self._spawn_bird()
                else:
                    self.dragging = False

        pigs_alive = sum(1 for p in self.pigs if p.alive)
        if pigs_alive == 0 and not self.level_clear:
            self.level_clear = True
            self.logger.info("Level clear! Score=%d", self.score)

        if self.birds_used >= self.max_birds and pigs_alive > 0 and \
           (self.current_bird is None or not self.current_bird.launched):
            self.game_over = True

    def draw_trajectory_preview(self, surface):
        if not (self.dragging and self.current_bird and not self.current_bird.launched):
            return
        dx = self.drag_end[0] - self.drag_start[0]
        dy = self.drag_end[1] - self.drag_start[1]
        dist = math.hypot(dx, dy)
        if dist < 5:
            return
        power = min(dist / MAX_DRAG_DIST, 1.0) * LAUNCH_POWER_SCALE / BIRD_MASS
        vx = -dx / dist * power
        vy = -dy / dist * power
        gx, gy = self.space.gravity
        px, py = SLING_X, SLING_Y
        for i in range(1, 30):
            t = i * 0.05
            tx = px + vx * t
            ty = py + vy * t + 0.5 * gy * t * t
            if ty > self.window_height - GROUND_HEIGHT * 2 or tx < 0 or tx > self.window_width:
                break
            alpha = 1.0 - i / 30.0
            color = (int(255 * alpha), int(255 * alpha), int(255 * alpha))
            pygame.draw.circle(surface, color, (int(tx), int(ty)), 3)

    def draw_slingshot(self, surface):
        sx, sy = SLING_X, SLING_Y
        fork_left = (sx - 15, sy - 40)
        fork_right = (sx + 15, sy - 40)
        pygame.draw.line(surface, SLING_COLOR, (sx, sy - 10), fork_left, 4)
        pygame.draw.line(surface, SLING_COLOR, (sx, sy - 10), fork_right, 4)
        pygame.draw.line(surface, SLING_COLOR, (sx, sy), (sx, sy - 10), 4)

        if self.dragging and self.current_bird and not self.current_bird.launched:
            bx, by = int(self.current_bird.body.position.x), int(self.current_bird.body.position.y)
            pygame.draw.line(surface, SLING_COLOR, fork_left, (bx, by), 3)
            pygame.draw.line(surface, SLING_COLOR, fork_right, (bx, by), 3)
        elif self.current_bird and not self.current_bird.launched:
            bx, by = int(self.current_bird.body.position.x), int(self.current_bird.body.position.y)
            pygame.draw.line(surface, SLING_COLOR, fork_left, (bx, by), 3)
            pygame.draw.line(surface, SLING_COLOR, fork_right, (bx, by), 3)

    def draw_hud(self):
        score_text = self.font.render(f"Score: {self.score}", True, BLACK)
        birds_text = self.font.render(f"Birds: {self.max_birds - self.birds_used}", True, BLACK)
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(birds_text, (self.window_width - 120, 10))

        if self.dragging and self.current_bird and not self.current_bird.launched:
            hint = self.font.render("Drag and release to launch!", True, GRAY)
            hint_rect = hint.get_rect(center=(self.window_width // 2, 30))
            self.screen.blit(hint, hint_rect)

    def draw_clear_overlay(self):
        if self.level_clear:
            text = self.big_font.render("LEVEL CLEAR!", True, GREEN)
            text_rect = text.get_rect(center=(self.window_width // 2, self.window_height // 2 - 30))
            self.screen.blit(text, text_rect)
            restart = self.font.render("Press R to restart, ESC to quit", True, BLACK)
            restart_rect = restart.get_rect(center=(self.window_width // 2, self.window_height // 2 + 20))
            self.screen.blit(restart, restart_rect)

    def draw_game_over(self):
        if self.game_over:
            text = self.big_font.render("GAME OVER", True, RED)
            text_rect = text.get_rect(center=(self.window_width // 2, self.window_height // 2 - 30))
            self.screen.blit(text, text_rect)
            restart = self.font.render("Press R to restart, ESC to quit", True, BLACK)
            restart_rect = restart.get_rect(center=(self.window_width // 2, self.window_height // 2 + 20))
            self.screen.blit(restart, restart_rect)

    def draw(self):
        self.screen.fill(SKY_COLOR)
        pygame.draw.rect(self.screen, GROUND_COLOR,
                         (0, self.window_height - GROUND_HEIGHT, self.window_width, GROUND_HEIGHT))
        pygame.draw.rect(self.screen, (80, 160, 60),
                         (0, self.window_height - GROUND_HEIGHT, self.window_width, 3))

        for block in self.blocks:
            block.draw(self.screen)
        for pig in self.pigs:
            pig.draw(self.screen)
        if self.current_bird and not self.current_bird.launched:
            self.draw_trajectory_preview(self.screen)
        self.draw_slingshot(self.screen)
        if self.current_bird:
            self.current_bird.draw(self.screen)
        self.draw_hud()
        self.draw_clear_overlay()
        self.draw_game_over()
        pygame.display.flip()

    def run(self):
        self.logger.info("Game started")
        while self.running:
            self.clock.tick(self.fps)
            self.handle_events()
            self.update()
            self.draw()
        self.logger.info("Game ended")
        pygame.quit()
        sys.exit()


def parse_args(argv):
    parser = argparse.ArgumentParser(description=WINDOW_TITLE)
    parser.add_argument("--fps", type=int, default=FPS, help="Frame rate (default: %(default)s)")
    parser.add_argument("--width", type=int, default=WINDOW_WIDTH, help="Window width (default: %(default)s)")
    parser.add_argument("--height", type=int, default=WINDOW_HEIGHT, help="Window height (default: %(default)s)")
    parser.add_argument("--birds", type=int, default=MAX_BIRDS, help="Number of birds (default: %(default)s)")
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
