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
        default_collision: pygame.Rect | None,
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


    def initialize(self):

        grid_wall = self.game_context.room_list[0][3]
        self.in_grid = self in grid_wall.objects
        if self.in_grid:
            self.use_grid_collisions()

        self.grid_reference = self.game_context.get_reference("grid")
        self.key_reference = self.game_context.get_reference("key")
        self.drawer_background_reference = self.game_context.get_reference("gray_bg_drawer")


    def use_grid_collisions(self):
        #json_path = self.game_context.room_list[0][3].json_collisions_path
        # if we are on the right wall of room 1 where the grid minigame is located
        self.grid_collisions = self.collision_rects[:-2] # we start at 1 because the first element in the json is the default rect
        self.raw_grid_collisions = self.grid_collisions.copy()
        grid_start_rect = self.collision_rects[-1]
        end_rect = self.collision_rects[-2]

        self.collision_rects = [grid_start_rect, end_rect]
        self.raw_collision_rects = self.collision_rects.copy()
        self.valid_rect = self.collision_rects[self.collision_rect_id]


    def change_collision_rects(self, json_collisions_path, wall_id_str):
        super().change_collision_rects(json_collisions_path, wall_id_str)
        # if we are on the right wall of room 1 where the grid minigame is located
        if self.game_context.current_room_id == 0 and self.game_context.current_wall_id == 3:
            self.use_grid_collisions()


    def resize_collision_rects(self):
        if self.game_context.current_room_id == 0 and self.game_context.current_wall_id == 3:
            resize_rects(self.collision_rects, self.raw_collision_rects, self.game_context.current_wall.delta)
            resize_rects(self.grid_collisions, self.raw_grid_collisions, self.game_context.current_wall.delta)
        else:
            super().resize_collision_rects()


    def display_collision_rect(self):
        if self.game_context.current_room_id == 0 and self.game_context.current_wall_id == 3 and self.grid_reference.displayed:
            display_debug_rects([self.collision_rects[0]], self.game_context.screen)
            display_debug_rects([self.collision_rects[1]], self.game_context.screen)
            display_debug_rects(self.grid_collisions, self.game_context.screen)
        else:
            super().display_collision_rect()


    def handle_click(self, event):
        #if self != self.game_context.inventory.current_object:
        dropped = self.game_context.drop_current_object(event)
        if dropped and self.game_context.current_room_id == 0 and self.game_context.current_wall_id == 3:
            self.in_grid = True
            if self.game_context.network_manager.is_connected:
                self.game_context.network_manager.send_package("variable", "magnet", "in_grid", True)
            if self.collision_rect_id == 1: # if we are on the finish square
                self.key_reference.displayed = True
                self.displayed = False
                # network
                if self.game_context.network_manager.is_connected:
                    self.game_context.network_manager.send_package("variable", "key", "displayed", True)
                    self.game_context.network_manager.send_package("variable", "magnet", "displayed", False)
        return True # avoid error


    def handle_click_selection(self, event):
        if self.game_context.current_room_id == 0 and self.game_context.current_wall_id == 3:
            self.displayed = self.grid_reference.displayed
            self.display_collision_rect_bool = self.grid_reference.displayed


    def handle_dragging(self, event):
        point_rect = pygame.Rect(self.rect.center[0], self.rect.center[1], 1, 1)
        col_id = point_rect.collidelist(self.grid_collisions)
        if col_id != -1:
            self.game_context.drop_current_object(event, self.collision_rects)


    def update(self, event):
        # prevent the magnet to be invisible for one player when the grid is opened in both players pov and the magnet is put inside
        key_found = self.key_reference.displayed or self.key_reference.collision_rect_id == 1 # if the key is displayed or it is in the closet
        if self.in_grid and self.grid_reference.displayed and not key_found:
            self.displayed = True

        if self.game_context.current_object == self and event.type == pygame.MOUSEMOTION:
            if self.game_context.current_room_id == 0 and self.game_context.current_wall_id == 3:
                if self.grid_reference.displayed:
                    self.handle_dragging(event)
