import argparse
import logging
import random
import sys

import pygame

# Constraint: 使用logger輸出訊息 - 用於除錯
logger = logging.getLogger("pygame-minesweeper")

# Constraint: 極簡風格呈現 - 強調玩法概念
CELL_SIZE = 32
HEADER_HEIGHT = 40

# Constraint: 踩地雷經典規格 (Windows 版本)
DIFFICULTIES = {
    "beginner": {"width": 9, "height": 9, "mines": 10},
    "intermediate": {"width": 16, "height": 16, "mines": 40},
    "expert": {"width": 30, "height": 16, "mines": 99},
}


def parse_args():
    parser = argparse.ArgumentParser(
        # Problem: 製作踩地雷遊戲原型
        description="Minesweeper prototype built with Pygame"
    )
    # Contract: 踩地雷經典規格
    parser.add_argument("--beginner", action="store_true", help="9x9 grid, 10 mines")
    parser.add_argument("--intermediate", action="store_true", help="16x16 grid, 40 mines")
    parser.add_argument("--expert", action="store_true", help="30x16 grid, 99 mines")
    parser.add_argument("--custom", nargs=3, type=int, metavar=("WIDTH", "HEIGHT", "MINES"),
                        help="Custom grid: WIDTH HEIGHT MINES")
    args = parser.parse_args()
    return args


def get_config(args):
    if args.beginner:
        return DIFFICULTIES["beginner"]
    elif args.intermediate:
        return DIFFICULTIES["intermediate"]
    elif args.expert:
        return DIFFICULTIES["expert"]
    elif args.custom:
        width, height, mines = args.custom
        if width < 1 or height < 1 or mines < 1:
            logger.error("Custom dimensions must be positive")
            sys.exit(1)
        if mines >= width * height:
            logger.error("Too many mines for grid size")
            sys.exit(1)
        return {"width": width, "height": height, "mines": mines}
    else:
        logger.info("No difficulty specified, defaulting to beginner")
        return DIFFICULTIES["beginner"]


# Contract: 遊戲核心規則
class Minesweeper:
    def __init__(self, width, height, num_mines):
        self.width = width
        self.height = height
        self.num_mines = num_mines
        self.mines_placed = False
        self.game_over = False
        self.won = False
        self.first_click = True
        self.flags_remaining = num_mines

        # 0 = hidden, 1 = revealed, 2 = flagged
        self.state = [[0 for _ in range(width)] for _ in range(height)]
        self.mines = [[False for _ in range(width)] for _ in range(height)]
        self.numbers = [[0 for _ in range(width)] for _ in range(height)]

    def place_mines(self, safe_row, safe_col):
        # Contract: 第一下必安全
        safe_positions = {(safe_row, safe_col)}
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                r, c = safe_row + dr, safe_col + dc
                if 0 <= r < self.height and 0 <= c < self.width:
                    safe_positions.add((r, c))

        positions = [(r, c) for r in range(self.height) for c in range(self.width)
                     if (r, c) not in safe_positions]
        random.shuffle(positions)
        mine_positions = positions[:self.num_mines]

        for r, c in mine_positions:
            self.mines[r][c] = True

        # Contract: 數字邏輯 - 計算周圍雷數
        for r in range(self.height):
            for c in range(self.width):
                if self.mines[r][c]:
                    continue
                count = 0
                for dr in (-1, 0, 1):
                    for dc in (-1, 0, 1):
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < self.height and 0 <= nc < self.width and self.mines[nr][nc]:
                            count += 1
                self.numbers[r][c] = count

        self.mines_placed = True
        logger.info("Placed %d mines on %dx%d grid", self.num_mines, self.width, self.height)

    def reveal(self, row, col):
        # Contract: 左鍵點擊
        if self.game_over or self.won:
            return
        if not (0 <= row < self.height and 0 <= col < self.width):
            return
        if self.state[row][col] != 0:
            return

        # Contract: 第一下必安全 - 第一次點擊後才佈雷
        if not self.mines_placed:
            self.place_mines(row, col)

        # Contract: 若點到地雷則遊戲結束
        if self.mines[row][col]:
            self.state[row][col] = 1
            self.game_over = True
            self.reveal_all_mines()
            logger.info("Game over - hit a mine at (%d, %d)", row, col)
            return

        # Contract: 數字邏輯 - flood fill for empty cells
        self._flood_fill(row, col)
        self._check_win()

    def _flood_fill(self, row, col):
        if not (0 <= row < self.height and 0 <= col < self.width):
            return
        if self.state[row][col] != 0:
            return
        if self.mines[row][col]:
            return

        self.state[row][col] = 1

        # Contract: 若為數字則顯示周圍8格的雷數
        if self.numbers[row][col] == 0:
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    self._flood_fill(row + dr, col + dc)

    def toggle_flag(self, row, col):
        # Contract: 右鍵標記
        if self.game_over or self.won:
            return
        if not (0 <= row < self.height and 0 <= col < self.width):
            return
        if self.state[row][col] == 1:
            return

        if self.state[row][col] == 0:
            self.state[row][col] = 2
            self.flags_remaining -= 1
        elif self.state[row][col] == 2:
            self.state[row][col] = 0
            self.flags_remaining += 1

    def reveal_all_mines(self):
        for r in range(self.height):
            for c in range(self.width):
                if self.mines[r][c] and self.state[r][c] != 2:
                    self.state[r][c] = 1

    def _check_win(self):
        # Contract: 獲勝條件 - 翻開所有沒有地雷的方格
        for r in range(self.height):
            for c in range(self.width):
                if not self.mines[r][c] and self.state[r][c] != 1:
                    return
        self.won = True
        logger.info("Game won!")

    def reset(self):
        self.__init__(self.width, self.height, self.num_mines)


