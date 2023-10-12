import os
import sys
import pygame
import util

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
os.environ['PYTHON_CONFIGURE_OPTS'] = '--enable-shared'


class PushBoxEditor:
    def __init__(self, board_size=12):
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

        obj_height = self.display_height - self.cell_size // 2 - 10
        self.box_img = pygame.image.load(util.get_resource_path(os.path.join('image', 'box.png')))
        self.box_img_rect = self.box_img.get_rect(
            center=(self.border_size + self.cell_size, obj_height))

        self.target_img = pygame.image.load(util.get_resource_path(os.path.join('image', 'target.png')))
        self.target_img_rect = self.target_img.get_rect(
            center=(self.border_size + self.cell_size * 2 + 10, obj_height))

        self.wall_img = pygame.image.load(util.get_resource_path(os.path.join('image', 'wall.png')))
        self.wall_img_rect = self.wall_img.get_rect(
            center=(self.border_size + self.cell_size * 3 + 10 * 2, obj_height))

        self.human_img = pygame.image.load(util.get_resource_path(os.path.join('image', 'human.png')))
        self.human_img_rect = self.human_img.get_rect(
            center=(self.border_size + self.cell_size * 4 + 10 * 3, obj_height))

        self.hammer_img = pygame.image.load(util.get_resource_path(os.path.join('image', 'hammer.png')))
        self.hammer_img_rect = self.hammer_img.get_rect(
            center=(self.border_size + self.cell_size * 5 + 10 * 4, obj_height))

        self.map = []
        self.human = None
        self.box = None
        self.target = None
        self.wall = None
        self.current_obj = ""

        self.reset()

    def reset(self):
        self.map = [["-"] * self.board_size for _ in range(self.board_size)]

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


if __name__ == "__main__":
    editor = PushBoxEditor()
    pygame.init()
    # editor.screen = pygame.display.set_mode((editor.display_width, editor.display_height))
    pygame.display.set_caption("Push Box Editor")
    editor.font = pygame.font.Font(None, 36)

    # Two hidden button for start and retry click detection
    start_button = editor.font.render("START", True, (0, 0, 0))
    retry_button = editor.font.render("RETRY", True, (0, 0, 0))
    reset_button = editor.font.render("RESET", True, (0, 0, 0))

    editor.draw_tool()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if editor.box_img_rect.collidepoint(mouse_pos):
                    editor.current_obj = "B"
                elif editor.target_img_rect.collidepoint(mouse_pos):
                    editor.current_obj = "T"
                elif editor.wall_img_rect.collidepoint(mouse_pos):
                    editor.current_obj = "#"
                elif editor.human_img_rect.collidepoint(mouse_pos):
                    editor.current_obj = "H"
                elif editor.hammer_img_rect.collidepoint(mouse_pos):
                    editor.current_obj = "-"
                else:
                    if editor.current_obj != "":
                        grid_x = (mouse_pos[0] - editor.border_size) // editor.cell_size
                        grid_y = (mouse_pos[1] - editor.border_size) // editor.cell_size
                        if editor.current_obj == "H":
                            human_arr = [(i, j) for i, row in enumerate(editor.map) for j, char in enumerate(row) if
                                         char == "H"]
                            for (i, j) in human_arr:
                                editor.map[i][j] = "-"
                        if grid_y < editor.board_size and grid_x < editor.board_size:
                            editor.map[grid_y][grid_x] = editor.current_obj
                            editor.render()

            if event.type == pygame.MOUSEMOTION:
                if editor.current_obj != "":
                    editor.render()

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()
