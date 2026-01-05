import pygame
from pathlib import Path

class Vase:
    def __init__(self, image_path, info_game_data):
        super().__init__()
        self.image = pygame.image.load(image_path)
        self.raw_cropped_image = pygame.image.load(str(Path(image_path).parent) + "/cropped_" + str(Path(image_path).name))
        self.cropped_image = self.raw_cropped_image
        self.x = info_game_data[0]
        self.y = info_game_data[1]
        self.w = info_game_data[2]
        self.h = info_game_data[3]
        self.x_valid = info_game_data[4]
        self.y_valid = info_game_data[5]
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        self.dragging = False

