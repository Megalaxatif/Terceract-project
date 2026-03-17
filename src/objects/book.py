import pygame
from object import Game_object


class Book(Game_object):
    def __init__(self, game_context, object_name, image_path : str, rect : pygame.Rect, collisions : list[pygame.Rect], collision_index : int):
        super().__init__(game_context, object_name, image_path, rect, collisions, collision_index, False)

    def update(self, event):
        # TODO: check if we are in the right room
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            pass