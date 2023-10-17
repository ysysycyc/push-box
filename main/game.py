import os
import random
import sys
import time

import pygame
from pygame import mixer

import chooseMap
import gameManager
import util
from page import Page

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
os.environ['PYTHON_CONFIGURE_OPTS'] = '--enable-shared'


class PushBoxGame(Page):
    def __init__(self, game_manager, seed=0, board_size=12, silent_mode=True, map='demo.txt'):
        super().__init__(game_manager, "Push Box Game", silent_mode=silent_mode)

        self.board_size = board_size
        self.grid_size = self.board_size ** 2
        self.cell_size = 40
        self.width = self.height = self.board_size * self.cell_size

        self.border_size = 20
        self.display_width = self.width + 2 * self.border_size
        self.display_height = self.height + 2 * self.border_size + 40

        self.box_img = pygame.image.load(util.get_resource_path(os.path.join('image', 'box.png')))
        self.target_img = pygame.image.load(util.get_resource_path(os.path.join('image', 'target.png')))
        self.wall_img = pygame.image.load(util.get_resource_path(os.path.join('image', 'wall.png')))
        self.human_img = pygame.image.load(util.get_resource_path(os.path.join('image', 'human.png')))

        # #:wall -:whitespace B:box H:human T:target
        # self.map = [
        #     "#####----",
        #     "#H--#----",
        #     "#-BB#-###",
        #     "#-B-#-#T#",
        #     "###-###T#",
        #     "-##----T#",
        #     "-#---#--#",
        #     "-#---####",
        #     "-#####---"
        # ]
        with open(util.get_resource_path(os.path.join('map', map)), 'r') as map_file:
            self.map = map_file.read().splitlines()

        self.silent_mode = silent_mode
        if not silent_mode:
            self.screen = pygame.display.set_mode((self.display_width, self.display_height))
            self.font = pygame.font.Font(None, 36)

            # Load sound effects
            mixer.init()
            self.sound_eat = mixer.Sound(util.get_resource_path(os.path.join('sound', 'eat.wav')))
            self.sound_game_over = mixer.Sound(util.get_resource_path(os.path.join('sound', 'game_over.wav')))
            self.sound_victory = mixer.Sound(util.get_resource_path(os.path.join('sound', 'victory.wav')))
        else:
            self.screen = None
            self.font = None

        self.human = None
        self.box = None
        self.target = None
        self.wall = None
        self.button_rect_dict = {}

        self.direction = None
        self.score = 0
        self.seed_value = seed

        random.seed(seed)  # Set random seed.

        self.reset()

    def reset(self):
        self.human = [(i, j) for i, row in enumerate(self.map) for j, char in enumerate(row) if char == "H"][0]
        self.box = [(i, j) for i, row in enumerate(self.map) for j, char in enumerate(row) if char == "B"]
        self.target = [(i, j) for i, row in enumerate(self.map) for j, char in enumerate(row) if char == "T"]
        self.wall = [(i, j) for i, row in enumerate(self.map) for j, char in enumerate(row) if char == "#"]
        self.direction = "DOWN"  # Human starts downward in each round
        self.score = 0

    def step(self, action):
        if action == -1:
            return False

        self._update_direction(action)  # Update direction based on action.

        # Move human based on current action.
        row, col = self._move_obj(self.human)
        human_next = (row, col)

        # skip when out of range
        if row < 0 or row >= self.board_size or col < 0 or col >= self.board_size:
            return False
        if (row, col) in self.wall:
            return False

        # Check if human occurs box
        if (row, col) in self.box:
            box_index = self.box.index((row, col))
            row, col = self._move_obj((row, col))
            if (row, col) not in self.wall and (row, col) not in self.box:
                self.human = human_next
                box_next = (row, col)
                self.box[box_index] = box_next
                if not self.silent_mode:
                    self.sound_eat.play()
        else:
            self.human = human_next

        # Check if snake collided with itself or the wall
        done = set(self.box) == set(self.target)

        if done:  # If game is over and the game is not in silent mode, play game over sound effect.
            if not self.silent_mode:
                self.sound_victory.play()

        return done

    def _move_obj(self, obj):
        row, col = obj
        if self.direction == "UP":
            row -= 1
        elif self.direction == "DOWN":
            row += 1
        elif self.direction == "LEFT":
            col -= 1
        elif self.direction == "RIGHT":
            col += 1
        return row, col

    # 0: UP, 1: LEFT, 2: RIGHT, 3: DOWN
    def _update_direction(self, action):
        if action == 0:
            self.direction = "UP"
        elif action == 1:
            self.direction = "LEFT"
        elif action == 2:
            self.direction = "RIGHT"
        elif action == 3:
            self.direction = "DOWN"

    def draw_score(self):
        # count box in target
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text,
                         (self.display_width // 2 - score_text.get_width() // 2, self.height + 2 * self.border_size))

    def draw_game_over_screen(self):
        game_over_text = self.font.render("GAME OVER", True, (255, 255, 255))
        final_score_text = self.font.render(f"SCORE: {self.score}", True, (255, 255, 255))
        retry_button_text = "RETRY"

        self.screen.fill((0, 0, 0))
        self.screen.blit(game_over_text,
                         (self.display_width // 2 - game_over_text.get_width() // 2, self.display_height // 4))
        self.screen.blit(final_score_text, (self.display_width // 2 - final_score_text.get_width() // 2,
                                            self.display_height // 4 + final_score_text.get_height() + 10))
        util.draw_button_text(self, retry_button_text, (self.display_width // 2, self.display_height // 2), "retry")
        pygame.display.update()

    def render(self):
        self.screen.fill((0, 0, 0))

        # Draw border
        pygame.draw.rect(self.screen, (255, 255, 255),
                         (self.border_size - 2, self.border_size - 2, self.width + 4, self.height + 4), 2)

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
        r, c = self.human
        self.screen.blit(self.human_img, (c * self.cell_size + self.border_size, r * self.cell_size + self.border_size))

        # Draw score
        self.score = len(set(self.box) & set(self.target)) * 10
        self.draw_score()
        self.draw_button()

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def draw_button(self):
        util.draw_button_text(self, "BACK", (40, self.display_height - 30), "back")
        # Draw reset button
        util.draw_button_text(self, "RESET", (self.display_width - 40, self.display_height - 30), "reset")

    def start(self):
        game_state = "running"

        update_interval = 0.1
        start_time = time.time()
        action = -1

        while True:
            for event in pygame.event.get():
                mouse_pos = pygame.mouse.get_pos()
                if game_state == "running":
                    if event.type == pygame.KEYDOWN:
                        if event.key in [pygame.K_UP, pygame.K_w]:
                            action = 0
                        elif event.key in [pygame.K_DOWN, pygame.K_s]:
                            action = 3
                        elif event.key in [pygame.K_LEFT, pygame.K_a]:
                            action = 1
                        elif event.key in [pygame.K_RIGHT, pygame.K_d]:
                            action = 2
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if self.button_rect_dict["reset"].collidepoint(mouse_pos):
                            self.reset()
                            game_state = "running"
                        elif self.button_rect_dict["back"].collidepoint(mouse_pos):
                            game_state = "stop"
                            self.game_manager.direct_page(chooseMap.PushBoxChooseMap(self.game_manager))

                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if game_state == "game_over" and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.button_rect_dict["retry"].collidepoint(mouse_pos):
                        self.reset()
                        game_state = "running"

            if game_state == "game_over":
                self.draw_game_over_screen()

            if game_state == 'running':
                if time.time() - start_time >= update_interval:
                    done = self.step(action)
                    self.render()
                    start_time = time.time()
                    action = -1

                    if done:
                        game_state = "game_over"


if __name__ == "__main__":
    seed = random.randint(0, 1e9)
    gameManager.GameManager().direct_page(
        PushBoxGame(gameManager.GameManager(), seed=seed, silent_mode=False, board_size=9))
