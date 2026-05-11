"""
Pygame Connect Four
Problem: 製作Connect Four遊戲原型 (Constraint: 實作時註解要與Problem關聯)
"""

import argparse
import logging
import random
import sys

import pygame

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("connect-four")
# Constraint: 使用logger輸出訊息 - 用於人類跟AI除錯

DEFAULT_ROWS = 6
DEFAULT_COLS = 7
WIN_LENGTH = 4
CELL_SIZE = 80
DISC_RADIUS = 30
LINE_WIDTH = 3
FPS = 60

BG_COLOR = (30, 30, 30)
BOARD_COLOR = (50, 50, 200)
EMPTY_COLOR = (30, 30, 30)
PLAYER1_COLOR = (255, 50, 50)
PLAYER2_COLOR = (255, 255, 50)
TEXT_COLOR = (255, 255, 255)


def create_board(rows, cols):
    return [[0 for _ in range(cols)] for _ in range(rows)]
    # Task: Gravity discs - empty cells represented as 0


def drop_disc(board, col, player):
    rows = len(board)
    for r in range(rows - 1, -1, -1):
        if board[r][col] == 0:
            board[r][col] = player
            logger.debug(f"Player {player} dropped disc at column {col}, row {r}")
            return r
    return -1
    # Contract: Gravity discs - disc falls to lowest empty cell in column


def check_win(board, row, col, player):
    rows = len(board)
    cols = len(board[0])
    # Contract: 4-way win check - horizontal, vertical, both diagonals

    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]

    for dr, dc in directions:
        count = 1
        for step in (1, -1):
            r, c = row + dr * step, col + dc * step
            while 0 <= r < rows and 0 <= c < cols and board[r][c] == player:
                count += 1
                r += dr * step
                c += dc * step
        if count >= WIN_LENGTH:
            logger.info(f"Player {player} wins with {count} in a row at ({row},{col})")
            return True
    return False


def is_board_full(board):
    return all(cell != 0 for row in board for cell in row)


def get_valid_columns(board):
    cols = len(board[0])
    return [c for c in range(cols) if board[0][c] == 0]


def ai_simple_move(board, ai_player, human_player):
    cols = len(board[0])
    valid = get_valid_columns(board)
    if not valid:
        return -1

    for col in valid:
        for r in range(len(board) - 1, -1, -1):
            if board[r][col] == 0:
                board[r][col] = ai_player
                if check_win(board, r, col, ai_player):
                    board[r][col] = 0
                    logger.info(f"AI wins by playing column {col}")
                    return col
                board[r][col] = 0
                break

    for col in valid:
        for r in range(len(board) - 1, -1, -1):
            if board[r][col] == 0:
                board[r][col] = human_player
                if check_win(board, r, col, human_player):
                    board[r][col] = 0
                    logger.info(f"AI blocks column {col}")
                    return col
                board[r][col] = 0
                break

    center = cols // 2
    if center in valid:
        logger.info(f"AI plays center column {center}")
        return center

    col = random.choice(valid)
    logger.info(f"AI plays random valid column {col}")
    return col


def draw_board(screen, board, rows, cols):
    board_width = cols * CELL_SIZE
    board_height = rows * CELL_SIZE
    board_left = (screen.get_width() - board_width) // 2
    board_top = (screen.get_height() - board_height) // 2

    pygame.draw.rect(
        screen, BOARD_COLOR,
        (board_left, board_top, board_width, board_height),
    )

    for r in range(rows):
        for c in range(cols):
            cx = board_left + c * CELL_SIZE + CELL_SIZE // 2
            cy = board_top + r * CELL_SIZE + CELL_SIZE // 2
            if board[r][c] == 1:
                color = PLAYER1_COLOR
            elif board[r][c] == 2:
                color = PLAYER2_COLOR
            else:
                color = EMPTY_COLOR
            pygame.draw.circle(screen, color, (cx, cy), DISC_RADIUS)


