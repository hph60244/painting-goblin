import argparse
import logging
import math
import random
import sys

import pygame

WINDOW_TITLE = "Bubble Shooter"
FPS = 60

COLS = 10
ROWS_VISIBLE = 12
BUBBLE_RADIUS = 20
BUBBLE_DIAMETER = BUBBLE_RADIUS * 2
HEX_X_STEP = BUBBLE_DIAMETER
HEX_Y_STEP = int(BUBBLE_RADIUS * 1.732)

SHOOT_SPEED = 12.0

COLORS = [
    (255, 50, 50),
    (50, 200, 50),
    (50, 130, 255),
    (255, 255, 50),
    (255, 130, 50),
    (200, 50, 255),
]

BG_COLOR = (20, 20, 30)
GRID_COLOR = (40, 40, 60)
AIM_LINE_COLOR = (255, 255, 255, 80)
NEXT_BUBBLE_BORDER = (200, 200, 200)


def hex_position(row, col):
    x = col * HEX_X_STEP + (HEX_X_STEP // 2 if row % 2 == 1 else 0)
    y = row * HEX_Y_STEP + BUBBLE_RADIUS
    return x, y


def hex_neighbors(r, c):
    parity = r % 2
    if parity == 0:
        offsets = [(-1, -1), (-1, 0), (0, -1), (0, 1), (1, -1), (1, 0)]
    else:
        offsets = [(-1, 0), (-1, 1), (0, -1), (0, 1), (1, 0), (1, 1)]
    neighbors = []
    for dr, dc in offsets:
        nr, nc = r + dr, c + dc
        if nr >= 0 and nc >= 0:
            neighbors.append((nr, nc))
    return neighbors


class BubbleGrid:
    def __init__(self, cols, rows_visible):
        self.cols = cols
        self.rows_visible = rows_visible
        self.cells = {}
        self.logger = logging.getLogger("BubbleShooter.Grid")

    def is_empty(self, r, c):
        return (r, c) not in self.cells

    def is_valid(self, r, c):
        col_count = self.cols if r % 2 == 0 else self.cols - 1
        return 0 <= r < self.rows_visible and 0 <= c < col_count

    def get(self, r, c):
        return self.cells.get((r, c))

    def place(self, r, c, color):
        self.cells[(r, c)] = color
        self.logger.info("Placed bubble at (%d,%d) color=%d", r, c, color)

    def remove(self, r, c):
        if (r, c) in self.cells:
            del self.cells[(r, c)]

    def find_match(self, r, c, color):
        visited = set()
        matched = set()
        stack = [(r, c)]
        while stack:
            cr, cc = stack.pop()
            if (cr, cc) in visited:
                continue
            visited.add((cr, cc))
            if self.get(cr, cc) == color:
                matched.add((cr, cc))
                for nr, nc in hex_neighbors(cr, cc):
                    if self.is_valid(nr, nc) and self.get(nr, nc) == color:
                        stack.append((nr, nc))
        return matched

    def find_floating(self):
        if not self.cells:
            return set()
        connected = set()
        stack = []
        for c in range(self.cols):
            if (0, c) in self.cells:
                stack.append((0, c))
        while stack:
            r, c = stack.pop()
            if (r, c) in connected:
                continue
            connected.add((r, c))
            for nr, nc in hex_neighbors(r, c):
                if self.is_valid(nr, nc) and (nr, nc) in self.cells and (nr, nc) not in connected:
                    stack.append((nr, nc))
        return set(self.cells.keys()) - connected

    def get_lowest_row(self):
        if not self.cells:
            return -1
        return max(r for r, _ in self.cells)

    def add_row_at_bottom(self):
        self.logger.info("Adding new row at bottom")
        new_cells = {}
        for (r, c), color in self.cells.items():
            if r + 1 < self.rows_visible:
                new_cells[(r + 1, c)] = color
        self.cells = new_cells


class BubbleShooter:
    def __init__(self, args):
        self.logger = logging.getLogger("BubbleShooter")
        self.logger.setLevel(getattr(logging, args.log_level.upper(), logging.INFO))

        self.cols = args.cols
        self.rows_visible = args.rows
        self.bubble_radius = args.bubble_radius
        self.num_colors = args.num_colors
        self.grid_bottom_advance_interval = args.advance_interval

        self.window_width = args.width or (self.cols * HEX_X_STEP + BUBBLE_RADIUS)
        self.window_height = args.height or (
            self.rows_visible * HEX_Y_STEP + 120
        )

        pygame.init()
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 24)
        self.font_small = pygame.font.Font(None, 18)
        self.running = True

        self.grid = BubbleGrid(self.cols, self.rows_visible)
        self.current_color = random.randrange(self.num_colors)
        self.next_color = random.randrange(self.num_colors)

        self.shooting = False
        self.shot_bubble = None
        self.aim_angle = -math.pi / 2

        self.score = 0
        self.game_over = False
        self.shots_fired = 0
        self.advance_counter = 0

        self._init_grid()
        self.logger.info(
            "Game initialized: %dx%d grid, radius=%d, colors=%d",
            self.cols, self.rows_visible, self.bubble_radius, self.num_colors,
        )

    def _init_grid(self):
        for row in range(min(5, self.rows_visible)):
            col_count = self.cols if row % 2 == 0 else self.cols - 1
            for col in range(col_count):
                color = random.randrange(self.num_colors)
                self.grid.place(row, col, color)

    def _random_color(self):
        return random.randrange(self.num_colors)

    def _next_shot_color(self):
        self.current_color = self.next_color
        self.next_color = random.randrange(self.num_colors)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_r and self.game_over:
                    self.reset_game()
            elif event.type == pygame.MOUSEMOTION:
                if not self.shooting and not self.game_over:
                    mx, my = event.pos
                    dx = mx - self.window_width // 2
                    dy = my - (self.window_height - 40)
                    if dy < 0:
                        self.aim_angle = math.atan2(dy, dx)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and not self.shooting and not self.game_over:
                    self._fire_bubble()

    def _fire_bubble(self):
        start_x = self.window_width // 2
        start_y = self.window_height - 40
        dx = math.cos(self.aim_angle)
        dy = math.sin(self.aim_angle)
        vx = dx * SHOOT_SPEED
        vy = dy * SHOOT_SPEED
        self.shot_bubble = {
            "x": start_x,
            "y": start_y,
            "vx": vx,
            "vy": vy,
            "color": self.current_color,
            "active": True,
        }
        self.shooting = True
        self.logger.debug("Fired bubble color=%d angle=%.2f", self.current_color, self.aim_angle)

    def _update_shot(self):
        if not self.shooting or self.shot_bubble is None:
            return

        b = self.shot_bubble
        b["x"] += b["vx"]
        b["y"] += b["vy"]

        if b["x"] - BUBBLE_RADIUS < 0:
            b["x"] = BUBBLE_RADIUS
            b["vx"] = -b["vx"]
        elif b["x"] + BUBBLE_RADIUS > self.window_width:
            b["x"] = self.window_width - BUBBLE_RADIUS
            b["vx"] = -b["vx"]

        if b["y"] < BUBBLE_RADIUS:
            b["y"] = BUBBLE_RADIUS
            self._land_bubble(b)
            return

        for (r, c), color in list(self.grid.cells.items()):
            gx, gy = hex_position(r, c)
            dx = b["x"] - gx
            dy = b["y"] - gy
            dist = math.sqrt(dx * dx + dy * dy)
            if dist < BUBBLE_RADIUS * 1.8:
                self._land_bubble(b)
                return

        if b["y"] > self.window_height:
            self.shooting = False
            self.shot_bubble = None

    def _land_bubble(self, b):
        self.shooting = False
        color = b["color"]

        best_dist = float("inf")
        best_pos = None
        for row in range(self.rows_visible):
            col_count = self.cols if row % 2 == 0 else self.cols - 1
            for col in range(col_count):
                if self.grid.is_empty(row, col):
                    gx, gy = hex_position(row, col)
                    dx = b["x"] - gx
                    dy = b["y"] - gy
                    dist = math.sqrt(dx * dx + dy * dy)
                    if dist < best_dist:
                        best_dist = dist
                        best_pos = (row, col)

        if best_pos is None:
            self.logger.warning("No valid landing position found")
            self.shot_bubble = None
            return

        row, col = best_pos
        self.grid.place(row, col, color)
        self.shots_fired += 1

        matched = self.grid.find_match(row, col, color)
        if len(matched) >= 3:
            for mr, mc in matched:
                self.grid.remove(mr, mc)
            pop_count = len(matched)
            self.score += pop_count * 10
            self.logger.info("Popped %d bubbles! Score=%d", pop_count, self.score)

            floating = self.grid.find_floating()
            if floating:
                for fr, fc in floating:
                    self.grid.remove(fr, fc)
                self.score += len(floating) * 20
                self.logger.info("Removed %d floating bubbles! Score=%d", len(floating), self.score)

        self.advance_counter += 1
        if self.advance_counter >= self.grid_bottom_advance_interval:
            self.advance_counter = 0
            self.grid.add_row_at_bottom()

        if self.grid.get_lowest_row() >= self.rows_visible - 1:
            self.game_over = True
            self.logger.info("Game over! Final score: %d", self.score)

        self._next_shot_color()
        self.shot_bubble = None

    def reset_game(self):
        self.logger.info("Game reset")
        self.grid = BubbleGrid(self.cols, self.rows_visible)
        self._init_grid()
        self.current_color = random.randrange(self.num_colors)
        self.next_color = random.randrange(self.num_colors)
        self.shooting = False
        self.shot_bubble = None
        self.score = 0
        self.game_over = False
        self.shots_fired = 0
        self.advance_counter = 0

    def draw_aim_line(self):
        if self.shooting or self.game_over:
            return
        start_x = self.window_width // 2
        start_y = self.window_height - 40
        end_x = start_x + math.cos(self.aim_angle) * 800
        end_y = start_y + math.sin(self.aim_angle) * 800

        surface = pygame.Surface((self.window_width, self.window_height), pygame.SRCALPHA)
        pygame.draw.line(surface, AIM_LINE_COLOR, (start_x, start_y), (end_x, end_y), 2)
        self.screen.blit(surface, (0, 0))

    def draw(self):
        self.screen.fill(BG_COLOR)
        self._draw_grid()
        self._draw_bubbles()
        self._draw_next_bubble()
        self._draw_ui()
        self.draw_aim_line()

        if self.shooting and self.shot_bubble:
            b = self.shot_bubble
            color = COLORS[b["color"]]
            pygame.draw.circle(self.screen, color, (int(b["x"]), int(b["y"])), BUBBLE_RADIUS)
            pygame.draw.circle(self.screen, (255, 255, 255), (int(b["x"]), int(b["y"])), BUBBLE_RADIUS, 2)

        if self.game_over:
            overlay = pygame.Surface((self.window_width, self.window_height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            self.screen.blit(overlay, (0, 0))
            go_text = self.font.render("GAME OVER", True, (255, 255, 255))
            go_rect = go_text.get_rect(center=(self.window_width // 2, self.window_height // 2 - 20))
            self.screen.blit(go_text, go_rect)
            restart_text = self.font_small.render("Press R to restart, ESC to quit", True, (255, 255, 255))
            restart_rect = restart_text.get_rect(center=(self.window_width // 2, self.window_height // 2 + 20))
            self.screen.blit(restart_text, restart_rect)

        pygame.display.flip()

    def _draw_grid(self):
        for row in range(self.rows_visible):
            col_count = self.cols if row % 2 == 0 else self.cols - 1
            for col in range(col_count):
                x, y = hex_position(row, col)
                pygame.draw.circle(self.screen, GRID_COLOR, (int(x), int(y)), BUBBLE_RADIUS, 1)

    def _draw_bubbles(self):
        for (r, c), color_idx in self.grid.cells.items():
            x, y = hex_position(r, c)
            color = COLORS[color_idx % len(COLORS)]
            pygame.draw.circle(self.screen, color, (int(x), int(y)), BUBBLE_RADIUS - 1)
            pygame.draw.circle(self.screen, (255, 255, 255), (int(x), int(y)), BUBBLE_RADIUS - 1, 1)
            hl_x = int(x - BUBBLE_RADIUS * 0.3)
            hl_y = int(y - BUBBLE_RADIUS * 0.3)
            hl_radius = int(BUBBLE_RADIUS * 0.25)
            pygame.draw.circle(self.screen, (255, 255, 255), (hl_x, hl_y), hl_radius)

    def _draw_next_bubble(self):
        bx = self.window_width - 60
        by = self.window_height - 60
        pygame.draw.circle(self.screen, NEXT_BUBBLE_BORDER, (bx, by), BUBBLE_RADIUS + 2, 2)
        color = COLORS[self.current_color % len(COLORS)]
        pygame.draw.circle(self.screen, color, (bx, by), BUBBLE_RADIUS)
        next_color = COLORS[self.next_color % len(COLORS)]
        nx = bx + 30
        ny = by - 10
        pygame.draw.circle(self.screen, next_color, (nx, ny), int(BUBBLE_RADIUS * 0.6))

    def _draw_ui(self):
        score_text = self.font.render(f"Score: {self.score}", True, (200, 200, 200))
        self.screen.blit(score_text, (10, self.window_height - 35))
        shots_text = self.font_small.render(f"Shots: {self.shots_fired}", True, (150, 150, 150))
        self.screen.blit(shots_text, (10, self.window_height - 18))

    def run(self):
        self.logger.info("Game started")
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()
            if not self.game_over:
                self._update_shot()
            self.draw()
        self.logger.info("Game ended")
        pygame.quit()
        sys.exit()


def parse_args(argv):
    parser = argparse.ArgumentParser(description=WINDOW_TITLE)
    parser.add_argument(
        "--cols", type=int, default=COLS,
        help="Number of columns (default: %(default)s)",
    )
    parser.add_argument(
        "--rows", type=int, default=ROWS_VISIBLE,
        help="Number of visible rows (default: %(default)s)",
    )
    parser.add_argument(
        "--bubble-radius", type=int, default=BUBBLE_RADIUS,
        help="Bubble radius in pixels (default: %(default)s)",
    )
    parser.add_argument(
        "--num-colors", type=int, default=4,
        help="Number of bubble colors (default: %(default)s)",
    )
    parser.add_argument(
        "--advance-interval", type=int, default=8,
        help="Shots before bottom row advances (default: %(default)s)",
    )
    parser.add_argument(
        "--width", type=int, default=None,
        help="Window width (default: auto)",
    )
    parser.add_argument(
        "--height", type=int, default=None,
        help="Window height (default: auto)",
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
    game = BubbleShooter(args)
    game.run()


if __name__ == "__main__":
    main()
