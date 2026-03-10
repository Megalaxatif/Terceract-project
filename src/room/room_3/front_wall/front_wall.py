import pygame
from wall_parent import Wall
from pathlib import Path

root_dir = Path(__file__).resolve().parent

class Front_wall_R3(Wall):
    def __init__(self, game, room_id, wall_id):
        super().__init__(game, root_dir, room_id, wall_id)