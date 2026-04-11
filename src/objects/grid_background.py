import pygame
from object import Game_object


class Grid_background(Game_object):
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
            displayed=False,
        )

    def initialize(self):
        self.magnet_reference = self.game_context.get_reference("magnet")  # useful to check if magnet was moved
        self.grid_reference = self.game_context.get_reference("grid")  # useful to check if grid was moved
        self.key_reference = self.game_context.get_reference("key")

    def handle_click_selection(self, event):
        self.displayed = False
        self.grid_reference.displayed = False
        if self.magnet_reference.in_grid:
            self.magnet_reference.displayed = False
            self.magnet_reference.display_collision_rect_bool = False
        if self.key_reference.found:
            self.key_reference.displayed = False