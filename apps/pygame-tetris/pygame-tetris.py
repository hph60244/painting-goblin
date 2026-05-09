import argparse
import logging
import random
import sys

import pygame

logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(name)s:%(message)s")
logger = logging.getLogger("tetris")

COLS = 10
ROWS = 20
CELL = 30

SRS_WALL_KICKS_JLSTZ = {
    (0, 1): [(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)],
    (1, 0): [(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)],
    (1, 2): [(0, 0), (1, 0), (1, -1), (0, 2), (1, 2)],
    (2, 1): [(0, 0), (-1, 0), (-1, 1), (0, -2), (-1, -2)],
    (2, 3): [(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)],
    (3, 2): [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)],
    (3, 0): [(0, 0), (-1, 0), (-1, -1), (0, 2), (-1, 2)],
    (0, 3): [(0, 0), (1, 0), (1, 1), (0, -2), (1, -2)],
}

SRS_WALL_KICKS_I = {
    (0, 1): [(0, 0), (-2, 0), (1, 0), (-2, -1), (1, 2)],
    (1, 0): [(0, 0), (2, 0), (-1, 0), (2, 1), (-1, -2)],
    (1, 2): [(0, 0), (-1, 0), (2, 0), (-1, 2), (2, -1)],
    (2, 1): [(0, 0), (1, 0), (-2, 0), (1, -2), (-2, 1)],
    (2, 3): [(0, 0), (2, 0), (-1, 0), (2, 1), (-1, -2)],
    (3, 2): [(0, 0), (-2, 0), (1, 0), (-2, -1), (1, 2)],
    (3, 0): [(0, 0), (1, 0), (-2, 0), (1, -2), (-2, 1)],
    (0, 3): [(0, 0), (-1, 0), (2, 0), (-1, 2), (2, -1)],
}

PIECES = {
    "I": {
        "cells": [
            [(0, 1), (1, 1), (2, 1), (3, 1)],
            [(2, 0), (2, 1), (2, 2), (2, 3)],
            [(0, 2), (1, 2), (2, 2), (3, 2)],
            [(1, 0), (1, 1), (1, 2), (1, 3)],
        ],
        "color": (0, 255, 255),
    },
    "O": {
        "cells": [
            [(1, 0), (2, 0), (1, 1), (2, 1)],
            [(1, 0), (2, 0), (1, 1), (2, 1)],
            [(1, 0), (2, 0), (1, 1), (2, 1)],
            [(1, 0), (2, 0), (1, 1), (2, 1)],
        ],
        "color": (255, 255, 0),
    },
    "T": {
        "cells": [
            [(1, 0), (0, 1), (1, 1), (2, 1)],
            [(1, 0), (1, 1), (2, 1), (1, 2)],
            [(0, 1), (1, 1), (2, 1), (1, 2)],
            [(1, 0), (0, 1), (1, 1), (1, 2)],
        ],
        "color": (128, 0, 128),
    },
    "S": {
        "cells": [
            [(1, 0), (2, 0), (0, 1), (1, 1)],
            [(1, 0), (1, 1), (2, 1), (2, 2)],
            [(1, 1), (2, 1), (0, 2), (1, 2)],
            [(0, 0), (0, 1), (1, 1), (1, 2)],
        ],
        "color": (0, 255, 0),
    },
    "Z": {
        "cells": [
            [(0, 0), (1, 0), (1, 1), (2, 1)],
            [(2, 0), (1, 1), (2, 1), (1, 2)],
            [(0, 1), (1, 1), (1, 2), (2, 2)],
            [(1, 0), (0, 1), (1, 1), (0, 2)],
        ],
        "color": (255, 0, 0),
    },
    "J": {
        "cells": [
            [(0, 0), (0, 1), (1, 1), (2, 1)],
            [(1, 0), (2, 0), (1, 1), (1, 2)],
            [(0, 1), (1, 1), (2, 1), (2, 2)],
            [(1, 0), (1, 1), (0, 2), (1, 2)],
        ],
        "color": (0, 0, 255),
    },
    "L": {
        "cells": [
            [(2, 0), (0, 1), (1, 1), (2, 1)],
            [(1, 0), (1, 1), (1, 2), (2, 2)],
            [(0, 1), (1, 1), (2, 1), (0, 2)],
            [(0, 0), (1, 0), (1, 1), (1, 2)],
        ],
        "color": (255, 165, 0),
    },
}

PIECE_NAMES = ["I", "O", "T", "S", "Z", "J", "L"]

SCORES = {1: 100, 2: 300, 3: 500, 4: 800}

LEVEL_SPEEDS = [
    48, 43, 38, 33, 28, 23, 18, 13, 8, 6,
    5, 5, 5, 4, 4, 4, 3, 3, 3, 2,
    2, 2, 2, 2, 2, 2, 2, 2, 2, 1,
]


