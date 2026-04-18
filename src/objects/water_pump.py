import pygame
from object import Game_object

class WaterPump(Game_object):
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

        self.disabled = True
        self.water_count = 0
        self.leaking = True

    def initialize(self):
        self.wallet_reference = self.game_context.get_reference("wallet")

    def update(self, event):
        if not self.leaking and self.water_count >= 2 : #faudra remettre 4 a la fin
            self.disabled = False

    def handle_click_selection(self, event):
        if not self.disabled:
            self.wallet_reference.displayed = True