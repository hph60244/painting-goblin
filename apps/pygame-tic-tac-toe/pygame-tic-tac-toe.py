"""
Pygame Tic-Tac-Toe with Minimax AI
Problem: 製作Tic-Tac-Toe遊戲原型 (Constraint: 實作時註解要與Problem關聯)
"""

import argparse
import logging
import sys
from enum import Enum

import pygame

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("tic-tac-toe")
# Constraint: 使用logger輸出訊息 - 用於人類跟AI除錯


class Player(Enum):
    X = "X"
    O = "O"
    EMPTY = " "

    def __str__(self):
        return self.value


BOARD_SIZE = 3
CELL_SIZE = 150
LINE_WIDTH = 4
MARK_X_WIDTH = 6
MARK_O_WIDTH = 6
WINDOW_SIZE = CELL_SIZE * BOARD_SIZE
FPS = 60

BG_COLOR = (30, 30, 30)
LINE_COLOR = (200, 200, 200)
X_COLOR = (100, 200, 255)
O_COLOR = (255, 150, 100)
TEXT_COLOR = (255, 255, 255)


def init_board():
    return [[Player.EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]


def check_winner(board):
    for row in board:
        if row[0] != Player.EMPTY and row[0] == row[1] == row[2]:
            return row[0]
    for col in range(BOARD_SIZE):
        if board[0][col] != Player.EMPTY and board[0][col] == board[1][col] == board[2][col]:
            return board[0][col]
    if board[0][0] != Player.EMPTY and board[0][0] == board[1][1] == board[2][2]:
        return board[0][0]
    if board[0][2] != Player.EMPTY and board[0][2] == board[1][1] == board[2][0]:
        return board[0][2]
    return None


def is_board_full(board):
    return all(cell != Player.EMPTY for row in board for cell in row)


def get_available_moves(board):
    moves = []
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if board[r][c] == Player.EMPTY:
                moves.append((r, c))
    return moves


def minimax(board, depth, is_maximizing, ai_player, human_player):
    """
    Minimax AI for Tic-Tac-Toe.
    Contract: 3x3 grid, minimax AI
    """
    winner = check_winner(board)
    if winner == ai_player:
        return 10 - depth
    if winner == human_player:
        return depth - 10
    if is_board_full(board):
        return 0

    if is_maximizing:
        best = -float("inf")
        for r, c in get_available_moves(board):
            board[r][c] = ai_player
            score = minimax(board, depth + 1, False, ai_player, human_player)
            board[r][c] = Player.EMPTY
            best = max(score, best)
        return best
    else:
        best = float("inf")
        for r, c in get_available_moves(board):
            board[r][c] = human_player
            score = minimax(board, depth + 1, True, ai_player, human_player)
            board[r][c] = Player.EMPTY
            best = min(score, best)
        return best


def ai_move(board, ai_player, human_player):
    """
    Select best move for AI using minimax.
    Constraint: 使用Pygame - 適合製作2D遊戲原型
    """
    moves = get_available_moves(board)
    if not moves:
        return None
    best_score = -float("inf")
    best_move = moves[0]
    for r, c in moves:
        board[r][c] = ai_player
        score = minimax(board, 0, False, ai_player, human_player)
        board[r][c] = Player.EMPTY
        logger.debug(f"Move ({r},{c}) score={score}")
        if score > best_score:
            best_score = score
            best_move = (r, c)
    logger.info(f"AI ({ai_player}) chooses move {best_move} with score {best_score}")
    return best_move


def draw_grid(screen):
    for i in range(1, BOARD_SIZE):
        pos = i * CELL_SIZE
        pygame.draw.line(screen, LINE_COLOR, (pos, 0), (pos, WINDOW_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (0, pos), (WINDOW_SIZE, pos), LINE_WIDTH)


def draw_mark(screen, row, col, player):
    """
    Constraint: 用極簡風格呈現 - simple geometric shapes, no sprites
    """
    center_x = col * CELL_SIZE + CELL_SIZE // 2
    center_y = row * CELL_SIZE + CELL_SIZE // 2
    offset = CELL_SIZE // 4
    if player == Player.X:
        pygame.draw.line(
            screen, X_COLOR,
            (center_x - offset, center_y - offset),
            (center_x + offset, center_y + offset),
            MARK_X_WIDTH,
        )
        pygame.draw.line(
            screen, X_COLOR,
            (center_x + offset, center_y - offset),
            (center_x - offset, center_y + offset),
            MARK_X_WIDTH,
        )
    elif player == Player.O:
        pygame.draw.circle(screen, O_COLOR, (center_x, center_y), offset, MARK_O_WIDTH)


def draw_status(screen, font, message):
    text = font.render(message, True, TEXT_COLOR)
    rect = text.get_rect(center=(WINDOW_SIZE // 2, WINDOW_SIZE + 20))
    screen.blit(text, rect)


def get_cell_from_pos(pos):
    x, y = pos
    if x < 0 or x >= WINDOW_SIZE or y < 0 or y >= WINDOW_SIZE:
        return None
    return y // CELL_SIZE, x // CELL_SIZE


def parse_args():
    parser = argparse.ArgumentParser(description="Pygame Tic-Tac-Toe with Minimax AI")
    parser.add_argument(
        "--first-player",
        choices=["human", "ai"],
        default="human",
        help="Who plays first (default: human)",
    )
    parser.add_argument(
        "--human-side",
        choices=["X", "O"],
        default="X",
        help="Human plays as X or O (default: X)",
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
    logger.info("Starting Pygame Tic-Tac-Toe")
    logger.info(f"First player: {args.first_player}, Human side: {args.human_side}")

    human_player = Player(args.human_side)
    ai_player = Player.O if human_player == Player.X else Player.X
    logger.info(f"Human: {human_player}, AI: {ai_player}")

    pygame.init()
    screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE + 60))
    pygame.display.set_caption("Tic-Tac-Toe")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 28)

    board = init_board()
    current_player = Player.X
    game_over = False
    result_message = ""

    logger.info("Game started")

    if args.first_player == "ai":
        logger.info("AI makes first move")
        move = ai_move(board, ai_player, human_player)
        if move:
            r, c = move
            board[r][c] = ai_player
        current_player = human_player

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                logger.info("Game window closed")
                running = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_r and game_over:
                logger.info("Game reset by player")
                board = init_board()
                current_player = Player.X
                game_over = False
                result_message = ""
                if args.first_player == "ai":
                    move = ai_move(board, ai_player, human_player)
                    if move:
                        r, c = move
                        board[r][c] = ai_player
                    current_player = human_player

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                if current_player == human_player:
                    cell = get_cell_from_pos(event.pos)
                    if cell is not None:
                        r, c = cell
                        logger.debug(f"Human clicks cell ({r},{c})")
                        if board[r][c] == Player.EMPTY:
                            board[r][c] = human_player
                            logger.info(f"Human played {human_player} at ({r},{c})")
                            winner = check_winner(board)
                            if winner:
                                result_message = f"{winner} wins!"
                                logger.info(f"Game over: {result_message}")
                                game_over = True
                            elif is_board_full(board):
                                result_message = "It's a draw!"
                                logger.info("Game over: Draw")
                                game_over = True
                            else:
                                current_player = ai_player
                                ai_move_result = ai_move(board, ai_player, human_player)
                                if ai_move_result:
                                    ai_r, ai_c = ai_move_result
                                    board[ai_r][ai_c] = ai_player
                                    logger.info(f"AI played {ai_player} at ({ai_r},{ai_c})")
                                winner = check_winner(board)
                                if winner:
                                    result_message = f"{winner} wins!"
                                    logger.info(f"Game over: {result_message}")
                                    game_over = True
                                elif is_board_full(board):
                                    result_message = "It's a draw!"
                                    logger.info("Game over: Draw")
                                    game_over = True
                                else:
                                    current_player = human_player
                        else:
                            logger.debug("Human clicked occupied cell")

        screen.fill(BG_COLOR)
        draw_grid(screen)
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                draw_mark(screen, r, c, board[r][c])

        if game_over:
            draw_status(screen, font, f"{result_message}  Press R to restart")
        elif current_player == human_player:
            draw_status(screen, font, f"Your turn ({human_player})")
        else:
            draw_status(screen, font, f"AI thinking ({ai_player})...")

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    logger.info("Game terminated")
    sys.exit(0)


if __name__ == "__main__":
    main()
