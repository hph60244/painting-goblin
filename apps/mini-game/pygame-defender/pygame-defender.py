import pygame
import sys
import math
import random
import argparse
import logging
from dataclasses import dataclass
from typing import Optional

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("defender")

SCREEN_W = 640
SCREEN_H = 480
RADAR_H = 40
TERRAIN_H = 80
PLAY_H = SCREEN_H - RADAR_H - TERRAIN_H
PLAY_TOP = RADAR_H
PLAY_BOTTOM = RADAR_H + PLAY_H

WORLD_W = 3200

FPS = 60

PLAYER_SPEED = 3
BULLET_SPEED = 8
LANDER_SPEED = 1.5
ABDUCTED_SPEED = 2

MOUNTAIN_COLOR = (60, 120, 60)
SKY_COLOR = (10, 10, 30)
STAR_COLOR = (100, 100, 140)
PLAYER_COLOR = (0, 200, 255)
BULLET_COLOR = (255, 255, 100)
HUMAN_COLOR = (200, 180, 100)
LANDER_COLOR = (200, 50, 200)
RADAR_BG = (20, 20, 40)
RADAR_PLAYER_COLOR = (0, 200, 255)
RADAR_HUMAN_COLOR = (200, 180, 100)
RADAR_LANDER_COLOR = (200, 50, 200)
RADAR_ABDUCTED_COLOR = (255, 100, 0)
TEXT_COLOR = (200, 200, 200)

NUM_STARS = 80
NUM_HUMANS = 12
NUM_LANDERS = 6
MAX_LANDERS = 10
LANDER_SPAWN_INTERVAL = 180


@dataclass
class Star:
    x: float
    y: float
    brightness: int


@dataclass
class TerrainPoint:
    x: float
    h: float


class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.active = True

    def update(self, camera_x):
        self.x += BULLET_SPEED
        if self.x > camera_x + SCREEN_W + 20:
            self.active = False

    def draw(self, screen, camera_x):
        sx = int(self.x - camera_x)
        if 0 <= sx <= SCREEN_W:
            pygame.draw.rect(screen, BULLET_COLOR, (sx - 1, int(self.y) - 1, 4, 3))


class Human:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.start_x = x
        self.start_y = y
        self.radius = 5
        self.alive = True
        self.abducted = False
        self.abduct_target_y = PLAY_TOP + 10
        self.returning = False

    def update(self):
        if self.abducted and not self.returning:
            if self.y > self.abduct_target_y:
                self.y -= ABDUCTED_SPEED
            if self.y <= self.abduct_target_y:
                logger.info("Human abducted!")
        elif self.returning:
            if self.y < self.start_y:
                self.y += ABDUCTED_SPEED * 0.5
            else:
                self.y = self.start_y
                self.returning = False
                self.abducted = False
                logger.info("Human returned to surface")

    def draw(self, screen, camera_x):
        if not self.alive:
            return
        sx = int(self.x - camera_x)
        if 0 <= sx <= SCREEN_W:
            color = HUMAN_COLOR
            if self.returning:
                color = (100, 200, 255)
            elif self.abducted:
                color = (255, 100, 0)
            pygame.draw.circle(screen, color, (sx, int(self.y)), self.radius)
            body_top = int(self.y) - self.radius - 4
            pygame.draw.line(screen, color, (sx, int(self.y) - self.radius), (sx, body_top), 2)
            arm_y = int(self.y) - self.radius - 2
            pygame.draw.line(screen, color, (sx - 3, arm_y), (sx + 3, arm_y), 1)


