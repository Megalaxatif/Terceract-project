import pygame
from object import Game_object


class Book(Game_object):
    def __init__(self, game_context, object_name, image_path : str,
                 rect : pygame.Rect, collisions : list[pygame.Rect],
                 collision_index : int, displayed, bait):
        super().__init__(game_context, object_name, image_path, rect, collisions, collision_index)
        self.movable = False
        self.interactible = True
        self.displayed = displayed
        self.open = self.displayed
        self.bait = bait

    def update(self, event):
        pass

    def handle_click(self, event):
        if "book_bait" in self.name:
            self.displayed = not self.displayed
            return
        wall = self.game_context.current_wall.objects
        for obj in wall:
            if isinstance(obj, Book) and not obj.open and not obj.bait:
                obj.displayed = not obj.displayed
        self.game_context.drop_current_object(event)