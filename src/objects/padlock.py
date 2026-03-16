import pygame
from object import Game_object
from pathlib import Path

class Padlock(Game_object):
    def __init__(self, game_context, object_name, image_path : str, rect : pygame.Rect, collisions : list[pygame.Rect], collision_index : int):
        super().__init__(game_context, object_name, image_path, rect, collisions, collision_index, False, False)
        self.code = "hope"
        self.text = ""


    def try_code(self):
        if self.text == self.code:
            self.game_context.unlock_room(self.game_context.current_room_id)
            print("code valid")


    def draw_text(self):
        font = pygame.font.Font(None, 35) # TODO: make the size of the font dynamic
        text_surface = font.render(
            self.text,
            True,           # anti-aliasing
            (0,0,0)
        )
        self.game_context.screen.blit(text_surface, (self.rect.x + self.rect.x / 8, self.rect.y + self.rect.h / 2))


    def update(self, event):
        if self.displayed:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                elif event.key == pygame.K_RETURN:
                    self.try_code()
                else:
                    self.text += event.unicode


    def draw(self): # draw every entities and the non entities
        if self.displayed:
            self.game_context.screen.blit(self.image, self.rect)
            self.draw_text()




