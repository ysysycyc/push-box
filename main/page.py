import pygame


class Page:
    def __init__(self, game_manager, page_name, silent_mode=False):
        self.game_manager = game_manager
        if not silent_mode:
            pygame.init()
            pygame.display.set_caption(page_name)

    def start(self):
        pass
