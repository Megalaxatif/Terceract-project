import pygame

#button class
class MenuButton():
    def __init__(self, x, y, image, scale):
        self.scale = scale
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.raw_image = self.image.copy()
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y) # without this, x and y are set to 0 after get_rect()
        self.raw_rect = self.rect.copy()

    def resize(self, delta):
        new_x = int(delta * self.raw_rect.x)
        new_y = int(delta * self.raw_rect.y)
        new_width = int(delta * self.raw_rect.w)
        new_height = int(delta * self.raw_rect.h)
        if (
            (new_width != self.rect.w)
            or (new_height != self.rect.h)
            or (new_x != self.rect.x)
            or (new_y != self.rect.y)
        ):
            self.image = pygame.transform.scale(self.raw_image, (new_width, new_height))
            self.rect = pygame.Rect(new_x, new_y, new_width, new_height)

    def draw(self, surface):
        #draw button on screen
        surface.blit(self.image, (self.rect.x, self.rect.y))
