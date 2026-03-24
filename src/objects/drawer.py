import pygame
from object import Game_object


class Drawer(Game_object):
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
        self.background = "gray_bg" in self.name
        self.gone = False

    def update(self, event):
        pass

    def handle_left_click(self, event):
        wall = self.game_context.current_wall.objects
        inv = self.game_context.inventory
        if "trigger" in self.name:
            for obj in wall:
                if isinstance(obj, Drawer) and obj.open and "withFB" in obj.name:
                    obj.displayed = not obj.displayed
                    obj.display_collision_rect_bool = obj.displayed
                    obj.gone = True
            return
        elif not self.open or self.background:
            for obj in wall:
                if isinstance(obj, Drawer) and obj.open and not obj.gone:
                    obj.displayed = not obj.displayed
                    obj.display_collision_rect_bool = self.displayed
            for obj2 in wall:
                if "obj_in_drawer" in obj2.name:
                    obj2.displayed = self.displayed
                    obj2.display_collision_rect_bool = self.displayed
        for i in range(inv.rows):
            for j in range(inv.cols):
                if inv.slots[i][j]:
                    if "obj_in_drawer" in inv.slots[i][j].name:
                        inv.slots[i][j].displayed = self.displayed
                        inv.slots[i][j].display_collision_rect_bool = self.displayed
        self.game_context.drop_current_object(event)
