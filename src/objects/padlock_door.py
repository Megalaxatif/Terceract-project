import pygame
from object import Game_object


class Padlock_door(Game_object):
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
            movable=False,
            displayed=True,
        )
        self.interactible = True
        self.padlock_reference = None

    def initialize(self):
        self.padlock_reference = self.game_context.get_reference("padlock")  # useful to change the visibility

    def handle_click_selection(self, event):
        self.padlock_reference.displayed = True