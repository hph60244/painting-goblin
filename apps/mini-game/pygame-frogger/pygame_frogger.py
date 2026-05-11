import argparse
import logging
import sys
import random

import pygame

# Constraint: 使用Pygame - 2D遊戲原型框架
WINDOW_TITLE = "Frogger"
FPS = 60

# Constraint: 極簡風格 - minimal grid-based layout
CELL_SIZE = 40
COLS = 15
ROWS = 13
WINDOW_WIDTH = COLS * CELL_SIZE
WINDOW_HEIGHT = ROWS * CELL_SIZE

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
WATER_BLUE = (20, 60, 140)
BROWN = (139, 69, 19)
GRAY = (100, 100, 100)
DARK_GRAY = (40, 40, 40)
YELLOW = (255, 255, 0)
LIGHT_GREEN = (100, 255, 100)
DARK_GREEN = (0, 80, 0)
SIDEWALK_COLOR = (60, 60, 60)
ROAD_COLOR = (50, 50, 50)
MEDIAN_COLOR = DARK_GREEN
GOAL_COLOR = (0, 60, 0)

# Row layout (0 = top)
ROW_GOAL = 0
ROW_RIVER_START = 1
ROW_RIVER_END = 4
ROW_MEDIAN = 5
ROW_ROAD_START = 6
ROW_ROAD_END = 10
ROW_START_SAFE = 11
ROW_FROG_START = 12

HOME_POSITIONS = [1, 4, 7, 10, 13]

# Task: Lane-based movement, moving platforms, multiple hazards
# Problem: River lanes with logs as moving platforms
RIVER_LANES = [
    {"row": 1, "dir": 1, "speed": 60, "count": 3, "min_len": 3, "max_len": 4},
    {"row": 2, "dir": -1, "speed": 80, "count": 2, "min_len": 4, "max_len": 5},
    {"row": 3, "dir": 1, "speed": 50, "count": 3, "min_len": 2, "max_len": 4},
    {"row": 4, "dir": -1, "speed": 70, "count": 2, "min_len": 3, "max_len": 5},
]

# Task: Multiple hazards - road lanes with cars moving at different speeds
ROAD_LANES = [
    {"row": 6, "dir": 1, "speed": 120, "count": 3, "length": 2},
    {"row": 7, "dir": -1, "speed": 150, "count": 2, "length": 2},
    {"row": 8, "dir": 1, "speed": 100, "count": 3, "length": 3},
    {"row": 9, "dir": -1, "speed": 180, "count": 2, "length": 2},
    {"row": 10, "dir": 1, "speed": 140, "count": 3, "length": 2},
]

INITIAL_LIVES = 5
TIME_LIMIT = 30.0


class Log:
    def __init__(self, x, row, width_px, direction, speed, cell_size):
        self.x = x
        self.row = row
        self.width = width_px
        self.direction = direction
        self.speed = speed
        self.cell_size = cell_size

    @property
    def y(self):
        return self.row * self.cell_size

    def update(self, dt):
        self.x += self.direction * self.speed * dt
        if self.direction > 0 and self.x > WINDOW_WIDTH:
            self.x = -self.width
        elif self.direction < 0 and self.x + self.width < 0:
            self.x = WINDOW_WIDTH

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.cell_size)

    def draw(self, surface):
        rect = self.get_rect()
        pygame.draw.rect(surface, BROWN, rect)
        pygame.draw.rect(surface, DARK_GRAY, rect, 1)


CAR_COLORS = [RED, (200, 100, 0), YELLOW, (255, 100, 100), (150, 50, 200)]


class Car:
    def __init__(self, x, row, width_px, direction, speed, color, cell_size):
        self.x = x
        self.row = row
        self.width = width_px
        self.direction = direction
        self.speed = speed
        self.color = color
        self.cell_size = cell_size

    @property
    def y(self):
        return self.row * self.cell_size

    def update(self, dt):
        self.x += self.direction * self.speed * dt
        if self.direction > 0 and self.x > WINDOW_WIDTH:
            self.x = -self.width
        elif self.direction < 0 and self.x + self.width < 0:
            self.x = WINDOW_WIDTH

    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.cell_size)

    def draw(self, surface):
        rect = self.get_rect()
        pygame.draw.rect(surface, self.color, rect)
        pygame.draw.rect(surface, BLACK, rect, 1)
        cabin_w = self.width * 0.5
        cabin_h = self.cell_size * 0.6
        cabin_x = self.x + (self.width - cabin_w) / 2
        cabin_y = self.y + (self.cell_size - cabin_h) / 2
        pygame.draw.rect(surface, WHITE, (cabin_x, cabin_y, cabin_w, cabin_h))


