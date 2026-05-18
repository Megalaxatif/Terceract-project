from pathlib import Path

import pygame

from . import menu_button


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

        root_dir = Path(__file__).resolve().parent.parent.parent.parent

        # load images raw
        self.background = pygame.image.load(root_dir / "assets/gui/background.png").convert_alpha()

        self.resume_img_raw = pygame.image.load(root_dir / "assets/gui/resume_button.png").convert_alpha()
        self.options_img_raw = pygame.image.load(root_dir / "assets/gui/options_button.png").convert_alpha()
        self.quit_img_raw = pygame.image.load(root_dir / "assets/gui/quit_button.png").convert_alpha()

        self.fullscreen_img_raw = pygame.image.load(root_dir / "assets/gui/fullscreen_button.png").convert_alpha()
        self.reset_img_raw = pygame.image.load(root_dir / "assets/gui/reset_button.png").convert_alpha()
        self.keys_img_raw = pygame.image.load(root_dir / "assets/gui/keybinds_button.png").convert_alpha()
        self.keys_info_img_raw = pygame.image.load(root_dir / "assets/gui/keybinds_info.png").convert_alpha()
        self.back_img_raw = pygame.image.load(root_dir / "assets/gui/back_button.png").convert_alpha()
        self.save_img_raw = pygame.image.load(root_dir / "assets/gui/save_button.png").convert_alpha()
        self.multi_img_raw = pygame.image.load(root_dir / "assets/gui/multi_button.png").convert_alpha()
        self.join_img_raw = pygame.image.load(root_dir / "assets/gui/join_button.png").convert_alpha()
        self.host_img_raw = pygame.image.load(root_dir / "assets/gui/host_button.png").convert_alpha()
        self.ip_field_img_raw = pygame.image.load(root_dir / "assets/gui/ip_field.png").convert_alpha()
        self.port_field_img_raw = pygame.image.load(root_dir / "assets/gui/port_field.png").convert_alpha()
        self.host_info_img_raw = pygame.image.load(root_dir / "assets/gui/host_info.png").convert_alpha()
        self.connect_img_raw = pygame.image.load(root_dir / "assets/gui/connect_button.png").convert_alpha()
        self.create_buttons()

    def create_buttons(self):
        center_x = self.SCREEN_WIDTH // 2
        delta = min(self.game_context.delta_w, self.game_context.delta_h)

        self.connect_img = pygame.transform.scale(
            self.connect_img_raw,
            (
                int(self.connect_img_raw.get_width() * delta),
                int(self.connect_img_raw.get_height() * delta),
            ),
        )

        self.host_info_img = pygame.transform.scale(
            self.host_info_img_raw,
            (
                int(self.host_info_img_raw.get_width() * delta),
                int(self.host_info_img_raw.get_height() * delta),
            ),
        )

        self.port_field_img = pygame.transform.scale(
            self.port_field_img_raw,
            (
                int(self.port_field_img_raw.get_width() * delta),
                int(self.port_field_img_raw.get_height() * delta),
            ),
        )

        self.ip_field_img = pygame.transform.scale(
            self.ip_field_img_raw,
            (
                int(self.ip_field_img_raw.get_width() * delta),
                int(self.ip_field_img_raw.get_height() * delta),
            ),
        )

        self.host_img = pygame.transform.scale(
            self.host_img_raw,
            (
                int(self.host_img_raw.get_width() * delta),
                int(self.host_img_raw.get_height() * delta),
            ),
        )

        self.join_img = pygame.transform.scale(
            self.join_img_raw,
            (
                int(self.join_img_raw.get_width() * delta),
                int(self.join_img_raw.get_height() * delta),
            ),
        )

        self.multi_img = pygame.transform.scale(
            self.multi_img_raw,
            (
                int(self.multi_img_raw.get_width() * delta),
                int(self.multi_img_raw.get_height() * delta),
            ),
        )

        self.save_img = pygame.transform.scale(
            self.save_img_raw,
            (
                int(self.save_img_raw.get_width() * delta),
                int(self.save_img_raw.get_height() * delta),
            ),
        )

        self.resume_img = pygame.transform.scale(
            self.resume_img_raw,
            (
                int(self.resume_img_raw.get_width() * delta),
                int(self.resume_img_raw.get_height() * delta),
            ),
        )

        self.options_img = pygame.transform.scale(
            self.options_img_raw,
            (
                int(self.options_img_raw.get_width() * delta),
                int(self.options_img_raw.get_height() * delta),
            ),
        )

        self.quit_img = pygame.transform.scale(
            self.quit_img_raw,
            (
                int(self.quit_img_raw.get_width() * delta),
                int(self.quit_img_raw.get_height() * delta),
            ),
        )

        self.fullscreen_img = pygame.transform.scale(
            self.fullscreen_img_raw,
            (
                int(self.fullscreen_img_raw.get_width() * delta),
                int(self.fullscreen_img_raw.get_height() * delta),
            ),
        )

        self.reset_img = pygame.transform.scale(
            self.reset_img_raw,
            (
                int(self.reset_img_raw.get_width() * delta),
                int(self.reset_img_raw.get_height() * delta),
            ),
        )

        self.keys_img = pygame.transform.scale(
            self.keys_img_raw,
            (
                int(self.keys_img_raw.get_width() * delta),
                int(self.keys_img_raw.get_height() * delta),
            ),
        )
        self.keys_info_img = pygame.transform.scale(
            self.keys_info_img_raw,
            (
                int(self.keys_info_img_raw.get_width() * delta),
                int(self.keys_info_img_raw.get_height() * delta),
            ),
        )

        self.back_img = pygame.transform.scale(
            self.back_img_raw,
            (
                int(self.back_img_raw.get_width() * delta),
                int(self.back_img_raw.get_height() * delta),
            ),
        )

        # main menu
        self.resume_button = menu_button.MenuButton(
            center_x - self.resume_img.get_width() // 2,
            int(self.SCREEN_HEIGHT * 0.05),
            self.resume_img,
            0.75,
        )

        self.save_button = menu_button.MenuButton(
            center_x - self.save_img.get_width() // 2,
            int(self.SCREEN_HEIGHT * 0.20),
            self.save_img,
            0.75,
        )

        self.multi_button = menu_button.MenuButton(
            center_x - self.multi_img.get_width() // 2,
            int(self.SCREEN_HEIGHT * 0.35),
            self.multi_img,
            0.75,
        )

        self.options_button = menu_button.MenuButton(
            center_x - self.options_img.get_width() // 2,
            int(self.SCREEN_HEIGHT * 0.50),
            self.options_img,
            0.75,
        )
        self.quit_button = menu_button.MenuButton(
            center_x - self.quit_img.get_width() // 2,
            int(self.SCREEN_HEIGHT * 0.65),
            self.quit_img,
            0.75,
        )

        # menu options
        self.fullscreen_button = menu_button.MenuButton(
            center_x - self.fullscreen_img.get_width() // 2,
            int(self.SCREEN_HEIGHT * 0.05),
            self.fullscreen_img,
            0.75,
        )
        self.reset_button = menu_button.MenuButton(
            center_x - self.reset_img.get_width() // 2,
            int(self.SCREEN_HEIGHT * 0.20),
            self.reset_img,
            0.75,
        )
        self.keys_button = menu_button.MenuButton(
            center_x - self.keys_img.get_width() // 2,
            int(self.SCREEN_HEIGHT * 0.35),
            self.keys_img,
            0.75,
        )
        self.back_button = menu_button.MenuButton(
            center_x - self.back_img.get_width() // 2,
            int(self.SCREEN_HEIGHT * 0.50),
            self.back_img,
            0.75,
        )
        # keybinds info
        self.keys_info_button = menu_button.MenuButton(
            center_x - self.keys_info_img.get_width() // 2.5,
            int(self.SCREEN_HEIGHT * 0.05),
            self.keys_info_img,
            0.75,
        )
        self.keys_back_button = menu_button.MenuButton(
            center_x - self.back_img.get_width() // 2,
            int(self.SCREEN_HEIGHT * 0.75),
            self.back_img,
            0.75,
        )
        # multi interface
        self.join_button = menu_button.MenuButton(
            center_x - self.join_img.get_width() // 2,
            int(self.SCREEN_HEIGHT * 0.05),
            self.join_img,
            0.75,
        )
        self.host_button = menu_button.MenuButton(
            center_x - self.host_img.get_width() // 2,
            int(self.SCREEN_HEIGHT * 0.20),
            self.host_img,
            0.75,
        )
        self.multi_back_button = menu_button.MenuButton(
            center_x - self.back_img.get_width() // 2,
            int(self.SCREEN_HEIGHT * 0.35),
            self.back_img,
            0.75,
        )
        # host interface
        self.host_info_button = menu_button.MenuButton(
            0,
            0,
            self.host_info_img,
            0.75,
        )
        self.host_back_button = menu_button.MenuButton(
            center_x - self.back_img.get_width() // 2,
            int(self.SCREEN_HEIGHT * 0.20),
            self.back_img,
            0.75,
        )
        # join interface
        self.ip_field = menu_button.MenuButton(
            center_x - self.ip_field_img.get_width() // 2,
            int(self.SCREEN_HEIGHT * 0.05),
            self.ip_field_img,
            0.75,
        )
        self.port_field = menu_button.MenuButton(
            center_x - self.port_field_img.get_width() // 2,
            int(self.SCREEN_HEIGHT * 0.20),
            self.port_field_img,
            0.75,
        )
        self.connect_button = menu_button.MenuButton(
            center_x - self.connect_img.get_width() // 2,
            int(self.SCREEN_HEIGHT * 0.35),
            self.connect_img,
            0.75,
        )
        self.join_back_button = menu_button.MenuButton(
            center_x - self.back_img.get_width() // 2,
            int(self.SCREEN_HEIGHT * 0.50),
            self.back_img,
            0.75,
        )

    def draw_text_centered(self, text, y):
        img = self.font.render(text, True, self.TEXT_COL)
        rect = img.get_rect(center=(self.SCREEN_WIDTH // 2, y))
        self.screen.blit(img, rect)

    def handle_events(self):
        for event in pygame.event.get():  # TODO: change this to respect the event queue
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.game_paused = not self.game_paused

        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = self.screen.get_size()
        self.create_buttons()

    def update(self):
        self.screen.blit(self.background, (0, 0, self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.SCREEN_WIDTH = 1080 * self.game_context.delta_w
        self.SCREEN_HEIGHT = 720 * self.game_context.delta_h

        if not hasattr(self, "pressed"):
            self.pressed = False  # initialize once

        # --- BUTTON DISPLAY ---
        if self.menu_state == "menu":
            resume_hover = self.resume_button.draw(self.screen)
            save_hover = self.save_button.draw(self.screen)
            multi_hover = self.multi_button.draw(self.screen)
            options_hover = self.options_button.draw(self.screen)
            quit_hover = self.quit_button.draw(self.screen)
        elif self.menu_state == "options":
            fullscreen_hover = self.fullscreen_button.draw(self.screen)
            reset_hover = self.reset_button.draw(self.screen)
            keys_hover = self.keys_button.draw(self.screen)
            back_hover = self.back_button.draw(self.screen)
        elif self.menu_state == "keybinds":
            keys_info_hover = self.keys_info_button.draw(self.screen)
            keys_back_hover = self.keys_back_button.draw(self.screen)
        elif self.menu_state == "multiplayer":
            join_hover = self.join_button.draw(self.screen)
            host_hover = self.host_button.draw(self.screen)
            multi_back_hover = self.multi_back_button.draw(self.screen)
        elif self.menu_state == "join":
            ip_hover = self.ip_field.draw(self.screen)
            port_hover = self.port_field.draw(self.screen)
            connect_hover = self.connect_button.draw(self.screen)
            join_back_hover = self.join_back_button.draw(self.screen)
        elif self.menu_state == "host":
            host_info_hover = self.host_info_button.draw(self.screen)
            host_back_hover = self.host_back_button.draw(self.screen)

        # --- CLICS HANDLING ---
        mouse_pressed = pygame.mouse.get_pressed()[0]  # left click

        if self.menu_state == "menu":
            if resume_hover and mouse_pressed and not self.pressed:
                self.pressed = True
                self.game_context.current_mini_game = "game"
            elif save_hover and mouse_pressed and not self.pressed:
                self.pressed = True
                self.game_context.save_game()
            elif multi_hover and mouse_pressed and not self.pressed:
                self.pressed = True
                self.menu_state = "multiplayer"
            elif options_hover and mouse_pressed and not self.pressed:
                self.pressed = True
                self.menu_state = "options"
            elif quit_hover and mouse_pressed and not self.pressed:
                self.pressed = True
                pygame.event.post(pygame.event.Event(pygame.QUIT))
                return
            elif not mouse_pressed:
                self.pressed = False  # release

        elif self.menu_state == "options":
            if fullscreen_hover and mouse_pressed and not self.pressed:
                self.pressed = True
                self.game_context.screen = pygame.display.set_mode((0, 0), pygame.NOFRAME)
                self.game_context.recalculate_deltas()
                pygame.display.toggle_fullscreen()
            elif reset_hover and mouse_pressed and not self.pressed:
                self.pressed = True
                self.game_context.reset_game()
            elif keys_hover and mouse_pressed and not self.pressed:
                self.pressed = True
                self.menu_state = "keybinds"
            elif back_hover and mouse_pressed and not self.pressed:
                self.pressed = True
                self.menu_state = "menu"
            elif not mouse_pressed:
                self.pressed = False  # release

        elif self.menu_state == "keybinds":
            if keys_back_hover and mouse_pressed and not self.pressed:
                self.pressed = True
                self.menu_state = "options"
            elif not mouse_pressed:
                self.pressed = False  # release
        elif self.menu_state == "multiplayer":
            if multi_back_hover and mouse_pressed and not self.pressed:
                self.pressed = True
                self.menu_state = "menu"
            elif join_hover and mouse_pressed and not self.pressed:
                self.pressed = True
                self.menu_state = "join"
            elif host_hover and mouse_pressed and not self.pressed:
                self.pressed = True
                self.menu_state = "host"
            elif not mouse_pressed:
                self.pressed = False # release
        elif self.menu_state == "join":
            if ip_hover and mouse_pressed and not self.pressed:
                pass
            elif port_hover and mouse_pressed and not self.pressed:
                pass
            elif connect_hover and mouse_pressed and not self.pressed:
                pass
            elif join_back_hover and mouse_pressed and not self.pressed:
                self.menu_state = "multiplayer"
            elif not mouse_pressed:
                self.pressed = False
        elif self.menu_state == "host":
            if host_back_hover and mouse_pressed and not self.pressed:
                self.menu_state = "multiplayer"
            elif not mouse_pressed:
                self.pressed = False
        self.handle_events()

        # pygame.display.update()
