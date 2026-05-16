import pygame
from object import Game_object


class BrokenPipe(Game_object):
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
            movable=True,
            displayed=True,
        )
        self.interactible = True
        self.collisions = collisions

    def initialize(self):
    #    self.stool_reference = self.game_context.get_reference("stool")
        self.water_pump_reference = self.game_context.get_reference("water_pump")

    def update(self, event):
        if self.rect.colliderect(self.collisions[1]):
            self.water_pump_reference.pipe_fixed = True
            if self.game_context.network_manager.is_connected:
                self.game_context.network_manager.send_package("variable", "water_pump", "pipe_fixed", True)
        else :
            self.water_pump_reference.pipe_fixed = False
            if self.game_context.network_manager.is_connected:
                self.game_context.network_manager.send_package("variable", "water_pump", "pipe_fixed", False)

    #def handle_click(self, event):
    #    if self.rect.colliderect(self.collisions[1]):
    #        print(f"{self.rect.colliderect(self.collisions[1])}")
    #        if self.stool_reference.placed[4] and self.rect.colliderect(self.collisions[1]):
    #            self.game_context.drop_current_object(event, [self.collisions[1]])
    #        else :
    #            #self.drop_in_collision_rect(0) #il veut pas arreter de suivre la souris
    #            self.game_context.drop_current_object(event, [self.collisions[0]])
    #    else:
    #        self.game_context.drop_current_object(event)