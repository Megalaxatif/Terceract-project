import pygame
from . import menu_button
from pathlib import Path

class Menu:
    def __init__(self, game_context):
        self.game_context = game_context
        self.SCREEN_WIDTH = 1080
        self.SCREEN_HEIGHT = 720
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("Main Menu")

        self.game_paused = True
        self.menu_state = "menu"
        self.button_lock = False

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
        self.save_img_raw  = pygame.image.load(root_dir / "images/button_save.png").convert_alpha()


        self.create_buttons()

    def create_buttons(self):
        center_x = self.SCREEN_WIDTH // 2
        delta = min(self.game_context.delta_w, self.game_context.delta_h)

        self.save_img = pygame.transform.scale(
            self.save_img_raw,
            (
                int(self.save_img_raw.get_width() * delta),
                int(self.save_img_raw.get_height() * delta)
            )
        )


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
        self.save_button = menu_button.MenuButton(
            center_x // 1.5 - self.save_img.get_width() // 2,
            int(self.SCREEN_HEIGHT * 0.1),
            self.save_img,
            1
        )

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
        for event in pygame.event.get(): # TODO: change this to respect the event queue
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.game_paused = not self.game_paused

        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = self.screen.get_size()
        self.create_buttons()

    def update(self):
        self.screen.fill((45, 45, 45))
        self.SCREEN_WIDTH = 1080 * self.game_context.delta_w
        self.SCREEN_HEIGHT = 720 * self.game_context.delta_h

        if not hasattr(self, "pressed"):
            self.pressed = False  # initialise une fois

        # --- AFFICHAGE DES BOUTONS ---
        if self.menu_state == "menu":
            save_hover = self.save_button.draw(self.screen)
            resume_hover = self.resume_button.draw(self.screen)
            options_hover = self.options_button.draw(self.screen)
            quit_hover = self.quit_button.draw(self.screen)
        elif self.menu_state == "options":
            video_hover = self.video_button.draw(self.screen)
            audio_hover = self.audio_button.draw(self.screen)
            keys_hover = self.keys_button.draw(self.screen)
            back_hover = self.back_button.draw(self.screen)

        # --- GESTION DES CLICS ---
        mouse_pressed = pygame.mouse.get_pressed()[0]  # clic gauche

        if self.menu_state == "menu":
            if resume_hover and mouse_pressed and not self.pressed:
                self.pressed = True
                self.game_context.current_mini_game = "game"
            elif save_hover and mouse_pressed and not self.pressed:
                self.game_context.save_game()

            elif options_hover and mouse_pressed and not self.pressed:
                self.pressed = True
                self.menu_state = "options"
            elif quit_hover and mouse_pressed and not self.pressed:
                self.pressed = True
                pygame.event.post(pygame.event.Event(pygame.QUIT))
                return
            elif not mouse_pressed:
                self.pressed = False  # relachement

        elif self.menu_state == "options":
            if video_hover and mouse_pressed and not self.pressed:
                self.pressed = True
                self.game_context.screen = pygame.display.set_mode(
                    (0, 0),
                    pygame.NOFRAME
                )
                pygame.display.toggle_fullscreen()
                print("Video Settings")
            elif audio_hover and mouse_pressed and not self.pressed:
                self.pressed = True
                print("Audio Settings")
            elif keys_hover and mouse_pressed and not self.pressed:
                self.pressed = True
                print("Change Key Bindings")
            elif back_hover and mouse_pressed and not self.pressed:
                self.pressed = True
                self.menu_state = "menu"
            elif not mouse_pressed:
                self.pressed = False  # relachement

        self.handle_events()

        # pygame.display.update()

