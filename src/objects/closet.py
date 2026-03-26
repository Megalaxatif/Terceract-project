import pygame
from object import Game_object


class Closet(Game_object):
    def __init__(
        self,
        game_context,
        object_name,
        image_path: str,
        rect: pygame.Rect,
        collisions: list[pygame.Rect],
        collision_index: int,
        displayed,
    ):
        super().__init__(
            game_context, object_name, image_path, rect, collisions, collision_index
        )
        self.movable = False
        self.interactible = True
        self.displayed = displayed
        self.open = not self.displayed

    def initialize(self):
        self.list_reference = self.game_context.get_reference_large("obj_in_closet") # useful to change the visibility
        if self.list_reference == []:
            print(f"initialize of object named \"{self.name}\" error: no object with \"obj_in_closet\" in its name found in the game, exiting")
            self.game_context.quit()

    def handle_click_selection(self, event):
        wall = self.game_context.current_wall.objects
        inv = self.game_context.inventory
        
        for obj in wall:
            if isinstance(obj, Closet) and obj.open:
                obj.displayed = not obj.displayed
                for obj2 in self.list_reference:
                    obj2.displayed = self.displayed
                    obj2.display_collision_rect_bool = self.displayed
        
        for i in range(inv.rows):
            for j in range(inv.cols):
                if inv.slots[i][j]:
                    if "obj_in_closet" in inv.slots[i][j].name:
                        inv.slots[i][j].displayed = self.displayed
                        inv.slots[i][j].display_collision_rect_bool = self.displayed
        self.game_context.drop_current_object(event)
