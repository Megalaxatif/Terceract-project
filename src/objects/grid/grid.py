# from pytmx.util_pygame import load_pygame
import pygame
from object import Game_object


class Grid(Game_object):
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
        displayed,
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
            displayed=displayed,
        )

        self.interactible = True
        self.displayed = displayed


    def initialize(self):
        self.magnet_reference = self.game_context.get_reference("magnet")  # useful to check if magnet was moved
        self.grid_reference = self.game_context.get_reference("grid")  # useful to check if grid was moved
        self.grid_background_reference = self.game_context.get_reference("grid_background")
        self.key_reference = self.game_context.get_reference("key")

    def handle_click_selection(self, event):
        self.grid_reference.displayed = True
        self.grid_background_reference.displayed = True

        if self.magnet_reference.in_grid and self.magnet_reference.collision_rect_id != 1:
            self.magnet_reference.display_collision_rect_bool = True
            self.magnet_reference.displayed = True

        #if the key is not on the closet and the magnet is at the end position
        is_key_displayable = self.key_reference.collision_rect_id != 1 and self.magnet_reference.collision_rect_id == 1
        if is_key_displayable:
            self.key_reference.displayed = True
            #self.game_context.dialogues.start_dialogue(10) #key found
