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
        self.interactible = "wallet" == self.name #en soi ca marche mais j'arrive pas a prendre la carte D:
        self.open = not self.displayed
        self.background = "gray_bg" in self.name
        self.card_taken = False
        self.displayed = False
        self.original_displayed = False

    def initialize(self):
        self.card_reference = self.game_context.get_reference("keycard") #g peur que la carte reste énorme meme en dehors du wallet
        self.menu_reference = self.game_context.get_reference("opened_wallet")
        self.bg_reference = self.game_context.get_reference("gray_bg_wallet")

    def swap_display(self):
        wall = self.game_context.current_wall.objects
        for obj in wall:
            if isinstance(obj, Wallet) and obj.open:
                obj.displayed = not obj.displayed
                obj.display_collision_rect_bool = self.displayed

        self.card_reference.displayed = self.displayed
        self.card_reference.display_collision_rect_bool = self.displayed # will follow the opening and the closing of the drawer automaticaly

    def handle_click_selection(self, event):
        inv = self.game_context.inventory

        if not self.open or self.background:
            self.swap_display()

        for i in range(inv.rows):
            for j in range(inv.cols):
                if inv.slots[i][j]:
                    if "keycard" in inv.slots[i][j].name:
                        inv.slots[i][j].displayed = self.displayed
                        inv.slots[i][j].display_collision_rect_bool = self.displayed

        self.game_context.drop_current_object(event)
