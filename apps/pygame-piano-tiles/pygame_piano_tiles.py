import argparse
import logging
import sys
import random

import pygame


WINDOW_TITLE = "Piano Tiles"
FPS = 60
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 600
LANE_COUNT = 4
HIT_ZONE_Y = WINDOW_HEIGHT - 80
HIT_ZONE_HEIGHT = 60
TILE_HEIGHT = 120
BASE_SPEED = 300
SPEED_INCREMENT = 15
MAX_SPEED = 800

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
HIT_ZONE_COLOR = (200, 200, 200)


class Tile:
    def __init__(self, lane, y, lane_width):
        self.lane = lane
        self.lane_width = lane_width
        self.rect = pygame.Rect(
            lane * lane_width, y,
            lane_width, TILE_HEIGHT,
        )
        self.hit = False

    def update(self, dt, speed):
        self.rect.y += speed * dt

    def draw(self, surface):
        if not self.hit:
            pygame.draw.rect(surface, BLACK, self.rect)

    def is_in_hit_zone(self):
        return self.rect.colliderect(
            pygame.Rect(0, HIT_ZONE_Y, WINDOW_WIDTH, HIT_ZONE_HEIGHT)
        )

    def is_past_hit_zone(self):
        return self.rect.y > HIT_ZONE_Y + HIT_ZONE_HEIGHT


class Game:
    def __init__(self, args):
        self.logger = logging.getLogger("PianoTiles")
        self.logger.setLevel(getattr(logging, args.log_level.upper(), logging.INFO))
        self.lane_count = args.lanes
        self.lane_width = WINDOW_WIDTH // self.lane_count
        self.speed = args.speed
        self.speed_increment = args.speed_increment
        self.score = 0
        self.game_over = False
        self.tiles = []
        self.spawn_timer = 0.0
        self.spawn_interval = 1.0
        self.last_lane = -1

        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption(WINDOW_TITLE)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.running = True

        self.logger.info(
            "Game initialized: %d lanes, speed=%.0fpx/s, increment=%.1f",
            self.lane_count, self.speed, self.speed_increment,
        )

    def spawn_tile(self):
        available = [l for l in range(self.lane_count) if l != self.last_lane]
        lane = random.choice(available)
        self.last_lane = lane
        tile = Tile(lane, -TILE_HEIGHT, self.lane_width)
        self.tiles.append(tile)
        self.logger.debug("Spawned tile in lane %d", lane)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_r and self.game_over:
                    self.reset_game()
            elif event.type == pygame.MOUSEBUTTONDOWN and not self.game_over:
                mx, my = event.pos
                lane = mx // self.lane_width
                hit_tile = None
                for tile in self.tiles:
                    if tile.lane == lane and not tile.hit and tile.is_in_hit_zone():
                        hit_tile = tile
                        break
                if hit_tile:
                    hit_tile.hit = True
                    self.score += 1
                    self.speed = min(self.speed + self.speed_increment, MAX_SPEED)
                    self.spawn_interval = max(0.3, self.spawn_interval - 0.02)
                    self.logger.debug("Tile hit! Score=%d, Speed=%.0f", self.score, self.speed)
                else:
                    self.logger.debug("Miss! Clicked lane %d with no tile in hit zone", lane)
                    self.game_over = True

    def reset_game(self):
        self.logger.info("Game reset")
        self.tiles = []
        self.score = 0
        self.speed = BASE_SPEED
        self.spawn_interval = 1.0
        self.spawn_timer = 0.0
        self.game_over = False

    def update(self, dt):
        if self.game_over:
            return

        self.spawn_timer += dt
        if self.spawn_timer >= self.spawn_interval:
            self.spawn_timer -= self.spawn_interval
            self.spawn_tile()

        for tile in self.tiles:
            tile.update(dt, self.speed)
            if not tile.hit and tile.is_past_hit_zone():
                self.logger.debug("Tile missed in lane %d", tile.lane)
                self.game_over = True
                return

        self.tiles = [t for t in self.tiles if t.rect.y < WINDOW_HEIGHT]

    def draw(self):
        self.screen.fill(WHITE)

        for i in range(1, self.lane_count):
            x = i * self.lane_width
            pygame.draw.line(
                self.screen, BLACK,
                (x, 0), (x, WINDOW_HEIGHT), 1,
            )

        pygame.draw.rect(
            self.screen, HIT_ZONE_COLOR,
            (0, HIT_ZONE_Y, WINDOW_WIDTH, HIT_ZONE_HEIGHT),
        )
        pygame.draw.line(
            self.screen, (150, 150, 150),
            (0, HIT_ZONE_Y), (WINDOW_WIDTH, HIT_ZONE_Y), 2,
        )
        pygame.draw.line(
            self.screen, (150, 150, 150),
            (0, HIT_ZONE_Y + HIT_ZONE_HEIGHT),
            (WINDOW_WIDTH, HIT_ZONE_Y + HIT_ZONE_HEIGHT), 2,
        )

        for tile in self.tiles:
            tile.draw(self.screen)

        score_text = self.font.render(f"Score: {self.score}", True, BLACK)
        self.screen.blit(score_text, (10, 10))

        speed_text = self.font.render(f"Speed: {int(self.speed)}", True, BLACK)
        speed_rect = speed_text.get_rect(topright=(WINDOW_WIDTH - 10, 10))
        self.screen.blit(speed_text, speed_rect)

        if self.game_over:
            game_over_text = self.font.render("Game Over! (R to restart, ESC to quit)", True, BLACK)
            text_rect = game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            self.screen.blit(game_over_text, text_rect)

        pygame.display.flip()

    def run(self):
        self.logger.info("Game started")
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0
            self.handle_events()
            self.update(dt)
            self.draw()
        self.logger.info("Game ended")
        pygame.quit()
        sys.exit()


def parse_args(argv):
    parser = argparse.ArgumentParser(description=WINDOW_TITLE)
    parser.add_argument(
        "--lanes", type=int, default=LANE_COUNT,
        help="Number of lanes (default: %(default)s)",
    )
    parser.add_argument(
        "--speed", type=float, default=BASE_SPEED,
        help="Initial tile fall speed in px/s (default: %(default)s)",
    )
    parser.add_argument(
        "--speed-increment", type=float, default=SPEED_INCREMENT,
        help="Speed increase per successful tap in px/s (default: %(default)s)",
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
