import pygame
#from pytmx.util_pygame import load_pygame

from pathlib import Path
from object import Game_object

class Grid(Game_object):
    def __init__(self, game_context, object_name, image_path : str,
                 rect : pygame.Rect, collisions : list[pygame.Rect],
                 collision_index : int, displayed):
        super().__init__(game_context, object_name, image_path, rect,
                         collisions, collision_index)
        self.movable = False
        self.interactible = True
        self.displayed = displayed
        self.on_wall = self.displayed

    def update(self, event):
        pass

    def handle_left_click(self, event):
        wall = self.game_context.current_wall.objects
        inv = self.game_context.inventory
        for obj in wall:
            if isinstance(obj, Grid) and not obj.on_wall:
                obj.displayed = not obj.displayed
                for obj2 in wall:
                    if "magnet" in obj2.name and obj2.in_grid:
                        obj2.displayed = not obj2.key_given and obj.displayed
                    if obj2.name == "key":
                        obj2.displayed = obj2.key_given and obj.displayed
        for i in range(inv.rows):
            for j in range(inv.cols):
                if inv.slots[i][j]:
                    if "magnet" in inv.slots[i][j].name:
                        inv.slots[i][j].displayed = self.displayed
                        inv.slots[i][j].display_collision_rect_bool = self.displayed
        self.game_context.drop_current_object(event)
