import pygame
from game import Game

# pygame
pygame.init()

# window
pygame.display.set_caption("The Grief Cube")
screen = pygame.display.set_mode((1080, 720), pygame.RESIZABLE)

# game
game = Game(screen)
game.start()

while game.game_running:
    game.update()