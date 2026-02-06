import pygame
from pathlib import Path

class Object(pygame.sprite.Sprite):

    def __init__(self, 
                 game_context,
                 object_name : str,
                 image_path : str,
                 rect : pygame.Rect, 
                 collisions : list[pygame.Rect],
                 movable : bool = True
                 ):
        super().__init__()

        self.name = object_name
        self.game_context = game_context
        self.screen = self.game_context.screen

        self.image_path = Path(image_path)
        self.image = pygame.image.load(self.image_path)
        self.raw_image = self.image

        parts = self.image_path.parts
        self.image_id = (Path(*parts[-7:])).as_posix()
        self.image_name = str(self.image_path.name)

        self.rect = rect
        self.raw_rect = self.rect
        self.valid_rect = self.rect.copy()

        self.collision_rects = collisions
        self.raw_collision_rects = self.collision_rects.copy()
        self.current_collision_rect_index = 0 # which collision rect the object is in

        self.displayed = True
        self.movable = movable

    def try_to_drop(self) -> bool: # try to fit the object in one of the collision rects, returns True if it fits, False otherwise
            return_code = False
            collision_index = self.rect.collidelist(self.collision_rects)
            if collision_index != -1:
                self.raw_rect.center = self.raw_collision_rects[collision_index].center
                self.valid_rect = self.raw_collision_rects[collision_index]
                self.current_collision_rect_index = collision_index
                print(f"Dropped {self.name} in collision rect {collision_index}")
                return_code = True
            else:
                self.raw_rect.center = self.valid_rect.center
                return_code = False
            
            #TODO: maybe add a functionality to place the item anywhere in  the box
            return return_code

    def draw(self): # draw every entities and the non entities
        if self.displayed:
            self.game_context.screen.blit(self.image, self.rect)

    def update(self, event):
        pass