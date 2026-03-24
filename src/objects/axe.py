import pygame
from object import Game_object

class Axe(Game_object):
    def __init__(self, game_context, object_name, image_path : str, rect : pygame.Rect, collisions : list[pygame.Rect], collision_index : int, default_collision, default_wall):
        super().__init__(game_context, object_name, image_path, rect, collisions, collision_index, True, True, default_collision, default_wall)

    #def handle_left_click(self, event):
     #   pass
