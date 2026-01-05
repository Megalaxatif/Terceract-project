import pygame
from wall_parent import Wall
from pathlib import Path

root_dir = Path(__file__).resolve().parent

class Front_wall_R4(Wall):
    def __init__(self, game):
        super().__init__(game, f"{game.root_dir}/assets/images/next_door.png", [f"{root_dir}/images/table_test.png"], root_dir)
        #self.background.fill((255,0,0))
        
class Table:
    def __init__(self, wall):
        pass