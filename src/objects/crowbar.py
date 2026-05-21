import pygame
from object import Game_object

class Crowbar(Game_object):
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
            displayed=False,
        )

        self.original_displayed = False

    def initialize(self):
        self.removable_planks_reference = self.game_context.get_reference_large("removable_plank") # useful to change the visibility
        if self.removable_planks_reference == []:
            print(f"initialize of object named \"{self.name}\" error: no object with \"removable_plank\" in its name found in the game, exiting")
            self.game_context.quit()

    def handle_click_selection(self, event):
        pass

    def handle_click(self, event):
        if self.game_context.current_wall.wall_id_str == "13":
            for obj in self.removable_planks_reference:
                if obj.displayed and obj.rect.collidepoint(event.pos):
                    obj.displayed = False
                    if not any([v.displayed for v in self.removable_planks_reference]):
                        self.game_context.unlock_room(self.game_context.current_room_id)
                        self.game_context.dialogues.start_dialogue(21) #door open
                    return True

        self.game_context.drop_current_object(event)
        return False