import pygame
from object import Game_object
from pathlib import Path
from utils import get_collision_rects, convert_to_pygame_rect_list
from objects.grid import key

class Magnet(Game_object):
    def __init__(self, game_context, object_name : str, image_path : str,
                 rect : pygame.Rect, collisions : list[pygame.Rect],
                 collision_index : int):
        super().__init__(game_context, object_name, image_path, rect, collisions, collision_index)
        #self.collision_rects = convert_to_pygame_rect_list(get_collision_rects(Path(self.game_context.root_dir / "src/room/room_1/right_wall/images/collision_layers"), self.name))
        #self.raw_collision_rects = self.collision_rects.copy()
        #print(len(self.collision_rects))
        #self.depart_rect = self.collision_rects[len(self.collision_rects)-1]
        #self.arrivee_rect = self.collision_rects[len(self.collision_rects)-2]
        #self.collision_rects.pop()
        #self.collision_rects.pop()
        self.displayed = False
        self.initial_center = rect.center
        self.grid_displayed = False
        self.key_given = False
        self.ongoing = False
        self.display_collision_rect_bool = False

    def update(self, event):
        depart_rect = self.collision_rects[-1]
        arrivee_rect = self.collision_rects[-2]
        
        #TODO : seuls pb restants : rectangles de collision visibles, clé apparait pas a l'arrivee, l'aimant se pose encore dans les rects autres
        #print(f"Ongoing: {self.ongoing} / key given : {self.key_given} / mousebuttonup : {event.type == pygame.MOUSEBUTTONUP}")
        if (event.type == pygame.MOUSEBUTTONDOWN or event.type == pygame.MOUSEBUTTONUP) and depart_rect.collidepoint(pygame.mouse.get_pos()) and not self.key_given:
            self.ongoing = True #mouse on beginning
            
        if self.ongoing and any(self.collision_rects[i].collidepoint(pygame.mouse.get_pos()) for i in range(len(self.collision_rects)-2)):
            self.ongoing = False #mouse on death
            if self.game_context.network_manager.is_connected:
                self.game_context.network_manager.send_package("variable", "game", "other_player_object_name", "")
                self.game_context.network_manager.send_package(
                    "function",
                    "game",
                    "drop_object",
                    self.game_context.current_object.name,
                    self.game_context.current_room_id,
                    self.game_context.current_wall_id,
                    self.game_context.current_object.collision_rect_id
                )
            self.game_context.current_object = None
            self.raw_rect.center = self.initial_center #ca remet magnet à sa place de départ
 
        if (event.type == pygame.MOUSEBUTTONDOWN) and self.ongoing and arrivee_rect.collidepoint(pygame.mouse.get_pos()):
            self.ongoing = False #mouse on end
            self.key_given = True #give the key
            for obj in self.game_context.current_wall.objects:
                if obj.name == "key":
                    obj.key_given = True #ca fait apparaitre la clé à l'arrivée (marche pas)
                    obj.displayed = True
                if obj.name == "magnet":
                    obj.grid_displayed = self.displayed
                    obj.displayed = obj.grid_displayed and not obj.key_given
            self.game_context.drop_current_object(event)

        if (event.type == pygame.MOUSEBUTTONDOWN) and self.ongoing and not arrivee_rect.collidepoint(pygame.mouse.get_pos()) and not depart_rect.collidepoint(pygame.mouse.get_pos()):
            self.ongoing = False
            self.rect.x, self.rect.y = depart_rect.x, depart_rect.y #ca remet magnet à sa place de départ (jsp si ca marche ou c la fonction drop qui override)
            self.game_context.drop_current_object(event)
    
    def handle_left_click(self, event):
        pass #tt passe par update