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
        self.interactible = True
        self.movable = True
        self.displayed = True

    def initialize(self):
        self.vase_reference = self.game_context.get_reference("water_vase")
        self.water_pump_reference = self.game_context.get_reference("water_pump")
    
    def handle_click(self, event):
        if not self.empty and self.water_pump_reference.rect.collidepoint(event.pos) and self.water_pump_reference.disabled:
            self.empty = True
            self.water_pump_reference.water_count += 1
            print("water the pump")

        elif not self.empty and self.water_pump_reference.rect.collidepoint(event.pos):
            print("the pump is already full")

        elif self.empty and self.vase_reference.rect.collidepoint(event.pos):
            if self.vase_reference.water_count <= 0:
                print("the vase is already empty")
            else:
                self.empty = False
                self.vase_reference.water_count -= 1
                print("steal water from the vase")
        
