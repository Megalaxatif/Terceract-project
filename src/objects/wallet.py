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
        movable: bool,
        displayed: bool,
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
            displayed,
        )
        self.interactible = "wallet" == self.name
        self.original_displayed = displayed
        self.displayed = displayed
        self.open = not self.displayed
        self.background = "gray_bg" in self.name
        self.card_taken = False

    def initialize(self):
        self.card_reference = self.game_context.get_reference("keycard") #g peur que la carte reste énorme meme en dehors du wallet
        self.menu_reference = self.game_context.get_reference("open_wallet")
        self.bg_reference = self.game_context.get_reference("gray_bg_wallet")

    def handle_click(self, event): 
        if self.open and not self.background:
            if self.menu_reference.collisions[0].collidepoint(event.pos): 
                self.card_taken = True
                self.open = False
                self.menu_reference.displayed = False
            else :
                self.open = False
                self.menu_reference.displayed = False
        elif not self.background:
            self.open = not self.open
            self.menu_reference.displayed = self.open
            self.bg_reference.displayed = self.open
            if not self.card_taken:
                self.card_reference.displayed = self.open
