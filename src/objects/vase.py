import pygame
from pathlib import Path
from object import Object

class Vase(pygame.sprite.Sprite):
    def __init__(self, game_context, image_path : str, rect : pygame.Rect, collisions : list[pygame.Rect]):
        super().__init__()
        self.name = "vase"
        
        self.game_context = game_context
        self.image = pygame.image.load(image_path)
        self.image_path = Path(image_path)
        parts = self.image_path.parts
        self.image_id = (Path(*parts[-7:])).as_posix()
        self.image_name = str(self.image_path.name)

        self.raw_image = self.image
        self.raw_rect = rect
        self.displayed = True

        self.rect = rect
        self.x_valid = self.rect.x
        self.y_valid = self.rect.y
        self.dragging = False

        self.valid_rect = self.rect.copy()
        self.collision_rects = collisions
        self.current_collision_rect_index = 0 # which collision rect the object is in
        self.raw_collision_rects = self.collision_rects.copy()
