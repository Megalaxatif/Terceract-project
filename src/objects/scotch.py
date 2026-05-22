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
                                        #lien avec pump fait

        self.displayed = False
        self.stool_reference = []
        self.collisions = collisions #pas de pb, ca marche :D

    def initialize(self):
        self.stool_reference = self.game_context.get_reference("stool", asker="scotch")
        self.leak_reference = self.game_context.get_reference_large("leak")
        if self.leak_reference == []:
            print(f"initialize of object named \"{self.name}\" error: no object with \"leak\" in its name found in the game, exiting")
            self.game_context.quit()

    def update(self, event):

        if self.game_context.current_room_id == 3 and self.game_context.current_wall_id == 1 and not self.displayed and event.type == pygame.MOUSEBUTTONDOWN and (self.collisions[0].collidepoint(event.pos) or self.collisions[1].collidepoint(event.pos)):
            self.displayed = True
            if self.game_context.network_manager.is_connected:
                self.game_context.network_manager.send_package("variable", "scotch", "displayed", True)
            self.game_context.dialogues.start_dialogue(12)

    def handle_click_selection(self, event):
        pass

    def handle_click(self, event):
        if self.game_context.current_wall.room_id == 3:
            for obj in self.leak_reference:
                if not obj.displayed and obj.rect.collidepoint(event.pos) and (not obj.name == "leak2" or self.game_context.stool_placed):
                    obj.displayed = True
                    #print("caché")
                    #print(f"{i}")
                    if self.game_context.network_manager.is_connected:
                        if obj.name == "leak1":
                            self.game_context.network_manager.send_package("variable", "leak1", "displayed", True)
                        if obj.name == "leak3":
                            self.game_context.network_manager.send_package("variable", "leak3", "displayed", True)
                        if obj.name == "leak4":
                            self.game_context.network_manager.send_package("variable", "leak4", "displayed", True)
                        if obj.name == "leak2":
                            self.game_context.network_manager.send_package("variable", "leak2", "displayed", True)
                    if not any([not v.displayed for v in self.leak_reference]):
                        for obj in self.game_context.back_wall_R4.objects:
                            if obj.name == "water_pump":
                                obj.leaking = False
                                if self.game_context.network_manager.is_connected:
                                    self.game_context.network_manager.send_package("variable", "water_pump", "leaking", False)
                    return True
                elif not obj.displayed and obj.rect.collidepoint(event.pos) and not self.game_context.stool_placed:
                    self.game_context.dialogues.start_dialogue(13)
                    return True

        self.game_context.drop_current_object(event)
        return False