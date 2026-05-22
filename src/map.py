import pygame
from pytmx.util_pygame import load_pygame
import pyscroll

class Map:
    def __init__(self, game_context, file_path):
        self.game_context = game_context
        self.screen = self.game_context.screen
        self.tmx_data = load_pygame(file_path) # raw data
        self.map_data = pyscroll.data.TiledMapData(self.tmx_data) # load data in pyscroll so that it can understand it
        self.map_layer = pyscroll.orthographic.BufferedRenderer(self.map_data, self.screen.get_size()) # create a map renderer optimised for orthographic maps
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=6) #layer group to render the map  and the sprites at the same time
        self.group.add(self.game_context.players) # always add the players to the map
        self.map_layer.zoom = 5

        self.collision_rects = []
        #retrieve the collisions
        for obj in self.tmx_data.objects:
            obj_class = getattr(obj, 'class')
            if obj_class == "collision":
                self.collision_rects.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

    def map_collision(self, rect):
        return rect.collidelist(self.collision_rects) > -1
