import pygame
from object import Game_object

class Fullscreen_paper(Game_object):
    def __init__(self, game_context, object_name, image_path : str, rect : pygame.Rect, collisions : list[pygame.Rect], collision_index : int):
        super().__init__(game_context, object_name, image_path, rect, collisions, collision_index, False, False)

    def handle_click_selection(self, event):
        self.displayed = False