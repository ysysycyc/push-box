import os
import sys
import pygame


def get_resource_path(file_path):
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    abs_path = os.path.join(base_path, file_path)
    print(abs_path)
    return abs_path
