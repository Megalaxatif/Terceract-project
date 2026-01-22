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
        self.raw_rect = self.rect
        self.valid_rect = self.rect.copy()

        self.collision_rects = collisions
        self.raw_collision_rects = self.collision_rects.copy()
        self.current_collision_rect_index = 0 # which collision rect the object is in

        self.displayed = True
        self.dragging = False

    def handle_event(self, event):
        collision_index = self.rect.collidelist(self.collision_rects)
        if collision_index != -1:
            self.raw_rect.center = self.collision_rects[collision_index].center
            self.valid_rect = self.collision_rects[collision_index]
        else:
            self.raw_rect.center = self.valid_rect.center
        
        #TODO: maybe add a functionality to place the item anywhere in  the box
        self.dragging = False # NOTE: dangerous because dragging is only defined in Vase
        self.game_context.current_item = None