class Frog:
    def __init__(self, col, row, cell_size):
        self.col = col
        self.row = row
        self.cell_size = cell_size
        self.x = col * cell_size + cell_size // 2
        self.y = row * cell_size + cell_size // 2
        self.alive = True
        self.on_log = None
        self.facing = 0

    def move_up(self, max_row=0):
        if self.row > max_row:
            self.row -= 1
            self.y = self.row * self.cell_size + self.cell_size // 2
            self.facing = 0

    def move_down(self, max_row=ROWS - 1):
        if self.row < max_row:
            self.row += 1
            self.y = self.row * self.cell_size + self.cell_size // 2
            self.facing = 2

    def move_left(self, min_col=0):
        if self.col > min_col:
            self.col -= 1
            self.x = self.col * self.cell_size + self.cell_size // 2
            self.facing = 3

    def move_right(self, max_col=COLS - 1):
        if self.col < max_col:
            self.col += 1
            self.x = self.col * self.cell_size + self.cell_size // 2
            self.facing = 1

    def get_rect(self):
        margin = 4
        return pygame.Rect(
            self.x - self.cell_size // 2 + margin,
            self.y - self.cell_size // 2 + margin,
            self.cell_size - margin * 2,
            self.cell_size - margin * 2,
        )

    def draw(self, surface):
        rect = self.get_rect()
        pygame.draw.ellipse(surface, GREEN, rect)
        eye_size = 4
        eye_offset = 5
        cx, cy = rect.centerx, rect.centery
        if self.facing == 0:
            lx, ly = cx - eye_offset, rect.top + 4
            rx, ry = cx + eye_offset, rect.top + 4
        elif self.facing == 2:
            lx, ly = cx - eye_offset, rect.bottom - 4
            rx, ry = cx + eye_offset, rect.bottom - 4
        elif self.facing == 3:
            lx, ly = rect.left + 4, cy - eye_offset
            rx, ry = rect.left + 4, cy + eye_offset
        else:
            lx, ly = rect.right - 4, cy - eye_offset
            rx, ry = rect.right - 4, cy + eye_offset
        pygame.draw.circle(surface, WHITE, (lx, ly), eye_size)
        pygame.draw.circle(surface, WHITE, (rx, ry), eye_size)
        pygame.draw.circle(surface, BLACK, (lx, ly), 2)
        pygame.draw.circle(surface, BLACK, (rx, ry), 2)

    def reset_position(self, col, row):
        self.col = col
        self.row = row
        self.x = col * self.cell_size + self.cell_size // 2
        self.y = row * self.cell_size + self.cell_size // 2
        self.alive = True
        self.on_log = None


