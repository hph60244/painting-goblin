"""
Snake game prototype using Pygame.

Problem: 製作Snake遊戲原型
Constraint: 使用Pygame - 適合製作2D遊戲原型, 輕量化
Constraint: 用極簡風格呈現 - 強調玩法概念, 節省製作時間
Constraint: 使用logger輸出訊息 - 用於人類跟AI除錯
"""

import argparse
import logging
import random
import sys

import pygame

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger(__name__)

# Constraint: 用極簡風格呈現 - 使用基本顏色常數，不引入複雜主題
BLACK = pygame.Color(0, 0, 0)
WHITE = pygame.Color(255, 255, 255)
GREEN = pygame.Color(0, 255, 0)
RED = pygame.Color(255, 0, 0)
GRAY = pygame.Color(128, 128, 128)


class Snake:
    """
    Contract: Snake - Grid movement, growing linked list, self-collision
    """

    def __init__(self, grid_width: int, grid_height: int):
        self.grid_width = grid_width
        self.grid_height = grid_height
        # Contract: Growing linked list - 使用list模擬linked list表示蛇身
        self.body: list[tuple[int, int]] = [
            (grid_width // 2, grid_height // 2)
        ]
        # Contract: Grid movement - 方向以(dx, dy)表示
        self.direction: tuple[int, int] = (1, 0)
        self.next_direction: tuple[int, int] = (1, 0)
        self.growing = False

    def set_direction(self, dx: int, dy: int) -> None:
        """防止反向移動 (Constraint: 實作時註解要與Constraint或Problem的關聯)"""
        if (dx, dy) != (-self.direction[0], -self.direction[1]):
            self.next_direction = (dx, dy)

    def move(self) -> bool:
        """
        Move snake one step. Returns True if alive, False on collision.
        Contract: Grid movement, self-collision
        """
        self.direction = self.next_direction
        head = self.body[0]
        new_head = (
            (head[0] + self.direction[0]) % self.grid_width,
            (head[1] + self.direction[1]) % self.grid_height,
        )

        # Contract: Self-collision - 檢查新頭部是否與身體碰撞
        # Constraint: 使用logger輸出訊息
        if new_head in self.body:
            logger.info("Snake collided with itself at %s", new_head)
            return False

        self.body.insert(0, new_head)  # Contract: Growing linked list

        if not self.growing:
            self.body.pop()
        else:
            self.growing = False

        return True

    def grow(self) -> None:
        """Trigger growth on next move."""
        self.growing = True

    def get_head(self) -> tuple[int, int]:
        return self.body[0]


class Food:
    """Randomly placed food on the grid."""

    def __init__(self, grid_width: int, grid_height: int):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.position: tuple[int, int] = (0, 0)

    def respawn(self, snake_body: list[tuple[int, int]]) -> None:
        """Place food at a random position not occupied by the snake."""
        while True:
            pos = (
                random.randint(0, self.grid_width - 1),
                random.randint(0, self.grid_height - 1),
            )
            if pos not in snake_body:
                self.position = pos
                break


class Game:
    """
    Main game controller.

    Task: 使腳本接收輸入參數
    """

    def __init__(
        self,
        grid_width: int = 20,
        grid_height: int = 20,
        cell_size: int = 30,
        fps: int = 10,
    ):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.cell_size = cell_size
        self.fps = fps
        self.screen_width = grid_width * cell_size
        self.screen_height = grid_height * cell_size

        # Constraint: 使用logger輸出訊息
        logger.info(
            "Initializing game: %dx%d grid, %dpx cells, %d FPS",
            grid_width, grid_height, cell_size, fps,
        )

        pygame.init()
        # Constraint: 用極簡風格呈現 - 基本視窗設定，無多餘裝飾
        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height)
        )
        pygame.display.set_caption("Snake")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)

        self.snake = Snake(grid_width, grid_height)
        self.food = Food(grid_width, grid_height)
        self.food.respawn(self.snake.body)
        self.score = 0
        self.running = True

    def handle_events(self) -> None:
        """
        Contract: Grid movement - 處理方向鍵輸入
        Constraint: 實作時註解要與Constraint或Problem的關聯
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.snake.set_direction(0, -1)
                elif event.key == pygame.K_DOWN:
                    self.snake.set_direction(0, 1)
                elif event.key == pygame.K_LEFT:
                    self.snake.set_direction(-1, 0)
                elif event.key == pygame.K_RIGHT:
                    self.snake.set_direction(1, 0)
                elif event.key == pygame.K_ESCAPE:
                    self.running = False

    def update(self) -> None:
        """Update game state."""
        alive = self.snake.move()
        if not alive:
            # Constraint: 使用logger輸出訊息
            logger.info("Game over! Final score: %d", self.score)
            self.running = False
            return

        # Check food collision
        if self.snake.get_head() == self.food.position:
            self.snake.grow()
            self.score += 1
            logger.info("Food eaten! Score: %d", self.score)
            self.food.respawn(self.snake.body)

    def draw(self) -> None:
        """Render the game."""
        self.screen.fill(BLACK)

        # Draw grid lines (極簡風格 - 只用淺灰線條區隔格子)
        for x in range(0, self.screen_width, self.cell_size):
            pygame.draw.line(self.screen, GRAY, (x, 0), (x, self.screen_height))
        for y in range(0, self.screen_height, self.cell_size):
            pygame.draw.line(self.screen, GRAY, (0, y), (self.screen_width, y))

        # Draw snake (極簡風格 - 純色方塊)
        for segment in self.snake.body:
            rect = pygame.Rect(
                segment[0] * self.cell_size,
                segment[1] * self.cell_size,
                self.cell_size,
                self.cell_size,
            )
            pygame.draw.rect(self.screen, GREEN, rect)

        # Draw food (極簡風格 - 純色圓形)
        center = (
            self.food.position[0] * self.cell_size + self.cell_size // 2,
            self.food.position[1] * self.cell_size + self.cell_size // 2,
        )
        pygame.draw.circle(self.screen, RED, center, self.cell_size // 2 - 2)

        pygame.display.flip()

    def run(self) -> None:
        """Main game loop."""
        # Constraint: 使用logger輸出訊息
        logger.info("Game started. Use arrow keys to move, ESC to quit.")
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.fps)

        pygame.quit()
        # Constraint: 使用logger輸出訊息
        logger.info("Game closed. Final score: %d", self.score)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """
    Task: 使腳本接收輸入參數
    Constraint: 實作時註解要與Constraint或Problem的關聯
    """
    parser = argparse.ArgumentParser(description="Snake game prototype")
    parser.add_argument(
        "--grid-width", "-gw", type=int, default=20,
        help="Number of cells horizontally (default: 20)",
    )
    parser.add_argument(
        "--grid-height", "-gh", type=int, default=20,
        help="Number of cells vertically (default: 20)",
    )
    parser.add_argument(
        "--cell-size", "-cs", type=int, default=30,
        help="Pixel size of each cell (default: 30)",
    )
    parser.add_argument(
        "--fps", "-f", type=int, default=10,
        help="Game speed in frames per second (default: 10)",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    """
    Task: 使腳本接收輸入參數
    """
    args = parse_args(argv)
    game = Game(
        grid_width=args.grid_width,
        grid_height=args.grid_height,
        cell_size=args.cell_size,
        fps=args.fps,
    )
    game.run()


if __name__ == "__main__":
    main()
