import pygame
from object import Game_object


class Closet(Game_object):
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
        displayed,
        lock
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
            displayed=displayed,
        )
        
        self.interactible = True
        self.original_displayed = displayed
        self.open = not self.displayed
        self.lock = lock

    def initialize(self):
        self.list_reference = self.game_context.get_reference_large("obj_in_closet")
        self.opened_closet_reference = self.game_context.get_reference("opened_closet")
        self.key_reference = self.game_context.get_reference("key")
        if self.key_reference.collision_rect_id == 1:
            self.lock = False

    def handle_click_selection(self, event):
        if not self.lock:
            inv = self.game_context.inventory

            if self.opened_closet_reference.open:
                    self.opened_closet_reference.displayed = not self.opened_closet_reference.displayed
                    for obj in self.list_reference:
                        obj.displayed = self.displayed
                        obj.display_collision_rect_bool = self.displayed

            for i in range(inv.rows):
                for j in range(inv.cols):
                    if inv.slots[i][j]:
                        if "obj_in_closet" in inv.slots[i][j].name:
                            inv.slots[i][j].displayed = self.displayed
                            inv.slots[i][j].display_collision_rect_bool = self.displayed
            self.game_context.drop_current_object(event)
