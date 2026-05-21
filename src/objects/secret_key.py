import pygame
from object import Game_object

class Secret_key(Game_object):
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
            movable=True,
            displayed=True,
        )

    def initialize(self):
        self.door_reference = self.game_context.get_reference("exit_door")
        self.open_lock = self.game_context.get_reference("endlock_open")
        self.closed_lock = self.game_context.get_reference("endlock_closed")
        self.game_context.exit_door_opened = self.game_context.is_obj_in_wall(self.name, 0, 0) # init exit_door_opened
        self.displayed = not self.game_context.exit_door_opened

    def handle_click(self, event):
        if self.game_context.current_room_id == 0 and self.game_context.current_wall_id == 0 and self.door_reference.rect.collidepoint(event.pos):
            self.game_context.dialogues.start_dialogue(26)
            self.displayed = False
            self.game_context.exit_door_opened = True
            self.open_lock.displayed = True
            self.closed_lock.displayed = False
            if self.game_context.network_manager.is_connected:
                self.game_context.network_manager.send_package("variable", "game", "exit_door_opened", True)
                self.game_context.network_manager.send_package("variable", "secret_key", "displayed", False)
                self.game_context.network_manager.send_package("variable", "endlock_open", "displayed", True)
                self.game_context.network_manager.send_package("variable", "endlock_closed", "displayed", False)
        return super().handle_click(event)