import pygame
from object import Game_object


class BrokenPipe(Game_object):
    def __init__(
        self,
        game_context,
        object_name,
        image_path: str,
        rect: pygame.Rect,
        collisions: list[pygame.Rect],
        default_collision: pygame.Rect,
        default_wall: str,
        collision_index: int,
    ):
        super().__init__(
            game_context,
            object_name,
            image_path,
            rect,
            collisions,
            default_collision,
            default_wall,
            collision_index,
            movable=False,
            displayed=True,
        ) 

        self.interactible = True           #fonctionne comme un closet mais avec 2 options
        self.unclogged = False
        self.collisions = collisions
        self.open = False
        self.background = "gray_bg" in self.name

    def initialize(self):
        self.menu_reference = self.game_context.get_reference("open_broken_pipe")
        self.bg_reference = self.game_context.get_reference("gray_bg_broken_pipe")

    def handle_click(self, event): #ca ouvre rien :( jsp pk
        if self.open:
            if self.menu_reference.collisions[1].collidepoint(event.pos):
                self.unclogged = True
                self.open = False
                self.menu_reference.displayed = False
            elif self.menu_reference.collisions[0].collidepoint(event.pos) and not self.unclogged:
                print("still clogged")
            elif self.menu_reference.collisions[0].collidepoint(event.pos) and self.unclogged:
                self.interactible = False
                self.movable = True
                self.open = False
                self.menu_reference.displayed = False
            else :
                self.open = False
                self.menu_reference.displayed = False
        elif not self.unclogged:
            self.open = not self.open
            self.menu_reference.displayed = self.open
            self.bg_reference.displayed = self.open
