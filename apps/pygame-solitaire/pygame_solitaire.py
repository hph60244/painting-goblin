import argparse
import logging
import random
import sys

import pygame

# Constraint: 使用Pygame - 適合製作2D遊戲原型
# Constraint: 用極簡風格呈現 - 強調玩法概念，節省製作時間
# Constraint: 使用logger輸出訊息 - 用於人類跟AI除錯

WINDOW_TITLE = "Solitaire (Klondike)"
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 620
FPS = 60

CARD_WIDTH = 71
CARD_HEIGHT = 96
HORIZONTAL_GAP = 18
VERTICAL_GAP_FACEUP = 28
VERTICAL_GAP_FACEDOWN = 18
MARGIN_X = 10
TOP_Y = 10
TABLEAU_Y = 135

COLUMN_STEP = CARD_WIDTH + HORIZONTAL_GAP

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_GREEN = (0, 100, 0)
LIGHT_GREEN = (0, 128, 0)
GRAY = (180, 180, 180)
DARK_GRAY = (100, 100, 100)
LIGHT_YELLOW = (255, 255, 200)
RED = (200, 30, 30)
BLUE = (30, 60, 180)
GOLD = (218, 165, 32)
CARD_BACK = (30, 80, 160)

SUITS = ['♠', '♥', '♦', '♣']
SUIT_NAMES = ['spades', 'hearts', 'diamonds', 'clubs']
RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']

RED_SUITS = {1, 2}  # hearts, diamonds


class Card:
    def __init__(self, suit_idx, rank_idx):
        self.suit_idx = suit_idx
        self.rank_idx = rank_idx
        self.face_up = False
        self.suit = SUITS[suit_idx]
        self.rank = RANKS[rank_idx]
        self.is_red = suit_idx in RED_SUITS

    @property
    def color(self):
        return RED if self.is_red else BLACK

    def __repr__(self):
        return f"{self.rank}{self.suit}"


