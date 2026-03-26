import pygame
from object import Game_object


class Padlock_door(Game_object):
    def __init__(self, game_context, object_name, image_path : str, rect : pygame.Rect, collisions : list[pygame.Rect], collision_index : int):
        super().__init__(game_context, object_name, image_path, rect, collisions, collision_index, False, True)


    def initialize(self):
        self.padlock_reference = self.game_context.get_reference("padlock")# useful to change the visibility
        if self.padlock_reference is None:
            print(f"initialize of object named \"{self.name}\" error: no object with name \"padlock\" found in the game, exiting")
            self.game_context.quit()


    def handle_click_selection(self, event):
        self.padlock_reference.displayed = True


