from pathlib import Path

import pygame
from pygame.locals import K_SPACE

from . import menu_button


class Menu:
    def __init__(self, game_context):
        self.game_context = game_context
        self.screen = self.game_context.screen
        self.SCREEN_HEIGHT = self.screen.get_height()
        self.SCREEN_WIDTH = self.screen.get_width()

        self.font_size = 70
        #self.font = pygame.font.SysFont("arialblack", self.font_size)

        self.menu_state = "menu"
        self.button_dict = {} # dictionary containing all the buttons ordered by menu

        root_dir = Path(__file__).resolve().parent.parent.parent.parent

        self.ip_field_str = ""
        self.port_field_str = "50004"
        self.duo_error_code = -1
        self.ip_field_selected = False
        self.port_field_selected = False

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


    def resize_all(self, delta):
        self.resize_font(delta)
        for menu in self.button_dict:
            for button in self.button_dict[menu]:
                button.resize(delta)


    def create_buttons(self):
        center_x = self.SCREEN_WIDTH // 2

        # main menu
        self.resume_button = menu_button.MenuButton(
            center_x - 0.8 * self.resume_img_raw.get_width() // 2,
            int(self.SCREEN_HEIGHT * 0.05),
            self.resume_img_raw,
            0.8,
        )

        self.save_button = menu_button.MenuButton(
            center_x - 0.8 * self.save_img_raw.get_width() // 2,
            int(self.SCREEN_HEIGHT * 0.22),
            self.save_img_raw,
            0.8,
        )

        self.multi_button = menu_button.MenuButton(
            center_x - 0.8 * self.multi_img_raw.get_width() // 2,
            int(self.SCREEN_HEIGHT * 0.39),
            self.multi_img_raw,
            0.8,
        )

        self.options_button = menu_button.MenuButton(
            center_x - 0.8 * self.options_img_raw.get_width() // 2,
            int(self.SCREEN_HEIGHT * 0.56),
            self.options_img_raw,
            0.8,
        )

        self.quit_button = menu_button.MenuButton(
            center_x - 0.8 * self.quit_img_raw.get_width() // 2,
            int(self.SCREEN_HEIGHT * 0.73),
            self.quit_img_raw,
            0.8,
        )
        self.button_dict["menu"] = [self.resume_button, self.save_button, self.multi_button, self.options_button, self.quit_button]

        # menu options
        self.fullscreen_button = menu_button.MenuButton(
            center_x - 0.8 * self.fullscreen_img_raw.get_width() // 2,
            int(self.SCREEN_HEIGHT * 0.05),
            self.fullscreen_img_raw,
            0.8,
        )
        self.reset_button = menu_button.MenuButton(
            center_x - 0.8 * self.reset_img_raw.get_width() // 2,
            int(self.SCREEN_HEIGHT * 0.22),
            self.reset_img_raw,
            0.8,
        )
        self.keys_button = menu_button.MenuButton(
            center_x - 0.8 * self.keys_img_raw.get_width() // 2,
            int(self.SCREEN_HEIGHT * 0.39),
            self.keys_img_raw,
            0.8,
        )
        self.back_button = menu_button.MenuButton(
            center_x - 0.8 * self.back_img_raw.get_width() // 2,
            int(self.SCREEN_HEIGHT * 0.56),
            self.back_img_raw,
            0.8,
        )
        self.button_dict["options"] = [self.fullscreen_button, self.reset_button, self.keys_button, self.back_button]

        # keybinds info
        self.keys_info_button = menu_button.MenuButton(
            center_x - 0.8 * self.keys_info_img_raw.get_width() // 2,
            int(self.SCREEN_HEIGHT * 0.05),
            self.keys_info_img_raw,
            0.8,
        )
        self.keys_back_button = menu_button.MenuButton(
            center_x - 0.8 * self.back_img_raw.get_width() // 2,
            int(self.SCREEN_HEIGHT * 0.22),
            self.back_img_raw,
            0.8,
        )
        self.button_dict["keybinds"] = [self.keys_info_button, self.keys_back_button]

        # multi interface
        self.join_button = menu_button.MenuButton(
            center_x - 0.8 * self.join_img_raw.get_width() // 2,
            int(self.SCREEN_HEIGHT * 0.05),
            self.join_img_raw,
            0.8,
        )
        self.host_button = menu_button.MenuButton(
            center_x - 0.8 * self.host_img_raw.get_width() // 2,
            int(self.SCREEN_HEIGHT * 0.22),
            self.host_img_raw,
            0.8,
        )
        self.multi_back_button = menu_button.MenuButton(
            center_x - 0.8 * self.back_img_raw.get_width() // 2,
            int(self.SCREEN_HEIGHT * 0.39),
            self.back_img_raw,
            0.8,
        )
        self.button_dict["multiplayer"] = [self.join_button, self.host_button, self.multi_back_button]

        # host interface
        self.host_info_button = menu_button.MenuButton(
            center_x - 0.8 * self.host_info_img_raw.get_width() // 2,
            int(self.SCREEN_HEIGHT * 0.05),
            self.host_info_img_raw,
            0.8,
        )
        self.host_back_button = menu_button.MenuButton(
            center_x - 0.8 * self.back_img_raw.get_width() // 2,
            int(self.SCREEN_HEIGHT * 0.22),
            self.back_img_raw,
            0.8,
        )
        self.button_dict["host"] = [self.host_info_button, self.host_back_button]

        # join interface
        self.ip_field = menu_button.MenuButton(
            center_x - 0.8 * self.ip_field_img_raw.get_width() // 2,
            int(self.SCREEN_HEIGHT * 0.05),
            self.ip_field_img_raw,
            0.8,
        )
        self.port_field = menu_button.MenuButton(
            center_x - 0.8 * self.port_field_img_raw.get_width() // 2,
            int(self.SCREEN_HEIGHT * 0.22),
            self.port_field_img_raw,
            0.8,
        )
        self.connect_button = menu_button.MenuButton(
            center_x - 0.8 * self.connect_img_raw.get_width() // 2,
            int(self.SCREEN_HEIGHT * 0.39),
            self.connect_img_raw,
            0.8,
        )
        self.join_back_button = menu_button.MenuButton(
            center_x - 0.8 * self.back_img_raw.get_width() // 2,
            int(self.SCREEN_HEIGHT * 0.56),
            self.back_img_raw,
            0.8,
        )
        self.button_dict["join"] = [self.ip_field, self.port_field, self.connect_button, self.join_back_button]

    # the two following methods are for rendering text properly in the fields
    def resize_font(self, delta):
        self.font = pygame.font.Font(None, int(self.font_size * delta))

    def draw_text(self, text, x, y, color = (0,0,0)):
        text_surface = self.font.render(
            text,
            True,
            color,
        )
        self.game_context.screen.blit(text_surface,(x,y))


    def handle_events(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = event.pos
                for button in self.button_dict[self.menu_state]:
                    if button.rect.collidepoint(pos):
                        self.execute_button_command(button)

            elif event.type == pygame.KEYDOWN:
                if self.ip_field_selected or self.port_field_selected:
                    if event.key == pygame.K_BACKSPACE:
                        if self.ip_field_selected:
                            self.ip_field_str = self.ip_field_str[:-1]
                        elif self.port_field_selected:
                            self.port_field_str = self.port_field_str[:-1]
                    elif self.ip_field_selected and ("a" <= event.unicode <= "z" or "0" <= event.unicode <= "9" or event.unicode == "."):
                        self.ip_field_str += event.unicode
                    elif self.port_field_selected and "0" <= event.unicode <= "9":
                        self.port_field_str+= event.unicode

    def update(self, events):
        self.handle_events(events)
        self.draw_menu()

    def draw_menu(self):
        screen_size = self.screen.get_size()
        self.screen.blit(self.background, (0, 0, screen_size[0], screen_size[1]))
        delta = min(self.game_context.delta_w, self.game_context.delta_h)
        self.resize_all(delta) # TODO: maybe optimize a little to resize only when chanching the size of the window
        self.draw_buttons()

    def draw_buttons(self):
        if self.menu_state == "menu":
            self.resume_button.draw(self.screen)
            self.save_button.draw(self.screen)
            self.multi_button.draw(self.screen)
            self.options_button.draw(self.screen)
            self.quit_button.draw(self.screen)
        elif self.menu_state == "options":
            self.fullscreen_button.draw(self.screen)
            self.reset_button.draw(self.screen)
            self.keys_button.draw(self.screen)
            self.back_button.draw(self.screen)
        elif self.menu_state == "keybinds":
            self.keys_info_button.draw(self.screen)
            self.keys_back_button.draw(self.screen)
        elif self.menu_state == "multiplayer":
            self.join_button.draw(self.screen)
            self.host_button.draw(self.screen)
            self.multi_back_button.draw(self.screen)
        elif self.menu_state == "join":
            self.ip_field.draw(self.screen)
            self.port_field.draw(self.screen)
            self.connect_button.draw(self.screen)
            self.join_back_button.draw(self.screen)
            self.draw_text(self.ip_field_str, self.ip_field.rect.x*2, self.ip_field.rect.y*1.8)
            self.draw_text(self.port_field_str, self.port_field.rect.x*2.5, self.port_field.rect.y*1.2)

            x = self.join_back_button.rect.x * 1.3
            y = self.join_back_button.rect.y * 1.4
            if self.duo_error_code > 0:
                self.draw_text("Invalid IP or port", x ,y, (255,0,0))
            elif self.duo_error_code == 0:
                self.draw_text("connected", x, y,(0,255,0))
        elif self.menu_state == "host":
            self.host_info_button.draw(self.screen)
            self.host_back_button.draw(self.screen)


    def execute_button_command(self, button):
        if self.menu_state == "menu":
            if button == self.resume_button:
                self.game_context.current_mini_game = "game"
            elif button == self.save_button:
                self.game_context.save_game()
            elif button == self.multi_button:
                self.menu_state = "multiplayer"
            elif button == self.options_button:
                self.menu_state = "options"
            elif button == self.quit_button:
                pygame.event.post(pygame.event.Event(pygame.QUIT))
                return

        elif self.menu_state == "options":
            if button == self.fullscreen_button:
                self.game_context.screen = pygame.display.set_mode((0, 0), pygame.NOFRAME)
                self.game_context.recalculate_deltas()
                pygame.display.toggle_fullscreen()
            elif button == self.reset_button:
                if not self.game_context.network_manager.is_connected:
                    self.game_context.reset_game()
            elif button == self.keys_button:
                self.menu_state = "keybinds"
            elif button == self.back_button:
                self.menu_state = "menu"

        elif self.menu_state == "keybinds":
            if button == self.keys_back_button:
                self.menu_state = "options"

        elif self.menu_state == "multiplayer":
            if button == self.multi_back_button:
                self.menu_state = "menu"
            elif button == self.join_button:
                self.menu_state = "join"
            elif button == self.host_button:
                self.menu_state = "host"

        elif self.menu_state == "join":
            if button == self.ip_field:
                self.port_field_selected = False
                self.ip_field_selected = True
            elif button == self.port_field:
                self.ip_field_selected = False
                self.port_field_selected = True
            elif button == self.connect_button:
                if self.ip_field_str and self.port_field_str:
                    self.duo_error_code = self.game_context.launch_duo(self.ip_field_str, int(self.port_field_str))
                else:
                    self.duo_error_code = 1
            elif button == self.join_back_button:
                self.menu_state = "multiplayer"
                self.ip_field_selected = False
                self.port_field_selected = False
                self.duo_error_code = -1

        elif self.menu_state == "host":
            if button == self.host_back_button:
                self.pressed = True
                self.menu_state = "multiplayer"