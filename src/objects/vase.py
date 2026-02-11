import pygame
from pathlib import Path
from object import Object

class Vase(Object):
    def __init__(self, game_context, image_path : str, rect : pygame.Rect, collisions : list[pygame.Rect], collision_index : int):
        super().__init__(game_context, "vase", image_path, rect, collisions, collision_index)
