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

    def handle_click(self, event):
        if not self.disabled:
            for obj in self.game_context.rooms[0].objects:
                if obj.name == "wallet": #a faire
                    obj.displayed = True
                    #todo : network
                    return True
        return False