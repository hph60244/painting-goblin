#!/usr/bin/env python3
# Problem: 製作Othello/Reversi遊戲原型

import argparse
import logging
import sys
from enum import IntEnum

# Constraint: 使用Pygame
import pygame

# Constraint: 使用logger輸出訊息 — 用於人類跟AI除錯
logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s:%(message)s")
log = logging.getLogger("othello")
log.info("啟動 Othello/Reversi")


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

# 顏色 — Constraint: 用極簡風格呈現
COLOR_BG = (34, 139, 34)          # 棋盤綠
COLOR_BOARD = (0, 100, 0)         # 深綠格子
COLOR_LINE = (20, 80, 20)         # 格線
COLOR_BLACK = (20, 20, 20)        # 黑子
COLOR_WHITE = (230, 230, 230)     # 白子
COLOR_HINT: tuple[int, int, int, int] = (255, 255, 100, 80)  # 提示標記 (RGBA)
COLOR_TEXT = (255, 255, 255)      # 文字
COLOR_BG_TEXT = (30, 30, 30)      # 資訊列底色
COLOR_OVER = (0, 0, 0, 160)       # 遊戲結束遮罩


# 8-dir flanking — 八個方向
DIRECTIONS = [(-1, -1), (-1, 0), (-1, 1),
              (0, -1),           (0, 1),
              (1, -1),  (1, 0),  (1, 1)]


class Player(IntEnum):
    EMPTY = 0
    BLACK = 1
    WHITE = 2

    def opponent(self):
        return Player.BLACK if self == Player.WHITE else Player.WHITE


