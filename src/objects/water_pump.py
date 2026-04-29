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

        self.disabled = True #a remettre a true a la fin
        self.water_count = 0 #remplir la pump
        self.leaking = True #boucher trous
        self.pipe_fixed = False #remettre morceau manquant

    def initialize(self):
        self.wallet_reference = self.game_context.get_reference("wallet")

    def water_increase(self):
        self.water_count += 1

    def update(self, event):
        if not self.leaking and self.water_count >= 4 and self.pipe_fixed: #faudra remettre 4 a la fin
            self.disabled = False

    def handle_click_selection(self, event):
        if not self.disabled:
            self.wallet_reference.displayed = True
            print("something happened...")