import pygame
from wall_parent import Wall
from pathlib import Path

root_dir = Path(__file__).resolve().parent

class Back_wall_R1(Wall):
    def __init__(self, game):
        super().__init__(game, root_dir)
        #self.background.fill((0,0,255))

    def update_current_wall(self):
        for obj in self.entities:
            if obj.name == "digicode":
                obj.handle_event(self.game_context.event)
                obj.draw()