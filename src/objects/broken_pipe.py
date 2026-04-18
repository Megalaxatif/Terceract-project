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
        movable: bool,
        displayed: bool,
        interactible: bool,
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
            movable,
            displayed
        )
        self.displayed = displayed
        self.interactible = interactible           #fonctionne comme un closet mais avec 2 options
        self.unclogged = False
        self.collisions = collisions
        self.open = False
        self.background = "gray_bg" in self.name
        self.movable = False

    def initialize(self):
        self.menu_reference = self.game_context.get_reference("open_broken_pipe")
        self.bg_reference = self.game_context.get_reference("gray_bg_broken_pipe")

    def handle_click_selection(self, event): #unclog sur les deux boutons ?? et bloqué après
        if self.open and not self.background:
            if self.menu_reference.collisions[0].collidepoint(event.pos):
                self.unclogged = True
                self.open = False
                self.menu_reference.displayed = False
                self.bg_reference.displayed = False
                print("pipe unclogged")
            elif self.menu_reference.collisions[1].collidepoint(event.pos) and not self.unclogged:
                print("still clogged")
            elif self.menu_reference.collisions[1].collidepoint(event.pos) and self.unclogged:
                self.interactible = False
                self.movable = True
                self.open = False
                self.menu_reference.displayed = False
                self.bg_reference.displayed = False
            else :
                self.open = False
                self.menu_reference.displayed = False
                self.bg_reference.displayed = False
        elif not self.background and not self.unclogged:
            self.open = not self.open
            self.menu_reference.displayed = self.open
            self.bg_reference.displayed = self.open
