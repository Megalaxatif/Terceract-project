import pygame
from . import menu_button
from pathlib import Path


class Menu:
    def __init__(self, game_context):
        self.game_context = game_context

        self.screen = pygame.display.set_mode(
            (self.game_context.screen.get_size())
        )
        pygame.display.set_caption("Main Menu")

        # state
        self.game_paused = True
        self.menu_state = "main"

        # font & colors
        self.font = pygame.font.SysFont("arialblack", 40)
        self.TEXT_COL = (255, 255, 255)

        # paths
        root_dir = Path(__file__).resolve().parent

        # load images
        self.resume_img = pygame.image.load(
            root_dir / "images/button_resume.png"
        ).convert_alpha()
        self.options_img = pygame.image.load(
            root_dir / "images/button_options.png"
        ).convert_alpha()
        self.quit_img = pygame.image.load(
            root_dir / "images/button_quit.png"
        ).convert_alpha()
        self.video_img = pygame.image.load(
            root_dir / "images/button_video.png"
        ).convert_alpha()
        self.audio_img = pygame.image.load(
            root_dir / "images/button_audio.png"
        ).convert_alpha()
        self.keys_img = pygame.image.load(
            root_dir / "images/button_keys.png"
        ).convert_alpha()
        self.back_img = pygame.image.load(
            root_dir / "images/button_back.png"
        ).convert_alpha()

        # buttons
        self.resume_button = menu_button.MenuButton(304, 125, self.resume_img, 1)
        self.options_button = menu_button.MenuButton(297, 250, self.options_img, 1)
        self.quit_button = menu_button.MenuButton(336, 375, self.quit_img, 1)

        self.video_button = menu_button.MenuButton(226, 75, self.video_img, 1)
        self.audio_button = menu_button.MenuButton(225, 200, self.audio_img, 1)
        self.keys_button = menu_button.MenuButton(246, 325, self.keys_img, 1)
        self.back_button = menu_button.MenuButton(332, 450, self.back_img, 1)

    def draw_text(self, text, x, y):
        img = self.font.render(text, True, self.TEXT_COL)
        self.screen.blit(img, (x, y))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.game_paused = not self.game_paused

    def update(self):
        self.screen.fill((45, 45, 45))

        if self.menu_state == "main":
            if self.resume_button.draw(self.screen):
                self.game_context.current_mini_game = "game"
            if self.options_button.draw(self.screen):
                self.menu_state = "options"
            if self.quit_button.draw(self.screen):
                pygame.event.post(pygame.event.Event(pygame.QUIT)) # quit properly without crash
                return
        elif self.menu_state == "options":
            if self.video_button.draw(self.screen):
                print("Video Settings")
            if self.audio_button.draw(self.screen):
                print("Audio Settings")
            if self.keys_button.draw(self.screen):
                print("Change Key Bindings")
            if self.back_button.draw(self.screen):
                self.menu_state = "main"

        else:
            self.draw_text("Press SPACE to pause", 160, 250)

        pygame.display.update()

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            self.handle_events()
            self.update()
            clock.tick(60)

        pygame.quit()

