import pygame
from wall_parent import Wall
from pathlib import Path

root_dir = Path(__file__).resolve().parent

class Front_wall_R2(Wall):
    def __init__(self, game):
        super().__init__(game, root_dir) #TODO: can we find a way to remove root_dir ?