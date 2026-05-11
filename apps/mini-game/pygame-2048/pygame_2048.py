import argparse
import logging
import sys
import random

import pygame

WINDOW_TITLE = "2048"
FPS = 60
CELL_SIZE = 100
GRID_SIZE = 4
GRID_GAP = 10
WINDOW_WIDTH = GRID_SIZE * CELL_SIZE + (GRID_SIZE + 1) * GRID_GAP
WINDOW_HEIGHT = WINDOW_WIDTH + 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (187, 173, 160)
DARK_GRAY = (100, 100, 100)
BG_COLOR = (250, 248, 239)
CELL_BG = (205, 193, 180)
GRID_BG = (187, 173, 160)

TILE_COLORS = {
    0: (205, 193, 180),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46),
}

TEXT_COLORS = {
    0: (205, 193, 180),
    2: (119, 110, 101),
    4: (119, 110, 101),
    8: (249, 246, 242),
    16: (249, 246, 242),
    32: (249, 246, 242),
    64: (249, 246, 242),
    128: (249, 246, 242),
    256: (249, 246, 242),
    512: (249, 246, 242),
    1024: (249, 246, 242),
    2048: (249, 246, 242),
}

DIRECTION_MAP = {
    pygame.K_UP: "up",
    pygame.K_DOWN: "down",
    pygame.K_LEFT: "left",
    pygame.K_RIGHT: "right",
}


class Grid:
    def __init__(self, size):
        self.size = size
        self.cells = [[0] * size for _ in range(size)]
        self.score = 0
        self.moved = False

    def reset(self):
        self.cells = [[0] * self.size for _ in range(self.size)]
        self.score = 0
        self.spawn_tile()
        self.spawn_tile()

    def get_empty_cells(self):
        empty = []
        for r in range(self.size):
            for c in range(self.size):
                if self.cells[r][c] == 0:
                    empty.append((r, c))
        return empty

    def spawn_tile(self):
        empty = self.get_empty_cells()
        if not empty:
            return False
        r, c = random.choice(empty)
        self.cells[r][c] = 2 if random.random() < 0.9 else 4
        return True

    def slide_row_left(self, row):
        new_row = [v for v in row if v != 0]
        merged = []
        skip = False
        row_score = 0
        for i in range(len(new_row)):
            if skip:
                skip = False
                continue
            if i + 1 < len(new_row) and new_row[i] == new_row[i + 1]:
                merged.append(new_row[i] * 2)
                row_score += new_row[i] * 2
                skip = True
            else:
                merged.append(new_row[i])
        merged += [0] * (self.size - len(merged))
        return merged, row_score

    def move(self, direction):
        self.moved = False
        old_cells = [row[:] for row in self.cells]
        rotation_count = {"up": 3, "down": 1, "left": 0, "right": 2}[direction]

        rotated = self._rotate_cw(self.cells, rotation_count)
        new_rows = []
        total_score = 0
        for row in rotated:
            new_row, row_score = self.slide_row_left(row)
            new_rows.append(new_row)
            total_score += row_score
        self.cells = self._rotate_cw(new_rows, (4 - rotation_count) % 4)
        self.score += total_score

        if old_cells != self.cells:
            self.moved = True

        return self.moved

    def _rotate_cw(self, matrix, times):
        result = matrix
        for _ in range(times):
            result = [list(reversed(col)) for col in zip(*result)]
        return result

    def can_merge(self):
        for r in range(self.size):
            for c in range(self.size):
                val = self.cells[r][c]
                if val == 0:
                    return True
                if c + 1 < self.size and self.cells[r][c + 1] == val:
                    return True
                if r + 1 < self.size and self.cells[r + 1][c] == val:
                    return True
        return False

    def has_won(self):
        for r in range(self.size):
            for c in range(self.size):
                if self.cells[r][c] >= 2048:
                    return True
        return False

    def get_max_tile(self):
        return max(max(row) for row in self.cells)


