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
        self.interactible = False     #ouvre que la porte que quand wallet est ouvert, et a voir pour multi
    
    def initialize(self):
        self.lock_reference = self.game_context.get_reference("keycard_reader")
        self.wallet_reference = self.game_context.get_reference("wallet")

    def handle_click(self, event):
        #print(f"{self.rect.colliderect(self.lock_reference.rect)}")
        if self.lock_reference.rect.collidepoint(event.pos) and self.game_context.current_room_id == 3 and self.game_context.current_wall_id == 2:
            #self.game_context.room_5_unlocked = True
            self.game_context.unlock_room(self.game_context.current_room_id)
            #if self.game_context.network_manager.is_connected:        # a voir comment on peut faire
            #        self.game_context.network_manager.send_package("variable", "game_context", "room_5_unlocked", True)
            self.game_context.dialogues.start_dialogue(21) #unlock the door