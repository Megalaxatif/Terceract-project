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
        for obj in wall:
            if isinstance(obj, Grid) and not obj.on_wall:
                obj.displayed = not obj.displayed
                for obj2 in wall:
                    if obj2.name == "magnet":
                        obj2.grid_displayed = self.displayed
                        obj2.displayed = obj2.grid_displayed and not obj2.key_given
                    if obj2.name == "key":
                        obj2.grid_displayed = self.displayed
                        obj2.displayed = obj2.grid_displayed and obj2.key_given
        self.game_context.drop_current_object(event)