class Game:
    def __init__(self, args):
        self.logger = logging.getLogger("2048")
        self.logger.setLevel(getattr(logging, args.log_level.upper(), logging.INFO))
        self.grid_size = args.grid_size
        self.cell_size = args.cell_size
        self.gap = args.gap
        self.board_width = self.grid_size * self.cell_size + (self.grid_size + 1) * self.gap
        self.board_height = self.board_width
        self.window_width = self.board_width
        self.window_height = self.board_height + 60
        self.game_over = False
        self.won = False
        self.continued = False

        pygame.init()
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        self.running = True

        self.grid = Grid(self.grid_size)
        self.grid.reset()
        self.logger.info(
            "Game initialized: %dx%d grid, cell=%dpx, gap=%dpx",
            self.grid_size, self.grid_size, self.cell_size, self.gap,
        )

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_r and self.game_over:
                    self.reset_game()
                elif event.key == pygame.K_c and self.won and not self.continued:
                    self.continued = True
                    self.logger.info("Player chose to continue after reaching 2048")
                elif event.key in DIRECTION_MAP and not self.game_over:
                    direction = DIRECTION_MAP[event.key]
                    moved = self.grid.move(direction)
                    if moved:
                        self.logger.debug("Moved %s, score=%d", direction, self.grid.score)
                        self.grid.spawn_tile()
                        if not self.grid.can_merge():
                            self.game_over = True
                            self.logger.info("Game over! Final score: %d", self.grid.score)
                        elif self.grid.has_won() and not self.continued:
                            self.won = True
                            self.logger.info("Player reached 2048!")

    def reset_game(self):
        self.logger.info("Game reset")
        self.grid.reset()
        self.game_over = False
        self.won = False
        self.continued = False

    def draw_tile(self, surface, value, x, y):
        rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
        color = TILE_COLORS.get(value, (60, 58, 50))
        pygame.draw.rect(surface, color, rect, border_radius=5)

        if value != 0:
            text_color = TEXT_COLORS.get(value, (249, 246, 242))
            text_str = str(value)
            if value < 100:
                font = self.font_large
            elif value < 10000:
                font = self.font_medium
            else:
                font = self.font_small
            text = font.render(text_str, True, text_color)
            text_rect = text.get_rect(center=rect.center)
            surface.blit(text, text_rect)

    def draw(self):
        self.screen.fill(BG_COLOR)

        board_x = 0
        board_y = 0
        board_rect = pygame.Rect(board_x, board_y, self.board_width, self.board_height)
        pygame.draw.rect(self.screen, GRID_BG, board_rect, border_radius=8)

        for r in range(self.grid_size):
            for c in range(self.grid_size):
                x = board_x + self.gap + c * (self.cell_size + self.gap)
                y = board_y + self.gap + r * (self.cell_size + self.gap)
                self.draw_tile(self.screen, self.grid.cells[r][c], x, y)

        score_text = self.font_small.render(f"Score: {self.grid.score}", True, DARK_GRAY)
        self.screen.blit(score_text, (10, self.board_height + 15))

        max_tile_text = self.font_small.render(f"Max: {self.grid.get_max_tile()}", True, DARK_GRAY)
        max_tile_rect = max_tile_text.get_rect(right=self.window_width - 10, top=self.board_height + 15)
        self.screen.blit(max_tile_text, max_tile_rect)

        if self.won and not self.continued:
            overlay = pygame.Surface((self.window_width, self.window_height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            self.screen.blit(overlay, (0, 0))

            win_text = self.font_large.render("You Win!", True, WHITE)
            win_rect = win_text.get_rect(center=(self.window_width // 2, self.window_height // 2 - 20))
            self.screen.blit(win_text, win_rect)

            continue_text = self.font_small.render("Press C to continue, ESC to quit", True, WHITE)
            continue_rect = continue_text.get_rect(center=(self.window_width // 2, self.window_height // 2 + 20))
            self.screen.blit(continue_text, continue_rect)

        if self.game_over:
            overlay = pygame.Surface((self.window_width, self.window_height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            self.screen.blit(overlay, (0, 0))

            go_text = self.font_large.render("Game Over!", True, WHITE)
            go_rect = go_text.get_rect(center=(self.window_width // 2, self.window_height // 2 - 20))
            self.screen.blit(go_text, go_rect)

            restart_text = self.font_small.render("Press R to restart, ESC to quit", True, WHITE)
            restart_rect = restart_text.get_rect(center=(self.window_width // 2, self.window_height // 2 + 20))
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
        "--grid-size", type=int, default=GRID_SIZE,
        help="Grid size (NxN) (default: %(default)s)",
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
