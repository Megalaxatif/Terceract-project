import pygame

from object import Game_object
from objects.book import Book


class Library(Game_object):
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

    def handle_click_selection(self, event):
        wall = self.game_context.current_wall.objects
        for obj in wall:
            if isinstance(obj, Book) and obj.bait:
                obj.displayed = not obj.displayed
        # Library is local to the player and it is not selected anyways

    def update(self, event):
        # TODO: check if we are in the right room
        pass