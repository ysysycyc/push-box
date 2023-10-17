import os
import sys

import pygame


def get_resource_path(file_path):
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    abs_path = os.path.join(base_path, file_path)
    return abs_path


def draw_button_text(self, button_text_str, pos, button_name, hover_color=(255, 255, 255),
                     normal_color=(100, 100, 100)):
    mouse_pos = pygame.mouse.get_pos()
    button_text = self.font.render(button_text_str, True, normal_color)
    self.button_rect_dict[button_name] = button_text.get_rect(center=pos)

    if self.button_rect_dict[button_name].collidepoint(mouse_pos):
        colored_text = self.font.render(button_text_str, True, hover_color)
    else:
        colored_text = self.font.render(button_text_str, True, normal_color)

    self.screen.blit(colored_text, self.button_rect_dict[button_name])
