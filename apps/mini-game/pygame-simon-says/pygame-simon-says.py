"""
Simon Says - Memory Game

Problem: 製作Simon Says遊戲原型
Constraint: 使用Pygame (適合製作2D遊戲原型，輕量化)
Constraint: 用極簡風格呈現 (強調玩法概念，節省製作時間)
Constraint: 使用logger輸出訊息 (用於人類跟AI除錯)
"""

import sys
import random
import argparse
import logging

import pygame

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

WINDOW_WIDTH = 500
WINDOW_HEIGHT = 500

BUTTON_SIZE = 200
GAP = 10
CENTER_GAP = WINDOW_WIDTH - 2 * BUTTON_SIZE - 2 * GAP

FLASH_MS = 300
PAUSE_MS = 150
ROUND_DELAY_MS = 800

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

RED_LIT = (255, 50, 50)
RED_DIM = (120, 0, 0)
GREEN_LIT = (50, 255, 50)
GREEN_DIM = (0, 120, 0)
BLUE_LIT = (50, 50, 255)
BLUE_DIM = (0, 0, 120)
YELLOW_LIT = (255, 255, 50)
YELLOW_DIM = (120, 120, 0)

BUTTON_COLORS = [
    (RED_LIT, RED_DIM),
    (GREEN_LIT, GREEN_DIM),
    (BLUE_LIT, BLUE_DIM),
    (YELLOW_LIT, YELLOW_DIM),
]

STATE_SHOWING = 0
STATE_WAITING = 1
STATE_GAME_OVER = 2


class SimonSays:
    def __init__(self, hard_mode: bool = False) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Simon Says")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 60)
        self.small_font = pygame.font.Font(None, 36)

        self.hard_mode = hard_mode
        self.flash_ms = FLASH_MS // (2 if hard_mode else 1)
        self.pause_ms = PAUSE_MS // (2 if hard_mode else 1)

        self.buttons = [
            pygame.Rect(GAP, GAP, BUTTON_SIZE, BUTTON_SIZE),
            pygame.Rect(
                GAP + BUTTON_SIZE + CENTER_GAP, GAP, BUTTON_SIZE, BUTTON_SIZE
            ),
            pygame.Rect(
                GAP, GAP + BUTTON_SIZE + CENTER_GAP, BUTTON_SIZE, BUTTON_SIZE
            ),
            pygame.Rect(
                GAP + BUTTON_SIZE + CENTER_GAP,
                GAP + BUTTON_SIZE + CENTER_GAP,
                BUTTON_SIZE,
                BUTTON_SIZE,
            ),
        ]

        self.reset()

    def reset(self) -> None:
        self.sequence: list[int] = []
        self.player_index = 0
        self.state = STATE_SHOWING
        self.score = 0
        self.flash_index = 0
        self.flash_start_time = 0
        self.flash_phase = 0
        self.lit_button: int | None = None
        self.round_over = False

        logger.info("Game reset")
        self._add_to_sequence()

    def _add_to_sequence(self) -> None:
        self.sequence.append(random.randint(0, 3))
        logger.info(f"Sequence: {self.sequence}")
        self.state = STATE_SHOWING
        self.flash_index = 0
        self.flash_phase = 0
        self.flash_start_time = pygame.time.get_ticks()
        self.lit_button = None
        self.round_over = False
        self.player_index = 0

    def _handle_click(self, pos: tuple[int, int]) -> None:
        if self.state != STATE_WAITING:
            return
        for i, rect in enumerate(self.buttons):
            if rect.collidepoint(pos):
                logger.info(f"Player clicked button {i}")
                self._check_player_input(i)
                return

    def _check_player_input(self, button_index: int) -> None:
        expected = self.sequence[self.player_index]
        if button_index == expected:
            self.player_index += 1
            self.lit_button = button_index
            pygame.time.set_timer(pygame.USEREVENT + 1, 200, 1)
            if self.player_index >= len(self.sequence):
                self.score += 1
                logger.info(f"Round complete! Score: {self.score}")
                self.round_over = True
                pygame.time.set_timer(
                    pygame.USEREVENT,
                    max(500, ROUND_DELAY_MS // (2 if self.hard_mode else 1)),
                    1,
                )
        else:
            logger.info(f"Wrong! Expected {expected}, got {button_index}")
            self.state = STATE_GAME_OVER
            self.lit_button = button_index

    def update(self) -> None:
        now = pygame.time.get_ticks()

        if self.state == STATE_SHOWING:
            if self.flash_index >= len(self.sequence):
                self.state = STATE_WAITING
                self.lit_button = None
                logger.info("Showing done, waiting for player")
                return

            if self.flash_phase == 0:
                self.lit_button = self.sequence[self.flash_index]
                if now - self.flash_start_time >= self.flash_ms:
                    self.flash_phase = 1
                    self.flash_start_time = now
            else:
                self.lit_button = None
                if now - self.flash_start_time >= self.pause_ms:
                    self.flash_phase = 0
                    self.flash_start_time = now
                    self.flash_index += 1

    def draw(self) -> None:
        self.screen.fill(BLACK)

        for i, ((lit_color, dim_color), rect) in enumerate(
            zip(BUTTON_COLORS, self.buttons)
        ):
            color = lit_color if self.lit_button == i else dim_color
            pygame.draw.rect(self.screen, color, rect)
            pygame.draw.rect(self.screen, GRAY, rect, 3)

        score_text = self.font.render(str(self.score), True, WHITE)
        score_rect = score_text.get_rect(
            center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
        )
        self.screen.blit(score_text, score_rect)

        if self.state == STATE_WAITING:
            label = self.small_font.render("Your turn", True, WHITE)
            label_rect = label.get_rect(
                center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 40)
            )
            self.screen.blit(label, label_rect)
        elif self.state == STATE_SHOWING and not self.round_over:
            label = self.small_font.render("Watch", True, WHITE)
            label_rect = label.get_rect(
                center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 40)
            )
            self.screen.blit(label, label_rect)

        if self.state == STATE_GAME_OVER:
            overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            self.screen.blit(overlay, (0, 0))
            go_text = self.font.render("GAME OVER", True, WHITE)
            go_rect = go_text.get_rect(
                center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 30)
            )
            self.screen.blit(go_text, go_rect)
            restart_text = self.small_font.render("Press R to restart", True, WHITE)
            restart_rect = restart_text.get_rect(
                center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 20)
            )
            self.screen.blit(restart_text, restart_rect)

        pygame.display.flip()

    def run(self) -> None:
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self._handle_click(event.pos)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r and self.state == STATE_GAME_OVER:
                        logger.info("Restarting game")
                        self.reset()
                elif event.type == pygame.USEREVENT:
                    self._add_to_sequence()
                elif event.type == pygame.USEREVENT + 1:
                    self.lit_button = None

            self.update()
            self.draw()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()


def main() -> None:
    parser = argparse.ArgumentParser(description="Simon Says - A memory game")
    parser.add_argument(
        "--hard",
        action="store_true",
        help="Enable hard mode with faster sequence playback",
    )
    args = parser.parse_args()

    logger.info(f"Starting Simon Says (hard_mode={args.hard})")
    game = SimonSays(hard_mode=args.hard)
    game.run()


if __name__ == "__main__":
    main()
