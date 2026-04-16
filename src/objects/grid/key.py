import pygame
from object import Game_object
from utils import *


class Key(Game_object):
    def __init__(
        self,
        game_context,
        object_name: str,
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
            movable=True,
            displayed=False,
        )

    def display_collision_rect(self):
        if self.game_context.current_room_id == 0 and self.game_context.current_wall_id == 3:
            if self.grid_reference.displayed and self.display_collision_rect_bool:
                display_debug_rects([self.collision_rects[0]], self.game_context.screen)
            else:
                display_debug_rects([self.collision_rects[1]], self.game_context.screen)
        else:
            super().display_collision_rect()


    def initialize(self):
        self.closed_closet_reference = self.game_context.get_reference("closed_closet")# useful to change the visibility
        self.grid_reference = self.game_context.get_reference("grid")

    def handle_click(self, event):
        #if self != self.game_context.inventory.current_object:
        # TODO: there is a non blocking error happening if we take the key out from the inventory.
        # this is because inventory drop is called after this function. solution: make a function drop() for the object that calls either inventory_drop or handle_click
        self.game_context.drop_current_object(event)
        if self.game_context.current_room_id == 0 and self.game_context.current_wall_id == 3:
            if self.collision_rect_id == 1:
                self.displayed = False
                self.closed_closet_reference.lock = False
                return True

        return False