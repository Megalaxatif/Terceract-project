import pygame
#import pyscroll
from pytmx.util_pygame import load_pygame
import sys
from pathlib import Path
from object import Object
pygame.init()
pygame.display.set_caption("The Grief Cube")
tmx_data = load_pygame("grid.tmx") # raw data from the tile file
magnet_image = pygame.image.load("magnet.png").convert_alpha() # load the image of the magnet
key_image = pygame.image.load("key.png").convert_alpha() # load the image of the key


class Magnet(Object):
    def __init__(self, game_context, image_path : str, rect : pygame.Rect, collisions : list[pygame.Rect], collision_index : int):
        super().__init__(game_context, "magnet", image_path, rect, collisions, collision_index)
        self.tmxdata = tmx_data.get_object_by_type("départ")
        self.rect = pygame.Rect(self.tmxdata[0].x, self.tmxdata[0].y, self.tmxdata[0].width, self.tmxdata[0].height)


class Key(Object):
    def __init__(self, game_context, image_path : str, rect : pygame.Rect, collisions : list[pygame.Rect], collision_index : int):
        super().__init__(game_context, "key", image_path, rect, collisions, collision_index)
        self.tmxdata = tmx_data.get_object_by_type("arrivée")
        self.rect = pygame.Rect(self.tmxdata[0].x, self.tmxdata[0].y, self.tmxdata[0].width, self.tmxdata[0].height)

class Grid(pygame.sprite.Sprite):
    def __init__(self, game_context, image_path : str, rect : pygame.Rect, collisions : list[pygame.Rect], collision_index : int, tmx_data):
        super().__init__(game_context, "grid", image_path, rect, collisions, collision_index)
        self.tmxdata = tmx_data.objects
        self.image = tmx_data.image
        self.object_group = pygame.sprite.Group() # create a sprite group to hold the objects
        self.rect_mort = []
        self.rect_depart = []
        self.rect_arrivee = []
        self.key_given = False
        self.ongoing = False
        for obj in self.tmxdata:
            self.object_group.add(obj)
            if obj:
                if obj.type == "mort":
                    self.rect_mort.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
                elif obj.type == "départ":
                    self.rect_depart.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
                elif obj.type == "arrivée":
                    self.rect_arrivee.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height)) 
    def update(self, event):
        if self.ongoing:
            magnet.displayed = True #ca suit la souris la
        if event.type == pygame.MOUSEBUTTONDOWN and any(r.collidepoint(pygame.mouse.get_pos()) for r in self.rect_depart) and not self.key_given:
            self.ongoing = True #mouse on beginning
        if event.type == pygame.MOUSEBUTTONDOWN and self.ongoing and any(r.collidepoint(pygame.mouse.get_pos()) for r in self.rect_mort):
            self.ongoing = False #mouse on death
            magnet.rect = self.rect_depart[0] #ca remet magnet à sa place de départ
        if event.type == pygame.MOUSEBUTTONUP and self.ongoing and any(r.collidepoint(pygame.mouse.get_pos()) for r in self.rect_arrivee):
            self.ongoing = False #mouse on end, normalement l'aimant disparait
            self.key_given = True #give the key
            key.displayed = True #ca fait apparaitre la clé à l'arrivée
        if event.type == pygame.MOUSEBUTTONUP and self.ongoing:
            self.ongoing = False
            magnet.rect = self.rect_depart[0] #ca remet magnet à sa place de départ
        
            
grille = Grid(None, "grid.tmx", pygame.Rect(0, 0, 0, 0), [], -1, tmx_data)
key = Key(None, "key.png", None, [], -1)
magnet = Magnet(None, "magnet.png", None, [], -1)