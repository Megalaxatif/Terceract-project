import pygame

class Vase(pygame.sprite.Sprite):
    def __init__(self, initial_posx: int | None, initial_posy: int | None, sprite_path : str | None):
        super().__init__()
        if sprite_path is not None:
            self.image = pygame.image.load(sprite_path)
            self.image = pygame.transform.scale_by(self.image, 1)
        else:
            self.image = pygame.Surface((10, 10))
            self.image.fill((255, 0, 0))

        self.rect = self.image.get_rect()