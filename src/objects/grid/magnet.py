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

        self.grid_collisions = self.collision_rects[1:-2] # we start at 1 because the first element in the json is the default rect
        self.raw_grid_collisions = self.grid_collisions.copy()

        start_rect = self.collision_rects[-1]
        end_rect = self.collision_rects[-2]

        self.collision_rects = [start_rect, end_rect]
        self.raw_collision_rects = self.collision_rects.copy()

        self.key_given = False
        self.in_grid = False
        self.in_drawer = True


    def resize_collision_rects(self):
        resize_rects(self.collision_rects, self.raw_collision_rects, self.game_context.current_wall.delta)
        resize_rects(self.grid_collisions, self.raw_grid_collisions, self.game_context.current_wall.delta)


    def display_collision_rect(self):
        if self.display_collision_rect_bool:
            display_debug_rects([self.collision_rects[0]], self.game_context.screen)
            display_debug_rects(self.grid_collisions, self.game_context.screen)


    def initialize(self):
        self.grid_reference = self.game_context.get_reference("grid")  # useful to check if grid was moved
        self.key_reference = self.game_context.get_reference("key")  # useful to check if key was moved
        self.drawer_reference = self.game_context.get_reference("drawer")  # useful to check if drawer was moved


    #def handle_click(self, event):
        # if self != self.game_context.inventory.current_object:
        #     self.game_context.drop_current_object(event)
        #     if self.collision_rect_id == 0 and self.grid_reference.displayed:
        #         self.in_grid = True
        #         print("in grid: ",self.in_grid)
        #     elif self.collision_rect_id == 0 and self.drawer_reference.displayed:
        #         print("in drawer: ",self.in_drawer)


    def handle_dragging(self, event):
        point_rect = pygame.Rect(self.rect.center[0], self.rect.center[1], 1, 1)
        col_id = point_rect.collidelist(self.grid_collisions)
        if col_id != -1:
            self.game_context.drop_current_object(event)


    def update(self, event):
        self.display_collision_rect_bool = True
        if self.game_context.current_object == self and event.type == pygame.MOUSEMOTION:
            if self.grid_reference.displayed:
                self.handle_dragging(event)
