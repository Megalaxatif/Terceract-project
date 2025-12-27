import pygame
from wall_parent import Wall

class Front_wall_R2(Wall):
    def __init__(self, game):
        super().__init__(game, f"{game.root_dir}/assets/images/next_door.png", None)
        #self.background.fill((255,0,0))