import pygame
from object import Game_object
from pathlib import Path

class Key(Game_object):
    def __init__(self, game_context, object_name : str, image_path : str,
                 rect : pygame.Rect, collisions : list[pygame.Rect],
                 collision_index : int):
        super().__init__(game_context, object_name, image_path, rect, collisions, collision_index)
        
        self.key_given = False
        self.displayed = False
        self.grid_displayed = False