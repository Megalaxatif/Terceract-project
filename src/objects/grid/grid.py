import pygame
from pytmx.util_pygame import load_pygame

from pathlib import Path
from object import Game_object

class Grid(Game_object):
    def __init__(self, game_context, object_name, image_path : str,
                 rect : pygame.Rect, collisions : list[pygame.Rect],
                 collision_index : int, displayed, objects_data):
        super().__init__(game_context, object_name, image_path, rect,
                         collisions, collision_index)
        self.movable = False
        self.interactible = True
        self.displayed = displayed
        self.on_wall = self.displayed
        if objects_data:
            self.objects_data = list(objects_data)
        else:
            self.objects_data = None

    def update(self, event):
        if not self.on_wall:
            wall = self.game_context.current_wall.objects
            for obj in wall:
                if obj.name == "magnet":
                    obj.grid_displayed = self.displayed
                    obj.displayed = obj.grid_displayed and not obj.key_given
                if obj.name == "key":
                    obj.grid_displayed = self.displayed
                    obj.displayed = obj.grid_displayed and obj.key_given



    def handle_left_click(self, event):
        wall = self.game_context.current_wall.objects
        for obj in wall:
            if isinstance(obj, Grid) and not obj.on_wall:
                obj.displayed = not obj.displayed
        self.game_context.drop_current_object(event)