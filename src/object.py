import pygame
from pathlib import Path

class Object(pygame.sprite.Sprite):

    def __init__(self, 
                 game_context,
                 object_name : str,
                 image_path : str,
                 rect : pygame.Rect, 
                 collisions : list[pygame.Rect]
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
        self.raw_rect = rect.copy()
        self.valid_rect = rect


        self.collision_rects = collisions
        self.raw_collision_rects = collisions
        self.current_collision_rect_index = 0 # which collision rect the object is in

        self.displayed = True
        self.dragging = False