class Game:
    def __init__(self, args):
        self.logger = logging.getLogger("Solitaire")
        self.logger.setLevel(getattr(logging, args.log_level.upper(), logging.INFO))
        self.draw_count = args.draw_count

        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 28)
        self.font_small = pygame.font.Font(None, 20)
        self.font_large = pygame.font.Font(None, 48)
        self.running = True

        self.dragging = False
        self.drag_cards = []
        self.drag_offset_x = 0
        self.drag_offset_y = 0
        self.drag_source = None
        self.drag_source_idx = 0
        self.message = ""
        self.message_timer = 0
        self.won = False

        self.stock = []
        self.waste = []
        self.foundations = [[] for _ in range(4)]
        self.tableau = [[] for _ in range(7)]

        self._deal()
        self.logger.info(
            "Game initialized: draw_count=%d",
            self.draw_count,
        )

    def _create_deck(self):
        deck = [Card(s, r) for s in range(4) for r in range(13)]
        random.shuffle(deck)
        return deck

    def _deal(self):
        deck = self._create_deck()
        self.logger.info("Deck shuffled, %d cards", len(deck))
        for col in range(7):
            for row in range(col + 1):
                card = deck.pop()
                if row == col:
                    card.face_up = True
                self.tableau[col].append(card)
        self.stock = deck
        self.logger.info("Dealt: stock=%d, tableau=%s",
                         len(self.stock),
                         [len(p) for p in self.tableau])

    def _get_card_at(self, pos):
        x, y = pos
        # Check tableau (iterate in reverse to get top cards first)
        for col in range(7):
            pile = self.tableau[col]
            px = MARGIN_X + col * COLUMN_STEP
            if px <= x <= px + CARD_WIDTH:
                for i in range(len(pile) - 1, -1, -1):
                    card = pile[i]
                    if not card.face_up:
                        py = TABLEAU_Y + (i) * VERTICAL_GAP_FACEDOWN
                    else:
                        face_down_count = sum(1 for c in pile if not c.face_up)
                        py = TABLEAU_Y + face_down_count * VERTICAL_GAP_FACEDOWN
                        py += (i - face_down_count) * VERTICAL_GAP_FACEUP
                    if py <= y <= py + CARD_HEIGHT:
                        if card.face_up:
                            return ('tableau', col, i)
                        else:
                            return None
        # Check waste
        wx = MARGIN_X + 1 * COLUMN_STEP
        if wx <= x <= wx + CARD_WIDTH and TOP_Y <= y <= TOP_Y + CARD_HEIGHT:
            if self.waste:
                return ('waste', 0, len(self.waste) - 1)
        # Check foundations
        for f in range(4):
            fx = MARGIN_X + (3 + f) * COLUMN_STEP
            if fx <= x <= fx + CARD_WIDTH and TOP_Y <= y <= TOP_Y + CARD_HEIGHT:
                if self.foundations[f]:
                    return ('foundation', f, len(self.foundations[f]) - 1)
        # Check stock
        sx = MARGIN_X + 0 * COLUMN_STEP
        if sx <= x <= sx + CARD_WIDTH and TOP_Y <= y <= TOP_Y + CARD_HEIGHT:
            if self.stock:
                return ('stock', 0, len(self.stock) - 1)
        return None

    def _get_tableau_target_col(self, x, y):
        for col in range(7):
            px = MARGIN_X + col * COLUMN_STEP
            if px <= x <= px + CARD_WIDTH:
                return col
        return None

    def _get_foundation_target(self, x, y):
        for f in range(4):
            fx = MARGIN_X + (3 + f) * COLUMN_STEP
            if fx <= x <= fx + CARD_WIDTH and TOP_Y <= y <= TOP_Y + CARD_HEIGHT:
                return f
        return None

    def _can_move_to_tableau(self, card, col):
        pile = self.tableau[col]
        if not pile:
            return card.rank_idx == 12
        top = pile[-1]
        if not top.face_up:
            return False
        return (top.rank_idx == card.rank_idx + 1 and
                top.is_red != card.is_red)

    def _can_move_to_foundation(self, card, f_idx):
        pile = self.foundations[f_idx]
        if not pile:
            return card.rank_idx == 0
        top = pile[-1]
        return (top.suit_idx == card.suit_idx and
                top.rank_idx == card.rank_idx - 1)

    def _is_valid_drag(self, source, idx):
        if source[0] == 'waste':
            return True
        elif source[0] == 'tableau':
            col, card_idx = source[1], source[2]
            pile = self.tableau[col]
            for i in range(card_idx, len(pile)):
                if not pile[i].face_up:
                    return False
                if i > card_idx:
                    prev = pile[i - 1]
                    curr = pile[i]
                    if (prev.rank_idx != curr.rank_idx + 1 or
                            prev.is_red == curr.is_red):
                        return False
            return True
        elif source[0] == 'foundation':
            return True
        return False

    def _draw_from_stock(self):
        if not self.stock and not self.waste:
            return
        if not self.stock:
            self.logger.debug("Recycling waste to stock")
            self.stock = list(reversed(self.waste))
            for c in self.stock:
                c.face_up = False
            self.waste = []
            return
        count = min(self.draw_count, len(self.stock))
        for _ in range(count):
            card = self.stock.pop()
            card.face_up = True
            self.waste.append(card)
        self.logger.debug("Drew %d card(s) from stock", count)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_r:
                    self._reset_game()
                elif event.key == pygame.K_d:
                    self._draw_from_stock()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.won:
                    if event.button == 1:
                        self._reset_game()
                    continue
                if event.button == 1:
                    hit = self._get_card_at(event.pos)
                    sx = MARGIN_X + 0 * COLUMN_STEP
                    ex, ey = event.pos
                    stock_area = (sx <= ex <= sx + CARD_WIDTH and TOP_Y <= ey <= TOP_Y + CARD_HEIGHT)
                    if stock_area:
                        self._draw_from_stock()
                    elif hit and self._is_valid_drag(hit, hit[2]):
                        self.dragging = True
                        self.drag_source = hit
                        self.drag_source_idx = hit[2]
                        cx, cy = event.pos
                        if hit[0] == 'tableau':
                            col = hit[1]
                            pile = self.tableau[col]
                            face_down = sum(1 for c in pile if not c.face_up)
                            card_y = TABLEAU_Y + face_down * VERTICAL_GAP_FACEDOWN
                            card_y += (hit[2] - face_down) * VERTICAL_GAP_FACEUP
                            self.drag_offset_x = cx - (MARGIN_X + col * COLUMN_STEP)
                            self.drag_offset_y = cy - card_y
                            self.drag_cards = pile[hit[2]:]
                        elif hit[0] == 'waste':
                            self.drag_offset_x = cx - (MARGIN_X + 1 * COLUMN_STEP)
                            self.drag_offset_y = cy - TOP_Y
                            self.drag_cards = [self.waste[-1]]
                        elif hit[0] == 'foundation':
                            self.drag_offset_x = cx - (MARGIN_X + (3 + hit[1]) * COLUMN_STEP)
                            self.drag_offset_y = cy - TOP_Y
                            self.drag_cards = [self.foundations[hit[1]][-1]]
                        self.logger.debug("Drag start: %s idx=%d cards=%s",
                                          hit, hit[2], self.drag_cards)
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.dragging:
                    self._finish_drag(event.pos)
            elif event.type == pygame.MOUSEMOTION:
                pass

    def _finish_drag(self, pos):
        x, y = pos
        if self.drag_source is None:
            self.dragging = False
            self.drag_cards = []
            return
        source_type, source_idx, _ = self.drag_source
        card = self.drag_cards[0]

        target_tableau = self._get_tableau_target_col(x, y)
        target_foundation = self._get_foundation_target(x, y)

        placed = False

        if target_tableau is not None:
            if self._can_move_to_tableau(card, target_tableau):
                self._do_move(source_type, source_idx, target_tableau, None)
                placed = True
                self.logger.debug("Moved %s to tableau col %d", card, target_tableau)

        if not placed and target_foundation is not None:
            if len(self.drag_cards) == 1 and self._can_move_to_foundation(card, target_foundation):
                self._do_move(source_type, source_idx, None, target_foundation)
                placed = True
                self.logger.debug("Moved %s to foundation %d", card, target_foundation)

        if not placed:
            self.logger.debug("Invalid drop, cancelling drag")

        self.dragging = False
        self.drag_cards = []
        self.drag_source = None

        self._check_win()

    def _do_move(self, source_type, source_idx, tcol, f_idx):
        if source_type == 'tableau':
            pile = self.tableau[source_idx]
            cards = pile[self.drag_source_idx:]
            del pile[self.drag_source_idx:]
            if pile and not pile[-1].face_up:
                pile[-1].face_up = True
                self.logger.debug("Flipped tableau[%d] top card", source_idx)
            if tcol is not None:
                self.tableau[tcol].extend(cards)
            elif f_idx is not None:
                self.foundations[f_idx].append(cards[0])
        elif source_type == 'waste':
            card = self.waste.pop()
            if tcol is not None:
                self.tableau[tcol].append(card)
            elif f_idx is not None:
                self.foundations[f_idx].append(card)
        elif source_type == 'foundation':
            card = self.foundations[source_idx].pop()
            if tcol is not None:
                self.tableau[tcol].append(card)

    def _check_win(self):
        if all(len(f) == 13 for f in self.foundations):
            self.won = True
            self.message = "You won! Click to play again"
            self.message_timer = -1
            self.logger.info("Game won!")

    def _reset_game(self):
        self.logger.info("Game reset")
        self.stock = []
        self.waste = []
        self.foundations = [[] for _ in range(4)]
        self.tableau = [[] for _ in range(7)]
        self.dragging = False
        self.drag_cards = []
        self.won = False
        self.message = ""
        self.message_timer = 0
        self._deal()

    def draw(self):
        self.screen.fill(DARK_GREEN)

        self._draw_foundation_slots()
        self._draw_stock()
        self._draw_waste()
        self._draw_tableau()

        if self.dragging:
            self._draw_drag_cards()

        self._draw_info()

        if self.won:
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
            overlay.set_alpha(180)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))
            text = self.font_large.render("You Won!", True, GOLD)
            text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 20))
            self.screen.blit(text, text_rect)
            sub = self.font.render("Click to play again", True, WHITE)
            sub_rect = sub.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 30))
            self.screen.blit(sub, sub_rect)

        pygame.display.flip()

    def _draw_card_back(self, x, y):
        rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
        pygame.draw.rect(self.screen, WHITE, rect)
        pygame.draw.rect(self.screen, BLACK, rect, 1)
        inner = rect.inflate(-8, -8)
        pygame.draw.rect(self.screen, CARD_BACK, inner)

    def _draw_card_face(self, x, y, card, highlight=False):
        rect = pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT)
        bg = LIGHT_YELLOW if highlight else WHITE
        pygame.draw.rect(self.screen, bg, rect)
        pygame.draw.rect(self.screen, BLACK, rect, 1)
        text = self.font.render(card.rank + card.suit, True, card.color)
        self.screen.blit(text, (x + 5, y + 4))
        text2 = self.font.render(card.rank + card.suit, True, card.color)
        self.screen.blit(text2, (x + CARD_WIDTH - 5 - text2.get_width(), y + CARD_HEIGHT - 4 - text2.get_height()))

    def _draw_foundation_slots(self):
        for f in range(4):
            fx = MARGIN_X + (3 + f) * COLUMN_STEP
            rect = pygame.Rect(fx, TOP_Y, CARD_WIDTH, CARD_HEIGHT)
            pygame.draw.rect(self.screen, (0, 80, 0), rect)
            pygame.draw.rect(self.screen, BLACK, rect, 1)
            is_dragging_f = (
                self.dragging and self.drag_source and
                self.drag_source[0] == 'foundation' and
                self.drag_source[1] == f
            )
            if self.foundations[f] and not is_dragging_f:
                self._draw_card_face(fx, TOP_Y, self.foundations[f][-1])
            else:
                suit = SUITS[f]
                text = self.font.render(suit, True, DARK_GRAY)
                tr = text.get_rect(center=rect.center)
                self.screen.blit(text, tr)

    def _draw_stock(self):
        sx = MARGIN_X + 0 * COLUMN_STEP
        if self.stock:
            self._draw_card_back(sx, TOP_Y)
        else:
            rect = pygame.Rect(sx, TOP_Y, CARD_WIDTH, CARD_HEIGHT)
            pygame.draw.rect(self.screen, (0, 80, 0), rect)
            pygame.draw.rect(self.screen, BLACK, rect, 1)
            if self.waste:
                text = self.font.render("↻", True, DARK_GRAY)
                tr = text.get_rect(center=rect.center)
                self.screen.blit(text, tr)

    def _draw_waste(self):
        wx = MARGIN_X + 1 * COLUMN_STEP
        if self.waste and not (self.dragging and self.drag_source and self.drag_source[0] == 'waste'):
            self._draw_card_face(wx, TOP_Y, self.waste[-1])
        elif not self.waste:
            rect = pygame.Rect(wx, TOP_Y, CARD_WIDTH, CARD_HEIGHT)
            pygame.draw.rect(self.screen, (0, 80, 0), rect)
            pygame.draw.rect(self.screen, BLACK, rect, 1)

    def _draw_tableau(self):
        for col in range(7):
            pile = self.tableau[col]
            if not pile:
                rect = pygame.Rect(MARGIN_X + col * COLUMN_STEP, TABLEAU_Y, CARD_WIDTH, CARD_HEIGHT)
                pygame.draw.rect(self.screen, (0, 80, 0), rect)
                pygame.draw.rect(self.screen, BLACK, rect, 1)
                continue
            face_down = sum(1 for c in pile if not c.face_up)
            for i, card in enumerate(pile):
                if not card.face_up:
                    py = TABLEAU_Y + i * VERTICAL_GAP_FACEDOWN
                    self._draw_card_back(MARGIN_X + col * COLUMN_STEP, py)
                else:
                    py = TABLEAU_Y + face_down * VERTICAL_GAP_FACEDOWN
                    py += (i - face_down) * VERTICAL_GAP_FACEUP
                    is_dragging_here = (
                        self.dragging and
                        self.drag_source and
                        self.drag_source[0] == 'tableau' and
                        self.drag_source[1] == col and
                        i >= self.drag_source[2]
                    )
                    if not is_dragging_here:
                        self._draw_card_face(MARGIN_X + col * COLUMN_STEP, py, card)

    def _draw_drag_cards(self):
        if not self.dragging or not self.drag_cards:
            return
        mx, my = pygame.mouse.get_pos()
        dx = mx - self.drag_offset_x
        dy = my - self.drag_offset_y
        for i, card in enumerate(self.drag_cards):
            self._draw_card_face(dx, dy + i * VERTICAL_GAP_FACEUP, card, highlight=True)

    def _draw_info(self):
        text = self.font_small.render(
            f"Stock: {len(self.stock)}  Waste: {len(self.waste)}  "
            f"[D]raw  [R]eset  ESC=quit",
            True, WHITE,
        )
        self.screen.blit(text, (10, WINDOW_HEIGHT - 25))

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
        "--draw-count", type=int, default=1, choices=[1, 3],
        help="Cards drawn from stock each click (1 or 3, default: %(default)s)",
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
