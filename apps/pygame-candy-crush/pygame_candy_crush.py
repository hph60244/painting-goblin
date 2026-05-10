import argparse
import logging
import random
import sys
import time

import pygame

WINDOW_TITLE = "Candy Crush"
FPS = 60

GRID_COLS = 8
GRID_ROWS = 8
CELL_SIZE = 60
CANDY_TYPES = 6

GRID_GAP = 4
BOARD_WIDTH = GRID_COLS * CELL_SIZE + (GRID_COLS + 1) * GRID_GAP
BOARD_HEIGHT = GRID_ROWS * CELL_SIZE + (GRID_ROWS + 1) * GRID_GAP
SCORE_HEIGHT = 60

WINDOW_WIDTH = BOARD_WIDTH
WINDOW_HEIGHT = BOARD_HEIGHT + SCORE_HEIGHT

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
DARK_GRAY = (50, 50, 50)
BG_COLOR = (30, 30, 40)
BOARD_BG = (40, 40, 55)
SELECTED_COLOR = (255, 255, 100)

CANDY_COLORS = [
    (255, 80, 80),
    (80, 200, 80),
    (80, 130, 255),
    (255, 200, 50),
    (200, 80, 255),
    (255, 140, 50),
]

CANDY_SYMBOLS = ["♥", "♦", "♣", "♠", "★", "●"]

SWAP_DURATION = 0.15
CASCADE_DELAY = 0.12


class Board:
    def __init__(self, cols, rows, candy_types):
        self.cols = cols
        self.rows = rows
        self.candy_types = candy_types
        self.grid = [[0] * cols for _ in range(rows)]
        self.score = 0

    def reset(self):
        self.fill_random()
        self.score = 0
        while True:
            matches = self.find_matches()
            if not matches:
                break
            self.remove_matches(matches)
            self.fill_random(from_top=True)

    def fill_random(self, from_top=False):
        for r in range(self.rows):
            for c in range(self.cols):
                if from_top or self.grid[r][c] == 0:
                    self.grid[r][c] = random.randint(1, self.candy_types)

    def find_matches(self):
        matched = set()
        for r in range(self.rows):
            for c in range(self.cols - 2):
                val = self.grid[r][c]
                if val and val == self.grid[r][c + 1] == self.grid[r][c + 2]:
                    end = c + 2
                    while end + 1 < self.cols and self.grid[r][end + 1] == val:
                        end += 1
                    for cc in range(c, end + 1):
                        matched.add((r, cc))
        for c in range(self.cols):
            for r in range(self.rows - 2):
                val = self.grid[r][c]
                if val and val == self.grid[r + 1][c] == self.grid[r + 2][c]:
                    end = r + 2
                    while end + 1 < self.rows and self.grid[end + 1][c] == val:
                        end += 1
                    for rr in range(r, end + 1):
                        matched.add((rr, c))
        return list(matched)

    def remove_matches(self, cells):
        for r, c in cells:
            self.grid[r][c] = 0
        self.score += len(cells) * 10 * max(1, len(cells) // 3 - 1)

    def apply_gravity(self):
        moves = []
        for c in range(self.cols):
            write_row = self.rows - 1
            for r in range(self.rows - 1, -1, -1):
                if self.grid[r][c] != 0:
                    if r != write_row:
                        moves.append((r, c, write_row, c))
                        self.grid[write_row][c] = self.grid[r][c]
                        self.grid[r][c] = 0
                    write_row -= 1
            empty_count = write_row + 1
            for r in range(empty_count):
                new_val = random.randint(1, self.candy_types)
                self.grid[r][c] = new_val
                moves.append(("new", c, r, c, new_val))
        return moves

    def swap(self, r1, c1, r2, c2):
        self.grid[r1][c1], self.grid[r2][c2] = self.grid[r2][c2], self.grid[r1][c1]

    def is_adjacent(self, r1, c1, r2, c2):
        return abs(r1 - r2) + abs(c1 - c2) == 1

    def get_empty_positions(self):
        empty = []
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] == 0:
                    empty.append((r, c))
        return empty


