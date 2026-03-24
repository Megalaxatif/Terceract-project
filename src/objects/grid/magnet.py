import pygame
from object import Game_object
from pathlib import Path
from utils import get_collision_rects, convert_to_pygame_rect_list
from objects.grid.grid import Grid

class Magnet(Game_object):
    def __init__(self,
                 game_context,
                 object_name : str,
                 image_path : str,
                 rect : pygame.Rect,
                 collisions : list[pygame.Rect],
                 collision_index : int = -1,
                 ):
        super().__init__(game_context, object_name, image_path, rect, collisions, collision_index)
        self.displayed = False
        self.initial_pos = self.rect.x, self.rect.y
        self.grid_displayed = False
        self.interactible = True
        self.key_given = False
        self.default_collision = self.collision_rects.pop()
        self.final_collision = [self.collision_rects.pop()]
        self.collision_rects_wall = self.collision_rects.copy()
        self.raw_collision_rects = [self.default_collision.copy()] # copy() is magic. don't touch it
        self.collision_rects = [self.default_collision.copy()]
        self.in_grid = False

    def update(self, event):
        #TODO : seuls pb restants : rectangles de collision visibles, clé apparait pas a l'arrivee, l'aimant se pose encore dans les rects autres
        #print(f"Ongoing: {self.ongoing} / key given : {self.key_given} / mousebuttonup : {event.type == pygame.MOUSEBUTTONUP}"

        if self.in_grid:
            pos = pygame.mouse.get_pos()[0] / self.game_context.current_wall.delta, pygame.mouse.get_pos()[1] / self.game_context.current_wall.delta
            point_rect = pygame.Rect(pos[0], pos[1], 1, 1)
            
            if (point_rect.collidelist(self.collision_rects_wall) != -1) and self == self.game_context.current_object:
                self.game_context.current_object = None
                self.raw_rect.x, self.raw_rect.y = self.initial_pos #ca remet magnet à sa place de départ

        
    def handle_left_click(self, event):
        if self.in_grid:
            start_rect = self.default_collision
            end_rect = self.final_collision[0]

            pos = event.pos[0] / self.game_context.current_wall.delta, event.pos[1] / self.game_context.current_wall.delta
                
            if end_rect.collidepoint(pos):
                self.key_given = True #give the key
                self.displayed = False
                
                for obj in self.game_context.current_wall.objects:
                    if obj.name == "key":
                        obj.key_given = True #ca fait apparaitre la clé à l'arrivée (marche pas)
                        obj.displayed = True
                        
                self.game_context.drop_current_object(event)

            
            elif not end_rect.collidepoint(pos) and not start_rect.collidepoint(pos):
                self.raw_rect.x, self.raw_rect.y = self.initial_pos
                self.game_context.drop_current_object(event)

        elif self == self.game_context.inventory.current_object:
            wall = self.game_context.current_wall.objects
            for obj in wall:
                if isinstance(obj, Grid) and not obj.on_wall and obj.displayed:
                    self.in_grid = True
                