class Lander:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.target_y = PLAY_TOP + random.randint(30, PLAY_H // 2)
        self.speed = LANDER_SPEED + random.uniform(-0.3, 0.3)
        self.alive = True
        self.has_human = False
        self.direction = 1
        self.move_timer = 0
        self.move_dir_change = random.randint(60, 180)

    def update(self, humans):
        if not self.alive:
            return

        self.move_timer += 1
        if self.move_timer >= self.move_dir_change:
            self.direction *= -1
            self.move_timer = 0
            self.move_dir_change = random.randint(60, 180)

        if self.has_human:
            if self.y > PLAY_TOP + 20:
                self.y -= self.speed * 0.8
            self.x += self.direction * self.speed * 0.5
        else:
            if self.y < self.target_y:
                self.y += self.speed * 0.5
            elif self.y > self.target_y:
                self.y -= self.speed * 0.5
            else:
                self.x += self.direction * self.speed

        self.x = max(20, min(WORLD_W - 20, self.x))
        self.y = max(PLAY_TOP + 10, min(PLAY_BOTTOM - 20, self.y))

        if not self.has_human:
            for h in humans:
                if h.alive and not h.abducted and not h.returning:
                    dx = abs(self.x - h.x)
                    dy = abs(self.y - h.y)
                    if dx < 15 and dy < 15:
                        h.abducted = True
                        self.has_human = True
                        logger.info("Lander picked up a human!")
                        break
        else:
            if self.y <= PLAY_TOP + 15:
                for h in humans:
                    if h.abducted and h.y <= self.y + 5 and abs(h.x - self.x) < 20:
                        h.alive = False
                        logger.info("Human lost to space!")
                self.has_human = False

    def draw(self, screen, camera_x):
        if not self.alive:
            return
        sx = int(self.x - camera_x)
        if 0 <= sx <= SCREEN_W:
            color = LANDER_COLOR
            if self.has_human:
                color = (255, 100, 0)
            body_y = int(self.y)
            pygame.draw.ellipse(screen, color, (sx - 8, body_y - 4, 16, 8))
            pygame.draw.line(screen, color, (sx - 6, body_y + 4), (sx - 6, body_y + 10), 2)
            pygame.draw.line(screen, color, (sx + 6, body_y + 4), (sx + 6, body_y + 10), 2)
            pygame.draw.line(screen, color, (sx - 6, body_y + 10), (sx - 10, body_y + 14), 1)
            pygame.draw.line(screen, color, (sx + 6, body_y + 10), (sx + 10, body_y + 14), 1)
            pygame.draw.circle(screen, (255, 0, 0), (sx - 3, body_y - 2), 2)
            pygame.draw.circle(screen, (255, 0, 0), (sx + 3, body_y - 2), 2)


class Player:
    def __init__(self):
        self.x = WORLD_W // 2
        self.y = PLAY_TOP + PLAY_H // 2
        self.speed = PLAYER_SPEED
        self.dx = 0
        self.dy = 0
        self.thrust = False

    def update(self):
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed
        self.x = max(20, min(WORLD_W - 20, self.x))
        self.y = max(PLAY_TOP + 10, min(PLAY_BOTTOM - 10, self.y))

    def draw(self, screen, camera_x):
        sx = int(self.x - camera_x)
        sy = int(self.y)
        color = PLAYER_COLOR
        if self.thrust:
            pygame.draw.polygon(screen, (255, 200, 50), [
                (sx - 10, sy + 6), (sx - 6, sy + 2), (sx - 14, sy + 2)
            ])
        pygame.draw.polygon(screen, color, [
            (sx + 10, sy), (sx - 8, sy - 5), (sx - 4, sy), (sx - 8, sy + 5)
        ])

    def reset(self):
        self.x = WORLD_W // 2
        self.y = PLAY_TOP + PLAY_H // 2
        self.dx = 0
        self.dy = 0


class DefenderGame:
    def __init__(self):
        logger.info("Initializing Defender game")
        pygame.init()

        args = self._parse_args()
        self.debug_mode = args.get("debug", False)
        if self.debug_mode:
            logger.setLevel(logging.DEBUG)
            logger.info("Debug mode enabled")

        self.screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
        pygame.display.set_caption("Defender")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 18)
        self.big_font = pygame.font.Font(None, 36)

        self.camera_x = 0.0
        self.running = True
        self.score = args.get("starting_score", 0)
        self.lives = 3
        self.game_over = False
        self.paused = False

        self.stars = self._generate_stars()
        self.terrain = self._generate_terrain()
        self.player = Player()
        self.bullets: list[Bullet] = []
        self.humans = self._generate_humans()
        self.landers = self._generate_landers()
        self.spawn_timer = 0
        self.fire_cooldown = 0

        logger.info(f"Game initialized. Humans: {len(self.humans)}, Landers: {len(self.landers)}")

    def _parse_args(self):
        parser = argparse.ArgumentParser(description="Defender game prototype")
        parser.add_argument("--debug", action="store_true", help="Enable debug logging")
        parser.add_argument("--score", type=int, default=0, help="Starting score")
        parsed = parser.parse_args()
        return {"debug": parsed.debug, "starting_score": parsed.score}

    def _generate_stars(self):
        stars = []
        for _ in range(NUM_STARS):
            stars.append(Star(
                x=random.uniform(0, WORLD_W),
                y=random.uniform(PLAY_TOP, SCREEN_H - TERRAIN_H),
                brightness=random.randint(30, 150),
            ))
        return stars

    def _generate_terrain(self):
        points = []
        step = 20
        x = 0
        while x <= WORLD_W:
            h = random.randint(20, TERRAIN_H - 10)
            points.append(TerrainPoint(x=x, h=h))
            x += step
        return points

    def _get_terrain_y(self, x):
        if len(self.terrain) < 2:
            return SCREEN_H - TERRAIN_H // 2
        for i in range(len(self.terrain) - 1):
            if self.terrain[i].x <= x <= self.terrain[i + 1].x:
                t = (x - self.terrain[i].x) / (self.terrain[i + 1].x - self.terrain[i].x)
                h = self.terrain[i].h + (self.terrain[i + 1].h - self.terrain[i].h) * t
                return SCREEN_H - h
        return SCREEN_H - TERRAIN_H // 2

    def _generate_humans(self):
        humans = []
        margin = 80
        for _ in range(NUM_HUMANS):
            x = random.uniform(margin, WORLD_W - margin)
            y = self._get_terrain_y(x) - 10
            humans.append(Human(x, y))
        return humans

    def _generate_landers(self):
        landers = []
        for _ in range(NUM_LANDERS):
            x = random.uniform(50, WORLD_W - 50)
            y = PLAY_TOP + random.randint(30, PLAY_H // 2)
            landers.append(Lander(x, y))
        return landers

    def _spawn_lander(self):
        side = random.choice(["left", "right"])
        if side == "left":
            x = max(20, self.camera_x - 50)
        else:
            x = min(WORLD_W - 20, self.camera_x + SCREEN_W + 50)
        y = PLAY_TOP + random.randint(20, PLAY_H // 3)
        self.landers.append(Lander(x, y))
        logger.debug(f"New lander spawned at ({x:.0f}, {y:.0f})")

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_p:
                    self.paused = not self.paused
                    logger.info(f"Game {'paused' if self.paused else 'unpaused'}")
                elif event.key == pygame.K_r and self.game_over:
                    self.reset_game()
                elif event.key == pygame.K_SPACE:
                    if not self.game_over and not self.paused:
                        if self.fire_cooldown <= 0:
                            self.bullets.append(Bullet(self.player.x + 12, self.player.y))
                            self.fire_cooldown = 12

        if not self.game_over and not self.paused:
            keys = pygame.key.get_pressed()
            self.player.dx = 0
            self.player.dy = 0
            self.player.thrust = False
            if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                self.player.dx = -1
            if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                self.player.dx = 1
                self.player.thrust = True
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                self.player.dy = -1
                self.player.thrust = True
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                self.player.dy = 1
            if keys[pygame.K_SPACE]:
                if self.fire_cooldown <= 0:
                    self.bullets.append(Bullet(self.player.x + 12, self.player.y))
                    self.fire_cooldown = 12

        if self.fire_cooldown > 0:
            self.fire_cooldown -= 1

    def update_camera(self):
        target_cx = self.player.x - SCREEN_W // 3
        target_cx = max(0, min(WORLD_W - SCREEN_W, target_cx))
        self.camera_x += (target_cx - self.camera_x) * 0.1

    def update_bullets(self):
        for b in self.bullets:
            b.update(self.camera_x)
            bx, by = b.x, b.y
            for lander in self.landers:
                if lander.alive:
                    dx = abs(bx - lander.x)
                    dy = abs(by - lander.y)
                    if dx < 12 and dy < 12:
                        lander.alive = False
                        b.active = False
                        self.score += 100
                        logger.info(f"Lander destroyed! Score: {self.score}")
                        if lander.has_human:
                            for h in self.humans:
                                if h.abducted and abs(h.x - lander.x) < 30:
                                    h.returning = True
                                    h.abducted = False
                                    h.y = min(h.y, lander.y)
                                    logger.info("Human rescued!")
                        break
        self.bullets = [b for b in self.bullets if b.active]

    def check_player_collisions(self):
        px, py = self.player.x, self.player.y
        for lander in self.landers:
            if lander.alive:
                dx = abs(px - lander.x)
                dy = abs(py - lander.y)
                if dx < 15 and dy < 15:
                    self.player_died()
                    return

    def player_died(self):
        self.lives -= 1
        logger.info(f"Player died! Lives left: {self.lives}")
        if self.lives <= 0:
            self.game_over = True
            logger.info("Game Over!")
        else:
            logger.info("Respawning...")
            self.player.reset()
            self.bullets.clear()
            self.fire_cooldown = 30

    def reset_game(self):
        logger.info("Resetting game")
        self.__init__()

    def update(self):
        if self.game_over or self.paused:
            return

        self.player.update()
        self.update_camera()

        self.spawn_timer += 1
        if self.spawn_timer >= LANDER_SPAWN_INTERVAL and len(self.landers) < MAX_LANDERS:
            self._spawn_lander()
            self.spawn_timer = 0

        for lander in self.landers:
            lander.update(self.humans)
        self.landers = [l for l in self.landers if l.alive]

        for h in self.humans:
            h.update()

        self.update_bullets()
        self.check_player_collisions()

        humans_left = sum(1 for h in self.humans if h.alive)
        if humans_left == 0:
            logger.info("All humans lost! Game over.")
            self.game_over = True

    def draw_radar(self):
        pygame.draw.rect(self.screen, RADAR_BG, (0, 0, SCREEN_W, RADAR_H))

        radar_scale = SCREEN_W / WORLD_W
        edge = self.camera_x * radar_scale
        bar_w = SCREEN_W * radar_scale
        pygame.draw.rect(self.screen, (40, 40, 60), (int(edge), 2, int(bar_w), RADAR_H - 4), 1)
        pygame.draw.rect(self.screen, (30, 30, 30), (int(edge), 2, int(bar_w), RADAR_H - 4))

        px_radar = int(self.player.x * radar_scale)
        pygame.draw.circle(self.screen, RADAR_PLAYER_COLOR, (px_radar, RADAR_H // 2), 3)

        for h in self.humans:
            if not h.alive:
                continue
            hx = int(h.x * radar_scale)
            if h.abducted:
                pygame.draw.circle(self.screen, RADAR_ABDUCTED_COLOR, (hx, RADAR_H // 2), 2)
            else:
                pygame.draw.circle(self.screen, RADAR_HUMAN_COLOR, (hx, RADAR_H // 2), 2)

        for lander in self.landers:
            if not lander.alive:
                continue
            lx = int(lander.x * radar_scale)
            color = RADAR_LANDER_COLOR
            if lander.has_human:
                color = RADAR_ABDUCTED_COLOR
            pygame.draw.circle(self.screen, color, (lx, RADAR_H // 2), 2)

        view_left = int(self.camera_x * radar_scale)
        view_right = int((self.camera_x + SCREEN_W) * radar_scale)
        pygame.draw.rect(self.screen, (100, 100, 100), (view_left, 0, view_right - view_left, RADAR_H), 1)

        score_text = self.font.render(f"SCORE: {self.score}", True, TEXT_COLOR)
        self.screen.blit(score_text, (4, RADAR_H - 14))
        lives_text = self.font.render(f"LIVES: {self.lives}", True, TEXT_COLOR)
        self.screen.blit(lives_text, (SCREEN_W - 80, RADAR_H - 14))

    def draw_terrain(self):
        color_step = 15
        for point in self.terrain:
            sx = int(point.x - self.camera_x)
            if -10 <= sx <= SCREEN_W + 10:
                terrain_top = SCREEN_H - int(point.h)
                pygame.draw.line(
                    self.screen, MOUNTAIN_COLOR,
                    (sx, terrain_top), (sx, SCREEN_H), 2
                )

        for i in range(len(self.terrain) - 1):
            p1 = self.terrain[i]
            p2 = self.terrain[i + 1]
            sx1 = int(p1.x - self.camera_x)
            sx2 = int(p2.x - self.camera_x)
            if max(sx1, sx2) < -10 or min(sx1, sx2) > SCREEN_W + 10:
                continue
            ty1 = SCREEN_H - int(p1.h)
            ty2 = SCREEN_H - int(p2.h)
            shade = min(255, max(0, 50 + int(p1.h) * 3))
            color = (20, shade, 20)
            pygame.draw.polygon(self.screen, color, [
                (sx1, ty1), (sx2, ty2), (sx2, SCREEN_H), (sx1, SCREEN_H)
            ])
            pygame.draw.line(self.screen, (40, 100, 40), (sx1, ty1), (sx2, ty2), 1)

    def draw(self):
        self.screen.fill(SKY_COLOR)

        for star in self.stars:
            sx = int(star.x - self.camera_x)
            if 0 <= sx <= SCREEN_W:
                sy = int(star.y)
                alpha = star.brightness
                pygame.draw.circle(self.screen, (alpha, alpha, alpha + 20), (sx, sy), 1)

        self.draw_terrain()
        self.draw_radar()

        for h in self.humans:
            h.draw(self.screen, self.camera_x)

        for lander in self.landers:
            lander.draw(self.screen, self.camera_x)

        for b in self.bullets:
            b.draw(self.screen, self.camera_x)

        self.player.draw(self.screen, self.camera_x)

        humans_alive = sum(1 for h in self.humans if h.alive and not h.returning and not h.abducted)
        humans_info = self.font.render(f"HUMANS: {humans_alive}", True, TEXT_COLOR)
        self.screen.blit(humans_info, (SCREEN_W // 2 - 40, SCREEN_H - 20))

        if self.game_over:
            text = self.big_font.render("GAME OVER", True, (255, 50, 50))
            rect = text.get_rect(center=(SCREEN_W // 2, SCREEN_H // 2 - 20))
            self.screen.blit(text, rect)
            restart = self.font.render("Press R to restart", True, TEXT_COLOR)
            rect2 = restart.get_rect(center=(SCREEN_W // 2, SCREEN_H // 2 + 20))
            self.screen.blit(restart, rect2)

        if self.paused:
            text = self.big_font.render("PAUSED", True, TEXT_COLOR)
            rect = text.get_rect(center=(SCREEN_W // 2, SCREEN_H // 2))
            self.screen.blit(text, rect)

        pygame.display.flip()

    def run(self):
        logger.info("Game loop started")
        while self.running:
            self.handle_input()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
        logger.info("Game exited")


def main():
    game = DefenderGame()
    game.run()


if __name__ == "__main__":
    main()
