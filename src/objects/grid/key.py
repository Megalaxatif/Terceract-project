import pygame
from object import Game_object


class Key(Game_object):
    def __init__(
        self,
        game_context,
        object_name: str,
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
            displayed=False,
        )

        self.key_given = False
        self.displayed = False
        
        
    def initialize(self):
        self.closed_closet_reference = self.game_context.get_reference("closed_closet")# useful to change the visibility
        if self.closed_closet_reference is None:
            print(f"initialize of object named \"{self.name}\" error: no object with name \"closed_closet\" found in the game, exiting")
            self.game_context.quit()
            
    def handle_click_selection(self, event):
        pass

    def handle_click(self, event):
        if self.closed_closet_reference.rect.collidepoint(event.pos):
            self.displayed = False
            self.gone = True
            self.closed_closet_reference.lock = False
            self.game_context.inventory.remove_current_object(event)
            print("unlocked")
            return True

        self.game_context.drop_current_object(event)
