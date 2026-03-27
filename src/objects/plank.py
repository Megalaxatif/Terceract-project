from pathlib import Path

import pygame
from object import Game_object


class Plank(Game_object):
    def __init__(
        self,
        game_context,
        object_name,
        image_path: str,
        rect: pygame.Rect,
        collisions: list[pygame.Rect],
        collision_index: int,
    ):
        super().__init__(
            game_context, object_name, image_path, rect, collisions, collision_index
        )

        self.movable = False
        self.interactible = "removable" in self.name
