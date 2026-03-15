import pygame
from pytmx.util_pygame import load_pygame

from pathlib import Path
from object import Game_object

class Grid(pygame.sprite.Sprite):
    def __init__(self, game_context, image_path : str, rect : pygame.Rect, collisions : list[pygame.Rect], collision_index : int):
        super().__init__(game_context, "grid", image_path, rect, collisions, collision_index)

        
