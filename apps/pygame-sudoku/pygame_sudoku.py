import argparse
import logging
import random
import sys

import pygame

# Constraint: 使用Pygame - 適合製作2D遊戲原型
# Constraint: 用極簡風格呈現 - 強調玩法概念，節省製作時間
# Constraint: 使用logger輸出訊息 - 用於人類跟AI除錯

WINDOW_TITLE = "Sudoku"
FPS = 60
CELL_SIZE = 60
BOARD_SIZE = 9
WINDOW_SIZE = BOARD_SIZE * CELL_SIZE
INFO_HEIGHT = 40

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
DARK_GRAY = (100, 100, 100)
LIGHT_BLUE = (200, 220, 255)
RED = (200, 50, 50)
GREEN = (50, 180, 50)

# Difficulty presets: number of cells to remove (clues to leave)
# Constraint: Backtracking solver, puzzle generation
DIFFICULTY = {
    "easy": 30,
    "medium": 45,
    "hard": 52,
}


class SudokuBoard:
    def __init__(self):
        self.grid = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.fixed = [[False] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.notes = [[set() for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

    def copy(self):
        new_board = SudokuBoard()
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                new_board.grid[r][c] = self.grid[r][c]
                new_board.fixed[r][c] = self.fixed[r][c]
        return new_board

    def is_valid_move(self, row, col, num):
        for c in range(BOARD_SIZE):
            if self.grid[row][c] == num:
                return False
        for r in range(BOARD_SIZE):
            if self.grid[r][col] == num:
                return False
        box_r, box_c = (row // 3) * 3, (col // 3) * 3
        for r in range(box_r, box_r + 3):
            for c in range(box_c, box_c + 3):
                if self.grid[r][c] == num:
                    return False
        return True

    def is_complete(self):
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if self.grid[r][c] == 0:
                    return False
        return True

    def is_correct(self):
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                val = self.grid[r][c]
                if val == 0:
                    return False
                self.grid[r][c] = 0
                if not self.is_valid_move(r, c, val):
                    self.grid[r][c] = val
                    return False
                self.grid[r][c] = val
        return True

    def get_conflicts(self):
        conflicts = set()
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                val = self.grid[r][c]
                if val == 0:
                    continue
                self.grid[r][c] = 0
                if not self.is_valid_move(r, c, val):
                    conflicts.add((r, c))
                self.grid[r][c] = val
        return conflicts


class SudokuSolver:
    # Constraint: Backtracking solver, puzzle generation
    @staticmethod
    def solve(board):
        empty = SudokuSolver._find_empty(board.grid)
        if not empty:
            return True
        row, col = empty
        for num in random.sample(range(1, 10), 9):
            if board.is_valid_move(row, col, num):
                board.grid[row][col] = num
                if SudokuSolver.solve(board):
                    return True
                board.grid[row][col] = 0
        return False

    @staticmethod
    def _find_empty(grid):
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if grid[r][c] == 0:
                    return (r, c)
        return None

    @staticmethod
    def count_solutions(grid, limit=2):
        count = 0

        def helper(board):
            nonlocal count
            if count >= limit:
                return
            empty = SudokuSolver._find_empty(board)
            if not empty:
                count += 1
                return
            row, col = empty
            for num in range(1, 10):
                if count >= limit:
                    return
                valid = True
                for c in range(BOARD_SIZE):
                    if board[row][c] == num:
                        valid = False
                        break
                if not valid:
                    continue
                for r in range(BOARD_SIZE):
                    if board[r][col] == num:
                        valid = False
                        break
                if not valid:
                    continue
                box_r, box_c = (row // 3) * 3, (col // 3) * 3
                for r in range(box_r, box_r + 3):
                    for c in range(box_c, box_c + 3):
                        if board[r][c] == num:
                            valid = False
                            break
                    if not valid:
                        break
                if not valid:
                    continue
                board[row][col] = num
                helper(board)
                board[row][col] = 0

        helper([row[:] for row in grid])
        return count


class SudokuGenerator:
    # Constraint: Backtracking solver, puzzle generation
    @staticmethod
    def generate(clues_to_remove):
        logger = logging.getLogger("Sudoku.Generator")
        board = SudokuBoard()
        solver = SudokuSolver()
        solver.solve(board)
        logger.info("Generated complete board")
        cells = [(r, c) for r in range(BOARD_SIZE) for c in range(BOARD_SIZE)]
        random.shuffle(cells)
        removed = 0
        for r, c in cells:
            if removed >= clues_to_remove:
                break
            backup = board.grid[r][c]
            board.grid[r][c] = 0
            if SudokuSolver.count_solutions(board.grid, 2) == 1:
                removed += 1
                logger.debug("Removed cell (%d,%d): %d/%d", r, c, removed, clues_to_remove)
            else:
                board.grid[r][c] = backup
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if board.grid[r][c] != 0:
                    board.fixed[r][c] = True
        logger.info("Puzzle generated with %d clues", BOARD_SIZE * BOARD_SIZE - removed)
        return board


class Game:
    def __init__(self, args):
        self.logger = logging.getLogger("Sudoku")
        self.logger.setLevel(getattr(logging, args.log_level.upper(), logging.INFO))
        self.difficulty = args.difficulty
        self.clues_to_remove = DIFFICULTY.get(self.difficulty, 45)
        self.cell_size = args.cell_size
        self.window_size = BOARD_SIZE * self.cell_size
        self.font_size = self.cell_size // 2

        pygame.init()
        self.screen = pygame.display.set_mode(
            (self.window_size, self.window_size + INFO_HEIGHT)
        )
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.Font(None, self.font_size * 2)
        self.font_small = pygame.font.Font(None, self.font_size)
        self.running = True
        self.selected = None
        self.message = ""
        self.message_timer = 0

        self.board = SudokuGenerator.generate(self.clues_to_remove)
        self.conflicts = set()
        self.logger.info(
            "Game initialized: difficulty=%s, cell=%dpx",
            self.difficulty, self.cell_size,
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
                elif event.key == pygame.K_n:
                    self.new_game()
                elif self.selected and not self.board.fixed[self.selected[0]][self.selected[1]]:
                    if pygame.K_1 <= event.key <= pygame.K_9:
                        num = event.key - pygame.K_0
                        self.place_number(self.selected[0], self.selected[1], num)
                    elif event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                        self.place_number(self.selected[0], self.selected[1], 0)
                if event.key == pygame.K_UP:
                    self.move_selection(-1, 0)
                elif event.key == pygame.K_DOWN:
                    self.move_selection(1, 0)
                elif event.key == pygame.K_LEFT:
                    self.move_selection(0, -1)
                elif event.key == pygame.K_RIGHT:
                    self.move_selection(0, 1)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                if y < self.window_size:
                    col = x // self.cell_size
                    row = y // self.cell_size
                    self.selected = (row, col)

    def move_selection(self, dr, dc):
        if self.selected is None:
            self.selected = (0, 0)
            return
        r, c = self.selected
        r = max(0, min(BOARD_SIZE - 1, r + dr))
        c = max(0, min(BOARD_SIZE - 1, c + dc))
        self.selected = (r, c)

    def place_number(self, row, col, num):
        self.board.grid[row][col] = num
        self.conflicts = self.board.get_conflicts()
        self.logger.debug("Placed %d at (%d,%d)", num, row, col)

        if self.board.is_complete() and not self.conflicts:
            self.message = "Puzzle solved! Press N for new game"
            self.message_timer = 300
            self.logger.info("Puzzle solved!")

    def reset_game(self):
        self.logger.info("Game reset")
        self.board = SudokuGenerator.generate(self.clues_to_remove)
        self.selected = None
        self.conflicts = set()
        self.message = ""
        self.message_timer = 0

    def new_game(self):
        self.logger.info("New game")
        self.board = SudokuGenerator.generate(self.clues_to_remove)
        self.selected = None
        self.conflicts = set()
        self.message = ""
        self.message_timer = 0

    def draw(self):
        self.screen.fill(WHITE)

        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                rect = pygame.Rect(
                    c * self.cell_size,
                    r * self.cell_size,
                    self.cell_size,
                    self.cell_size,
                )
                if self.selected == (r, c):
                    pygame.draw.rect(self.screen, LIGHT_BLUE, rect)
                elif (r, c) in self.conflicts:
                    pygame.draw.rect(self.screen, (255, 220, 220), rect)
                val = self.board.grid[r][c]
                if val != 0:
                    color = BLACK if self.board.fixed[r][c] else DARK_GRAY
                    text = self.font_large.render(str(val), True, color)
                    text_rect = text.get_rect(center=rect.center)
                    self.screen.blit(text, text_rect)

        # Draw grid lines
        for i in range(BOARD_SIZE + 1):
            line_width = 3 if i % 3 == 0 else 1
            pygame.draw.line(
                self.screen, BLACK,
                (i * self.cell_size, 0),
                (i * self.cell_size, self.window_size),
                line_width,
            )
            pygame.draw.line(
                self.screen, BLACK,
                (0, i * self.cell_size),
                (self.window_size, i * self.cell_size),
                line_width,
            )

        # Info bar
        info_rect = pygame.Rect(0, self.window_size, self.window_size, INFO_HEIGHT)
        pygame.draw.rect(self.screen, GRAY, info_rect)

        if self.message:
            text = self.font_small.render(self.message, True, GREEN if "solved" in self.message else BLACK)
        else:
            hints = sum(1 for r in range(BOARD_SIZE) for c in range(BOARD_SIZE) if self.board.fixed[r][c])
            text = self.font_small.render(
                f"Difficulty: {self.difficulty}  Clues: {hints}  (R=reset, N=new, arrows=move)",
                True, BLACK,
            )
        text_rect = text.get_rect(center=(self.window_size // 2, self.window_size + INFO_HEIGHT // 2))
        self.screen.blit(text, text_rect)

        pygame.display.flip()

    def run(self):
        self.logger.info("Game started")
        while self.running:
            self.clock.tick(FPS)
            self.handle_events()
            if self.message_timer > 0:
                self.message_timer -= 1
                if self.message_timer == 0:
                    self.message = ""
            self.draw()
        self.logger.info("Game ended")
        pygame.quit()
        sys.exit()


def parse_args(argv):
    parser = argparse.ArgumentParser(description=WINDOW_TITLE)
    # Constraint: 使腳本接收輸入參數
    parser.add_argument(
        "--difficulty", type=str, default="medium",
        choices=list(DIFFICULTY.keys()),
        help="Puzzle difficulty (default: %(default)s)",
    )
    parser.add_argument(
        "--cell-size", type=int, default=CELL_SIZE,
        help="Cell size in pixels (default: %(default)s)",
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
