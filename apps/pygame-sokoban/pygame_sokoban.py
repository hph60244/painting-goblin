import argparse
import logging
import sys
import os

import pygame

WINDOW_TITLE = "Sokoban"
FPS = 60
CELL_SIZE = 64

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
DARK_GRAY = (60, 60, 60)
BG_COLOR = (40, 40, 40)
WALL_COLOR = (120, 100, 80)
FLOOR_COLOR = (60, 60, 50)
GOAL_COLOR = (200, 80, 80)
BOX_COLOR = (180, 150, 100)
BOX_ON_GOAL_COLOR = (120, 180, 120)
PLAYER_COLOR = (220, 200, 80)
PLAYER_ON_GOAL_COLOR = (220, 220, 100)

DIRECTION_MAP = {
    pygame.K_UP: (0, -1),
    pygame.K_DOWN: (0, 1),
    pygame.K_LEFT: (-1, 0),
    pygame.K_RIGHT: (1, 0),
}


class Level:
    def __init__(self, filepath):
        self.logger = logging.getLogger("Sokoban.Level")
        self.filepath = filepath
        self.width = 0
        self.height = 0
        self.walls = set()
        self.goals = set()
        self.boxes = set()
        self.player_pos = None
        self._load(filepath)

    def _load(self, filepath):
        self.logger.info("Loading level from %s", filepath)
        with open(filepath, "r") as f:
            lines = [line.rstrip("\n") for line in f.readlines()]

        self.height = len(lines)
        self.width = max(len(line) for line in lines)
        self.walls.clear()
        self.goals.clear()
        self.boxes.clear()
        self.player_pos = None

        for y, line in enumerate(lines):
            for x, ch in enumerate(line):
                if ch == "#":
                    self.walls.add((x, y))
                elif ch == ".":
                    self.goals.add((x, y))
                elif ch == "$":
                    self.boxes.add((x, y))
                elif ch == "@":
                    self.player_pos = (x, y)
                elif ch == "+":
                    self.player_pos = (x, y)
                    self.goals.add((x, y))
                elif ch == "*":
                    self.boxes.add((x, y))
                    self.goals.add((x, y))

        self.logger.info(
            "Level loaded: %dx%d, walls=%d, goals=%d, boxes=%d, player=%s",
            self.width, self.height, len(self.walls), len(self.goals),
            len(self.boxes), self.player_pos,
        )

    def is_wall(self, x, y):
        return (x, y) in self.walls

    def is_box(self, x, y):
        return (x, y) in self.boxes

    def is_goal(self, x, y):
        return (x, y) in self.goals

    def is_complete(self):
        return self.goals and self.goals.issubset(self.boxes)

    def clone_state(self):
        return {
            "player": self.player_pos,
            "boxes": frozenset(self.boxes),
        }

    def restore_state(self, state):
        self.player_pos = state["player"]
        self.boxes = set(state["boxes"])


