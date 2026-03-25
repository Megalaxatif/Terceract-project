from pathlib import Path

import pygame
from object import Game_object
from objects.plank import Plank


class Screwdriver(Game_object):
    def __init__(
        self,
        game_context,
        object_name,
        image_path: str,
        rect: pygame.Rect,
        collisions: list[pygame.Rect],
        collision_index: int,
        default_collision,
        default_wall,
    ):
        super().__init__(
            game_context,
            object_name,
            image_path,
            rect,
            collisions,
            collision_index,
            default_collision=default_collision,
            default_wall=default_wall,
        )

        self.displayed = False
        self.interactible = True
        self.initial_pos = self.rect.x, self.rect.y

    def handle_click_selection(self, event):
        pass
    
    def handle_click(self, event):

        wall = self.game_context.current_wall
        if wall.wall_id_str == "13":
            for obj in reversed(
                wall.objects.sprites()
            ):  # reversed so we click the top object first
                if obj.displayed and obj.rect.collidepoint(event.pos):
                    if isinstance(obj, Plank):
                        obj.displayed = not obj.displayed

        self.game_context.drop_current_object(event)