# Constraint: 極簡風格呈現
COLORS = {
    "background": (192, 192, 192),
    "unrevealed": (162, 162, 162),
    "revealed": (224, 224, 224),
    "border_light": (255, 255, 255),
    "border_dark": (128, 128, 128),
    "text": (0, 0, 0),
    "flag": (255, 0, 0),
    "mine": (0, 0, 0),
    "header_bg": (192, 192, 192),
    "game_over_bg": (64, 64, 64),
    "won_bg": (0, 128, 0),
}

NUMBER_COLORS = {
    1: (0, 0, 255),
    2: (0, 128, 0),
    3: (255, 0, 0),
    4: (0, 0, 128),
    5: (128, 0, 0),
    6: (0, 128, 128),
    7: (0, 0, 0),
    8: (128, 128, 128),
}


def draw_cell(screen, font, game, row, col, cell_size):
    x = col * cell_size
    y = HEADER_HEIGHT + row * cell_size

    state = game.state[row][col]
    is_mine = game.mines[row][col]

    if state == 0:
        # Unrevealed cell - draw raised border
        pygame.draw.rect(screen, COLORS["unrevealed"], (x, y, cell_size, cell_size))
        pygame.draw.line(screen, COLORS["border_light"], (x, y), (x + cell_size - 1, y), 2)
        pygame.draw.line(screen, COLORS["border_light"], (x, y), (x, y + cell_size - 1), 2)
        pygame.draw.line(screen, COLORS["border_dark"], (x + cell_size - 1, y), (x + cell_size - 1, y + cell_size - 1), 2)
        pygame.draw.line(screen, COLORS["border_dark"], (x, y + cell_size - 1), (x + cell_size - 1, y + cell_size - 1), 2)
    elif state == 2:
        # Flagged cell
        pygame.draw.rect(screen, COLORS["unrevealed"], (x, y, cell_size, cell_size))
        pygame.draw.line(screen, COLORS["border_light"], (x, y), (x + cell_size - 1, y), 2)
        pygame.draw.line(screen, COLORS["border_light"], (x, y), (x, y + cell_size - 1), 2)
        pygame.draw.line(screen, COLORS["border_dark"], (x + cell_size - 1, y), (x + cell_size - 1, y + cell_size - 1), 2)
        pygame.draw.line(screen, COLORS["border_dark"], (x, y + cell_size - 1), (x + cell_size - 1, y + cell_size - 1), 2)
        # Draw flag
        flag_text = font.render("F", True, COLORS["flag"])
        text_rect = flag_text.get_rect(center=(x + cell_size // 2, y + cell_size // 2))
        screen.blit(flag_text, text_rect)
    elif state == 1:
        # Revealed cell
        pygame.draw.rect(screen, COLORS["revealed"], (x, y, cell_size, cell_size))
        if is_mine:
            mine_text = font.render("*", True, COLORS["mine"])
            text_rect = mine_text.get_rect(center=(x + cell_size // 2, y + cell_size // 2))
            screen.blit(mine_text, text_rect)
        elif game.numbers[row][col] > 0:
            num = game.numbers[row][col]
            color = NUMBER_COLORS.get(num, COLORS["text"])
            num_text = font.render(str(num), True, color)
            text_rect = num_text.get_rect(center=(x + cell_size // 2, y + cell_size // 2))
            screen.blit(num_text, text_rect)


def draw_header(screen, font, game, screen_width):
    header_rect = pygame.Rect(0, 0, screen_width, HEADER_HEIGHT)
    pygame.draw.rect(screen, COLORS["header_bg"], header_rect)
    pygame.draw.line(screen, COLORS["border_dark"], (0, HEADER_HEIGHT - 1), (screen_width, HEADER_HEIGHT - 1), 2)

    mine_count_text = font.render(f"Mines: {game.flags_remaining}", True, COLORS["text"])
    screen.blit(mine_count_text, (8, (HEADER_HEIGHT - mine_count_text.get_height()) // 2))

    if game.game_over:
        status = "GAME OVER - Press R to restart"
    elif game.won:
        status = "YOU WIN! - Press R to restart"
    else:
        status = "Minesweeper"
    status_text = font.render(status, True, COLORS["text"])
    status_x = (screen_width - status_text.get_width()) // 2
    screen.blit(status_text, (status_x, (HEADER_HEIGHT - status_text.get_height()) // 2))

    size_text = font.render(f"{game.width}x{game.height}", True, COLORS["text"])
    screen.blit(size_text, (screen_width - size_text.get_width() - 8, (HEADER_HEIGHT - size_text.get_height()) // 2))


def main():
    # Constraint: 使用logger輸出訊息
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(name)s] %(levelname)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    args = parse_args()
    config = get_config(args)

    logger.info("Starting Minesweeper: %dx%d, %d mines",
                config["width"], config["height"], config["mines"])

    # Constraint: 使用Pygame - 適合製作2D遊戲原型
    pygame.init()

    screen_width = config["width"] * CELL_SIZE
    screen_height = HEADER_HEIGHT + config["height"] * CELL_SIZE
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Minesweeper")

    font = pygame.font.SysFont("Courier New", CELL_SIZE // 2, bold=True)
    header_font = pygame.font.SysFont("Courier New", 16, bold=True)

    game = Minesweeper(config["width"], config["height"], config["mines"])
    running = True

    logger.info("Game initialized. Left click to reveal, right click to flag, R to restart.")

    # Contract: 測試各種模式下遊戲可執行
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    game.reset()
                    logger.info("Game reset")
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game.game_over or game.won:
                    continue
                mx, my = event.pos
                col = mx // CELL_SIZE
                row = (my - HEADER_HEIGHT) // CELL_SIZE
                if not (0 <= row < game.height and 0 <= col < game.width):
                    continue
                if event.button == 1:
                    game.reveal(row, col)
                elif event.button == 3:
                    game.toggle_flag(row, col)

        screen.fill(COLORS["background"])
        draw_header(screen, header_font, game, screen_width)

        for r in range(game.height):
            for c in range(game.width):
                draw_cell(screen, font, game, r, c, CELL_SIZE)

        pygame.display.flip()

    pygame.quit()
    logger.info("Game closed")


if __name__ == "__main__":
    main()