class Game:
    def __init__(self, args):
        self.logger = logging.getLogger("Sokoban")
        self.logger.setLevel(getattr(logging, args.log_level.upper(), logging.INFO))
        self.cell_size = args.cell_size
        self.level_file = args.level
        self.push_count = 0
        self.move_count = 0
        self.undo_stack = []
        self.won = False

        if not os.path.isfile(self.level_file):
            self.logger.error("Level file not found: %s", self.level_file)
            sys.exit(1)

        self.level = Level(self.level_file)
        self._init_display()

    def _init_display(self):
        board_width = self.level.width * self.cell_size
        board_height = self.level.height * self.cell_size
        self.window_width = board_width + self.cell_size
        self.window_height = board_height + self.cell_size + 60

        pygame.init()
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 28)
        self.font_small = pygame.font.Font(None, 22)
        self.running = True

        self.logger.info(
            "Display initialized: %dx%d, cell=%dpx",
            self.window_width, self.window_height, self.cell_size,
        )

    def _save_state(self):
        self.undo_stack.append(self.level.clone_state())

    def _undo(self):
        if not self.undo_stack:
            self.logger.debug("Nothing to undo")
            return
        state = self.undo_stack.pop()
        old_boxes = self.level.boxes
        self.level.restore_state(state)
        self.logger.debug("Undo: player=%s, boxes=%s", state["player"], state["boxes"])
        self.won = False

    def _try_move(self, dx, dy):
        if self.level.player_pos is None:
            return False
        px, py = self.level.player_pos
        nx, ny = px + dx, py + dy

        if self.level.is_wall(nx, ny):
            self.logger.debug("Blocked by wall at (%d,%d)", nx, ny)
            return False

        if self.level.is_box(nx, ny):
            bx, by = nx + dx, ny + dy
            if self.level.is_wall(bx, by) or self.level.is_box(bx, by):
                self.logger.debug("Box blocked at (%d,%d)", bx, by)
                return False
            self._save_state()
            self.level.boxes.remove((nx, ny))
            self.level.boxes.add((bx, by))
            self.level.player_pos = (nx, ny)
            self.push_count += 1
            self.move_count += 1
            self.logger.debug(
                "Push: box (%d,%d)->(%d,%d), player (%d,%d)->(%d,%d)",
                nx, ny, bx, by, px, py, nx, ny,
            )
            if self.level.is_complete():
                self.won = True
                self.logger.info("Level complete! Pushes: %d, Moves: %d", self.push_count, self.move_count)
            return True

        self._save_state()
        self.level.player_pos = (nx, ny)
        self.move_count += 1
        self.logger.debug("Move: player (%d,%d)->(%d,%d)", px, py, nx, ny)
        return True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_r:
                    self.reset_game()
                elif event.key == pygame.K_z and not self.won:
                    self._undo()
                elif event.key in DIRECTION_MAP and not self.won:
                    dx, dy = DIRECTION_MAP[event.key]
                    self._try_move(dx, dy)

    def reset_game(self):
        self.logger.info("Resetting level")
        self.undo_stack.clear()
        self.push_count = 0
        self.move_count = 0
        self.won = False
        self.level = Level(self.level_file)

    def draw(self):
        self.screen.fill(BG_COLOR)

        offset_x = (self.cell_size // 2)
        offset_y = (self.cell_size // 2)

        for y in range(self.level.height):
            for x in range(self.level.width):
                rx = offset_x + x * self.cell_size
                ry = offset_y + y * self.cell_size
                rect = pygame.Rect(rx, ry, self.cell_size, self.cell_size)

                if self.level.is_wall(x, y):
                    pygame.draw.rect(self.screen, WALL_COLOR, rect)
                    pygame.draw.rect(self.screen, DARK_GRAY, rect, 1)
                elif self.level.is_goal(x, y):
                    pygame.draw.rect(self.screen, FLOOR_COLOR, rect)
                    inner = rect.inflate(-12, -12)
                    pygame.draw.circle(self.screen, GOAL_COLOR, inner.center, inner.width // 2)
                else:
                    pygame.draw.rect(self.screen, FLOOR_COLOR, rect)
                    pygame.draw.rect(self.screen, DARK_GRAY, rect, 1)

                if self.level.is_box(x, y):
                    inner = rect.inflate(-8, -8)
                    color = BOX_ON_GOAL_COLOR if self.level.is_goal(x, y) else BOX_COLOR
                    pygame.draw.rect(self.screen, color, inner, border_radius=4)
                    pygame.draw.rect(self.screen, BLACK, inner, 2, border_radius=4)

        if self.level.player_pos:
            px, py = self.level.player_pos
            rx = offset_x + px * self.cell_size
            ry = offset_y + py * self.cell_size
            center = (rx + self.cell_size // 2, ry + self.cell_size // 2)
            color = PLAYER_ON_GOAL_COLOR if self.level.is_goal(px, py) else PLAYER_COLOR
            pygame.draw.circle(self.screen, color, center, self.cell_size // 2 - 6)
            pygame.draw.circle(self.screen, BLACK, center, self.cell_size // 2 - 6, 2)

        hud_y = self.level.height * self.cell_size + self.cell_size // 2 + 10
        move_text = self.font_small.render(f"Moves: {self.move_count}", True, WHITE)
        self.screen.blit(move_text, (10, hud_y))

        push_text = self.font_small.render(f"Pushes: {self.push_count}", True, WHITE)
        push_rect = push_text.get_rect(right=self.window_width - 10, top=hud_y)
        self.screen.blit(push_text, push_rect)

        level_name = os.path.basename(self.level_file)
        name_text = self.font_small.render(f"Level: {level_name}", True, GRAY)
        name_rect = name_text.get_rect(center=(self.window_width // 2, hud_y))
        self.screen.blit(name_text, name_rect)

        if self.won:
            overlay = pygame.Surface((self.window_width, self.window_height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            self.screen.blit(overlay, (0, 0))

            win_text = self.font.render("Level Complete!", True, WHITE)
            win_rect = win_text.get_rect(center=(self.window_width // 2, self.window_height // 2 - 20))
            self.screen.blit(win_text, win_rect)

            info_text = self.font_small.render(
                f"Pushes: {self.push_count}  Moves: {self.move_count}",
                True, WHITE,
            )
            info_rect = info_text.get_rect(center=(self.window_width // 2, self.window_height // 2 + 10))
            self.screen.blit(info_text, info_rect)

            restart_text = self.font_small.render("Press R to restart, ESC to quit", True, WHITE)
            restart_rect = restart_text.get_rect(center=(self.window_width // 2, self.window_height // 2 + 40))
            self.screen.blit(restart_text, restart_rect)

        pygame.display.flip()

    def run(self):
        self.logger.info("Game started: %s", self.level_file)
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
        "--level", type=str, default=os.path.join("levels", "level1.txt"),
        help="Path to level file (default: %(default)s)",
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
