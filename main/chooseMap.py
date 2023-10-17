import os
import sys
import time

import pygame

import game
import gameManager
import util
import welcome
from page import Page


class PushBoxChooseMap(Page):
    def __init__(self, game_manager):
        super().__init__(game_manager, "Choose Map")
        self.display_width = 800
        self.display_height = 600
        self.screen = pygame.display.set_mode((self.display_width, self.display_height))
        self.font = pygame.font.Font(None, 36)

        self.button_rect_dict = {}
        self.map_dict = {}
        self.image_group = pygame.sprite.Group()

        self.map_screenshot_path_list = self.get_all_files_in_folder(util.get_resource_path('map_screenshot'))
        self.add_map_screenshot()

    @staticmethod
    def get_all_files_in_folder(folder_path):
        all_files = []

        # 获取文件夹下的所有文件和文件夹名称
        file_list = os.listdir(folder_path)

        # 遍历文件夹下的所有文件和文件夹
        for file_name in file_list:
            # 获取文件（或文件夹）的完整路径
            full_path = os.path.join(folder_path, file_name)

            # 如果是文件则加入all_files列表
            if os.path.isfile(full_path):
                all_files.append(full_path)

        return all_files

    def add_map_screenshot(self):
        # define image size and spacing
        image_width = 200
        image_height = 200
        image_spacing = 20

        # define image rows and columns
        rows = 3
        columns = 3

        screenshot_index = 0

        for row in range(rows):
            for column in range(columns):
                if screenshot_index >= len(self.map_screenshot_path_list):
                    break
                x = (image_width + image_spacing) * column + 50
                y = (image_height + image_spacing) * row + 100
                image_sprite = pygame.sprite.Sprite()
                image_sprite.image = self.get_map_screenshot(self.map_screenshot_path_list[screenshot_index],
                                                             image_width, image_height)
                image_sprite.rect = image_sprite.image.get_rect()
                image_sprite.name = os.path.basename(self.map_screenshot_path_list[screenshot_index]).split(".")[
                                        0] + ".txt"
                image_sprite.rect.x = x
                image_sprite.rect.y = y
                image_sprite.add(self.image_group)
                screenshot_index += 1

    @staticmethod
    def get_map_screenshot(absolute_path, image_width, image_height):
        image = pygame.image.load(absolute_path)
        return pygame.transform.scale(image, (image_width, image_height))

    def draw_button(self):
        util.draw_button_text(self, "BACK", (40, self.display_height - 30), "back")

    def render(self):
        self.draw_button()
        self.image_group.draw(self.screen)

    def start(self):
        self.render()

        status = "running"
        update_interval = 0.15
        start_time = time.time()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.button_rect_dict["back"].collidepoint(mouse_pos):
                        status = "stop"
                        self.game_manager.direct_page(welcome.PushBoxWelcome(self.game_manager))
                    else:
                        for image_sprite in self.image_group:
                            if image_sprite.rect.collidepoint(event.pos):
                                status = "stop"
                                self.game_manager.direct_page(
                                    game.PushBoxGame(self.game_manager, silent_mode=False, map=image_sprite.name))

                if event.type == pygame.MOUSEMOTION:
                    if time.time() - start_time >= update_interval:
                        self.render()
                        start_time = time.time()

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            pygame.display.update()

            if status != "running":
                break


if __name__ == "__main__":
    gameManager.GameManager().direct_page(PushBoxChooseMap(gameManager.GameManager()))
