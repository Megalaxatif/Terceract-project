import pygame
from pathlib import Path

class Vase(pygame.sprite.Sprite):
    def __init__(self, game_context, image_path : str, rect):
        super().__init__()
        self.game_context = game_context
        self.image = pygame.image.load(image_path)
        self.image_path = image_path
        self.image_name = str(self.image_path.name)

        self.raw_image = self.image
        self.raw_rect = rect

        self.rect = rect
        self.x_valid = self.rect.x
        self.y_valid = self.rect.y
        self.dragging = False

