import argparse
import logging
import sys
import random

import pygame

WINDOW_TITLE = "Wordle"
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
DARK_GRAY = (50, 50, 50)
GREEN = (80, 180, 80)
YELLOW = (200, 180, 60)
RED = (200, 50, 50)

WORD_LENGTH = 5
MAX_GUESSES = 6

WORDS = [
    "apple", "bread", "crane", "dance", "eagle",
    "flame", "grape", "house", "iguana", "joker",
    "knife", "lemon", "mango", "noble", "ocean",
    "piano", "queen", "river", "snake", "tiger",
    "ultra", "vivid", "waste", "xenon", "yacht",
    "zebra", "adult", "beach", "cabin", "demon",
    "eager", "fairy", "giant", "happy", "image",
    "jolly", "kayak", "lodge", "magic", "novel",
    "orbit", "pearl", "radar", "sugar", "tulip",
    "umbra", "valve", "waltz", "amber", "bloom",
]

KEYBOARD_ROWS = [
    "QWERTYUIOP",
    "ASDFGHJKL",
    "ZXCVBNM",
]

KEY_COLOR_NONE = DARK_GRAY
KEY_COLOR_GRAY = GRAY
KEY_COLOR_YELLOW = YELLOW
KEY_COLOR_GREEN = GREEN


