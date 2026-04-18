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
            displayed=True,                  #todo network
                           #problemes : manque collisions du stool 
        )
        self.placed = [False, True, True, False, False] #back wall, right wall wall, right wall, front wall, left wall (broken pipe)
        self.collisions = collisions

    def update(self, event):
        if self.rect.colliderect(self.collisions[0]) and self.game_context.current_wall_id == 0: #back wall
            self.placed[0] = True
        else : 
            self.placed[0] = False

        if self.rect.colliderect(self.collisions[0]) and self.game_context.current_wall_id == 2: #front wall
            self.placed[3] = True
        else :
            self.placed[3] = False

        if self.rect.colliderect(self.collisions[0]) and self.game_context.current_wall_id == 3: #left wall
            self.placed[4] = True
        else :
            self.placed[4] = False
