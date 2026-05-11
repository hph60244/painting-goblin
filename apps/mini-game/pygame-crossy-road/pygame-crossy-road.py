#!/usr/bin/env python3
"""
Crossy Road 遊戲原型
Problem: 製作Crossy Road遊戲原型 (Constraint: 實作時註解要與Constraint或Problem的關聯)
"""

import argparse
import logging
import random
import sys
from dataclasses import dataclass, field
from typing import List, Optional, Tuple

import pygame

# Constraint: 使用logger輸出訊息 - 用於人類跟AI除錯
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("crossy-road")

# ---------------------------------------------------------------------------
# Constraint: 用極簡風格呈現 - 強調玩法概念, 節省製作時間
# 使用簡單的幾何形狀和顏色來表示遊戲元素
# ---------------------------------------------------------------------------

# 顏色常數 (RGB)
COLOR_GRASS = (76, 153, 0)
COLOR_ROAD = (80, 80, 80)
COLOR_ROAD_LINE = (255, 255, 0)
COLOR_WATER = (0, 102, 204)
COLOR_PLAYER = (255, 255, 0)
COLOR_CAR = (200, 50, 50)
COLOR_TRUCK = (150, 40, 40)
COLOR_LOG = (139, 90, 43)
COLOR_TRAIN = (180, 40, 180)
COLOR_RAIL = (100, 100, 100)
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_GRAY = (128, 128, 128)
COLOR_SCORE_BG = (0, 0, 0, 128)

# 遊戲設定
GRID_SIZE = 60
LANE_HEIGHT = GRID_SIZE
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 40
FPS = 60

# 車道類型
LANE_GRASS = "grass"
LANE_ROAD = "road"
LANE_WATER = "water"
LANE_RAIL = "rail"


@dataclass
class Obstacle:
    """道路上的障礙物 (車子、火車、木頭)"""
    x: float
    y: float
    width: int
    height: int
    speed: float
    color: Tuple[int, int, int]
    direction: int  # 1 = right, -1 = left


@dataclass
class Lane:
    """一條水平車道"""
    lane_type: str  # grass, road, water, rail
    y: int
    obstacles: List[Obstacle] = field(default_factory=list)
    spawn_timer: float = 0.0
    spawn_interval: float = 2.0


@dataclass
class Player:
    """玩家角色"""
    grid_x: int
    grid_y: int
    pixel_x: float
    pixel_y: float
    moving: bool = False
    target_x: float = 0.0
    target_y: float = 0.0
    move_speed: float = 10.0
    alive: bool = True
    score: int = 0
    max_y: int = 0  # 記錄最遠到達的y位置


def parse_args() -> argparse.Namespace:
    """Task: 使腳本接收輸入參數 - Contract: Lane hopping, procedural generation"""
    parser = argparse.ArgumentParser(description="Crossy Road 遊戲原型")
    parser.add_argument("--width", type=int, default=480, help="視窗寬度 (預設: 480)")
    parser.add_argument("--height", type=int, default=720, help="視窗高度 (預設: 720)")
    parser.add_argument("--fps", type=int, default=FPS, help="更新率 (預設: 60)")
    parser.add_argument("--debug", action="store_true", help="啟用除錯模式")
    return parser.parse_args()


