import pygame
from wall_parent import Wall
class Front_wall_R5(Wall):
    def __init__(self, game):
        super().__init__(game, f"{game.root_dir}/assets/images/door.png", None)
        #self.background.fill((255,0,0))