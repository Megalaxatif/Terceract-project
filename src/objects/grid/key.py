import pygame
from object import Game_object
from pathlib import Path

class Key(Game_object):
    def __init__(self, game_context, image_path : str, rect : pygame.Rect, collisions : list[pygame.Rect], collision_index : int):
        super().__init__(game_context, "key", image_path, rect, collisions, collision_index)