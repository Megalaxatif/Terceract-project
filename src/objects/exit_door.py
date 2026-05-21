import pygame
from object import Game_object

class Exit_door(Game_object):
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

    def handle_click_selection(self, event):
        if self.game_context.exit_door_opened:
            self.game_context.current_mini_game = "end_screen"
        else:
            self.game_context.dialogues.start_dialogue(7) #door locked