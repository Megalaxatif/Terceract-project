import pygame

class Vase(pygame.sprite.Sprite):
    def __init__(self, game_context, image_path : str, rect : pygame.Rect, collisions : list[pygame.Rect]):
        super().__init__()
        self.game_context = game_context
        self.image = pygame.image.load(image_path)
        self.raw_image = self.image
        self.rect = rect
        self.raw_rect = self.rect.copy()
        self.valid_rect = self.rect.copy()
        self.collision_rects = collisions
        self.current_collision_rect_index = 0 # which collision rect the object is in
        self.raw_collision_rects = self.collision_rects.copy()
        self.dragging = False

