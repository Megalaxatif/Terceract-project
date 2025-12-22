import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, initial_posx: int | None, initial_posy: int | None, sprite_path : str | None, id, displayed):
        super().__init__()
        if sprite_path is not None:
            self.image = pygame.image.load(sprite_path)
            self.image = pygame.transform.scale_by(self.image, 1)
        else:
            self.image = pygame.Surface((10, 10))
            self.image.fill((255, 0, 0))

        self.rect = self.image.get_rect()
        #print(self.rect
        self.hitbox = pygame.Rect(0,0, self.rect.width *0.5, self.rect.height *0.25)
        self.rect.x = initial_posx if initial_posx is not None else 0
        self.rect.y = initial_posy if initial_posy is not None else 0
        self.precise_x = initial_posx if initial_posx is not None else 0
        self.precise_y = initial_posy if initial_posx is not None else 0 
        self.base_velocity = 5
        self.velocity = self.base_velocity
        self.player_id = id
        self.is_displayed = displayed
        self.old_x = initial_posx if initial_posx is not None else 0
        self.old_y = initial_posy if initial_posy is not None else 0


    def move_up(self):
        self.rect.y -= self.velocity

    def move_down(self):
        self.rect.y += self.velocity

    def move_right(self):
        self.rect.x += self.velocity

    def move_left(self):
        self.rect.x -= self.velocity

    def set_posX (self, posx):
        self.rect.x = posx
        self.precise_x = posx
        self.old_x = posx

    def set_posY (self, posy):
        self.rect.y = posy
        self.precise_y = posy
        self.old_y = posy

    def get_posX(self):
        return self.rect.x
    
    def get_posY(self):
        return self.rect.y
    
    def get_width(self):
        return self.rect.width
    
    def get_height(self):
        return self.rect.height

    def get_velocity(self):
        return self.velocity

    def update_velocity(self, coeff):
        self.velocity = self.base_velocity * coeff
