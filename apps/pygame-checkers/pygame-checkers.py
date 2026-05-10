#!/usr/bin/env python3
# Problem: 製作Checkers遊戲原型

import argparse
import logging
import sys
from copy import deepcopy
from enum import IntEnum

# Constraint: 使用Pygame
import pygame

# Constraint: 使用logger輸出訊息 — 用於人類跟AI除錯
logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s:%(message)s")
log = logging.getLogger("checkers")
log.info("啟動 Checkers 遊戲原型")


# ---------------------------------------------------------------------------
# 遊戲常數
# ---------------------------------------------------------------------------
BOARD_SIZE = 8
CELL_SIZE = 64
MARGIN = 40
INFO_HEIGHT = 80
WINDOW_WIDTH = BOARD_SIZE * CELL_SIZE + MARGIN * 2
WINDOW_HEIGHT = BOARD_SIZE * CELL_SIZE + MARGIN * 2 + INFO_HEIGHT
FPS = 30

# Constraint: 用極簡風格呈現
COLOR_BG = (40, 40, 40)
COLOR_BOARD_LIGHT = (238, 215, 170)
COLOR_BOARD_DARK = (140, 90, 40)
COLOR_LINE = (100, 65, 25)
COLOR_PIECE_BLACK = (40, 40, 40)
COLOR_PIECE_WHITE = (220, 220, 220)
COLOR_KING_MARK = (255, 215, 0)
COLOR_SELECTED = (100, 200, 255)
COLOR_HINT = (0, 200, 80, 120)
COLOR_TEXT = (255, 255, 255)
COLOR_BG_TEXT = (30, 30, 30)
COLOR_OVER = (0, 0, 0, 160)

# Direction vectors for diagonal moves
FORWARD_DIRS_BLACK = [(1, -1), (1, 1)]  # black moves down the board
FORWARD_DIRS_WHITE = [(-1, -1), (-1, 1)]  # white moves up


class Player(IntEnum):
    EMPTY = 0
    BLACK = 1
    WHITE = 2

    def opponent(self):
        return Player.BLACK if self == Player.WHITE else Player.WHITE

    def forward_dirs(self):
        return FORWARD_DIRS_BLACK if self == Player.BLACK else FORWARD_DIRS_WHITE


# ---------------------------------------------------------------------------
# 核心邏輯 — 棋子、跳吃、升王
# ---------------------------------------------------------------------------

class Piece:
    __slots__ = ("player", "is_king")

    def __init__(self, player: Player, is_king: bool = False):
        self.player = player
        self.is_king = is_king

    def __repr__(self):
        k = "K" if self.is_king else ""
        return f"{k}{self.player.name[0]}"


