import pygame
from . import menu_button
from pathlib import Path

class Menu:
    def __init__(self, game_context):
        self.game_context = game_context

        pygame.init()

        self.SCREEN_WIDTH = 1080
        self.SCREEN_HEIGHT = 720
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("Main Menu")

        self.game_paused = True
        self.menu_state = "main"

        self.font = pygame.font.SysFont("arialblack", 40)
        self.TEXT_COL = (255, 255, 255)

        root_dir = Path(__file__).resolve().parent

        # load images raw
        self.resume_img_raw  = pygame.image.load(root_dir / "images/button_resume.png").convert_alpha()
        self.options_img_raw = pygame.image.load(root_dir / "images/button_options.png").convert_alpha()
        self.quit_img_raw    = pygame.image.load(root_dir / "images/button_quit.png").convert_alpha()

        self.video_img_raw = pygame.image.load(root_dir / "images/button_video.png").convert_alpha()
        self.audio_img_raw = pygame.image.load(root_dir / "images/button_audio.png").convert_alpha()
        self.keys_img_raw  = pygame.image.load(root_dir / "images/button_keys.png").convert_alpha()
        self.back_img_raw  = pygame.image.load(root_dir / "images/button_back.png").convert_alpha()


        self.create_buttons()

    def create_buttons(self):
        center_x = self.SCREEN_WIDTH // 2
        delta = min(self.game_context.delta_w, self.game_context.delta_h)

        self.resume_img = pygame.transform.scale(
            self.resume_img_raw,
            (
                int(self.resume_img_raw.get_width() * delta),
                int(self.resume_img_raw.get_height() * delta)
            )
        )

        self.options_img = pygame.transform.scale(
            self.options_img_raw,
            (
                int(self.options_img_raw.get_width() * delta),
                int(self.options_img_raw.get_height() * delta)
            )
        )

        self.quit_img = pygame.transform.scale(
            self.quit_img_raw,
            (
                int(self.quit_img_raw.get_width() * delta),
                int(self.quit_img_raw.get_height() * delta)
            )
        )

        self.video_img = pygame.transform.scale(
            self.video_img_raw,
            (
                int(self.video_img_raw.get_width() * delta),
                int(self.video_img_raw.get_height() * delta)
            )
        )

        self.audio_img = pygame.transform.scale(
            self.audio_img_raw,
            (
                int(self.audio_img_raw.get_width() * delta),
                int(self.audio_img_raw.get_height() * delta)
            )
        )

        self.keys_img = pygame.transform.scale(
            self.keys_img_raw,
            (
                int(self.keys_img_raw.get_width() * delta),
                int(self.keys_img_raw.get_height() * delta)
            )
        )

        self.back_img = pygame.transform.scale(
            self.back_img_raw,
            (
                int(self.back_img_raw.get_width() * delta),
                int(self.back_img_raw.get_height() * delta)
            )
        )

        # menu principal
        self.resume_button = menu_button.MenuButton(
            center_x // 1.5 - self.resume_img.get_width() // 2,
            int(self.SCREEN_HEIGHT * 0.25),
            self.resume_img,
            1
        )
        
        self.options_button = menu_button.MenuButton(
            center_x // 1.5- self.options_img.get_width() // 2,
            int(self.SCREEN_HEIGHT * 0.4),
            self.options_img,
            1
        )
        self.quit_button = menu_button.MenuButton(
            center_x // 1.5 - self.quit_img.get_width() // 2,
            int(self.SCREEN_HEIGHT * 0.55),
            self.quit_img,
            1
        )

        # menu options
        self.video_button = menu_button.MenuButton(
            center_x // 1.5 - self.video_img.get_width() // 2,
            int(self.SCREEN_HEIGHT * 0.25),
            self.video_img,
            1
        )
        self.audio_button = menu_button.MenuButton(
            center_x // 1.5 - self.audio_img.get_width() // 2,
            int(self.SCREEN_HEIGHT * 0.4),
            self.audio_img,
            1
        )
        self.keys_button = menu_button.MenuButton(
            center_x // 1.5 - self.keys_img.get_width() // 2,
            int(self.SCREEN_HEIGHT * 0.55),
            self.keys_img,
            1
        )
        self.back_button = menu_button.MenuButton(
            center_x // 1.5 - self.back_img.get_width() // 2,
            int(self.SCREEN_HEIGHT * 0.7),
            self.back_img,
            1
        )

    def draw_text_centered(self, text, y):
        img = self.font.render(text, True, self.TEXT_COL)
        rect = img.get_rect(center=(self.SCREEN_WIDTH // 2, y))
        self.screen.blit(img, rect)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.game_paused = not self.game_paused

        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = self.screen.get_size()
        self.create_buttons()

    def update(self):
        self.screen.fill((45, 45, 45))
        self.SCREEN_WIDTH = 1080 * self.game_context.delta_w
        self.SCREEN_HEIGHT = 720 * self.game_context.delta_h

        if self.menu_state == "main":
            if self.resume_button.draw(self.screen):
                self.game_context.current_mini_game = "game"
            if self.options_button.draw(self.screen):
                self.menu_state = "options"
            if self.quit_button.draw(self.screen):
                pygame.quit()

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
            self.draw_text_centered("Press SPACE to pause", self.SCREEN_HEIGHT // 2)
        
        self.handle_events()
        # pygame.display.update()

