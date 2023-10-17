import os
import sys
import time
from datetime import datetime

import pygame

import chooseMap
import gameManager
import util
from page import Page

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
os.environ['PYTHON_CONFIGURE_OPTS'] = '--enable-shared'


class PushBoxEditor(Page):
    def __init__(self, game_manager, board_size=12):
        super().__init__(game_manager, "Push Box Editor")

        self.board_size = board_size
        self.grid_size = self.board_size ** 2
        self.cell_size = 40
        self.width = self.height = self.board_size * self.cell_size

        self.border_size = 20
        self.display_width = self.width + 2 * self.border_size
        self.display_height = self.height + 2 * self.border_size + 40

        self.screen = pygame.display.set_mode((self.display_width, self.display_height))

        pygame.draw.rect(self.screen, (255, 255, 255),
                         (self.border_size - 2, self.border_size - 2, self.width + 4, self.height + 4), 2)
        self.font = pygame.font.Font(None, 36)

        obj_height = self.display_height - self.cell_size // 2 - 10
        self.box_img = pygame.image.load(util.get_resource_path(os.path.join('image', 'box.png')))
        self.box_img_rect = self.box_img.get_rect(
            center=(self.border_size + self.cell_size + 50, obj_height))

        self.target_img = pygame.image.load(util.get_resource_path(os.path.join('image', 'target.png')))
        self.target_img_rect = self.target_img.get_rect(
            center=(self.border_size + self.cell_size * 2 + 10 + 50, obj_height))

        self.wall_img = pygame.image.load(util.get_resource_path(os.path.join('image', 'wall.png')))
        self.wall_img_rect = self.wall_img.get_rect(
            center=(self.border_size + self.cell_size * 3 + 10 * 2 + 50, obj_height))

        self.human_img = pygame.image.load(util.get_resource_path(os.path.join('image', 'human.png')))
        self.human_img_rect = self.human_img.get_rect(
            center=(self.border_size + self.cell_size * 4 + 10 * 3 + 50, obj_height))

        self.hammer_img = pygame.image.load(util.get_resource_path(os.path.join('image', 'hammer.png')))
        self.hammer_img_rect = self.hammer_img.get_rect(
            center=(self.border_size + self.cell_size * 5 + 10 * 4 + 50, obj_height))

        self.map = []
        self.human = None
        self.box = None
        self.target = None
        self.wall = None
        self.current_obj = ""
        self.button_rect_dict = {}
        current_time = datetime.now()
        self.filename = current_time.strftime("%Y%m%d%H%M")

        self.reset()
        self.draw_tool()

    def reset(self):
        self.map = [["-"] * self.board_size for _ in range(self.board_size)]
        self.human = None
        self.box = None
        self.target = None
        self.wall = None
        self.current_obj = ""
        self.button_rect_dict = {}

    def draw_tool(self):
        self.screen.blit(self.box_img, self.box_img_rect)
        self.screen.blit(self.target_img, self.target_img_rect)
        self.screen.blit(self.wall_img, self.wall_img_rect)
        self.screen.blit(self.human_img, self.human_img_rect)
        self.screen.blit(self.hammer_img, self.hammer_img_rect)
        pygame.draw.rect(self.screen, (255, 255, 255),
                         (self.border_size - 2, self.border_size - 2, self.width + 4, self.height + 4), 2)

    def render(self):
        self.screen.fill((0, 0, 0))
        self.draw_tool()
        self.draw_button()

        human_arr = [(i, j) for i, row in enumerate(self.map) for j, char in enumerate(row) if char == "H"]
        self.human = human_arr[0] if len(human_arr) > 0 else None
        self.box = [(i, j) for i, row in enumerate(self.map) for j, char in enumerate(row) if char == "B"]
        self.target = [(i, j) for i, row in enumerate(self.map) for j, char in enumerate(row) if char == "T"]
        self.wall = [(i, j) for i, row in enumerate(self.map) for j, char in enumerate(row) if char == "#"]

        # Draw wall
        for r, c in self.wall:
            self.screen.blit(self.wall_img,
                             (c * self.cell_size + self.border_size, r * self.cell_size + self.border_size))

        # Draw target
        for r, c in self.target:
            self.screen.blit(self.target_img,
                             (c * self.cell_size + self.border_size, r * self.cell_size + self.border_size))

        # Draw box
        for r, c in self.box:
            self.screen.blit(self.box_img,
                             (c * self.cell_size + self.border_size, r * self.cell_size + self.border_size))

        # Draw human
        if self.human:
            r, c = self.human
            self.screen.blit(self.human_img,
                             (c * self.cell_size + self.border_size, r * self.cell_size + self.border_size))

        point_img = ""
        if self.current_obj == "B":
            point_img = self.box_img
        elif self.current_obj == "T":
            point_img = self.target_img
        elif self.current_obj == "H":
            point_img = self.human_img
        elif self.current_obj == "#":
            point_img = self.wall_img
        elif self.current_obj == "-":
            point_img = self.hammer_img

        if point_img != "":
            copy_img = point_img.copy()
            copy_img.set_alpha(128)
            mouse_x, mouse_y = pygame.mouse.get_pos()
            self.screen.blit(copy_img, (mouse_x - self.cell_size // 2, mouse_y - self.cell_size // 2))

    def draw_button(self):
        util.draw_button_text(self, "SAVE", (self.display_width - 40, self.display_height - 30), "save")
        util.draw_button_text(self, "BACK", (40, self.display_height - 30), "back")

    def save_map(self):
        map_file = open('map/' + self.filename + '.txt', 'w')
        map_file.write('\n'.join([''.join(row) for row in self.map]))
        map_file.close()
        # save screenshot
        rect = pygame.Rect(self.border_size - 2, self.border_size - 2, self.width + 4, self.height + 4)
        screenshot = self.screen.subsurface(rect)
        pygame.image.save(screenshot, 'map_screenshot/' + self.filename + '.png')

    def start(self):
        status = "running"
        update_interval = 0.15
        start_time = time.time()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.box_img_rect.collidepoint(mouse_pos):
                        self.current_obj = "B"
                    elif self.target_img_rect.collidepoint(mouse_pos):
                        self.current_obj = "T"
                    elif self.wall_img_rect.collidepoint(mouse_pos):
                        self.current_obj = "#"
                    elif self.human_img_rect.collidepoint(mouse_pos):
                        self.current_obj = "H"
                    elif self.hammer_img_rect.collidepoint(mouse_pos):
                        self.current_obj = "-"
                    elif self.button_rect_dict["save"].collidepoint(mouse_pos):
                        self.save_map()
                    elif self.button_rect_dict["back"].collidepoint(mouse_pos):
                        status = "stop"
                        self.game_manager.direct_page(chooseMap.PushBoxChooseMap(self.game_manager))
                    else:
                        if self.current_obj != "":
                            grid_x = (mouse_pos[0] - self.border_size) // self.cell_size
                            grid_y = (mouse_pos[1] - self.border_size) // self.cell_size
                            if self.current_obj == "H":
                                human_arr = [(i, j) for i, row in enumerate(self.map) for j, char in enumerate(row) if
                                             char == "H"]
                                for (i, j) in human_arr:
                                    self.map[i][j] = "-"
                            if grid_y < self.board_size and grid_x < self.board_size:
                                self.map[grid_y][grid_x] = self.current_obj
                                self.render()

                if event.type == pygame.MOUSEMOTION:
                    if self.current_obj != "":
                        if time.time() - start_time >= update_interval:
                            self.render()
                            start_time = time.time()
                    else:
                        self.draw_button()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.current_obj = ""
                        self.render()

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()

            if status != "running":
                break


if __name__ == "__main__":
    gameManager.GameManager().direct_page(PushBoxEditor(gameManager.GameManager()))