# ---------------------------------------------------------------------------
# 核心邏輯 — 8-dir flanking
# ---------------------------------------------------------------------------
class OthelloGame:
    def __init__(self):
        self.board = [[Player.EMPTY] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.board[3][3] = Player.WHITE
        self.board[3][4] = Player.BLACK
        self.board[4][3] = Player.BLACK
        self.board[4][4] = Player.WHITE
        self.current_player = Player.BLACK
        self.game_over = False
        self.winner = None
        self.move_count = 0
        log.info("棋局初始化完成")

    def clone(self):
        g = OthelloGame.__new__(OthelloGame)
        g.board = [row[:] for row in self.board]
        g.current_player = self.current_player
        g.game_over = self.game_over
        g.winner = self.winner
        g.move_count = self.move_count
        return g

    # 8-dir flanking: 檢查某個方向是否可翻
    def _flank_in_dir(self, row, col, dr, dc):
        r, c = row + dr, col + dc
        opponent = self.current_player.opponent()
        if not (0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE):
            return []
        if self.board[r][c] != opponent:
            return []
        cells = [(r, c)]
        while True:
            r += dr
            c += dc
            if not (0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE):
                return []
            if self.board[r][c] == Player.EMPTY:
                return []
            if self.board[r][c] == self.current_player:
                return cells
            cells.append((r, c))

    def get_valid_moves(self):
        moves = []
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if self.board[r][c] != Player.EMPTY:
                    continue
                flips = []
                for dr, dc in DIRECTIONS:
                    flips.extend(self._flank_in_dir(r, c, dr, dc))
                if flips:
                    moves.append((r, c))
        return moves

    def is_valid_move(self, row, col):
        if self.board[row][col] != Player.EMPTY:
            return False
        for dr, dc in DIRECTIONS:
            if self._flank_in_dir(row, col, dr, dc):
                return True
        return False

    def apply_move(self, row, col):
        if self.game_over:
            log.warning("遊戲已結束，無法下子")
            return False
        if not self.is_valid_move(row, col):
            return False
        flips = []
        for dr, dc in DIRECTIONS:
            flips.extend(self._flank_in_dir(row, col, dr, dc))
        self.board[row][col] = self.current_player
        for r, c in flips:
            self.board[r][c] = self.current_player
        self.move_count += 1
        log.info(f"玩家 {self.current_player.name} 下 ({row},{col}), 翻轉 {len(flips)} 子")
        self._next_turn()
        return True

    def _next_turn(self):
        self.current_player = self.current_player.opponent()
        if self.get_valid_moves():
            return
        self.current_player = self.current_player.opponent()
        if self.get_valid_moves():
            log.info(f"玩家 {self.current_player.name} 無棋可下，換回 {self.current_player.opponent().name}")
            self.current_player = self.current_player.opponent()
            return
        self.game_over = True
        scores = self.get_scores()
        if scores[Player.BLACK] > scores[Player.WHITE]:
            self.winner = Player.BLACK
        elif scores[Player.WHITE] > scores[Player.BLACK]:
            self.winner = Player.WHITE
        else:
            self.winner = None
        log.info(f"遊戲結束 — 黑:{scores[Player.BLACK]} 白:{scores[Player.WHITE]}")

    def get_scores(self):
        black = sum(row.count(Player.BLACK) for row in self.board)
        white = sum(row.count(Player.WHITE) for row in self.board)
        return {Player.BLACK: black, Player.WHITE: white}


# ---------------------------------------------------------------------------
# Heuristic AI — 基於位置權重與貪婪搜索
# ---------------------------------------------------------------------------

# 位置權重表 (8x8)，鼓勵搶角、避開星位
POSITION_WEIGHTS = [
    [100, -20,  10,   5,   5,  10, -20, 100],
    [-20, -50,  -2,  -2,  -2,  -2, -50, -20],
    [ 10,  -2,   1,   1,   1,   1,  -2,  10],
    [  5,  -2,   1,   0,   0,   1,  -2,   5],
    [  5,  -2,   1,   0,   0,   1,  -2,   5],
    [ 10,  -2,   1,   1,   1,   1,  -2,  10],
    [-20, -50,  -2,  -2,  -2,  -2, -50, -20],
    [100, -20,  10,   5,   5,  10, -20, 100],
]


def evaluate_board(game, player):
    score = 0
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if game.board[r][c] == player:
                score += POSITION_WEIGHTS[r][c]
            elif game.board[r][c] == player.opponent():
                score -= POSITION_WEIGHTS[r][c]
    return score


def ai_move(game, depth=2):
    # depth層minimax搜索
    log.info(f"AI ({game.current_player.name}) 思考中 (depth={depth}) ...")
    best_score = float("-inf")
    best_move = None
    moves = game.get_valid_moves()
    if not moves:
        return None
    for r, c in moves:
        sim = game.clone()
        sim.apply_move(r, c)
        if sim.game_over:
            sc = evaluate_board(sim, game.current_player) * 10
        else:
            sc = -_negamax(sim, depth - 1, float("-inf"), float("inf"),
                           game.current_player.opponent(),
                           game.current_player)
        if sc > best_score:
            best_score = sc
            best_move = (r, c)
    if best_move is not None:
        log.info(f"AI 選擇 ({best_move[0]},{best_move[1]}) 分數={best_score:.1f}")
    return best_move


def _negamax(game, depth, alpha, beta, player, root_player):
    if depth == 0:
        return evaluate_board(game, root_player) if player == root_player else -evaluate_board(game, root_player)
    moves = game.get_valid_moves()
    if not moves:
        sim = game.clone()
        sim._next_turn()
        if sim.game_over:
            sc = evaluate_board(sim, root_player)
            return sc * 100
        return -_negamax(sim, depth - 1, -beta, -alpha,
                         root_player if sim.current_player == root_player else root_player.opponent(),
                         root_player)
    for r, c in moves:
        sim = game.clone()
        sim.apply_move(r, c)
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

class OthelloUI:
    def __init__(self, ai_enabled=True, ai_depth=2):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Othello / Reversi")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("arial", 20, bold=True)
        self.font_small = pygame.font.SysFont("arial", 16)
        self.font_big = pygame.font.SysFont("arial", 40, bold=True)
        self.game = OthelloGame()
        self.ai_enabled = ai_enabled
        self.ai_depth = ai_depth
        self.ai_player: Player | None = Player.WHITE
        self.human_player = Player.BLACK
        self.running = True
        self.show_hints = True
        self.message = ""
        self.message_timer = 0
        self.hint_surface: pygame.Surface = pygame.Surface((1, 1), pygame.SRCALPHA)

        self._make_hint_surface()

    def _make_hint_surface(self):
        size = CELL_SIZE // 4
        self.hint_surface = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(self.hint_surface, (255, 255, 100, 100),
                           (size // 2, size // 2), size // 2)

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
                if event.key == pygame.K_h:
                    self.show_hints = not self.show_hints
                    log.info(f"提示 {'開啟' if self.show_hints else '關閉'}")
                elif event.key == pygame.K_r and self.game.game_over:
                    self.game = OthelloGame()
                    log.info("重新開始遊戲")
                elif event.key == pygame.K_ESCAPE:
                    self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not self.game.game_over:
                if self.ai_enabled and self.game.current_player == self.ai_player:
                    return
                mx, my = event.pos
                col = (mx - MARGIN) // CELL_SIZE
                row = (my - MARGIN) // CELL_SIZE
                if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
                    if self.game.apply_move(row, col):
                        self.message = ""
                    else:
                        self.message = "無效移動!"
                        self.message_timer = 60

    def _update(self):
        if self.game.game_over:
            return
        if self.ai_enabled and self.game.current_player == self.ai_player:
            move = ai_move(self.game, self.ai_depth)
            if move:
                pygame.time.wait(300)
                self.game.apply_move(move[0], move[1])

    def _draw(self):
        self.screen.fill(COLOR_BG)
        self._draw_board()
        self._draw_pieces()
        if self.show_hints and not self.game.game_over:
            self._draw_hints()
        self._draw_info()
        if self.game.game_over:
            self._draw_game_over()
        pygame.display.flip()

    def _draw_board(self):
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                x = MARGIN + c * CELL_SIZE
                y = MARGIN + r * CELL_SIZE
                color = COLOR_BOARD if (r + c) % 2 == 0 else COLOR_BG
                pygame.draw.rect(self.screen, color, (x, y, CELL_SIZE, CELL_SIZE))
                pygame.draw.rect(self.screen, COLOR_LINE, (x, y, CELL_SIZE, CELL_SIZE), 1)

    def _draw_pieces(self):
        piece_radius = CELL_SIZE // 2 - 4
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                if self.game.board[r][c] == Player.EMPTY:
                    continue
                cx = MARGIN + c * CELL_SIZE + CELL_SIZE // 2
                cy = MARGIN + r * CELL_SIZE + CELL_SIZE // 2
                color = COLOR_BLACK if self.game.board[r][c] == Player.BLACK else COLOR_WHITE
                pygame.draw.circle(self.screen, color, (cx, cy), piece_radius)
                pygame.draw.circle(self.screen, (100, 100, 100), (cx, cy), piece_radius, 1)

    def _draw_hints(self):
        moves = self.game.get_valid_moves()
        size = CELL_SIZE // 4
        for r, c in moves:
            x = MARGIN + c * CELL_SIZE + (CELL_SIZE - size) // 2
            y = MARGIN + r * CELL_SIZE + (CELL_SIZE - size) // 2
            self.screen.blit(self.hint_surface, (x, y))

    def _draw_info(self):
        # 資訊列背景
        info_y = MARGIN + BOARD_SIZE * CELL_SIZE
        pygame.draw.rect(self.screen, COLOR_BG_TEXT,
                         (0, info_y, WINDOW_WIDTH, INFO_HEIGHT))
        scores = self.game.get_scores()

        # 分數
        txt = self.font.render(f"黑: {scores[Player.BLACK]}", True, COLOR_BLACK)
        self.screen.blit(txt, (20, info_y + 10))
        txt = self.font.render(f"白: {scores[Player.WHITE]}", True, COLOR_WHITE)
        self.screen.blit(txt, (20, info_y + 35))

        # 當前玩家
        if not self.game.game_over:
            color = COLOR_BLACK if self.game.current_player == Player.BLACK else COLOR_WHITE
            label = "AI" if (self.ai_enabled and self.game.current_player == self.ai_player) else "你"
            txt = self.font.render(f"輪到: {label} ({self.game.current_player.name})", True, color)
            self.screen.blit(txt, (150, info_y + 10))

        # 提示
        hint_label = "提示:ON (H切換)" if self.show_hints else "提示:OFF (H切換)"
        txt = self.font_small.render(hint_label, True, (180, 180, 180))
        self.screen.blit(txt, (150, info_y + 40))

        # 訊息
        if self.message:
            txt = self.font.render(self.message, True, (255, 100, 100))
            self.screen.blit(txt, (WINDOW_WIDTH // 2 - 50, info_y + 10))
            self.message_timer -= 1
            if self.message_timer <= 0:
                self.message = ""

    def _draw_game_over(self):
        overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.screen.blit(overlay, (0, 0))
        scores = self.game.get_scores()
        if self.game.winner:
            msg = f"{self.game.winner.name} 獲勝! ({scores[Player.BLACK]} - {scores[Player.WHITE]})"
        else:
            msg = f"平局! ({scores[Player.BLACK]} - {scores[Player.WHITE]})"
        txt = self.font_big.render(msg, True, (255, 255, 100))
        rect = txt.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 20))
        self.screen.blit(txt, rect)
        txt = self.font.render("按 R 重新開始, ESC 離開", True, (200, 200, 200))
        rect = txt.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 30))
        self.screen.blit(txt, rect)


# ---------------------------------------------------------------------------
# Entry point — 使腳本接收輸入參數
# ---------------------------------------------------------------------------
def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Othello/Reversi 遊戲原型")
    parser.add_argument("--two-player", action="store_true",
                        help="雙人模式 (預設: 對抗AI)")
    parser.add_argument("--depth", type=int, default=2, choices=[1, 2, 3],
                        help="AI 搜索深度 (預設: 2)")
    parser.add_argument("--first", choices=["black", "white"], default="black",
                        help="玩家執棋顏色 (預設: black)")
    return parser.parse_args(argv)


def main():
    # Constraint: 使腳本接收輸入參數
    args = parse_args()
    log.info(f"參數: two_player={args.two_player}, depth={args.depth}, first={args.first}")

    ai_enabled = not args.two_player
    human_player = Player.BLACK if args.first == "black" else Player.WHITE

    ui = OthelloUI(ai_enabled=ai_enabled, ai_depth=args.depth)
    ui.human_player = human_player
    ui.ai_player = human_player.opponent() if ai_enabled else None

    log.info("啟動 Othello 遊戲")
    ui.run()


if __name__ == "__main__":
    main()
