import pygame
from object import Game_object


class Wallet(Game_object):
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
            displayed=False,
        )
        #va fonctionner comme un closet, faut prendre la carte qu'il contient
        self.interactible = True
        self.original_displayed = False
        self.open = False
        self.collisions = collisions
        self.card_taken = False
        self.background = "gray_bg" in self.name

    def initialize(self):
        self.menu_reference = self.game_context.get_reference("open_wallet")
        self.bg_reference = self.game_context.get_reference("gray_bg_wallet")

    def handle_click(self, event): 
        if self.open:
            if self.menu_reference.collisions[0].collidepoint(event.pos): 
                self.card_taken = True
                self.open = False
                self.menu_reference.displayed = False
            else :
                self.open = False
                self.menu_reference.displayed = False
        elif not self.card_taken:
            self.open = not self.open
            self.menu_reference.displayed = self.open
            self.bg_reference.displayed = self.open
