import pygame
from wall_parent import Wall
from pathlib import Path

root_dir = Path(__file__).resolve().parent

class Right_wall_R2(Wall):
    def __init__(self, game):
        super().__init__(game, f"{game.root_dir}/assets/images/painting_2.png", None, root_dir)
        #self.background.fill((125,125,50))