def draw_status(screen, font, message):
    text = font.render(message, True, TEXT_COLOR)
    rect = text.get_rect(center=(screen.get_width() // 2, 20))
    screen.blit(text, rect)


def get_column_from_mouse(pos, cols, board_left, cell_width):
    x = pos[0]
    col = (x - board_left) // cell_width
    if 0 <= col < cols:
        return col
    return -1


def parse_args():
    parser = argparse.ArgumentParser(description="Pygame Connect Four")
    parser.add_argument(
        "--first-player",
        choices=["human", "ai"],
        default="human",
        help="Who plays first (default: human)",
    )
    parser.add_argument(
        "--rows",
        type=int,
        default=DEFAULT_ROWS,
        help=f"Number of rows (default: {DEFAULT_ROWS})",
    )
    parser.add_argument(
        "--cols",
        type=int,
        default=DEFAULT_COLS,
        help=f"Number of columns (default: {DEFAULT_COLS})",
    )
    parser.add_argument(
        "--log-level",
        choices=["DEBUG", "INFO", "WARNING", "ERROR"],
        default="INFO",
        help="Set logging level (default: INFO)",
    )
    return parser.parse_args()
    # Task: 使腳本接收輸入參數


def main():
    args = parse_args()
    logger.setLevel(getattr(logging, args.log_level))
    logger.info("Starting Pygame Connect Four")
    logger.info(f"Board: {args.rows}x{args.cols}, First: {args.first_player}")

    rows = args.rows
    cols = args.cols
    board_width = cols * CELL_SIZE
    board_height = rows * CELL_SIZE
    window_width = board_width + 40
    window_height = board_height + 60

    human_player = 1
    ai_player = 2
    current_player = 1

    pygame.init()
    screen = pygame.display.set_mode((window_width, window_height))
    pygame.display.set_caption("Connect Four")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 24)

    board = create_board(rows, cols)
    game_over = False
    result_message = ""
    board_left = (screen.get_width() - board_width) // 2

    logger.info("Game started")

    if args.first_player == "ai":
        logger.info("AI makes first move")
        col = ai_simple_move(board, ai_player, human_player)
        if col >= 0:
            row = drop_disc(board, col, ai_player)
            if check_win(board, row, col, ai_player):
                result_message = f"Player {ai_player} (AI) wins!"
                game_over = True
            current_player = human_player

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                logger.info("Game window closed")
                running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_r and game_over:
                logger.info("Game reset by player")
                board = create_board(rows, cols)
                current_player = 1
                game_over = False
                result_message = ""
                if args.first_player == "ai":
                    col = ai_simple_move(board, ai_player, human_player)
                    if col >= 0:
                        row = drop_disc(board, col, ai_player)
                        if check_win(board, row, col, ai_player):
                            result_message = f"Player {ai_player} (AI) wins!"
                            game_over = True
                        current_player = human_player

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                if current_player == human_player:
                    col = get_column_from_mouse(event.pos, cols, board_left, CELL_SIZE)
                    if col >= 0 and board[0][col] == 0:
                        logger.debug(f"Human drops disc in column {col}")
                        row = drop_disc(board, col, human_player)
                        if row >= 0:
                            if check_win(board, row, col, human_player):
                                result_message = f"Player {human_player} wins!"
                                logger.info(f"Game over: {result_message}")
                                game_over = True
                            elif is_board_full(board):
                                result_message = "It's a draw!"
                                logger.info("Game over: Draw")
                                game_over = True
                            else:
                                current_player = ai_player
                                ai_col = ai_simple_move(board, ai_player, human_player)
                                if ai_col >= 0:
                                    ai_row = drop_disc(board, ai_col, ai_player)
                                    logger.info(f"AI played column {ai_col}, row {ai_row}")
                                    if check_win(board, ai_row, ai_col, ai_player):
                                        result_message = f"Player {ai_player} (AI) wins!"
                                        logger.info(f"Game over: {result_message}")
                                        game_over = True
                                    elif is_board_full(board):
                                        result_message = "It's a draw!"
                                        logger.info("Game over: Draw")
                                        game_over = True
                                    else:
                                        current_player = human_player
                    else:
                        logger.debug("Human clicked invalid or full column")

        screen.fill(BG_COLOR)
        draw_board(screen, board, rows, cols)

        if game_over:
            draw_status(screen, font, f"{result_message}  Press R to restart")
        elif current_player == human_player:
            draw_status(screen, font, "Your turn")
        else:
            draw_status(screen, font, "AI thinking...")

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    logger.info("Game terminated")
    sys.exit(0)


if __name__ == "__main__":
    main()
