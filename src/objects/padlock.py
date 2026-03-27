import pygame
from object import Game_object


class Padlock(Game_object):
    def __init__(
        self,
        game_context,
        object_name,
        image_path: str,
        rect: pygame.Rect,
        collisions: list[pygame.Rect],
        default_collision: pygame.Rect,
        default_wall: str,
        collision_index: int,
        movable: bool = True,
        displayed: bool = True,
    ):
        super().__init__(
            game_context,
            object_name,
            image_path,
            rect,
            collisions,
            default_collision,
            default_wall,
            collision_index,
            movable,
            displayed,
        )
        self.code = "hope"
        self.text = ""
        self.last_delta = None
        self.font = pygame.font.Font(None, int(35 * self.game_context.delta))


    def try_code(self):
        if self.text == self.code:
            self.game_context.unlock_room(self.game_context.current_room_id)
            self.displayed = False
            # self.game_context.network_manager.send_package("variable", ) # TODO: network
            print("code valid")

    def update_font(self):
        if self.last_delta != self.game_context.delta:
            self.last_delta = self.game_context.delta
            self.font = pygame.font.Font(None, int(35 * self.game_context.delta))

    def draw_text(self):
        self.update_font()

        text_surface = self.font.render(
            self.text,
            True,
            (0, 0, 0),
        )

        self.game_context.screen.blit(
            text_surface,
            (self.rect.w / 3 + self.rect.w / 30, self.rect.h / 3 + self.rect.h / 6),
        )

    def handle_click_selection(self, event):
        self.displayed = False

    def update(self, event):
        if self.displayed:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.key == pygame.K_RETURN:
                    self.try_code()
                else:
                    self.text += event.unicode

    def draw(self):  # draw every entities and the non entities
        if self.displayed:
            self.game_context.screen.blit(self.image, self.rect)
            self.draw_text()
