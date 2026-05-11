import argparse
import logging
import sys
import random

import pygame

WINDOW_TITLE = "Bejeweled"
FPS = 60

GRID_COLS = 8
GRID_ROWS = 8
CELL_SIZE = 60
GRID_GAP = 4
NUM_GEM_TYPES = 6

GRID_PIXEL_WIDTH = GRID_COLS * CELL_SIZE + (GRID_COLS + 1) * GRID_GAP
GRID_PIXEL_HEIGHT = GRID_ROWS * CELL_SIZE + (GRID_ROWS + 1) * GRID_GAP
PANEL_WIDTH = 160
WINDOW_WIDTH = GRID_PIXEL_WIDTH + PANEL_WIDTH
WINDOW_HEIGHT = GRID_PIXEL_HEIGHT + 20

SCORE_3 = 30
SCORE_4 = 60
SCORE_5 = 120

BG_COLOR = (30, 30, 40)
GRID_BG = (40, 40, 55)
PANEL_BG = (35, 35, 50)
WHITE = (255, 255, 255)
GRAY = (180, 180, 180)
SELECTED_BORDER = (255, 255, 100)

GEM_COLORS = [
    (255, 80, 80),
    (80, 200, 80),
    (80, 130, 255),
    (255, 220, 60),
    (200, 80, 255),
    (255, 140, 50),
]

GEM_SHAPES = ["circle", "diamond", "square", "triangle", "star", "hexagon"]


