import pygame
from object import Game_object


class Water_bottle(Game_object):
    def __init__(
        self,
        game_context,
        object_name,
        image_path: str,
        rect: pygame.Rect,
        collisions: list[pygame.Rect],
        default_collision: pygame.Rect,
        default_wall: str,
        collision_index: int,
        movable: bool,
        displayed: bool,
    ):
        super().__init__(
            game_context,
            object_name,
            image_path,
            rect,
            collisions,
            default_collision,
            default_wall,
            collision_index,
            movable,
            displayed,
        )
        self.empty = False
        self.interactible = True   #si je synchro empty en multi ca casse tout ?? "center_object_error: invalid object name, the name water_bottle was not found in the inventory"
    
    def initialize(self):
        self.vase_reference = self.game_context.get_reference("water_vase")
        self.water_pump_reference = self.game_context.get_reference("water_pump")
    
    def handle_click(self, event):
        if not self.empty and self.water_pump_reference.rect.collidepoint(event.pos) and self.water_pump_reference.water_count < 2 and self.game_context.current_room_id == 3 and self.game_context.current_wall_id == 0:
            self.empty = True
            self.water_pump_reference.water_count += 1
            if self.game_context.network_manager.is_connected:
                self.game_context.network_manager.send_package("function", "water_pump", "water_increase", "1")
                #self.game_context.network_manager.send_package("variable", "water_bottle", "empty", True)
            print("water the pump")

        elif not self.empty and self.water_pump_reference.rect.collidepoint(event.pos) and self.game_context.current_room_id == 3 and self.game_context.current_wall_id == 0:
            print("the pump is already full")

        elif self.empty and self.vase_reference.rect.collidepoint(event.pos) and self.game_context.current_room_id == 1 and self.game_context.current_wall_id == 0:
            if self.vase_reference.water_count <= 0:
                print("the vase is already empty")
            else:
                self.empty = False
                self.vase_reference.water_count -= 1
                if self.game_context.network_manager.is_connected:
                    self.game_context.network_manager.send_package("function", "water_vase", "decrease_water", "1")
                    #self.game_context.network_manager.send_package("variable", "water_bottle", "empty", False)
                print("steal water from the vase")
        #self.game_context.drop_current_object(event)
        