class Game:
    def __init__(self, args):
        # Constraint: 使用logger輸出訊息
        self.logger = logging.getLogger("Frogger")
        self.logger.setLevel(getattr(logging, args.log_level.upper(), logging.INFO))
        self.cell_size = args.cell_size
        self.cols = args.cols
        self.rows = args.rows
        self.window_width = self.cols * self.cell_size
        self.window_height = self.rows * self.cell_size
        self.lives = args.lives
        self.time_limit = args.time_limit
        self.score = 0
        self.game_over = False
        self.won = False
        self.time_remaining = self.time_limit
        self.filled_homes = [False] * len(HOME_POSITIONS)
        self.move_cooldown = 0.0
        self.move_delay = 0.15

        pygame.init()
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        self.big_font = pygame.font.Font(None, 36)
        self.running = True

        # Constraint: 使用Pygame - 初始化移動平台
        self.logs = []
        for lane in RIVER_LANES:
            row = lane["row"]
            direction = lane["dir"]
            speed = lane["speed"]
            count = lane["count"]
            min_len = lane["min_len"]
            max_len = lane["max_len"]
            spacing = WINDOW_WIDTH / count
            for i in range(count):
                length = random.randint(min_len, max_len) * self.cell_size
                x = i * spacing + random.uniform(0, spacing * 0.3)
                if x + length > WINDOW_WIDTH:
                    x = WINDOW_WIDTH - length
                self.logs.append(Log(x, row, length, direction, speed, self.cell_size))

        # Constraint: 使用Pygame - 初始化障礙物
        self.cars = []
        for lane in ROAD_LANES:
            row = lane["row"]
            direction = lane["dir"]
            speed = lane["speed"]
            count = lane["count"]
            car_length = lane["length"]
            color = random.choice(CAR_COLORS)
            spacing = WINDOW_WIDTH / count
            for i in range(count):
                width_px = car_length * self.cell_size
                x = i * spacing + random.uniform(0, spacing * 0.5)
                if x + width_px > WINDOW_WIDTH:
                    x = WINDOW_WIDTH - width_px
                self.cars.append(Car(x, row, width_px, direction, speed, color, self.cell_size))

        self.frog = Frog(HOME_POSITIONS[2], ROW_FROG_START, self.cell_size)
        self.start_col = self.frog.col
        self.start_row = self.frog.row

        # Constraint: 使用logger輸出訊息
        self.logger.info(
            "Game initialized: %dx%d grid, cell=%dpx, lives=%d, time=%.1fs",
            self.cols, self.rows, self.cell_size, self.lives, self.time_limit,
        )

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_r and (self.game_over or self.won):
                    self.reset_game()
                elif not self.game_over and not self.won and self.move_cooldown <= 0:
                    if event.key == pygame.K_UP:
                        self.frog.move_up()
                        self.move_cooldown = self.move_delay
                        self.logger.debug("Frog moved to (%d, %d)", self.frog.col, self.frog.row)
                    elif event.key == pygame.K_DOWN:
                        self.frog.move_down()
                        self.move_cooldown = self.move_delay
                        self.logger.debug("Frog moved to (%d, %d)", self.frog.col, self.frog.row)
                    elif event.key == pygame.K_LEFT:
                        self.frog.move_left()
                        self.move_cooldown = self.move_delay
                        self.logger.debug("Frog moved to (%d, %d)", self.frog.col, self.frog.row)
                    elif event.key == pygame.K_RIGHT:
                        self.frog.move_right()
                        self.move_cooldown = self.move_delay
                        self.logger.debug("Frog moved to (%d, %d)", self.frog.col, self.frog.row)

    def reset_game(self):
        self.logger.info("Game reset")
        self.lives = INITIAL_LIVES
        self.score = 0
        self.game_over = False
        self.won = False
        self.time_remaining = self.time_limit
        self.filled_homes = [False] * len(HOME_POSITIONS)
        self.frog.reset_position(self.start_col, self.start_row)

    def respawn_frog(self):
        self.lives -= 1
        self.logger.debug("Frog died. Lives left: %d", self.lives)
        if self.lives <= 0:
            self.game_over = True
            self.logger.info("Game over - no lives")
        else:
            self.time_remaining = self.time_limit
            self.frog.reset_position(self.start_col, self.start_row)

    def _check_river(self):
        if not (ROW_RIVER_START <= self.frog.row <= ROW_RIVER_END):
            self.frog.on_log = None
            return True
        frog_rect = self.frog.get_rect()
        for log in self.logs:
            if log.row == self.frog.row and frog_rect.colliderect(log.get_rect()):
                self.frog.on_log = log
                return True
        self.logger.debug("Frog drowned at row %d", self.frog.row)
        self.respawn_frog()
        return False

    def _check_road(self):
        if not (ROW_ROAD_START <= self.frog.row <= ROW_ROAD_END):
            return True
        frog_rect = self.frog.get_rect()
        for car in self.cars:
            if car.row == self.frog.row and frog_rect.colliderect(car.get_rect()):
                self.logger.debug("Frog hit by car at row %d", self.frog.row)
                self.respawn_frog()
                return False
        return True

    def _check_goal(self):
        if self.frog.row != ROW_GOAL:
            return
        for i, home_col in enumerate(HOME_POSITIONS):
            if self.frog.col == home_col and not self.filled_homes[i]:
                self.filled_homes[i] = True
                self.score += 100
                self.logger.info("Home %d filled! Score: %d", i + 1, self.score)
                if all(self.filled_homes):
                    self.won = True
                    self.logger.info("All homes filled! Win!")
                else:
                    self.time_remaining = self.time_limit
                    self.frog.reset_position(self.start_col, self.start_row)
                return

    def _ride_log(self, dt):
        log = self.frog.on_log
        self.frog.x += log.direction * log.speed * dt
        frog_rect = self.frog.get_rect()
        on_log = False
        for other in self.logs:
            if other.row == self.frog.row and frog_rect.colliderect(other.get_rect()):
                self.frog.on_log = other
                on_log = True
                break
        if not on_log:
            self.logger.debug("Frog fell off log at row %d", self.frog.row)
            self.respawn_frog()
            return False
        self.frog.col = round((self.frog.x - self.cell_size // 2) / self.cell_size)
        self.frog.col = max(0, min(self.cols - 1, self.frog.col))
        if self.frog.x - self.cell_size // 2 < 0 or self.frog.x + self.cell_size // 2 > self.window_width:
            self.logger.debug("Frog went off screen edge")
            self.respawn_frog()
            return False
        return True

    def update(self, dt):
        if self.game_over or self.won:
            return
        self.move_cooldown = max(0, self.move_cooldown - dt)
        for log in self.logs:
            log.update(dt)
        for car in self.cars:
            car.update(dt)

        if self.frog.on_log is not None:
            if not self._ride_log(dt):
                return

        self.time_remaining -= dt
        if self.time_remaining <= 0:
            self.logger.debug("Time expired")
            self.respawn_frog()
            return

        if not self._check_river():
            return
        if not self._check_road():
            return
        self._check_goal()

    def _draw_lane(self, row, color):
        pygame.draw.rect(self.screen, color, (0, row * self.cell_size, self.window_width, self.cell_size))

    def draw(self):
        self.screen.fill(BLACK)
        self._draw_lane(ROW_GOAL, GOAL_COLOR)
        for r in range(ROW_RIVER_START, ROW_RIVER_END + 1):
            self._draw_lane(r, WATER_BLUE)
        self._draw_lane(ROW_MEDIAN, MEDIAN_COLOR)
        for r in range(ROW_ROAD_START, ROW_ROAD_END + 1):
            self._draw_lane(r, ROAD_COLOR)
            for c in range(0, self.window_width, self.cell_size * 2):
                pygame.draw.rect(self.screen, YELLOW, (c, r * self.cell_size + self.cell_size // 2 - 1, self.cell_size, 2))
        for r in range(ROW_START_SAFE, self.rows):
            self._draw_lane(r, SIDEWALK_COLOR)

        for i, col in enumerate(HOME_POSITIONS):
            x = col * self.cell_size
            rect = pygame.Rect(x, 0, self.cell_size, self.cell_size)
            if self.filled_homes[i]:
                pygame.draw.rect(self.screen, LIGHT_GREEN, rect)
                pygame.draw.circle(self.screen, GREEN, rect.center, self.cell_size // 4)
            else:
                pygame.draw.rect(self.screen, DARK_GREEN, rect, 2)

        for log in self.logs:
            log.draw(self.screen)
        for car in self.cars:
            car.draw(self.screen)
        if self.frog.alive and not self.game_over and not self.won:
            self.frog.draw(self.screen)

        score_surf = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_surf, (10, 10))
        lives_surf = self.font.render(f"Lives: {self.lives}", True, WHITE)
        self.screen.blit(lives_surf, (10, 30))
        time_surf = self.font.render(f"Time: {max(0, int(self.time_remaining))}", True, WHITE)
        self.screen.blit(time_surf, (10, 50))

        if self.game_over:
            msg = self.big_font.render("Game Over! (R to restart, ESC to quit)", True, RED)
            msg_rect = msg.get_rect(center=(self.window_width // 2, self.window_height // 2))
            self.screen.blit(msg, msg_rect)
        elif self.won:
            msg = self.big_font.render("You Win! (R to restart, ESC to quit)", True, GREEN)
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
    parser.add_argument("--cell-size", type=int, default=CELL_SIZE, help="Cell size in pixels (default: %(default)s)")
    parser.add_argument("--cols", type=int, default=COLS, help="Grid columns (default: %(default)s)")
    parser.add_argument("--rows", type=int, default=ROWS, help="Grid rows (default: %(default)s)")
    parser.add_argument("--lives", type=int, default=INITIAL_LIVES, help="Number of lives (default: %(default)s)")
    parser.add_argument("--time-limit", type=float, default=TIME_LIMIT, help="Time per frog in seconds (default: %(default)s)")
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
