import pygame
from pathlib import Path

class Object(pygame.sprite.Sprite):

    def __init__(self,
                 game_context,
                 object_name : str,
                 image_path : str,
                 rect : pygame.Rect,
                 collisions : list[pygame.Rect],
                 collision_index : int = -1,
                 movable : bool = True
                 ):
        super().__init__()

        self.name = object_name
        self.game_context = game_context
        self.screen = self.game_context.screen

        self.image_path = Path(image_path)
        self.image = pygame.image.load(Path(self.game_context.root_dir / self.image_path))
        self.raw_image = self.image

        parts = self.image_path.parts
        self.image_id = (Path(*parts[-7:])).as_posix()
        self.image_name = str(self.image_path.name)

        self.collision_rects = collisions
        self.raw_collision_rects = self.collision_rects.copy()
        self.collision_rect_index = collision_index # which collision rect the object is in

        self.rect = rect
        self.raw_rect = self.rect
        if self.collision_rect_index != -1 :
            self.valid_rect = self.collision_rects[self.collision_rect_index]
        else:
            self.valid_rect = self.rect.copy()
        self.displayed = True
        self.movable = movable

    def drop(self, x, y) -> bool: # try to fit the object in one of the collision rects, returns True if it fits, False otherwise
            print(f"Trying to drop {self.name} at ({x}, {y})")
            return_code = False
            point_rect = pygame.Rect(int(x), int(y), 1, 1)
            collision_index = point_rect.collidelist(self.collision_rects)
            if collision_index != -1:
                self.raw_rect.center = self.raw_collision_rects[collision_index].center
                self.valid_rect = self.raw_collision_rects[collision_index]
                self.collision_rect_index = collision_index
                print(f"Dropped {self.name} in collision rect {collision_index}")
                return_code = True

            else:
                self.raw_rect.center = self.valid_rect.center

            return return_code

    def draw(self): # draw every entities and the non entities
        if self.displayed:
            self.game_context.screen.blit(self.image, self.rect)

    def update(self, event):
        pass