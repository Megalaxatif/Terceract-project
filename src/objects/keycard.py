import pygame
from object import Game_object


class Keycard(Game_object):
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
        self.displayed = False #pour poser et prendre c le meme systeme que magnet (g pas compris ou il le fait)
        self.collisions = collisions
        self.movable = True
    
    def initialize(self):
        self.lock_reference = self.game_context.get_reference("keycard_reader")
        self.wallet_reference = self.game_context.get_reference("wallet")

    def handle_click(self, event):
        if self.rect.colliderect(self.lock_reference.rect):
            self.lock_reference.unlocked = True
            self.game_context.room_5_unlocked = True
            print("the door is unlocked")