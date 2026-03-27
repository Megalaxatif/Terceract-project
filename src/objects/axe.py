import pygame

from object import Game_object


class Axe(Game_object):
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

    def initialize(self):
        self.hole_reference = self.game_context.get_reference("hole")  # useful to change the visibility
        if self.hole_reference is None:
            print(
                f'initialize of object named "{self.name}" error: no object with name "hole" found in the game, exiting'
            )
            self.game_context.quit()

        self.paper_reference = self.game_context.get_reference("paper")  # useful to change the visibility
        if self.paper_reference is None:
            print(
                f'initialize of object named "{self.name}" error: no object with name "paper" found in the game, exiting'
            )
            self.game_context.quit()

        self.clock_reference = self.game_context.get_reference("clock")  # useful to check if the clock was moved
        if self.clock_reference is None:
            print(
                f'initialize of object named "{self.name}" error: no object with name "clock" found in the game, exiting'
            )
            self.game_context.quit()

    def handle_click(self, event):
        # check if we clicked on the hole and if the clock has been moved from it's original position
        if (
            self.hole_reference.collision_rects[0].collidepoint(event.pos)
            and self.clock_reference.collision_rect_id > 0
        ):
            self.hole_reference.displayed = True
            self.paper_reference.displayed = True

        elif self != self.game_context.inventory.current_object:
            self.game_context.drop_current_object(event)