class Game:
    def __init__(self, args):
        self.logger = logging.getLogger("CandyCrush")
        self.logger.setLevel(getattr(logging, args.log_level.upper(), logging.INFO))
        self.cols = args.cols
        self.rows = args.rows
        self.candy_types = args.candy_types
        self.cell_size = args.cell_size
        self.gap = args.gap

        self.board_width = self.cols * self.cell_size + (self.cols + 1) * self.gap
        self.board_height = self.rows * self.cell_size + (self.rows + 1) * self.gap
        self.window_width = self.board_width
        self.window_height = self.board_height + SCORE_HEIGHT

        pygame.init()
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 28)
        self.score_font = pygame.font.Font(None, 24)
        self.running = True
        self.game_over = False

        self.board = Board(self.cols, self.rows, self.candy_types)
        self.board.reset()
        self.selected = None
        self.animating = False
        self.anim_start = 0.0
        self.anim_swap = None
        self.cascading = False
        self.cascade_matches = []
        self.cascade_timer = 0.0

        self.logger.info(
            "Game initialized: %dx%d grid, %d candy types, cell=%dpx, gap=%dpx",
            self.cols, self.rows, self.candy_types, self.cell_size, self.gap,
        )

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_r:
                    self.reset_game()
            elif event.type == pygame.MOUSEBUTTONDOWN and not self.animating and not self.cascading and not self.game_over:
                mx, my = event.pos
                if my < self.board_height:
                    col = (mx - self.gap) // (self.cell_size + self.gap)
                    row = (my - self.gap) // (self.cell_size + self.gap)
                    if 0 <= col < self.cols and 0 <= row < self.rows:
                        self.handle_click(row, col)

    def handle_click(self, row, col):
        if self.selected is None:
            self.selected = (row, col)
            self.logger.debug("Selected cell (%d, %d)", row, col)
        else:
            sr, sc = self.selected
            if (sr, sc) == (row, col):
                self.selected = None
            elif self.board.is_adjacent(sr, sc, row, col):
                self.logger.debug("Attempting swap (%d,%d) <-> (%d,%d)", sr, sc, row, col)
                self.selected = None
                self.try_swap(sr, sc, row, col)
            else:
                self.selected = (row, col)
                self.logger.debug("Re-selected cell (%d, %d)", row, col)

    def try_swap(self, r1, c1, r2, c2):
        self.board.swap(r1, c1, r2, c2)
        matches = self.board.find_matches()
        if matches:
            self.logger.info("Swap created %d matching cells, starting cascade", len(matches))
            self.animating = True
            self.anim_swap = (r1, c1, r2, c2)
            self.anim_start = time.time()
            self.cascading = True
            self.cascade_matches = matches
            self.cascade_timer = 0.0
        else:
            self.board.swap(r1, c1, r2, c2)
            self.logger.debug("Swap produced no match, reverted")

    def process_cascade(self, dt):
        if not self.cascading:
            return
        self.cascade_timer += dt
        if self.cascade_timer < SWAP_DURATION:
            return
        self.animating = False
        self.anim_swap = None

        if self.cascade_matches:
            self.board.remove_matches(self.cascade_matches)
            self.board.apply_gravity()
            self.cascade_matches = self.board.find_matches()
            if self.cascade_matches:
                self.cascade_timer = 0.0
                self.logger.debug("Cascade continues, %d new matches", len(self.cascade_matches))
            else:
                self.cascading = False
                self.logger.info("Cascade complete. Score: %d", self.board.score)
                if not self.has_valid_moves():
                    self.game_over = True
                    self.logger.info("No valid moves left. Game over!")
        else:
            self.cascading = False

    def has_valid_moves(self):
        for r in range(self.rows):
            for c in range(self.cols):
                for dr, dc in [(0, 1), (1, 0)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.rows and 0 <= nc < self.cols:
                        self.board.swap(r, c, nr, nc)
                        if self.board.find_matches():
                            self.board.swap(r, c, nr, nc)
                            return True
                        self.board.swap(r, c, nr, nc)
        return False

    def reset_game(self):
        self.logger.info("Game reset")
        self.board.reset()
        self.selected = None
        self.animating = False
        self.anim_swap = None
        self.cascading = False
        self.cascade_matches = []
        self.cascade_timer = 0.0
        self.game_over = False

    def get_cell_rect(self, row, col):
        x = self.gap + col * (self.cell_size + self.gap)
        y = self.gap + row * (self.cell_size + self.gap)
        return pygame.Rect(x, y, self.cell_size, self.cell_size)

    def draw_candy(self, surface, row, col, value, offset_x=0, offset_y=0):
        rect = self.get_cell_rect(row, col)
        rect.x += offset_x
        rect.y += offset_y
        color = CANDY_COLORS[(value - 1) % len(CANDY_COLORS)]
        cx, cy = rect.center
        radius = self.cell_size // 2 - 4

        if value == 1:
            pygame.draw.circle(surface, color, (cx, cy), radius)
            inner_radius = radius // 2
            inner_color = tuple(min(c + 60, 255) for c in color)
            pygame.draw.circle(surface, inner_color, (cx - 4, cy - 4), inner_radius)
        elif value == 2:
            points = [
                (cx, cy - radius),
                (cx + radius, cy),
                (cx, cy + radius),
                (cx - radius, cy),
            ]
            pygame.draw.polygon(surface, color, points)
        elif value == 3:
            points = []
            for i in range(6):
                angle = i * 60 - 30
                px = cx + radius * pygame.math.Vector2(1, 0).rotate(angle).x
                py = cy + radius * pygame.math.Vector2(1, 0).rotate(angle).y
                points.append((px, py))
            pygame.draw.polygon(surface, color, points)
        elif value == 4:
            rect_inner = pygame.Rect(0, 0, radius * 1.4, radius * 1.4)
            rect_inner.center = (cx, cy)
            pygame.draw.rect(surface, color, rect_inner, border_radius=3)
        elif value == 5:
            points = []
            for i in range(5):
                angle = i * 72 - 90
                px = cx + radius * pygame.math.Vector2(1, 0).rotate(angle).x
                py = cy + radius * pygame.math.Vector2(1, 0).rotate(angle).y
                points.append((px, py))
                angle2 = angle + 36
                inner_r = radius * 0.45
                px = cx + inner_r * pygame.math.Vector2(1, 0).rotate(angle2).x
                py = cy + inner_r * pygame.math.Vector2(1, 0).rotate(angle2).y
                points.append((px, py))
            pygame.draw.polygon(surface, color, points)
        elif value == 6:
            pygame.draw.ellipse(surface, color, rect.inflate(-8, -4))
            inner_ellipse = rect.inflate(-16, -10)
            inner_color = tuple(min(c + 40, 255) for c in color)
            pygame.draw.ellipse(surface, inner_color, inner_ellipse)

    def draw(self):
        self.screen.fill(BG_COLOR)

        board_rect = pygame.Rect(0, 0, self.board_width, self.board_height)
        pygame.draw.rect(self.screen, BOARD_BG, board_rect, border_radius=6)

        anim_offset_r = 0
        anim_offset_c = 0
        if self.animating and self.anim_swap and self.cascading:
            elapsed = time.time() - self.anim_start
            progress = min(elapsed / SWAP_DURATION, 1.0)
            progress = progress * progress * (3 - 2 * progress)
            r1, c1, r2, c2 = self.anim_swap
            dr = (r2 - r1) * (self.cell_size + self.gap) * progress
            dc = (c2 - c1) * (self.cell_size + self.gap) * progress
            anim_offset_r = dr
            anim_offset_c = dc

        for r in range(self.rows):
            for c in range(self.cols):
                val = self.board.grid[r][c]
                if val == 0:
                    continue
                ofs_x, ofs_y = 0, 0
                if self.animating and self.anim_swap:
                    r1, c1, r2, c2 = self.anim_swap
                    if (r, c) == (r1, c1):
                        ofs_x = anim_offset_c
                        ofs_y = anim_offset_r
                    elif (r, c) == (r2, c2):
                        ofs_x = -anim_offset_c
                        ofs_y = -anim_offset_r
                self.draw_candy(self.screen, r, c, val, ofs_x, ofs_y)

        if self.selected is not None:
            sr, sc = self.selected
            rect = self.get_cell_rect(sr, sc)
            pygame.draw.rect(self.screen, SELECTED_COLOR, rect, 3, border_radius=4)

        score_text = self.score_font.render(f"Score: {self.board.score}", True, WHITE)
        self.screen.blit(score_text, (10, self.board_height + 18))

        if self.game_over:
            overlay = pygame.Surface((self.window_width, self.window_height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            self.screen.blit(overlay, (0, 0))

            go_text = self.font.render("No Moves Left!", True, WHITE)
            go_rect = go_text.get_rect(center=(self.window_width // 2, self.window_height // 2 - 20))
            self.screen.blit(go_text, go_rect)

            restart_text = self.score_font.render("Press R to restart, ESC to quit", True, WHITE)
            restart_rect = restart_text.get_rect(center=(self.window_width // 2, self.window_height // 2 + 20))
            self.screen.blit(restart_text, restart_rect)

        pygame.display.flip()

    def run(self):
        self.logger.info("Game started")
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            self.handle_events()
            if self.cascading:
                self.process_cascade(dt)
            self.draw()
        self.logger.info("Game ended")
        pygame.quit()
        sys.exit()


def parse_args(argv):
    parser = argparse.ArgumentParser(description=WINDOW_TITLE)
    parser.add_argument(
        "--cols", type=int, default=GRID_COLS,
        help="Grid columns (default: %(default)s)",
    )
    parser.add_argument(
        "--rows", type=int, default=GRID_ROWS,
        help="Grid rows (default: %(default)s)",
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
        "--candy-types", type=int, default=CANDY_TYPES,
        help="Number of candy types (default: %(default)s)",
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