class Wordle:
    def __init__(self, args):
        self.logger = logging.getLogger("Wordle")
        self.logger.setLevel(getattr(logging, args.log_level.upper(), logging.INFO))
        self.target = (args.word or random.choice(WORDS)).upper()
        self.max_guesses = args.max_guesses
        self.guesses = []
        self.current_guess = ""
        self.game_over = False
        self.won = False
        self.key_colors = {}
        self.flip_animating = False
        self.flip_row = -1
        self.flip_col = -1

        pygame.init()
        self.screen = pygame.display.set_mode((600, 800))
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock = pygame.time.Clock()
        self.font_letter = pygame.font.Font(None, 56)
        self.font_message = pygame.font.Font(None, 40)
        self.font_key = pygame.font.Font(None, 32)
        self.running = True

        self.logger.info(
            "Game initialized: target_len=%d, max_guesses=%d, target=%s",
            len(self.target), self.max_guesses, self.target,
        )

    def evaluate_guess(self, guess):
        result = [""] * WORD_LENGTH
        target_chars = list(self.target)
        for i, c in enumerate(guess):
            if c == target_chars[i]:
                result[i] = "green"
                target_chars[i] = ""
        for i, c in enumerate(guess):
            if result[i]:
                continue
            if c in target_chars:
                result[i] = "yellow"
                target_chars[target_chars.index(c)] = ""
            else:
                result[i] = "gray"

        for i, c in enumerate(guess):
            existing = self.key_colors.get(c)
            color = result[i]
            if color == "green":
                self.key_colors[c] = "green"
            elif color == "yellow" and existing != "green":
                self.key_colors[c] = "yellow"
            elif existing is None:
                self.key_colors[c] = "gray"

        return result

    def submit_guess(self):
        if self.game_over:
            return
        if len(self.current_guess) != WORD_LENGTH:
            return
        guess = self.current_guess.upper()
        result = self.evaluate_guess(guess)
        self.guesses.append((guess, result))
        self.logger.debug("Guess submitted: '%s' -> %s", guess, result)
        self.current_guess = ""

        if guess == self.target:
            self.won = True
            self.game_over = True
            self.logger.info("Player won! Target was '%s'", self.target)
        elif len(self.guesses) >= self.max_guesses:
            self.game_over = True
            self.logger.info("Player lost! Target was '%s'", self.target)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_r and self.game_over:
                    self.reset_game()
                elif event.key == pygame.K_RETURN and self.game_over:
                    self.running = False
                elif event.key == pygame.K_RETURN:
                    self.submit_guess()
                elif event.key == pygame.K_BACKSPACE:
                    if self.current_guess and not self.game_over and not self.flip_animating:
                        self.current_guess = self.current_guess[:-1]
                elif event.key >= pygame.K_a and event.key <= pygame.K_z:
                    if len(self.current_guess) < WORD_LENGTH and not self.game_over and not self.flip_animating:
                        self.current_guess += chr(event.key).upper()

    def reset_game(self):
        self.logger.info("Game reset")
        self.target = random.choice(WORDS).upper()
        self.guesses = []
        self.current_guess = ""
        self.game_over = False
        self.won = False
        self.key_colors = {}
        self.logger.info("New target chosen: len=%d", len(self.target))

    def draw_grid(self):
        grid_width = WORD_LENGTH * 70 + (WORD_LENGTH - 1) * 8
        grid_height = self.max_guesses * 70 + (self.max_guesses - 1) * 8
        start_x = (600 - grid_width) // 2
        start_y = 60

        for row in range(self.max_guesses):
            for col in range(WORD_LENGTH):
                x = start_x + col * 78
                y = start_y + row * 78
                rect = pygame.Rect(x, y, 70, 70)
                color = DARK_GRAY
                letter = ""

                if row < len(self.guesses):
                    guess, result = self.guesses[row]
                    letter = guess[col]
                    if result[col] == "green":
                        color = GREEN
                    elif result[col] == "yellow":
                        color = YELLOW
                    else:
                        color = GRAY
                elif row == len(self.guesses):
                    if col < len(self.current_guess):
                        letter = self.current_guess[col]
                        color = DARK_GRAY

                pygame.draw.rect(self.screen, color, rect, border_radius=6)
                if row >= len(self.guesses) or (row == len(self.guesses) and col >= len(self.current_guess)):
                    pygame.draw.rect(self.screen, GRAY, rect, width=2, border_radius=6)

                if letter:
                    text = self.font_letter.render(letter, True, WHITE)
                    text_rect = text.get_rect(center=rect.center)
                    self.screen.blit(text, text_rect)

    def draw_keyboard(self):
        key_w = 44
        key_h = 50
        gap = 6
        total_width = sum(len(row) * (key_w + gap) for row in KEYBOARD_ROWS)
        max_row_width = max(len(row) * (key_w + gap) - gap for row in KEYBOARD_ROWS)
        start_y = 560

        for row_idx, row in enumerate(KEYBOARD_ROWS):
            row_width = len(row) * (key_w + gap) - gap
            start_x = (600 - row_width) // 2
            for col_idx, key_char in enumerate(row):
                x = start_x + col_idx * (key_w + gap)
                y = start_y + row_idx * (key_h + gap)
                rect = pygame.Rect(x, y, key_w, key_h)
                color = self.key_colors.get(key_char, KEY_COLOR_NONE)
                pygame.draw.rect(self.screen, color, rect, border_radius=4)
                text = self.font_key.render(key_char, True, WHITE)
                text_rect = text.get_rect(center=rect.center)
                self.screen.blit(text, text_rect)

    def draw(self):
        self.screen.fill(BLACK)
        self.draw_grid()
        self.draw_keyboard()

        if self.game_over:
            if self.won:
                msg = "You Win! (R: restart, ENTER: quit)"
                color = GREEN
            else:
                msg = f"Game Over! Word: {self.target} (R: restart, ENTER: quit)"
                color = RED
            overlay = pygame.Surface((600, 800), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            self.screen.blit(overlay, (0, 0))
            text_surface = self.font_message.render(msg, True, color)
            text_rect = text_surface.get_rect(center=(300, 400))
            self.screen.blit(text_surface, text_rect)

        pygame.display.flip()

    def run(self):
        self.logger.info("Game started")
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
        "--word", type=str, default=None,
        help="Custom target word (default: random from pool)",
    )
    parser.add_argument(
        "--max-guesses", type=int, default=MAX_GUESSES,
        help="Maximum guesses allowed (default: %(default)s)",
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
    game = Wordle(args)
    game.run()


if __name__ == "__main__":
    main()
