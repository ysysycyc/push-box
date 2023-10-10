import pygame
import sys

# 游戏窗口尺寸
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# 方格尺寸
GRID_SIZE = 50

# 颜色常量
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# 游戏地图
MAP = [
    "########",
    "#      #",
    "#      #",
    "#  BP  #",
    "#  T   #",
    "#      #",
    "#      #",
    "########"
]

# 游戏初始化
pygame.init()
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Push Box Game")

# 游戏角色图片
player_img = pygame.image.load("image/human.png")
box_img = pygame.image.load("image/box.png")
target_img = pygame.image.load("image/target.png")
wall_img = pygame.image.load("image/wall.png")

# 游戏角色在地图中的位置
player_x = 3
player_y = 3

# 游戏主循环
while True:
    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if MAP[player_y - 1][player_x] != "#":
                    if MAP[player_y - 1][player_x] == "B" and MAP[player_y - 2][player_x] != "#":
                        MAP[player_y - 2] = MAP[player_y - 2][:player_x] + "B" + MAP[player_y - 2][player_x + 1:]
                    player_y -= 1
            elif event.key == pygame.K_DOWN:
                if MAP[player_y + 1][player_x] != "#":
                    if MAP[player_y + 1][player_x] == "B" and MAP[player_y + 2][player_x] != "#":
                        MAP[player_y + 2] = MAP[player_y + 2][:player_x] + "B" + MAP[player_y + 2][player_x + 1:]
                    player_y += 1
            elif event.key == pygame.K_LEFT:
                if MAP[player_y][player_x - 1] != "#":
                    if MAP[player_y][player_x - 1] == "B" and MAP[player_y][player_x - 2] != "#":
                        MAP[player_y] = MAP[player_y][:player_x - 2] + "B" + MAP[player_y][player_x - 1:]
                    player_x -= 1
            elif event.key == pygame.K_RIGHT:
                if MAP[player_y][player_x + 1] != "#":
                    if MAP[player_y][player_x + 1] == "B" and MAP[player_y][player_x + 2] != "#":
                        MAP[player_y] = MAP[player_y][:player_x + 2] + "B" + MAP[player_y][player_x + 3:]
                    player_x += 1

    # 清空窗口
    window.fill(BLACK)

    # 绘制地图
    for row in range(len(MAP)):
        for col in range(len(MAP[0])):
            x = col * GRID_SIZE
            y = row * GRID_SIZE
            if MAP[row][col] == "#":
                window.blit(wall_img, (x, y))
            elif MAP[row][col] == "P":
                window.blit(player_img, (x, y))
            elif MAP[row][col] == "B":
                window.blit(box_img, (x, y))
            elif MAP[row][col] == "T":
                window.blit(target_img, (x, y))

    # 更新窗口
    pygame.display.update()