def draw_gem_shape(surface, color, center_x, center_y, size, shape):
    if shape == "circle":
        pygame.draw.circle(surface, color, (center_x, center_y), size // 2 - 2)
        highlight = tuple(min(255, c + 60) for c in color)
        pygame.draw.circle(surface, highlight, (center_x - 2, center_y - 2), size // 4)
    elif shape == "diamond":
        half = size // 2 - 1
        points = [
            (center_x, center_y - half),
            (center_x + half, center_y),
            (center_x, center_y + half),
            (center_x - half, center_y),
        ]
        pygame.draw.polygon(surface, color, points)
    elif shape == "square":
        rect = pygame.Rect(
            center_x - size // 2 + 2,
            center_y - size // 2 + 2,
            size - 4,
            size - 4,
        )
        pygame.draw.rect(surface, color, rect, border_radius=4)
    elif shape == "triangle":
        half = size // 2 - 1
        points = [
            (center_x, center_y - half),
            (center_x + half, center_y + half),
            (center_x - half, center_y + half),
        ]
        pygame.draw.polygon(surface, color, points)
    elif shape == "star":
        cx, cy = center_x, center_y
        outer_r = size // 2 - 2
        inner_r = outer_r // 2
        points = []
        for i in range(10):
            angle = -90 + i * 36
            rad = outer_r if i % 2 == 0 else inner_r
            import math
            points.append((
                cx + rad * math.cos(math.radians(angle)),
                cy + rad * math.sin(math.radians(angle)),
            ))
        pygame.draw.polygon(surface, color, points)
    elif shape == "hexagon":
        cx, cy = center_x, center_y
        r = size // 2 - 2
        points = []
        for i in range(6):
            angle = 30 + i * 60
            import math
            points.append((
                cx + r * math.cos(math.radians(angle)),
                cy + r * math.sin(math.radians(angle)),
            ))
        pygame.draw.polygon(surface, color, points)


class Board:
    def __init__(self, cols, rows, num_types):
        self.cols = cols
        self.rows = rows
        self.num_types = num_types
        self.gems = [[0] * cols for _ in range(rows)]
        self.score = 0
        self._fill_no_matches()

    def _random_gem(self):
        return random.randint(0, self.num_types - 1)

    def _get_matches(self):
        matched = set()
        for r in range(self.rows):
            c = 0
            while c < self.cols:
                val = self.gems[r][c]
                if val < 0:
                    c += 1
                    continue
                end = c + 1
                while end < self.cols and self.gems[r][end] == val:
                    end += 1
                if end - c >= 3:
                    for mc in range(c, end):
                        matched.add((r, mc))
                c = end
        for c in range(self.cols):
            r = 0
            while r < self.rows:
                val = self.gems[r][c]
                if val < 0:
                    r += 1
                    continue
                end = r + 1
                while end < self.rows and self.gems[end][c] == val:
                    end += 1
                if end - r >= 3:
                    for mr in range(r, end):
                        matched.add((mr, c))
                r = end
        return matched

    def _fill_no_matches(self):
        for r in range(self.rows):
            for c in range(self.cols):
                self.gems[r][c] = self._random_gem()
        while self._get_matches():
            for r in range(self.rows):
                for c in range(self.cols):
                    self.gems[r][c] = self._random_gem()

    def has_valid_moves(self):
        for r in range(self.rows):
            for c in range(self.cols):
                for dr, dc in [(0, 1), (1, 0)]:
                    nr, nc = r + dr, c + dc
                    if nr >= self.rows or nc >= self.cols:
                        continue
                    self.gems[r][c], self.gems[nr][nc] = self.gems[nr][nc], self.gems[r][c]
                    has_match = bool(self._get_matches())
                    self.gems[r][c], self.gems[nr][nc] = self.gems[nr][nc], self.gems[r][c]
                    if has_match:
                        return True
        return False

    def swap(self, r1, c1, r2, c2):
        self.gems[r1][c1], self.gems[r2][c2] = self.gems[r2][c2], self.gems[r1][c1]

    def process_matches(self):
        total_score = 0
        any_matched = False
        while True:
            matches = self._get_matches()
            if not matches:
                break
            any_matched = True
            match_count = len(matches)
            if match_count >= 5:
                total_score += SCORE_5
            elif match_count >= 4:
                total_score += SCORE_4
            else:
                total_score += SCORE_3
            for r, c in matches:
                self.gems[r][c] = -1
            self._apply_gravity()
            self._fill_empty()
        if any_matched:
            self.score += total_score
        return any_matched

    def _apply_gravity(self):
        for c in range(self.cols):
            write_row = self.rows - 1
            for r in range(self.rows - 1, -1, -1):
                if self.gems[r][c] >= 0:
                    self.gems[write_row][c] = self.gems[r][c]
                    write_row -= 1
            for r in range(write_row, -1, -1):
                self.gems[r][c] = -1

    def _fill_empty(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.gems[r][c] < 0:
                    self.gems[r][c] = self._random_gem()

    def is_adjacent(self, r1, c1, r2, c2):
        return abs(r1 - r2) + abs(c1 - c2) == 1


class Game:
    def __init__(self, args):
        self.logger = logging.getLogger("bejeweled")
        self.logger.setLevel(getattr(logging, args.log_level.upper(), logging.INFO))
        self.cell_size = args.cell_size
        self.gap = args.gap
        self.cols = args.cols
        self.rows = args.rows
        self.num_types = args.num_types
        self.grid_width = self.cols * self.cell_size + (self.cols + 1) * self.gap
        self.grid_height = self.rows * self.cell_size + (self.rows + 1) * self.gap
        self.panel_width = args.panel_width
        self.window_width = self.grid_width + self.panel_width
        self.window_height = max(self.grid_height + 20, self.grid_height)
        self.game_over = False

        pygame.init()
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock = pygame.time.Clock()
        self.font_small = pygame.font.Font(None, 22)
        self.font_medium = pygame.font.Font(None, 28)
        self.font_large = pygame.font.Font(None, 36)
        self.running = True

        self.board = Board(self.cols, self.rows, self.num_types)
        self.selected = None
        self.logger.info(
            "Game initialized: %dx%d grid, %d gem types, cell=%dpx",
            self.cols, self.rows, self.num_types, self.cell_size,
        )

    def _grid_to_pixel(self, row, col):
        x = self.gap + col * (self.cell_size + self.gap)
        y = self.gap + row * (self.cell_size + self.gap)
        return x, y

    def _pixel_to_grid(self, px, py):
        col = (px - self.gap) // (self.cell_size + self.gap)
        row = (py - self.gap) // (self.cell_size + self.gap)
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return row, col
        return None

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_r and self.game_over:
                    self.reset_game()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if self.game_over:
                    continue
                pos = self._pixel_to_grid(event.pos[0], event.pos[1])
                if pos is None:
                    continue
                row, col = pos
                if self.selected is None:
                    self.selected = (row, col)
                    self.logger.debug("Selected gem at (%d, %d)", row, col)
                else:
                    sr, sc = self.selected
                    if (row, col) == (sr, sc):
                        self.selected = None
                    elif self.board.is_adjacent(sr, sc, row, col):
                        self.logger.debug("Swapping (%d,%d) <-> (%d,%d)", sr, sc, row, col)
                        self.board.swap(sr, sc, row, col)
                        if self.board.process_matches():
                            self.logger.info(
                                "Swap successful. Score: %d", self.board.score
                            )
                            if not self.board.has_valid_moves():
                                self.game_over = True
                                self.logger.info(
                                    "Game over! Final score: %d", self.board.score
                                )
                        else:
                            self.board.swap(sr, sc, row, col)
                            self.logger.debug("Invalid swap, reverting")
                        self.selected = None
                    else:
                        self.selected = (row, col)

    def reset_game(self):
        self.logger.info("Game reset")
        self.board = Board(self.cols, self.rows, self.num_types)
        self.selected = None
        self.game_over = False

    def draw_gem(self, surface, value, x, y):
        rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
        color = GEM_COLORS[value % len(GEM_COLORS)]
        shape = GEM_SHAPES[value % len(GEM_SHAPES)]
        cx = x + self.cell_size // 2
        cy = y + self.cell_size // 2
        draw_gem_shape(surface, color, cx, cy, self.cell_size, shape)

    def draw(self):
        self.screen.fill(BG_COLOR)
        grid_rect = pygame.Rect(0, 0, self.grid_width, self.grid_height)
        pygame.draw.rect(self.screen, GRID_BG, grid_rect, border_radius=6)

        grid_x = 0
        grid_y = 0
        for r in range(self.rows):
            for c in range(self.cols):
                x = grid_x + self.gap + c * (self.cell_size + self.gap)
                y = grid_y + self.gap + r * (self.cell_size + self.gap)
                val = self.board.gems[r][c]
                if val >= 0:
                    self.draw_gem(self.screen, val, x, y)

        if self.selected is not None:
            sr, sc = self.selected
            sx = grid_x + self.gap + sc * (self.cell_size + self.gap)
            sy = grid_y + self.gap + sr * (self.cell_size + self.gap)
            border_rect = pygame.Rect(sx - 2, sy - 2, self.cell_size + 4, self.cell_size + 4)
            pygame.draw.rect(self.screen, SELECTED_BORDER, border_rect, width=3, border_radius=6)

        panel_x = self.grid_width + 15
        panel_y = 15
        panel_rect = pygame.Rect(self.grid_width, 0, self.panel_width, self.window_height)
        pygame.draw.rect(self.screen, PANEL_BG, panel_rect)

        score_label = self.font_small.render("SCORE", True, GRAY)
        self.screen.blit(score_label, (panel_x, panel_y))

        score_val = self.font_large.render(str(self.board.score), True, WHITE)
        self.screen.blit(score_val, (panel_x, panel_y + 22))

        help_y = panel_y + 80
        help_lines = [
            "Click a gem to",
            "select it,",
            "then click an",
            "adjacent gem",
            "to swap.",
            "",
            "Match 3+ gems",
            "in a row to",
            "score points!",
            "",
            "R: restart",
            "ESC: quit",
        ]
        for line in help_lines:
            text = self.font_small.render(line, True, GRAY)
            self.screen.blit(text, (panel_x, help_y))
            help_y += 20

        if self.game_over:
            overlay = pygame.Surface((self.window_width, self.window_height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            self.screen.blit(overlay, (0, 0))

            go_text = self.font_large.render("Game Over!", True, WHITE)
            go_rect = go_text.get_rect(center=(self.window_width // 2, self.window_height // 2 - 20))
            self.screen.blit(go_text, go_rect)

            restart_text = self.font_small.render("Press R to restart, ESC to quit", True, WHITE)
            restart_rect = restart_text.get_rect(
                center=(self.window_width // 2, self.window_height // 2 + 15)
            )
            self.screen.blit(restart_text, restart_rect)

        pygame.display.flip()

    def run(self):
        self.logger.info("Game started")
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()
            self.draw()
        self.logger.info("Game ended")
        pygame.quit()
        sys.exit()


def parse_args(argv):
    parser = argparse.ArgumentParser(description=WINDOW_TITLE)
    parser.add_argument(
        "--cols", type=int, default=GRID_COLS,
        help="Number of columns (default: %(default)s)",
    )
    parser.add_argument(
        "--rows", type=int, default=GRID_ROWS,
        help="Number of rows (default: %(default)s)",
    )
    parser.add_argument(
        "--cell-size", type=int, default=CELL_SIZE,
        help="Cell size in pixels (default: %(default)s)",
    )
    parser.add_argument(
        "--gap", type=int, default=GRID_GAP,
        help="Gap between cells in pixels (default: %(default)s)",
    )
    parser.add_argument(
        "--num-types", type=int, default=NUM_GEM_TYPES,
        help="Number of gem types (default: %(default)s)",
    )
    parser.add_argument(
        "--panel-width", type=int, default=PANEL_WIDTH,
        help="Side panel width in pixels (default: %(default)s)",
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
