import pygame
from object import Game_object

class Paper(Game_object):
    def __init__(self, game_context, object_name, image_path : str, rect : pygame.Rect, collisions : list[pygame.Rect], collision_index : int, default_collision, default_wall):
        super().__init__(game_context, object_name, image_path, rect, collisions, collision_index, False, False, default_collision, default_wall)


    def initialize(self):
        self.fullscreen_paper_reference = self.game_context.get_reference("fullscreen_paper")# useful to change the visibility
        if self.fullscreen_paper_reference is None:
            print(f"initialize of object named \"{self.name}\" error: no object with name \"fullscreen_paper\" found in the game, exiting")
            self.game_context.quit()


    def handle_click_selection(self, event):
        self.fullscreen_paper_reference.displayed = True

    def handle_left_click(self, event):
        pass

    def update(self, event):
        if self.fullscreen_paper_reference.displayed and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            self.fullscreen_paper_reference.displayed = False
