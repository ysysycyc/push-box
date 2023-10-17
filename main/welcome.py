import sys
import time

import pygame

import chooseMap
import editor
import gameManager
import util
from page import Page


class PushBoxWelcome(Page):
    def __init__(self, game_manager):
        super().__init__(game_manager, "Welcome Push Box Game")
        self.display_width = 800
        self.display_height = 600
        self.screen = pygame.display.set_mode((self.display_width, self.display_height))
        self.font = pygame.font.Font(None, 36)

        self.button_rect_dict = {}

    def draw_button(self):
        util.draw_button_text(self, "CHOOSE MAP", (self.display_width // 2, self.display_height // 2 - 40),
                              "choose_map")
        util.draw_button_text(self, "EDITOR", (self.display_width // 2, self.display_height // 2), "editor")

    def render(self):
        self.draw_button()

    @staticmethod
    def open_editor():
        editor.PushBoxEditor().start()

    def start(self):
        self.render()

        status = "running"
        update_interval = 0.15
        start_time = time.time()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.button_rect_dict["choose_map"].collidepoint(mouse_pos):
                        status = "stop"
                        self.game_manager.direct_page(chooseMap.PushBoxChooseMap(self.game_manager))
                    elif self.button_rect_dict["editor"].collidepoint(mouse_pos):
                        status = "stop"
                        self.game_manager.direct_page(editor.PushBoxEditor(self.game_manager))

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
    gameManager.GameManager().direct_page(PushBoxWelcome(gameManager.GameManager()))
