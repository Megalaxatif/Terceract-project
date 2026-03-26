import pygame
from object import Game_object
from objects.book import Book


class Library(Game_object):
    def __init__(self, game_context, object_name, image_path : str, rect : pygame.Rect, collisions : list[pygame.Rect], collision_index : int):
        super().__init__(game_context, object_name, image_path, rect, collisions, collision_index, False)

    def initialize(self):
        self.book_bait1_reference = self.game_context.get_reference("book_bait1") # useful to change the visibility
        if self.book_bait1_reference is None:
            print(f"initialize of object named \"{self.name}\" error: no object with name \"book_bait1\" found in the game, exiting")
            self.game_context.quit()


    def handle_click_selection(self, event):
        self.book_bait1_reference.displayed = not self.book_bait1_reference.displayed
        #self.game_context.drop_current_object(event) # the library is local to the player and it is not selected anyways