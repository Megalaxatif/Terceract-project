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
        self.placed = [False, True, True, False, False]
        self.collisions = collisions

    def update(self, event):
        #print(f"{self.placed[0]}, {self.placed[1]}, {self.placed[2]}, {self.placed[3]}, {self.placed[4]}, {self.game_context.current_wall_id}")

        if self.rect.colliderect(self.collisions[0]) and self.game_context.current_wall_id == 0: #back wall
            self.placed[0] = True
            if self.game_context.network_manager.is_connected:
                    self.game_context.network_manager.send_package("variable", "stool", "placed[0]", True)
        else : 
            self.placed[0] = False
            if self.game_context.network_manager.is_connected:
                    self.game_context.network_manager.send_package("variable", "stool", "placed[0]", False)

        if self.rect.colliderect(self.collisions[0]) and self.game_context.current_wall_id == 2: #front wall
            self.placed[3] = True
            if self.game_context.network_manager.is_connected:
                    self.game_context.network_manager.send_package("variable", "stool", "placed[3]", True)
        else :
            self.placed[3] = False
            if self.game_context.network_manager.is_connected:
                    self.game_context.network_manager.send_package("variable", "stool", "placed[3]", False)

        if self.rect.colliderect(self.collisions[0]) and self.game_context.current_wall_id == 3: #right wall
            self.placed[4] = True
            if self.game_context.network_manager.is_connected:
                    self.game_context.network_manager.send_package("variable", "stool", "placed[4]", True)

        else :
            self.placed[4] = False
            if self.game_context.network_manager.is_connected:
                    self.game_context.network_manager.send_package("variable", "stool", "placed[4]", False)
