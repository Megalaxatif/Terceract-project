import pygame
from wall_parent import Wall
class Back_wall_R5(Wall):
    def __init__(self, game):
        super().__init__(game, f"{game.root_dir}/assets/images/previous_door.png", None)
        #self.background.fill((0,0,255))