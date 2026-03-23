import pygame
from object import Game_object

class Borne(Game_object):
    def __init__(self, game_context, object_name, image_path : str,
                 rect : pygame.Rect, collisions : list[pygame.Rect],
                 collision_index : int):
        super().__init__(game_context, object_name, image_path, rect, collisions, collision_index)
        self.movable = False
        self.interactible = True


    def update(self, event):
        pass


    def handle_left_click(self, event):
        self.game_context.current_mini_game = "laboratory"
        