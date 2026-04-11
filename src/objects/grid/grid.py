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
        self.on_wall = self.displayed

    def update(self, event):
        pass

    def initialize(self):
        self.magnet_reference = self.game_context.get_reference("magnet")  # useful to check if magnet was moved
        self.grid_reference = self.game_context.get_reference("grid")  # useful to check if grid was moved
        self.grid_background_reference = self.game_context.get_reference("grid_background")
        self.key_reference = self.game_context.get_reference("key")

    def handle_click_selection(self, event):
        self.grid_reference.displayed = True
        self.grid_background_reference.displayed = True
        if self.magnet_reference.in_grid:
            self.magnet_reference.display_collision_rect_bool = True
            self.magnet_reference.displayed = True
        if self.key_reference.found:
            self.key_reference.displayed = True

    # def handle_click_selection(self, event):
    #     wall = self.game_context.current_wall.objects
    #     inv = self.game_context.inventory

    #     # Toggle the "loose" grid (the one that is not on the wall)
    #     for obj in wall:
    #         if isinstance(obj, Grid) and not obj.on_wall:
    #             obj.displayed = not obj.displayed

    #             # Toggle dependent objects on the wall
    #             for obj2 in wall:
    #                 if "magnet" in obj2.name and getattr(obj2, "in_grid", False):
    #                     obj2.displayed = (not getattr(obj2, "key_given", False)) and obj.displayed

    #                 if obj2.name == "key":
    #                     obj2.displayed = getattr(obj2, "key_given", False) and obj.displayed

    #     # Toggle magnets in inventory (keep old behavior)
    #     for i in range(inv.rows):
    #         for j in range(inv.cols):
    #             if inv.slots[i][j]:
    #                 if "magnet" in inv.slots[i][j].name:
    #                     inv.slots[i][j].displayed = self.displayed
    #                     inv.slots[i][j].display_collision_rect_bool = self.displayed

    #     self.game_context.drop_current_object(event)