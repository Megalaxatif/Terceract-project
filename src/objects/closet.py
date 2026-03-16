import pygame
from pathlib import Path
from object import Game_object
import os
from utils import load_json_file, convert_to_pygame_rect, convert_to_pygame_rect_list, create_object

class Closet(Game_object):
    def __init__(self, game_context, object_name, image_path : str,
                 rect : pygame.Rect, collisions : list[pygame.Rect],
                 collision_index : int, displayed, objects_data):
        super().__init__(game_context, object_name, image_path, rect, collisions, collision_index)
        self.movable = False
        self.interactable = True
        self.collision_rects = []
        self.displayed = displayed
        self.open = self.displayed
        if objects_data:
            self.objects_data = list(objects_data)
        else:
            self.objects_data = None
    
    def update(self, event):
        if not self.open:
            wall = self.game_context.current_wall.objects
            for obj in wall:
                if "obj_in_closet" in obj.name:
                    obj.displayed = self.displayed
        
        
    def handle_left_click(self, event):
        wall = self.game_context.current_wall.objects
        for obj in wall:
            if isinstance(obj, Closet) and not obj.open:
                obj.displayed = not obj.displayed
        self.game_context.drop_current_object(event)