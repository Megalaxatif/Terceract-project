import pygame
from object import Game_object

class Stool(Game_object):
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
                           #problemes : manque collisions du stool mais c ok
        )
        self.placed = False
        self.collisions = collisions

    def handle_click(self, event):
        code = super().handle_click(event)
        if self.game_context.current_wall_id == 2 and self.game_context.current_room_id == 3:
            self.placed = True
            if self.game_context.network_manager.is_connected:
                    self.game_context.network_manager.send_package("variable", "stool", "placed", True)
        else :
            self.placed = False
            if self.game_context.network_manager.is_connected:
                    self.game_context.network_manager.send_package("variable", "stool", "placed", False)
        return code