def get_grid_x_from_pixel(pixel_x: int, screen_width: int) -> int:
    """將像素座標轉換為網格座標"""
    grid_count = screen_width // GRID_SIZE
    return max(0, min(grid_count - 1, pixel_x // GRID_SIZE))


def get_lane_index_from_y(y: int) -> int:
    """從像素y座標取得車道索引"""
    return y // LANE_HEIGHT


def generate_obstacles_for_lane(lane: Lane, lane_index: int, screen_width: int) -> None:
    """Constraint: Lane hopping, procedural generation - 根據車道類型生成障礙物"""
    if lane.lane_type == LANE_GRASS:
        return  # 草地上沒有障礙物

    direction = random.choice([-1, 1])

    if lane.lane_type == LANE_ROAD:
        # 生成車子
        count = random.randint(1, 3)
        spacing = screen_width // count
        for i in range(count):
            x = i * spacing + random.randint(0, spacing // 2)
            car_width = random.choice([30, 40, 50])
            car_height = LANE_HEIGHT - 10
            speed = random.uniform(2.0, 5.0)
            color = COLOR_CAR if car_width < 45 else COLOR_TRUCK
            lane.obstacles.append(Obstacle(
                x=x, y=lane.y + 5,
                width=car_width, height=car_height,
                speed=speed, color=color, direction=direction,
            ))
        logger.debug(f"Generated {count} cars on road lane {lane_index}")

    elif lane.lane_type == LANE_WATER:
        # 生成木頭
        count = random.randint(1, 2)
        spacing = screen_width // (count + 1)
        for i in range(count):
            x = (i + 1) * spacing + random.randint(-20, 20)
            log_width = random.randint(80, 120)
            log_height = LANE_HEIGHT - 10
            speed = random.uniform(1.5, 3.5)
            lane.obstacles.append(Obstacle(
                x=x, y=lane.y + 5,
                width=log_width, height=log_height,
                speed=speed, color=COLOR_LOG, direction=direction,
            ))
        logger.debug(f"Generated {count} logs on water lane {lane_index}")

    elif lane.lane_type == LANE_RAIL:
        # 生成火車
        x = random.randint(0, screen_width // 2)
        train_width = random.randint(120, 200)
        train_height = LANE_HEIGHT - 10
        speed = random.uniform(4.0, 7.0)
        lane.obstacles.append(Obstacle(
            x=x, y=lane.y + 5,
            width=train_width, height=train_height,
            speed=speed, color=COLOR_TRAIN, direction=direction,
        ))
        logger.debug(f"Generated train on rail lane {lane_index}")


def generate_lane(lane_index: int, screen_width: int, previous_type: Optional[str] = None) -> Lane:
    """
    Constraint: Lane hopping, procedural generation
    程序化生成新車道，避免連續相同類型的車道
    """
    # 決定車道類型 - 避免連續相同類型
    weights = [40, 30, 20, 10]  # grass, road, water, rail
    lane_types = [LANE_GRASS, LANE_ROAD, LANE_WATER, LANE_RAIL]

    if previous_type:
        idx = lane_types.index(previous_type)
        weights[idx] = max(5, weights[idx] // 2)  # 降低相同類型的機率

    lane_type = random.choices(lane_types, weights=weights)[0]

    y = lane_index * LANE_HEIGHT
    lane = Lane(lane_type=lane_type, y=y)
    generate_obstacles_for_lane(lane, lane_index, screen_width)
    return lane


def check_collision(player: Player, lanes: List[Lane], screen_width: int) -> bool:
    """
    Constraint: Lane hopping, procedural generation
    檢查玩家是否與障礙物碰撞
    """
    player_rect = pygame.Rect(
        player.pixel_x - PLAYER_WIDTH // 2,
        player.pixel_y - PLAYER_HEIGHT // 2,
        PLAYER_WIDTH,
        PLAYER_HEIGHT,
    )

    lane_index = get_lane_index_from_y(int(player.pixel_y))
    if 0 <= lane_index < len(lanes):
        lane = lanes[lane_index]
        for obs in lane.obstacles:
            obs_rect = pygame.Rect(obs.x, obs.y, obs.width, obs.height)
            if player_rect.colliderect(obs_rect):
                logger.info(f"Player collided with obstacle on lane {lane_index}")
                return True

    return False


def is_player_on_log(player: Player, lanes: List[Lane]) -> bool:
    """檢查玩家是否在水道上且站在木頭上"""
    lane_index = get_lane_index_from_y(int(player.pixel_y))
    if lane_index < 0 or lane_index >= len(lanes):
        return False

    lane = lanes[lane_index]
    if lane.lane_type != LANE_WATER:
        return True  # 不是水道，安全

    player_rect = pygame.Rect(
        player.pixel_x - PLAYER_WIDTH // 2,
        player.pixel_y - PLAYER_HEIGHT // 2,
        PLAYER_WIDTH,
        PLAYER_HEIGHT,
    )

    for obs in lane.obstacles:
        obs_rect = pygame.Rect(obs.x, obs.y, obs.width, obs.height)
        if player_rect.colliderect(obs_rect):
            return True  # 站在木頭上

    return False  # 掉進水裡


def update_obstacles(lanes: List[Lane], screen_width: int, dt: float) -> None:
    """更新所有障礙物的位置"""
    for lane in lanes:
        for obs in lane.obstacles:
            obs.x += obs.speed * obs.direction * dt * 60
            # 循環繞圈 - 從一側消失後從另一側出現
            if obs.direction > 0 and obs.x > screen_width + 50:
                obs.x = -obs.width - 50
                obs.y = lane.y + 5
            elif obs.direction < 0 and obs.x < -obs.width - 50:
                obs.x = screen_width + 50
                obs.y = lane.y + 5


def generate_front_lanes(lanes: List[Lane], max_lanes: int, screen_width: int) -> None:
    """在前方生成新車道，確保遠方也有車道"""
    while len(lanes) < max_lanes:
        prev_type = lanes[-1].lane_type if lanes else None
        new_lane = generate_lane(len(lanes), screen_width, prev_type)
        lanes.append(new_lane)
        logger.debug(f"Generated new lane {len(lanes) - 1}: {new_lane.lane_type}")


def generate_rear_lanes(lanes: List[Lane], player: Player, screen_width: int) -> None:
    """當玩家前進時，在畫面頂部生成新車道，移除底部舊車道"""
    # 確保前方有足夠的車道
    while len(lanes) <= player.grid_y + 15:
        prev_type = lanes[-1].lane_type if lanes else None
        new_lane = generate_lane(len(lanes), screen_width, prev_type)
        lanes.append(new_lane)
        logger.debug(f"Generated new lane {len(lanes) - 1}: {new_lane.lane_type}")


def render_lane(screen: pygame.Surface, lane: Lane, lane_index: int, scroll_y: int, screen_width: int) -> None:
    """繪製單條車道"""
    y_draw = lane.y - scroll_y

    if lane.lane_type == LANE_GRASS:
        pygame.draw.rect(screen, COLOR_GRASS, (0, y_draw, screen_width, LANE_HEIGHT))

    elif lane.lane_type == LANE_ROAD:
        pygame.draw.rect(screen, COLOR_ROAD, (0, y_draw, screen_width, LANE_HEIGHT))
        # 道路中線
        for x in range(0, screen_width, 40):
            pygame.draw.rect(screen, COLOR_ROAD_LINE, (x, y_draw + LANE_HEIGHT // 2 - 1, 20, 2))

    elif lane.lane_type == LANE_WATER:
        pygame.draw.rect(screen, COLOR_WATER, (0, y_draw, screen_width, LANE_HEIGHT))

    elif lane.lane_type == LANE_RAIL:
        pygame.draw.rect(screen, COLOR_RAIL, (0, y_draw, screen_width, LANE_HEIGHT))
        # 鐵軌線
        for x in range(0, screen_width, 30):
            pygame.draw.rect(screen, COLOR_GRAY, (x, y_draw + 10, 15, 4))
            pygame.draw.rect(screen, COLOR_GRAY, (x, y_draw + LANE_HEIGHT - 14, 15, 4))

    # 繪製障礙物
    for obs in lane.obstacles:
        obs_y = y_draw + 5
        pygame.draw.rect(screen, obs.color, (obs.x, obs_y, obs.width, obs.height))


def render_player(screen: pygame.Surface, player: Player, scroll_y: int) -> None:
    """繪製玩家角色 (極簡風格)"""
    if not player.alive:
        return

    x = int(player.pixel_x)
    y = int(player.pixel_y - scroll_y)

    # 身體
    pygame.draw.rect(screen, COLOR_PLAYER, (x - PLAYER_WIDTH // 2, y - PLAYER_HEIGHT // 2, PLAYER_WIDTH, PLAYER_HEIGHT))
    # 眼睛
    pygame.draw.circle(screen, COLOR_BLACK, (x - 6, y - 6), 4)
    pygame.draw.circle(screen, COLOR_BLACK, (x + 6, y - 6), 4)


def render_score(screen: pygame.Surface, score: int, screen_width: int) -> None:
    """顯示分數"""
    font = pygame.font.Font(None, 48)
    score_text = font.render(f"{score}", True, COLOR_WHITE)
    # 分數背景
    text_rect = score_text.get_rect(center=(screen_width // 2, 40))
    bg_rect = text_rect.inflate(20, 10)
    bg_surf = pygame.Surface(bg_rect.size, pygame.SRCALPHA)
    bg_surf.fill(COLOR_SCORE_BG)
    screen.blit(bg_surf, bg_rect)
    screen.blit(score_text, text_rect)


def render_game_over(screen: pygame.Surface, score: int, screen_width: int, screen_height: int) -> None:
    """顯示遊戲結束畫面"""
    overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))

    font_big = pygame.font.Font(None, 72)
    font_small = pygame.font.Font(None, 36)

    game_over_text = font_big.render("Game Over", True, COLOR_WHITE)
    score_text = font_small.render(f"Score: {score}", True, COLOR_WHITE)
    restart_text = font_small.render("Press R to Restart", True, COLOR_WHITE)

    screen.blit(game_over_text, (screen_width // 2 - game_over_text.get_width() // 2, screen_height // 2 - 80))
    screen.blit(score_text, (screen_width // 2 - score_text.get_width() // 2, screen_height // 2))
    screen.blit(restart_text, (screen_width // 2 - restart_text.get_width() // 2, screen_height // 2 + 60))


def reset_game(screen_width: int) -> Tuple[Player, List[Lane]]:
    """重設遊戲狀態"""
    player = Player(
        grid_x=screen_width // (2 * GRID_SIZE),
        grid_y=0,
        pixel_x=screen_width // 2,
        pixel_y=LANE_HEIGHT * 2,
        score=0,
        max_y=0,
    )

    # 生成初始車道 (確保起點附近是安全的草地)
    lanes: List[Lane] = []
    lane_count = 15
    for i in range(lane_count):
        if i <= 2:
            lane = Lane(lane_type=LANE_GRASS, y=i * LANE_HEIGHT)
        else:
            prev_type = lanes[-1].lane_type if lanes else None
            lane = generate_lane(i, screen_width, prev_type)
        lanes.append(lane)

    return player, lanes


def main() -> None:
    """遊戲主迴圈"""
    args = parse_args()

    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logger.debug("Debug mode enabled")

    logger.info(f"Starting Crossy Road game ({args.width}x{args.height})")

    # 初始化 Pygame
    # Constraint: 使用Pygame - 適合製作2D遊戲原型
    pygame.init()
    screen = pygame.display.set_mode((args.width, args.height))
    pygame.display.set_caption("Crossy Road")
    clock = pygame.time.Clock()

    player, lanes = reset_game(args.width)
    running = True
    game_over = False

    while running:
        dt = clock.tick(args.fps) / 1000.0

        # 事件處理
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

                if game_over:
                    if event.key == pygame.K_r:
                        logger.info("Restarting game")
                        player, lanes = reset_game(args.width)
                        game_over = False
                    continue

                # Task: 使腳本接收輸入參數 - 方向鍵控制移動
                # Constraint: Lane hopping - 玩家在車道之間跳躍
                if not player.moving and player.alive:
                    target_x, target_y = player.pixel_x, player.pixel_y
                    moved = False

                    if event.key == pygame.K_UP or event.key == pygame.K_w:
                        target_y = player.pixel_y - LANE_HEIGHT
                        player.grid_y += 1
                        moved = True
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        target_y = player.pixel_y + LANE_HEIGHT
                        player.grid_y -= 1
                        moved = True
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        target_x = player.pixel_x - GRID_SIZE
                        player.grid_x -= 1
                        moved = True
                    elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        target_x = player.pixel_x + GRID_SIZE
                        player.grid_x += 1
                        moved = True

                    if moved:
                        # 確保玩家不會超出螢幕左右邊界
                        target_x = max(PLAYER_WIDTH // 2, min(args.width - PLAYER_WIDTH // 2, target_x))
                        player.moving = True
                        player.target_x = target_x
                        player.target_y = target_y
                        logger.debug(f"Player moving to grid ({player.grid_x}, {player.grid_y})")

        # 更新玩家位置 (平滑移動)
        if player.moving and player.alive:
            dx = player.target_x - player.pixel_x
            dy = player.target_y - player.pixel_y
            dist = (dx ** 2 + dy ** 2) ** 0.5

            if dist < 2:
                player.pixel_x = player.target_x
                player.pixel_y = player.target_y
                player.moving = False

                # 更新分數 (基於最遠到達位置)
                # Constraint: Lane hopping - 計算跳躍次數作為分數
                lane_index = get_lane_index_from_y(int(player.pixel_y))
                if lane_index > player.max_y:
                    player.max_y = lane_index
                    player.score = player.max_y
                    logger.debug(f"Score updated: {player.score}")

                # 生成更多車道
                generate_rear_lanes(lanes, player, args.width)
            else:
                move_amount = player.move_speed * dt * 60
                player.pixel_x += (dx / dist) * move_amount
                player.pixel_y += (dy / dist) * move_amount

        # 更新障礙物位置
        update_obstacles(lanes, args.width, dt)

        # 碰撞檢測
        if player.alive and not player.moving:
            # 檢查是否超出畫面底部
            if player.pixel_y > len(lanes) * LANE_HEIGHT:
                logger.info("Player fell off the bottom")
                player.alive = False
                game_over = True

            # 檢查障礙物碰撞 (道路和鐵軌)
            lane_idx = get_lane_index_from_y(int(player.pixel_y))
            if 0 <= lane_idx < len(lanes):
                lane = lanes[lane_idx]
                if lane.lane_type in (LANE_ROAD, LANE_RAIL):
                    if check_collision(player, lanes, args.width):
                        player.alive = False
                        game_over = True
                        logger.info(f"Game Over! Score: {player.score}")

                # 水道上檢查是否在木頭上
                elif lane.lane_type == LANE_WATER:
                    if not is_player_on_log(player, lanes):
                        player.alive = False
                        game_over = True
                        logger.info(f"Player drowned! Score: {player.score}")

        # 計算捲軸偏移 (讓玩家保持在畫面中央偏下)
        scroll_y = player.pixel_y - args.height * 0.6

        # 渲染
        screen.fill(COLOR_BLACK)

        # 繪製車道
        for i, lane in enumerate(lanes):
            y_draw = lane.y - scroll_y
            if -LANE_HEIGHT < y_draw < args.height + LANE_HEIGHT:
                render_lane(screen, lane, i, int(scroll_y), args.width)

        # 繪製玩家
        render_player(screen, player, int(scroll_y))

        # 繪製分數
        render_score(screen, player.score, args.width)

        # 繪製遊戲結束
        if game_over:
            render_game_over(screen, player.score, args.width, args.height)

        pygame.display.flip()

    pygame.quit()
    logger.info("Game closed")


if __name__ == "__main__":
    main()
