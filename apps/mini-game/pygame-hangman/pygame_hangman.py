import argparse
import logging
import sys
import random

import pygame

WINDOW_TITLE = "Hangman"
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 50, 50)
GREEN = (50, 200, 50)
GRAY = (100, 100, 100)
BLUE = (80, 160, 240)

WORDS = [
    "python", "pygame", "hangman", "computer", "keyboard",
    "display", "program", "goblin", "painting", "adventure",
    "galaxy", "puzzle", "rocket", "wizard", "dragon",
]

MAX_WRONG = 6


class Hangman:
    def __init__(self, args):
        self.logger = logging.getLogger("Hangman")
        self.logger.setLevel(getattr(logging, args.log_level.upper(), logging.INFO))
        self.word = args.word if args.word else random.choice(WORDS)
        self.max_wrong = args.max_wrong
        self.guessed_letters = set()
        self.wrong_guesses = set()
        self.game_over = False
        self.won = False

        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock = pygame.time.Clock()
        self.font_large = pygame.font.Font(None, 64)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 32)
        self.running = True

        self.logger.info(
            "Game initialized: word_len=%d, max_wrong=%d",
            len(self.word), self.max_wrong,
        )

    def guess(self, letter):
        if self.game_over:
            return
        if len(letter) != 1 or not letter.isalpha():
            return
        letter = letter.lower()
        if letter in self.guessed_letters or letter in self.wrong_guesses:
            return
        if letter in self.word:
            self.guessed_letters.add(letter)
            self.logger.debug("Correct guess: '%s'", letter)
            if all(c in self.guessed_letters for c in self.word):
                self.won = True
                self.game_over = True
                self.logger.info("Player won! Word was '%s'", self.word)
        else:
            self.wrong_guesses.add(letter)
            self.logger.debug("Wrong guess: '%s' (%d/%d)", letter, len(self.wrong_guesses), self.max_wrong)
            if len(self.wrong_guesses) >= self.max_wrong:
                self.game_over = True
                self.logger.info("Player lost! Word was '%s'", self.word)

    def get_display_word(self):
        return " ".join(c if c in self.guessed_letters else "_" for c in self.word)

    def draw_gallows(self, offset_x, offset_y):
        base = 180
        height = 220
        pygame.draw.line(self.screen, WHITE, (offset_x, offset_y + height), (offset_x + base, offset_y + height), 4)
        pygame.draw.line(self.screen, WHITE, (offset_x + 40, offset_y + height), (offset_x + 40, offset_y), 4)
        pygame.draw.line(self.screen, WHITE, (offset_x + 40, offset_y), (offset_x + 140, offset_y), 4)
        pygame.draw.line(self.screen, WHITE, (offset_x + 140, offset_y), (offset_x + 140, offset_y + 40), 3)

    def draw_hangman(self, offset_x, offset_y, wrong_count):
        center_x = offset_x + 140
        rope_top = offset_y + 40
        head_y = rope_top + 30
        body_top = head_y + 30
        body_bottom = body_top + 70
        arm_y = body_top + 20
        leg_y = body_bottom
        arm_len = 40
        leg_len = 45

        if wrong_count >= 1:
            pygame.draw.circle(self.screen, WHITE, (center_x, head_y), 25, 3)
        if wrong_count >= 2:
            pygame.draw.line(self.screen, WHITE, (center_x, head_y + 25), (center_x, body_bottom), 3)
        if wrong_count >= 3:
            pygame.draw.line(self.screen, WHITE, (center_x, arm_y), (center_x - arm_len, arm_y + 15), 3)
        if wrong_count >= 4:
            pygame.draw.line(self.screen, WHITE, (center_x, arm_y), (center_x + arm_len, arm_y + 15), 3)
        if wrong_count >= 5:
            pygame.draw.line(self.screen, WHITE, (center_x, body_bottom), (center_x - leg_len, leg_y + leg_len), 3)
        if wrong_count >= 6:
            pygame.draw.line(self.screen, WHITE, (center_x, body_bottom), (center_x + leg_len, leg_y + leg_len), 3)

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
                elif event.key >= pygame.K_a and event.key <= pygame.K_z:
                    letter = chr(event.key)
                    self.guess(letter)

    def reset_game(self):
        self.logger.info("Game reset")
        self.word = random.choice(WORDS)
        self.guessed_letters = set()
        self.wrong_guesses = set()
        self.game_over = False
        self.won = False
        self.logger.info("New word chosen: len=%d", len(self.word))

    def draw(self):
        self.screen.fill(BLACK)

        wrong_count = len(self.wrong_guesses)
        self.draw_gallows(50, 120)
        self.draw_hangman(50, 120, wrong_count)

        word_surface = self.font_large.render(self.get_display_word(), True, WHITE)
        word_rect = word_surface.get_rect(center=(400, 500))
        self.screen.blit(word_surface, word_rect)

        wrong_text = self.font_small.render(
            "Wrong: " + ", ".join(sorted(self.wrong_guesses)) if self.wrong_guesses else "Wrong: (none)",
            True, RED,
        )
        self.screen.blit(wrong_text, (250, 60))

        guessed_text = self.font_small.render(
            "Guessed: " + ", ".join(sorted(self.guessed_letters)) if self.guessed_letters else "",
            True, GREEN,
        )
        self.screen.blit(guessed_text, (250, 30))

        remaining = self.max_wrong - wrong_count
        lives_text = self.font_small.render(f"Remaining: {remaining}", True, GRAY)
        self.screen.blit(lives_text, (600, 30))

        if self.game_over:
            if self.won:
                msg = "You Win! (R: restart, ENTER: quit)"
                color = GREEN
            else:
                msg = f"Game Over! Word was: {self.word} (R: restart, ENTER: quit)"
                color = RED
            overlay = pygame.Surface((800, 600), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            self.screen.blit(overlay, (0, 0))
            text_surface = self.font_medium.render(msg, True, color)
            text_rect = text_surface.get_rect(center=(400, 300))
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
        help="Custom word to guess (default: random from pool)",
    )
    parser.add_argument(
        "--max-wrong", type=int, default=MAX_WRONG,
        help="Maximum wrong guesses allowed (default: %(default)s)",
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
    game = Hangman(args)
    game.run()


if __name__ == "__main__":
    main()
