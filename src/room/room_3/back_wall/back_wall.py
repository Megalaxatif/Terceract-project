import pygame
from wall_parent import Wall
from pathlib import Path

root_dir = Path(__file__).resolve().parent

class Back_wall_R3(Wall):
    def __init__(self, game):
        super().__init__(game, root_dir)
        #self.background.fill((0,0,255))