class Move:
    def __init__(self, path: list[tuple[int, int]]):
        self.path = path  # list of (row, col) from start to end

    @property
    def start(self):
        return self.path[0]

    @property
    def end(self):
        return self.path[-1]

    @property
    def captured(self) -> list[tuple[int, int]]:
        """Return positions of captured pieces."""
        caps = []
        for i in range(len(self.path) - 1):
            r1, c1 = self.path[i]
            r2, c2 = self.path[i + 1]
            if abs(r2 - r1) == 2:
                caps.append(((r1 + r2) // 2, (c1 + c2) // 2))
        return caps

    @property
    def is_jump(self) -> bool:
        return len(self.captured) > 0


class CheckersGame:
    def __init__(self):
        self.board: list[list[Piece | None]] = [[None] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.current_player = Player.BLACK
        self.game_over = False
        self.winner: Player | None = None
        self.move_count = 0
        self._setup_board()
        log.info("棋局初始化完成")

    def _setup_board(self):
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if (r + c) % 2 == 1:
                    if r < 3:
                        self.board[r][c] = Piece(Player.BLACK)
                    elif r > BOARD_SIZE - 4:
                        self.board[r][c] = Piece(Player.WHITE)

    def clone(self):
        g = CheckersGame.__new__(CheckersGame)
        g.board = [[deepcopy(self.board[r][c]) for c in range(BOARD_SIZE)] for r in range(BOARD_SIZE)]
        g.current_player = self.current_player
        g.game_over = self.game_over
        g.winner = self.winner
        g.move_count = self.move_count
        return g

    def get_piece(self, row: int, col: int) -> Piece | None:
        if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
            return self.board[row][col]
        return None

    def _gen_simple_moves(self, row: int, col: int, piece: Piece) -> list[Move]:
        """Generate non-jump moves for a piece."""
        moves = []
        dirs = piece.player.forward_dirs() if not piece.is_king else [(1, -1), (1, 1), (-1, -1), (-1, 1)]
        for dr, dc in dirs:
            nr, nc = row + dr, col + dc
            if 0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE and self.board[nr][nc] is None:
                moves.append(Move([(row, col), (nr, nc)]))
        return moves

    def _gen_jumps_from(self, row: int, col: int, piece: Piece, visited: set) -> list[Move]:
        """Recursively generate all jump sequences from a position."""
        jumps = []
        dirs = piece.player.forward_dirs() if not piece.is_king else [(1, -1), (1, 1), (-1, -1), (-1, 1)]
        for dr, dc in dirs:
            mr, mc = row + dr, col + dc
            nr, nc = row + dr * 2, col + dc * 2
            if not (0 <= nr < BOARD_SIZE and 0 <= nc < BOARD_SIZE):
                continue
            mid = self.board[mr][mc]
            if mid is None or mid.player != piece.player.opponent():
                continue
            if self.board[nr][nc] is not None:
                continue
            landing = (nr, nc)
            if landing in visited:
                continue
            visited.add(landing)
            sub_jumps = self._gen_jumps_from(nr, nc, piece, visited)
            visited.discard(landing)
            if sub_jumps:
                for sub in sub_jumps:
                    full_path = [(row, col)] + sub.path
                    jumps.append(Move(full_path))
            else:
                jumps.append(Move([(row, col), (nr, nc)]))
        return jumps

    def get_moves_for(self, row: int, col: int) -> list[Move]:
        """Get all valid moves for piece at (row, col)."""
        piece = self.board[row][col]
        if piece is None or piece.player != self.current_player:
            return []
        jumps = self._gen_jumps_from(row, col, piece, {(row, col)})
        if jumps:
            return jumps
        return self._gen_simple_moves(row, col, piece)

    def get_all_moves(self) -> list[Move]:
        """Get all valid moves for the current player."""
        all_moves = []
        has_jumps = False
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                piece = self.board[r][c]
                if piece is None or piece.player != self.current_player:
                    continue
                jumps = self._gen_jumps_from(r, c, piece, {(r, c)})
                if jumps:
                    all_moves.extend(jumps)
                    has_jumps = True
        if has_jumps:
            return all_moves
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                piece = self.board[r][c]
                if piece is None or piece.player != self.current_player:
                    continue
                all_moves.extend(self._gen_simple_moves(r, c, piece))
        return all_moves

    def get_mandatory_jumps(self) -> list[Move]:
        """Return only jump moves (mandatory)."""
        all_jumps = []
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                piece = self.board[r][c]
                if piece is None or piece.player != self.current_player:
                    continue
                all_jumps.extend(self._gen_jumps_from(r, c, piece, {(r, c)}))
        return all_jumps

    # Contract: Jump captures
    def apply_move(self, move: Move) -> bool:
        if self.game_over:
            log.warning("遊戲已結束，無法移動")
            return False
        # Apply the move
        path = move.path
        piece = self.board[path[0][0]][path[0][1]]
        if piece is None:
            return False
        self.board[path[0][0]][path[0][1]] = None
        # Remove captured pieces
        for cr, cc in move.captured:
            self.board[cr][cc] = None
        # Place piece at destination
        end_r, end_c = path[-1]
        self.board[end_r][end_c] = piece
        # Contract: King promotion
        promoted = False
        if not piece.is_king:
            if piece.player == Player.BLACK and end_r == BOARD_SIZE - 1:
                piece.is_king = True
                promoted = True
                log.info(f"黑子升王 at ({end_r},{end_c})")
            elif piece.player == Player.WHITE and end_r == 0:
                piece.is_king = True
                promoted = True
                log.info(f"白子升王 at ({end_r},{end_c})")
        self.move_count += 1
        log.info(f"玩家 {piece.player.name} 移動 {path[0]}->{path[-1]}, "
                 f"捕獲 {len(move.captured)} 子{' 升王' if promoted else ''}")
        # Check for additional jumps (multi-jump continuation)
        if move.is_jump:
            extra_jumps = self._gen_jumps_from(end_r, end_c, piece, {(end_r, end_c)})
            if extra_jumps:
                log.info(f"玩家 {piece.player.name} 可繼續連跳")
                return True
        self._next_turn()
        return True

    def _next_turn(self):
        self.current_player = self.current_player.opponent()
        # Check if opponent has any moves
        if not self.get_all_moves():
            self.game_over = True
            self.winner = self.current_player.opponent()
            log.info(f"遊戲結束 — {self.winner.name} 獲勝 (對手無棋可走)")
            return
        # Check for draw by insufficient material (simplified: 40 moves rule)
        if self.move_count >= 200:
            self.game_over = True
            self.winner = None
            log.info("遊戲結束 — 平局 (超過200步)")

    def count_pieces(self, player: Player) -> int:
        count = 0
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                p = self.board[r][c]
                if p is not None and p.player == player:
                    count += 1
        return count


# ---------------------------------------------------------------------------
# Heuristic AI — 基於位置與棋子價值的Minimax搜索
# ---------------------------------------------------------------------------

PIECE_VALUE = 100
KING_VALUE = 150
PIECE_WEIGHTS = [
    [0,  0,  0,  0,  0,  0,  0,  0],
    [0,  2,  4,  4,  4,  4,  2,  0],
    [0,  4,  6,  8,  8,  6,  4,  0],
    [0,  4,  8, 10, 10,  8,  4,  0],
    [0,  4,  8, 10, 10,  8,  4,  0],
    [0,  4,  6,  8,  8,  6,  4,  0],
    [0,  2,  4,  4,  4,  4,  2,  0],
    [0,  0,  0,  0,  0,  0,  0,  0],
]


def evaluate_board(game: CheckersGame, player: Player) -> int:
    score = 0
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            p = game.board[r][c]
            if p is None:
                continue
            val = (PIECE_VALUE + PIECE_WEIGHTS[r][c]) if not p.is_king else (KING_VALUE + PIECE_WEIGHTS[r][c])
            if p.player == player:
                score += val
            else:
                score -= val
    return score


# Contract: minimax
def ai_move(game: CheckersGame, depth: int = 4) -> Move | None:
    log.info(f"AI ({game.current_player.name}) 思考中 (depth={depth}) ...")
    moves = game.get_all_moves()
    if not moves:
        return None
    best_score = float("-inf")
    best_moves = []
    for move in moves:
        sim = game.clone()
        sim.apply_move(move)
        if sim.game_over:
            sc = evaluate_board(sim, game.current_player)
            sc += 10000 if sim.winner == game.current_player else -10000
        else:
            sc = -_negamax(sim, depth - 1, float("-inf"), float("inf"),
                           game.current_player.opponent(), game.current_player)
        if sc > best_score:
            best_score = sc
            best_moves = [move]
        elif sc == best_score:
            best_moves.append(move)
    import random
    best_move = random.choice(best_moves) if best_moves else None
    if best_move is not None:
        log.info(f"AI 選擇 {best_move.start}->{best_move.end} 分數={best_score:.1f} 捕獲={len(best_move.captured)}")
    return best_move


def _negamax(game: CheckersGame, depth: int, alpha: float, beta: float,
             player: Player, root_player: Player) -> float:
    if depth == 0:
        return evaluate_board(game, root_player) if player == root_player else -evaluate_board(game, root_player)
    moves = game.get_all_moves()
    if not moves:
        sim = game.clone()
        sim._next_turn()
        if sim.game_over:
            sc = evaluate_board(sim, root_player)
            return sc * 100
        return -_negamax(sim, depth - 1, -beta, -alpha,
                         player.opponent(), root_player)
    for move in moves:
        sim = game.clone()
        sim.apply_move(move)
        sc = -_negamax(sim, depth - 1, -beta, -alpha,
                       root_player if sim.current_player == root_player else root_player.opponent(),
                       root_player)
        if sc > alpha:
            alpha = sc
        if alpha >= beta:
            break
    return alpha


# ---------------------------------------------------------------------------
# Pygame UI — Constraint: 用極簡風格呈現
# ---------------------------------------------------------------------------

class CheckersUI:
    def __init__(self, ai_enabled: bool = True, ai_depth: int = 4, ai_player: Player = Player.WHITE):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Checkers")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("arial", 20, bold=True)
        self.font_small = pygame.font.SysFont("arial", 16)
        self.font_big = pygame.font.SysFont("arial", 40, bold=True)
        self.game = CheckersGame()
        self.ai_enabled = ai_enabled
        self.ai_depth = ai_depth
        self.ai_player = ai_player
        self.human_player = ai_player.opponent() if ai_enabled else Player.BLACK
        self.running = True
        self.selected: tuple[int, int] | None = None
        self.valid_moves: list[Move] = []
        self.message = ""
        self.message_timer = 0

    def _board_to_screen(self, row: int, col: int) -> tuple[int, int]:
        x = MARGIN + col * CELL_SIZE
        y = MARGIN + row * CELL_SIZE
        return x, y

    def _screen_to_board(self, mx: int, my: int) -> tuple[int, int] | None:
        col = (mx - MARGIN) // CELL_SIZE
        row = (my - MARGIN) // CELL_SIZE
        if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
            return row, col
        return None

    def run(self):
        log.info("UI 啟動")
        while self.running:
            self._handle_events()
            self._update()
            self._draw()
            self.clock.tick(FPS)
        pygame.quit()
        log.info("UI 關閉")

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and self.game.game_over:
                    self.game = CheckersGame()
                    self.selected = None
                    self.valid_moves = []
                    log.info("重新開始遊戲")
                elif event.key == pygame.K_ESCAPE:
                    self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not self.game.game_over:
                if self.ai_enabled and self.game.current_player == self.ai_player:
                    return
                board_pos = self._screen_to_board(event.pos[0], event.pos[1])
                if board_pos is None:
                    return
                row, col = board_pos
                # If a piece is selected and we click a valid move target
                if self.selected is not None:
                    for move in self.valid_moves:
                        if move.end == (row, col):
                            if self.game.apply_move(move):
                                self.selected = None
                                self.valid_moves = []
                                self.message = ""
                            else:
                                self.message = "無效移動!"
                                self.message_timer = 60
                            return
                    # Click on own piece -> reselect
                    piece = self.game.get_piece(row, col)
                    if piece is not None and piece.player == self.human_player:
                        self.selected = (row, col)
                        self.valid_moves = self.game.get_moves_for(row, col)
                        return
                    # Click elsewhere -> deselect
                    self.selected = None
                    self.valid_moves = []
                else:
                    piece = self.game.get_piece(row, col)
                    if piece is not None and piece.player == self.human_player:
                        self.selected = (row, col)
                        self.valid_moves = self.game.get_moves_for(row, col)

    def _update(self):
        if self.game.game_over:
            return
        if self.ai_enabled and self.game.current_player == self.ai_player:
            move = ai_move(self.game, self.ai_depth)
            if move:
                pygame.time.wait(300)
                self.game.apply_move(move)
                # If there's a multi-jump continuation for AI, keep going
                while self.ai_enabled and self.game.current_player == self.ai_player and not self.game.game_over:
                    jump_moves = self.game.get_all_moves()
                    if jump_moves and any(m.is_jump for m in jump_moves):
                        move = ai_move(self.game, self.ai_depth)
                        if move:
                            pygame.time.wait(200)
                            self.game.apply_move(move)
                        else:
                            break
                    else:
                        break

    def _draw(self):
        self.screen.fill(COLOR_BG)
        self._draw_board()
        self._draw_pieces()
        self._draw_selection_and_hints()
        self._draw_info()
        if self.game.game_over:
            self._draw_game_over()
        pygame.display.flip()

    def _draw_board(self):
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                x, y = self._board_to_screen(r, c)
                color = COLOR_BOARD_LIGHT if (r + c) % 2 == 0 else COLOR_BOARD_DARK
                pygame.draw.rect(self.screen, color, (x, y, CELL_SIZE, CELL_SIZE))

    def _draw_pieces(self):
        piece_radius = CELL_SIZE // 2 - 5
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                p = self.board[r][c]
                if p is None:
                    continue
                cx = MARGIN + c * CELL_SIZE + CELL_SIZE // 2
                cy = MARGIN + r * CELL_SIZE + CELL_SIZE // 2
                color = COLOR_PIECE_BLACK if p.player == Player.BLACK else COLOR_PIECE_WHITE
                pygame.draw.circle(self.screen, color, (cx, cy), piece_radius)
                pygame.draw.circle(self.screen, (80, 80, 80), (cx, cy), piece_radius, 2)
                if p.is_king:
                    inner = piece_radius - 6
                    pygame.draw.circle(self.screen, COLOR_KING_MARK, (cx, cy), inner, 2)
                    # Draw crown symbol
                    pts = [
                        (cx, cy - inner + 4),
                        (cx - 5, cy - 2),
                        (cx - 3, cy - 2),
                        (cx, cy - 5),
                        (cx + 3, cy - 2),
                        (cx + 5, cy - 2),
                    ]
                    pygame.draw.lines(self.screen, COLOR_KING_MARK, False, pts, 2)

    def _draw_selection_and_hints(self):
        if self.selected is not None:
            r, c = self.selected
            x, y = self._board_to_screen(r, c)
            pygame.draw.rect(self.screen, COLOR_SELECTED, (x, y, CELL_SIZE, CELL_SIZE), 3)
        # Draw hints for valid moves
        for move in self.valid_moves:
            er, ec = move.end
            cx = MARGIN + ec * CELL_SIZE + CELL_SIZE // 2
            cy = MARGIN + er * CELL_SIZE + CELL_SIZE // 2
            s = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
            if move.is_jump:
                pygame.draw.circle(s, (255, 50, 50, 120), (CELL_SIZE // 2, CELL_SIZE // 2), CELL_SIZE // 2 - 2)
            else:
                pygame.draw.circle(s, (0, 200, 80, 100), (CELL_SIZE // 2, CELL_SIZE // 2), CELL_SIZE // 6)
            self.screen.blit(s, (MARGIN + ec * CELL_SIZE, MARGIN + er * CELL_SIZE))

    def _draw_info(self):
        info_y = MARGIN + BOARD_SIZE * CELL_SIZE
        pygame.draw.rect(self.screen, COLOR_BG_TEXT,
                         (0, info_y, WINDOW_WIDTH, INFO_HEIGHT))

        black_count = self.game.count_pieces(Player.BLACK)
        white_count = self.game.count_pieces(Player.WHITE)
        txt = self.font.render(f"黑: {black_count}", True, COLOR_PIECE_BLACK)
        self.screen.blit(txt, (20, info_y + 10))
        txt = self.font.render(f"白: {white_count}", True, COLOR_PIECE_WHITE)
        self.screen.blit(txt, (20, info_y + 35))

        if not self.game.game_over:
            color = COLOR_PIECE_BLACK if self.game.current_player == Player.BLACK else COLOR_PIECE_WHITE
            label = "AI" if (self.ai_enabled and self.game.current_player == self.ai_player) else "你"
            txt = self.font.render(f"輪到: {label} ({self.game.current_player.name})", True, color)
            self.screen.blit(txt, (150, info_y + 10))

        txt = self.font_small.render("R:重開  ESC:離開", True, (180, 180, 180))
        self.screen.blit(txt, (150, info_y + 40))

        if self.message:
            txt = self.font.render(self.message, True, (255, 100, 100))
            self.screen.blit(txt, (WINDOW_WIDTH // 2 - 50, info_y + 10))
            self.message_timer -= 1
            if self.message_timer <= 0:
                self.message = ""

    def _draw_game_over(self):
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill(COLOR_OVER)
        self.screen.blit(overlay, (0, 0))
        black_count = self.game.count_pieces(Player.BLACK)
        white_count = self.game.count_pieces(Player.WHITE)
        if self.game.winner:
            msg = f"{self.game.winner.name} 獲勝! ({black_count} - {white_count})"
        else:
            msg = f"平局! ({black_count} - {white_count})"
        txt = self.font_big.render(msg, True, (255, 255, 100))
        rect = txt.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 20))
        self.screen.blit(txt, rect)
        txt = self.font.render("按 R 重新開始, ESC 離開", True, (200, 200, 200))
        rect = txt.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 30))
        self.screen.blit(txt, rect)

    @property
    def board(self):
        return self.game.board


# ---------------------------------------------------------------------------
# Entry point — 使腳本接收輸入參數
# ---------------------------------------------------------------------------
def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Checkers 遊戲原型")
    parser.add_argument("--two-player", action="store_true",
                        help="雙人模式 (預設: 對抗AI)")
    parser.add_argument("--depth", type=int, default=4, choices=[1, 2, 3, 4, 5, 6],
                        help="AI 搜索深度 (預設: 4)")
    parser.add_argument("--first", choices=["black", "white"], default="black",
                        help="玩家執棋顏色 (預設: black)")
    return parser.parse_args(argv)


def main():
    args = parse_args()
    log.info(f"參數: two_player={args.two_player}, depth={args.depth}, first={args.first}")

    ai_enabled = not args.two_player
    human_player = Player.BLACK if args.first == "black" else Player.WHITE
    if ai_enabled:
        ai_player: Player = human_player.opponent()
    else:
        ai_player = Player.WHITE  # not used in two-player mode
    ui = CheckersUI(ai_enabled=ai_enabled, ai_depth=args.depth,
                    ai_player=ai_player)
    ui.human_player = human_player

    log.info("啟動 Checkers 遊戲")
    ui.run()


if __name__ == "__main__":
    main()