class Tetris:
    def __init__(self, cols=COLS, rows=ROWS, cell=CELL, start_level=1):
        self.cols = cols
        self.rows = rows
        self.cell = cell
        self.grid = [[None for _ in range(cols)] for _ in range(rows)]
        self.score = 0
        self.level = start_level
        self.lines_cleared = 0
        self.game_over = False
        self.bag = []
        self.current_piece = None
        self.current_x = 0
        self.current_y = 0
        self.current_rotation = 0
        self.next_piece = None
        self.lock_delay = 0
        self._fill_bag()
        self.next_piece = self.bag[-1] if self.bag else None
        self._spawn_piece()

    def _fill_bag(self):
        if not self.bag:
            self.bag = PIECE_NAMES[:]
            random.shuffle(self.bag)

    def _spawn_piece(self):
        self._fill_bag()
        name = self.bag.pop()
        self.current_piece = name
        self.current_rotation = 0
        if name == "I":
            self.current_x = 3
            self.current_y = -1
        elif name == "O":
            self.current_x = 4
            self.current_y = 0
        else:
            self.current_x = 3
            self.current_y = 0
        self.lock_delay = 0
        self.next_piece = self.bag[-1] if self.bag else None
        if self._collides(self.current_piece, self.current_rotation, self.current_x, self.current_y):
            self.game_over = True
            logger.info("Game over")

    def _get_cells(self, name, rotation, x, y):
        offsets = PIECES[name]["cells"][rotation]
        return [(x + ox, y + oy) for ox, oy in offsets]

    def _collides(self, name, rotation, x, y):
        for cx, cy in self._get_cells(name, rotation, x, y):
            if cx < 0 or cx >= self.cols:
                return True
            if cy >= self.rows:
                return True
            if cy >= 0 and self.grid[cy][cx] is not None:
                return True
        return False

    def _try_move(self, dx, dy):
        if self.game_over:
            return False
        if not self._collides(self.current_piece, self.current_rotation, self.current_x + dx, self.current_y + dy):
            self.current_x += dx
            self.current_y += dy
            return True
        return False

    def move_left(self):
        self._try_move(-1, 0)

    def move_right(self):
        self._try_move(1, 0)

    def soft_drop(self):
        if self._try_move(0, 1):
            self.score += 1
            return True
        return False

    def hard_drop(self):
        if self.game_over:
            return
        while self._try_move(0, 1):
            self.score += 2
        self._lock_piece()

    def rotate(self, direction=1):
        if self.game_over:
            return
        name = self.current_piece
        old_rot = self.current_rotation
        new_rot = (old_rot + direction) % 4
        kicks = SRS_WALL_KICKS_I if name == "I" else SRS_WALL_KICKS_JLSTZ
        key = (old_rot, new_rot)
        if key in kicks:
            for dx, dy in kicks[key]:
                if not self._collides(name, new_rot, self.current_x + dx, self.current_y - dy):
                    self.current_x += dx
                    self.current_y -= dy
                    self.current_rotation = new_rot
                    return

    def _lock_piece(self):
        for cx, cy in self._get_cells(
            self.current_piece, self.current_rotation, self.current_x, self.current_y
        ):
            if 0 <= cy < self.rows:
                self.grid[cy][cx] = self.current_piece
        self._clear_lines()
        self._spawn_piece()

    def _clear_lines(self):
        cleared = 0
        for y in range(self.rows - 1, -1, -1):
            if all(cell is not None for cell in self.grid[y]):
                del self.grid[y]
                self.grid.insert(0, [None for _ in range(self.cols)])
                cleared += 1
        if cleared > 0:
            self.lines_cleared += cleared
            self.score += SCORES.get(cleared, 0) * self.level
            self.level = 1 + self.lines_cleared // 10
            logger.info("Cleared %d lines, level %d, score %d", cleared, self.level, self.score)

    def get_ghost_y(self):
        y = self.current_y
        while not self._collides(self.current_piece, self.current_rotation, self.current_x, y + 1):
            y += 1
        return y

    def update(self):
        if self.game_over:
            return
        frame_speed = LEVEL_SPEEDS[min(self.level - 1, len(LEVEL_SPEEDS) - 1)]
        self.lock_delay += 1
        if self.lock_delay >= frame_speed:
            self.lock_delay = 0
            if not self._try_move(0, 1):
                self._lock_piece()


