import pygame
from wall_parent import Wall
from pathlib import Path

root_dir = Path(__file__).resolve().parent

class Left_wall_R4(Wall):
    def __init__(self, game):
        super().__init__(game, root_dir)
