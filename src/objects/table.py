import pygame
from object import Game_object


class Table(Game_object):
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
        movable: bool = True,
        displayed: bool = True,
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
        self.interactible = "table" == self.name
        self.displayed = displayed
        self.open = not self.displayed
        self.background = "gray_bg" in self.name
        self.gone = False

    def initialize(self):
        self.list_reference = self.game_context.get_reference_large("obj_in_table")  # useful to change the visibility
        if self.list_reference == []:
            print(f'initialize of object named "{self.name}" error: no object with "obj_in_table" in its name found in the game, exiting')
            self.game_context.quit()

        self.opened_table_reference = self.game_context.get_reference("opened_table")  # useful to change the visibility

        self.bg_reference = self.game_context.get_reference("gray_bg_table")  # useful to change the visibility

        self.list_reference.append(self.bg_reference)


    def handle_click_selection(self, event):
        inv = self.game_context.inventory

        if not self.open or self.background:
            self.opened_table_reference.displayed = (
                not self.opened_table_reference.displayed
            )
            for obj in self.list_reference:
                print(obj.name)
                obj.displayed = not obj.displayed
                obj.display_collision_rect_bool = self.displayed

        for i in range(inv.rows):
            for j in range(inv.cols):
                if inv.slots[i][j]:
                    if "obj_in_table" in inv.slots[i][j].name:
                        inv.slots[i][j].displayed = self.displayed
                        inv.slots[i][j].display_collision_rect_bool = self.displayed

        self.game_context.drop_current_object(event)
