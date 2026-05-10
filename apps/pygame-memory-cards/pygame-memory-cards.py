"""
Memory Cards - Pygame memory card matching game.

Flip cards to find matching pairs. Minimalist style with flip animation.

Usage:
    python pygame-memory-cards.py [--rows ROWS] [--cols COLS] [--delay DELAY]

Options:
    --rows ROWS     Number of rows (default: 4, total cards must be even)
    --cols COLS     Number of columns (default: 4)
    --delay DELAY   Seconds before unmatched cards flip back (default: 1.0)
"""

import argparse
import logging
import random
import sys
from enum import auto, Enum

import pygame

logger = logging.getLogger("memory-cards")

# Visual constants
CARD_W = 90
CARD_H = 110
CARD_GAP = 12
PADDING = 12
TEXT_AREA = 40
FLIP_TIME = 0.3

COLORS = {
    "bg": (44, 62, 80),
    "card_back": (52, 73, 94),
    "card_border": (236, 240, 241),
    "card_front": (255, 255, 255),
    "text": (44, 62, 80),
    "matched": (39, 174, 96),
    "status": (189, 195, 199),
}


class CardState(Enum):
    HIDDEN = auto()
    FLIPPING = auto()
    REVEALED = auto()
    MATCHED = auto()


class Card:
    def __init__(self, value, row, col):
        self.value = value
        self.row = row
        self.col = col
        self.state = CardState.HIDDEN
        self.anim_t = 0.0
        self.anim_reveal = True

    @property
    def rect(self):
        x = PADDING + self.col * (CARD_W + CARD_GAP)
        y = PADDING + self.row * (CARD_H + CARD_GAP)
        return pygame.Rect(x, y, CARD_W, CARD_H)

    def flip(self, reveal):
        self.state = CardState.FLIPPING
        self.anim_t = 0.0
        self.anim_reveal = reveal

    def update(self, dt):
        if self.state != CardState.FLIPPING:
            return
        self.anim_t = min(self.anim_t + dt, FLIP_TIME)
        if self.anim_t >= FLIP_TIME:
            self.state = CardState.REVEALED if self.anim_reveal else CardState.HIDDEN

    def draw(self, surface, font):
        r = self.rect
        progress = self.anim_t / FLIP_TIME if self.state == CardState.FLIPPING else 0.0

        showing_front = (
            self.state in (CardState.REVEALED, CardState.MATCHED)
            or (self.state == CardState.FLIPPING and self.anim_reveal == (progress >= 0.5))
        )

        if self.state == CardState.FLIPPING:
            if progress < 0.5:
                display_w = int(CARD_W * (1.0 - progress / 0.5))
            else:
                display_w = int(CARD_W * ((progress - 0.5) / 0.5))
        else:
            display_w = CARD_W

        draw_r = pygame.Rect(
            r.x + (CARD_W - display_w) // 2, r.y, max(display_w, 2), CARD_H
        )

        if showing_front:
            pygame.draw.rect(surface, COLORS["card_front"], draw_r, border_radius=6)
            if display_w > 20:
                label = font.render(chr(65 + self.value), True, COLORS["text"])
                surface.blit(label, label.get_rect(center=draw_r.center))
            if self.state == CardState.MATCHED:
                pygame.draw.rect(surface, COLORS["matched"], draw_r, 3, border_radius=6)
        else:
            pygame.draw.rect(surface, COLORS["card_back"], draw_r, border_radius=6)
            pygame.draw.rect(surface, COLORS["card_border"], draw_r, 2, border_radius=6)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Memory Cards - Pygame memory card matching game"
    )
    parser.add_argument(
        "--rows", type=int, default=4, help="Number of rows (default: 4)"
    )
    parser.add_argument(
        "--cols", type=int, default=4, help="Number of columns (default: 4)"
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=1.0,
        help="Seconds before unmatched cards flip back (default: 1.0)",
    )
    parser.add_argument(
        "--debug", action="store_true", help="Enable debug logging"
    )
    return parser.parse_args()


def main():
    args = parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.debug else logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )

    total = args.rows * args.cols
    if total % 2 != 0:
        logger.error("Total cards (%d) must be even", total)
        sys.exit(1)
    if total < 2:
        logger.error("Need at least 2 cards")
        sys.exit(1)

    pygame.init()
    font = pygame.font.Font(None, 48)
    small_font = pygame.font.Font(None, 24)

    screen_w = PADDING * 2 + args.cols * (CARD_W + CARD_GAP) - CARD_GAP
    screen_h = PADDING * 2 + args.rows * (CARD_H + CARD_GAP) - CARD_GAP + TEXT_AREA
    screen = pygame.display.set_mode((screen_w, screen_h))
    pygame.display.set_caption("Memory Cards")
    clock = pygame.time.Clock()

    pairs = total // 2
    values = list(range(pairs)) * 2
    random.shuffle(values)
    cards = [
        Card(values[row * args.cols + col], row, col)
        for row in range(args.rows)
        for col in range(args.cols)
    ]

    logger.info("Game: %dx%d, %d pairs, delay=%.1fs", args.rows, args.cols, pairs, args.delay)

    running = True
    selected = []
    mismatched = []
    mismatch_timer = 0.0
    matched_count = 0

    while running:
        dt = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if len(selected) < 2 and not mismatched:
                    pos = event.pos
                    for card in cards:
                        if card.state != CardState.HIDDEN:
                            continue
                        if card.rect.collidepoint(pos):
                            card.flip(True)
                            selected.append(card)
                            logger.debug(
                                "Flipped card at (%d,%d) value=%d",
                                card.row, card.col, card.value,
                            )
                            break

        for card in cards:
            card.update(dt)

        if mismatched:
            mismatch_timer -= dt
            if mismatch_timer <= 0:
                for c in mismatched:
                    c.flip(False)
                mismatched = []
                selected = []

        if len(selected) == 2 and not mismatched:
            c1, c2 = selected
            if c1.state == CardState.REVEALED and c2.state == CardState.REVEALED:
                if c1.value == c2.value:
                    c1.state = CardState.MATCHED
                    c2.state = CardState.MATCHED
                    matched_count += 1
                    selected = []
                    logger.info("Match! (%d/%d)", matched_count, pairs)
                    if matched_count == pairs:
                        logger.info("Game over! All pairs matched.")
                else:
                    mismatched = [c1, c2]
                    mismatch_timer = args.delay

        screen.fill(COLORS["bg"])
        for card in cards:
            card.draw(screen, font)

        status = small_font.render(
            f"Pairs: {matched_count}/{pairs}", True, COLORS["status"]
        )
        screen.blit(status, (PADDING, screen_h - TEXT_AREA // 2 - 8))

        if matched_count == pairs:
            msg = font.render("You Win!", True, COLORS["matched"])
            msg_rect = msg.get_rect(
                center=(screen_w // 2, screen_h - TEXT_AREA // 2)
            )
            screen.blit(msg, msg_rect)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
