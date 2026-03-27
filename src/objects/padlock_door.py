import pygame
from object import Game_object


class Padlock_door(Game_object):
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
        self.interactible = True
        self.padlock_reference = None

    def initialize(self):
        self.padlock_reference = self.game_context.get_reference("padlock")  # useful to change the visibility
        if self.padlock_reference is None:
            print(
                f'initialize of object named "{self.name}" error: no object with name "padlock" found in the game, exiting'
            )
            self.game_context.quit()

    def handle_click_selection(self, event):
        if self.padlock_reference is None:
            # In case initialize() hasn't been called for some reason
            self.initialize()
            if self.padlock_reference is None:
                return
        self.padlock_reference.displayed = True