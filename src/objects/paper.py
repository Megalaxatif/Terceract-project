import pygame
from object import Game_object


class Paper(Game_object):
    def __init__(
        self,
        game_context,
        object_name,
        image_path: str,
        rect: pygame.Rect,
        collisions: list[pygame.Rect],
        default_collision: pygame.Rect,
        default_wall: str,
        collision_index: int
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
        self.fullscreen_paper_reference = self.game_context.get_reference("fullscreen_paper")

    def handle_click_selection(self, event):
        self.fullscreen_paper_reference.displayed = True