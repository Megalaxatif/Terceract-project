import pygame
from object import Game_object

class Scotch(Game_object):
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
        )                                #network FAIT hihihihi

        self.displayed = False
        self.stool_reference = []
        self.collisions = collisions #pas de pb, ca marche :D (mais pas pu vérifier avec leak derriere stash)

    def initialize(self):
        self.stool_reference = self.game_context.get_reference("stool")
        self.leak_reference = self.game_context.get_reference_large("leak") 
        if self.leak_reference == []:
            print(f"initialize of object named \"{self.name}\" error: no object with \"leak\" in its name found in the game, exiting")
            self.game_context.quit()

    def update(self, event):

        if self.game_context.current_room_id == 3 and self.game_context.current_wall_id == 1 and not self.displayed and event.type == pygame.MOUSEBUTTONDOWN and (self.collisions[0].collidepoint(event.pos) or self.collisions[1].collidepoint(event.pos)):
            self.displayed = True

    def handle_click_selection(self, event):
        pass

    def handle_click(self, event):
        if self.game_context.current_wall.room_id == 3: 
            for i in range(len(self.leak_reference)):
                obj = self.leak_reference[i]
                if obj.displayed and obj.rect.collidepoint(event.pos) and self.stool_reference.placed[i]: #normalement match
                    obj.displayed = False
                    #print(f"{i}")
                    if self.game_context.network_manager.is_connected:
                        if i == 0 : 
                            self.game_context.network_manager.send_package("variable", "leak1", "displayed", False)
                        if i == 1 : 
                            self.game_context.network_manager.send_package("variable", "leak3", "displayed", False)
                        if i == 2 : 
                            self.game_context.network_manager.send_package("variable", "leak4", "displayed", False)
                        if i == 3 : 
                            self.game_context.network_manager.send_package("variable", "leak2", "displayed", False)
                    if not any([v.displayed for v in self.leak_reference]):
                        for obj in self.game_context.rooms[self.game_context.current_room_id].objects:
                            if obj.name == "water_pump":
                                obj.leaking = False
                                if self.game_context.network_manager.is_connected:
                                    self.game_context.network_manager.send_package("variable", "water_pump", "leaking", False)
                    return True

        self.game_context.drop_current_object(event)
        return False