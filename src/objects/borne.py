import pygame
from object import Game_object

class Borne(Game_object):
    def __init__(self, game_context, object_name, image_path : str,
                 rect : pygame.Rect, collisions : list[pygame.Rect],
                 collision_index : int):
        super().__init__(game_context, object_name, image_path, rect, collisions, collision_index)
        self.movable = False


    def handle_click_selection(self, event):
        self.game_context.current_mini_game = "laboratory"