def draw_grid(screen, tetris, cell):
    for y in range(tetris.rows):
        for x in range(tetris.cols):
            rect = pygame.Rect(x * cell, y * cell, cell, cell)
            pygame.draw.rect(screen, (40, 40, 40), rect, 1)

    for y in range(tetris.rows):
        for x in range(tetris.cols):
            piece_name = tetris.grid[y][x]
            if piece_name:
                color = PIECES[piece_name]["color"]
                rect = pygame.Rect(x * cell, y * cell, cell, cell)
                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, (255, 255, 255), rect, 1)

    if tetris.current_piece and not tetris.game_over:
        piece = tetris.current_piece
        ghost_y = tetris.get_ghost_y()
        ghost_cells = tetris._get_cells(piece, tetris.current_rotation, tetris.current_x, ghost_y)
        for cx, cy in ghost_cells:
            if cy >= 0:
                rect = pygame.Rect(cx * cell, cy * cell, cell, cell)
                pygame.draw.rect(screen, (80, 80, 80), rect)
                pygame.draw.rect(screen, (60, 60, 60), rect, 1)

        cells = tetris._get_cells(piece, tetris.current_rotation, tetris.current_x, tetris.current_y)
        color = PIECES[piece]["color"]
        for cx, cy in cells:
            if cy >= 0:
                rect = pygame.Rect(cx * cell, cy * cell, cell, cell)
                pygame.draw.rect(screen, color, rect)
                pygame.draw.rect(screen, (255, 255, 255), rect, 1)


def draw_sidebar(screen, tetris, cell, cols):
    sidebar_x = cols * cell + 20
    font = pygame.font.SysFont("Arial", 18, bold=True)
    big_font = pygame.font.SysFont("Arial", 14)

    texts = [
        ("NEXT", big_font, (255, 255, 255), sidebar_x, 20),
        ("SCORE", big_font, (255, 255, 255), sidebar_x, 140),
        (str(tetris.score), big_font, (255, 255, 0), sidebar_x, 160),
        ("LEVEL", big_font, (255, 255, 255), sidebar_x, 200),
        (str(tetris.level), big_font, (255, 255, 0), sidebar_x, 220),
        ("LINES", big_font, (255, 255, 255), sidebar_x, 260),
        (str(tetris.lines_cleared), big_font, (255, 255, 0), sidebar_x, 280),
    ]
    for text, fnt, color, sx, sy in texts:
        surf = fnt.render(text, True, color)
        screen.blit(surf, (sx, sy))

    if tetris.next_piece:
        name = tetris.next_piece
        cells = PIECES[name]["cells"][0]
        color = PIECES[name]["color"]
        preview_cell = 20
        min_x = min(c[0] for c in cells)
        min_y = min(c[1] for c in cells)
        for cx, cy in cells:
            rect = pygame.Rect(
                sidebar_x + (cx - min_x) * preview_cell,
                40 + (cy - min_y) * preview_cell,
                preview_cell, preview_cell,
            )
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, (255, 255, 255), rect, 1)

    if tetris.game_over:
        surf = big_font.render("GAME OVER", True, (255, 0, 0))
        screen.blit(surf, (sidebar_x, 320))


def main():
    parser = argparse.ArgumentParser(description="Tetris game prototype")
    parser.add_argument("--cols", type=int, default=COLS, help="Grid columns")
    parser.add_argument("--rows", type=int, default=ROWS, help="Grid rows")
    parser.add_argument("--cell", type=int, default=CELL, help="Cell size in pixels")
    parser.add_argument("--level", type=int, default=1, help="Starting level")
    parser.add_argument("--fps", type=int, default=60, help="Target FPS")
    args = parser.parse_args()

    logger.info("Starting Tetris with args: %s", args)

    cell = args.cell
    cols = args.cols
    rows = args.rows
    screen_width = cols * cell + 180
    screen_height = rows * cell

    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()

    tetris = Tetris(cols=cols, rows=rows, cell=cell, start_level=args.level)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    tetris.move_left()
                elif event.key == pygame.K_RIGHT:
                    tetris.move_right()
                elif event.key == pygame.K_DOWN:
                    tetris.soft_drop()
                elif event.key == pygame.K_UP:
                    tetris.rotate(1)
                elif event.key == pygame.K_z:
                    tetris.rotate(-1)
                elif event.key == pygame.K_SPACE:
                    tetris.hard_drop()
                elif event.key == pygame.K_r and tetris.game_over:
                    tetris = Tetris(cols=cols, rows=rows, cell=cell, start_level=args.level)
                elif event.key == pygame.K_ESCAPE:
                    running = False

        tetris.update()

        screen.fill((0, 0, 0))
        draw_grid(screen, tetris, cell)
        draw_sidebar(screen, tetris, cell, cols)
        pygame.display.flip()
        clock.tick(args.fps)

    pygame.quit()
    logger.info("Tetris exited")


if __name__ == "__main__":
    main()
