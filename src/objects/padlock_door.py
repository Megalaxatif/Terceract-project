import pygame
from object import Game_object


class Padlock_door(Game_object):
    def __init__(self, game_context, object_name, image_path : str, rect : pygame.Rect, collisions : list[pygame.Rect], collision_index : int):
        super().__init__(game_context, object_name, image_path, rect, collisions, collision_index, False)
        self.interactible = True
        self.padlock = None

    def handle_click(self, event):
        wall = self.game_context.current_wall
        if not self.padlock:
            for obj in wall.objects:
                if obj.name == "padlock":
                    self.padlock = obj
                    self.padlock.displayed = True
        else:
            self.padlock.displayed = False
            self.padlock = None
            self.game_context.drop_current_object(event)

