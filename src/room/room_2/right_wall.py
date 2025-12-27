import pygame
from wall_parent import Wall

class Right_wall_R2(Wall):
    def __init__(self, game):
        super().__init__(game, f"{game.root_dir}/assets/images/closet.png", None)
        #self.background.fill((125,125,50))