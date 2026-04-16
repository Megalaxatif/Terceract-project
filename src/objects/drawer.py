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
        default_collision: pygame.Rect,
        default_wall: str,
        collision_index: int,
        displayed,
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
            movable=False,
            displayed=displayed,
        )

        self.movable = False
        self.interactible = "trigger" in self.name or "drawer" == self.name
        self.displayed = displayed
        self.open = not self.displayed
        self.background = "gray_bg" in self.name
        self.gone = False


    def initialize(self):
        self.magnet_reference = self.game_context.get_reference("magnet")  # useful to change the visibility
        self.glue_reference = self.game_context.get_reference("obj_in_drawer_glue")  # useful to change the visibility
        self.trigger_reference = self.game_context.get_reference("drawer_up_view_withFB_trigger")  # useful to change the visibility
        self.withFB_list_reference = self.game_context.get_reference_large("withFB")  # useful to change the visibility


    def swap_display(self):
        wall = self.game_context.current_wall.objects
        for obj in wall:
            if isinstance(obj, Drawer) and obj.open and not obj.gone:
                obj.displayed = not obj.displayed
                obj.display_collision_rect_bool = self.displayed

        self.magnet_reference.displayed = self.displayed
        self.magnet_reference.display_collision_rect_bool = self.displayed # will follow the opening and the closing of the drawer automaticaly

        self.glue_reference.displayed = self.displayed
        self.glue_reference.display_collision_rect_bool = self.displayed


    def handle_click_selection(self, event):
        inv = self.game_context.inventory

        if self == self.trigger_reference:
            for obj in self.withFB_list_reference:
                obj.displayed = not obj.displayed
                obj.display_collision_rect_bool = obj.displayed
                obj.gone = True
            return

        elif not self.open or self.background:
            self.swap_display()

        for i in range(inv.rows):
            for j in range(inv.cols):
                if inv.slots[i][j]:
                    if "obj_in_drawer" in inv.slots[i][j].name:
                        inv.slots[i][j].displayed = self.displayed
                        inv.slots[i][j].display_collision_rect_bool = self.displayed

        self.game_context.drop_current_object(event)
