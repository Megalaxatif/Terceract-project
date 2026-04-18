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
        )                                #todo network

        self.original_displayed = False
        self.stool_reference = []
        self.collisions = collisions #problemes : scotch pas caché au début

    def initialize(self):
        self.stool_reference = self.game_context.get_reference("stool")
        self.leak_reference = self.game_context.get_reference_large("leak") # useful to change the visibility
        if self.leak_reference == []:
            print(f"initialize of object named \"{self.name}\" error: no object with \"leak\" in its name found in the game, exiting")
            self.game_context.quit()

    def update(self, event):
        #if self.leak_reference[0].rect.collidepoint(pygame.mouse.get_pos()) :
        #    print(f"0") #back wall
        #if self.leak_reference[1].rect.collidepoint(pygame.mouse.get_pos()) :
        #    print(f"1") #coté
        #if self.leak_reference[2].rect.collidepoint(pygame.mouse.get_pos()) :
        #    print(f"2") #coté
        #if self.leak_reference[3].rect.collidepoint(pygame.mouse.get_pos()) :
        #    print(f"3") #front

        if self.game_context.current_room_id == 3 and self.game_context.current_wall_id == 1 and not self.displayed and event.type == pygame.MOUSEBUTTONDOWN and self.collisions[0].collidepoint(event.pos) :
            self.displayed = True

    def handle_click_selection(self, event):
        pass

    def handle_click(self, event):
        if self.game_context.current_wall.room_id == 3: 
            for i in range(len(self.leak_reference)):
                obj = self.leak_reference[i]
                if obj.displayed and obj.rect.collidepoint(event.pos) and self.stool_reference.placed[i]: #normalement match
                    obj.displayed = False
                    if not any([v.displayed for v in self.leak_reference]):
                        for obj in self.game_context.rooms[self.game_context.current_room_id].objects:
                            if obj.name == "water_pump":
                                obj.disabled = False
                    return True

        self.game_context.drop_current_object(event)
        return False