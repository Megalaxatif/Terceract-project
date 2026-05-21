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
        self.collisions = collisions

    def initialize(self):
        self.door_reference = self.game_context.get_reference("exit_door")

    def handle_click(self, event):
        #self.game_context.drop_current_object(event)
        if self.game_context.current_room_id == 0 and self.game_context.current_wall_id == 0 and self.door_reference.rect.collidepoint(event.pos):
            self.game_context.dialogues.start_dialogue(26) #door open (il veut pas jsp pk)
            self.displayed = False
            self.door_reference.open = True
            if self.game_context.network_manager.is_connected:
                self.game_context.network_manager.send_package("variable", "exit_door", "open", True)
                self.game_context.network_manager.send_package("variable", "secret_key", "displayed", False)
                return True

        return False