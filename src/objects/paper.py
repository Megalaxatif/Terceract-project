import pygame
from object import Game_object


class Paper(Game_object):
    def __init__(self, game_context, object_name, image_path : str, rect : pygame.Rect, collisions : list[pygame.Rect], collision_index : int):
        super().__init__(game_context, object_name, image_path, rect, collisions, collision_index, False, False)


    def initialize(self):
        self.fullscreen_paper_reference = self.game_context.get_reference("fullscreen_paper")# useful to change the visibility
        if self.fullscreen_paper_reference is None:
            print(f"initialize of object named \"{self.name}\" error: no object with name \"fullscreen_paper\" found in the game, exiting")
            self.game_context.quit()


    def handle_click_selection(self, event):
        self.fullscreen_paper_reference.displayed = True
