import pygame
from wall_parent import Wall
class Left_wall_R4(Wall):
    def __init__(self, game):
        super().__init__(game, f"{game.root_dir}/assets/images/painting_1.png", None)
        #self.background.fill((0,255,0))
