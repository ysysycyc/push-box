import os
import random
import sys
import pygame
from pygame import mixer

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = '1'
os.environ['PYTHON_CONFIGURE_OPTS'] = '--enable-shared'


class PushBoxGame:
    def __init__(self, seed=0, board_size=12, silent_mode=True, map='demo.txt'):
        self.board_size = board_size
        self.grid_size = self.board_size ** 2
        self.cell_size = 40
        self.width = self.height = self.board_size * self.cell_size

        self.border_size = 20
        self.display_width = self.width + 2 * self.border_size
        self.display_height = self.height + 2 * self.border_size + 40

        self.box_img = pygame.image.load(self._get_resouce_path(os.path.join('image', 'box.png')))
        self.target_img = pygame.image.load(self._get_resouce_path(os.path.join('image', 'target.png')))
        self.wall_img = pygame.image.load(self._get_resouce_path(os.path.join('image', 'wall.png')))
        self.human_img = pygame.image.load(self._get_resouce_path(os.path.join('image', 'human.png')))

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
        with open(self._get_resouce_path(os.path.join('map', map)), 'r') as map_file:
            self.map = map_file.read().splitlines()

        self.silent_mode = silent_mode
        if not silent_mode:
            pygame.init()
            pygame.display.set_caption("Push Box Game")
            self.screen = pygame.display.set_mode((self.display_width, self.display_height))
            self.font = pygame.font.Font(None, 36)

            # Load sound effects
            mixer.init()
            self.sound_eat = mixer.Sound(self._get_resouce_path(os.path.join('sound', 'eat.wav')))
            self.sound_game_over = mixer.Sound(self._get_resouce_path(os.path.join('sound', 'game_over.wav')))
            self.sound_victory = mixer.Sound(self._get_resouce_path(os.path.join('sound', 'victory.wav')))
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

    def _get_resouce_path(self, file_path):
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            base_path = sys._MEIPASS
        else:
            base_path = os.path.abspath(".")
        abs_path = os.path.join(base_path, file_path)
        print(abs_path)
        return abs_path

    def draw_score(self):
        # count box in target
        score_text = self.font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_text, (self.border_size, self.height + 2 * self.border_size))

    def draw_welcome_screen(self):
        title_text = self.font.render("PUSH BOX GAME", True, (255, 255, 255))
        start_button_text = "START"

        self.screen.fill((0, 0, 0))
        self.screen.blit(title_text, (self.display_width // 2 - title_text.get_width() // 2, self.display_height // 4))
        self.draw_button_text(start_button_text, (self.display_width // 2, self.display_height // 2), "start")
        pygame.display.update()

    def draw_game_over_screen(self):
        game_over_text = self.font.render("GAME OVER", True, (255, 255, 255))
        final_score_text = self.font.render(f"SCORE: {self.score}", True, (255, 255, 255))
        retry_button_text = "RETRY"

        self.screen.fill((0, 0, 0))
        self.screen.blit(game_over_text,
                         (self.display_width // 2 - game_over_text.get_width() // 2, self.display_height // 4))
        self.screen.blit(final_score_text, (self.display_width // 2 - final_score_text.get_width() // 2,
                                            self.display_height // 4 + final_score_text.get_height() + 10))
        self.draw_button_text(retry_button_text, (self.display_width // 2, self.display_height // 2), "retry")
        pygame.display.update()

    def draw_button_text(self, button_text_str, pos, button_name, hover_color=(255, 255, 255), normal_color=(100, 100, 100)):
        mouse_pos = pygame.mouse.get_pos()
        button_text = self.font.render(button_text_str, True, normal_color)
        self.button_rect_dict[button_name] = button_text.get_rect(center=pos)

        if self.button_rect_dict[button_name].collidepoint(mouse_pos):
            colored_text = self.font.render(button_text_str, True, hover_color)
        else:
            colored_text = self.font.render(button_text_str, True, normal_color)

        self.screen.blit(colored_text, self.button_rect_dict[button_name])

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

        # Draw reset button
        self.draw_button_text("RESET", (self.display_width - 40, self.display_height - 40), "reset")

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


if __name__ == "__main__":
    import time

    seed = random.randint(0, 1e9)
    game = PushBoxGame(seed=seed, silent_mode=False, board_size=9)
    pygame.init()
    game.screen = pygame.display.set_mode((game.display_width, game.display_height))
    pygame.display.set_caption("Push Box Game")
    game.font = pygame.font.Font(None, 36)

    game_state = "welcome"

    # Two hidden button for start and retry click detection
    start_button = game.font.render("START", True, (0, 0, 0))
    retry_button = game.font.render("RETRY", True, (0, 0, 0))
    reset_button = game.font.render("RESET", True, (0, 0, 0))

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
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if game.button_rect_dict["reset"].collidepoint(mouse_pos):
                        game.reset()
                        game_state = "running"

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if game_state == "welcome" and event.type == pygame.MOUSEBUTTONDOWN:
                if game.button_rect_dict["start"].collidepoint(mouse_pos):
                    action = -1  # Reset action variable when starting a new game
                    game_state = "running"

            if game_state == "game_over" and event.type == pygame.MOUSEBUTTONDOWN:
                if game.button_rect_dict["retry"].collidepoint(mouse_pos):
                    game.reset()
                    game_state = "running"

        if game_state == "welcome":
            game.draw_welcome_screen()

        if game_state == "game_over":
            game.draw_game_over_screen()

        if game_state == 'running':
            if time.time() - start_time >= update_interval:
                done = game.step(action)
                game.render()
                start_time = time.time()
                action = -1

                if done:
                    game_state = "game_over"
