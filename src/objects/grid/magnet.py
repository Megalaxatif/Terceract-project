from __future__ import annotations

import pygame

from object import Game_object
from utils import *

class Magnet(Game_object):
    def __init__(
        self,
        game_context,
        object_name: str,
        image_path: str,
        rect: pygame.Rect,
        collisions: list[pygame.Rect],
        default_collision: pygame.Rect,
        default_wall: str,
        collision_index: int = -1,
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

        self.start_rect = self.collision_rects[-1]
        self.end_rect = self.collision_rects[-2]

        self.grid_collisions = self.collision_rects[:-2]
        self.raw_grid_collisions = self.grid_collisions.copy()

        self.collision_rects = [self.start_rect, self.end_rect]
        self.raw_collision_rects = self.collision_rects.copy()

        self.key_given = False


    def resize_collision_rects(self):
        resize_rects(self.collision_rects, self.raw_collision_rects, self.game_context.current_wall.delta)
        resize_rects(self.grid_collisions, self.raw_grid_collisions, self.game_context.current_wall.delta)


    def initialize(self):
        self.grid_reference = self.game_context.get_reference("grid")  # useful to check if grid was moved
        if self.grid_reference is None:
            print(f'initialize of object named "{self.name}" error: no object with name "grid" found in the game, exiting')
            self.game_context.quit()

        self.key_reference = self.game_context.get_reference("key")  # useful to check if key was moved
        if self.key_reference is None:
            print(f'initialize of object named "{self.name}" error: no object with name "key" found in the game, exiting')
            self.game_context.quit()


    def handle_click(self, event):
        if self != self.game_context.inventory.current_object:
            self.game_context.drop_current_object(event)
            if self.collision_rect_id == self.end_rect_id:
                self.key_reference.displayed = True


    def handle_dragging(self, event):
        point_rect = pygame.Rect(self.rect.center[0], self.rect.center[1], 1, 1)
        if point_rect.collidelist(list(self.collision_rects[:-2])):
            print("collision")
            self.game_context.drop_current_object(event)


    def update(self, event):
        if self.game_context.current_object == self and event.type == pygame.MOUSEMOTION:
            if self.grid_reference.displayed:
                self.handle_dragging(event)