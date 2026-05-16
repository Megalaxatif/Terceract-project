from pathlib import Path

import pygame
from pygame.locals import MOUSEBUTTONDOWN
from utils import *


class Game_object(pygame.sprite.Sprite):
    def __init__(
        self,
        game_context,
        object_name: str,
        image_path: str,
        rect: pygame.Rect,
        collisions: list[pygame.Rect],
        default_collision: pygame.Rect,
        default_wall: str,
        collision_index: int = -1,
        movable: bool = True,
        displayed: bool = True,
    ):
        super().__init__()

        self.name = object_name
        self.game_context = game_context
        self.screen = self.game_context.screen

        self.image_path = Path(image_path)
        self.image = pygame.image.load(Path(self.game_context.root_dir / self.image_path)).convert_alpha()
        self.raw_image = self.image

        parts = self.image_path.parts
        self.image_id = (Path(*parts[-7:])).as_posix()
        self.image_name = str(self.image_path.name)

        self.collision_rects = collisions
        self.raw_collision_rects = self.collision_rects.copy()
        self.default_collision = default_collision
        self.raw_default_collision = self.default_collision.copy()
        self.collision_rect_id = collision_index
        self.default_wall = default_wall
        self.rect = rect
        self.raw_rect = self.rect
        if self.collision_rect_id != -1:
            self.valid_rect = self.collision_rects[self.collision_rect_id]
        else:
            self.valid_rect = self.rect.copy()
        self.original_displayed = displayed
        self.displayed = displayed
        self.movable = movable
        self.interactible = movable
        # TODO: this is not clean to put something exclusively related to closet in the parent class
        self.display_collision_rect_bool = not ("obj_in_closet" in self.name)  # TODO why this name ?
        self.last_inventory_pos = -1, -1

    def replace(self):
        self.raw_rect.center = self.valid_rect.center

    def drop_in_collision_rect(self, collision_index):
        if self.raw_collision_rects is None or collision_index < 0 or collision_index >= len(self.raw_collision_rects):
            print(f"drop_in_collision_rect error, impossible to drop the object {self.name} at collision_index {collision_index}")
            return -1
        self.raw_rect.center = self.raw_collision_rects[collision_index].center
        self.valid_rect = self.raw_collision_rects[collision_index]
        self.collision_rect_id = collision_index


    # try to fit the object in one of the collision rects, returns True if it fits, False otherwise
    def drop_at_pos(self, x, y, collisions = None, force=False) -> bool:
        #NOTE: the force argument means that the function will try to drop
        # the object regardless if display_collision_rect_bool is True or not
        if collisions is None:
            collisions = self.collision_rects
        return_code = False
        point_rect = pygame.Rect(int(x), int(y), 1, 1)

        if not collisions:
            collision_index = -1
        else:
            collision_index = point_rect.collidelist(collisions)

        if self.display_collision_rect_bool or force:
            if collision_index != -1:
                self.drop_in_collision_rect(collision_index)
                return_code = True
            elif self.game_context.inventory.current_object:
                return_code = False
            else:
                self.replace()
        return return_code

    def resize_image(self):
        delta = self.game_context.current_wall.delta
        new_x = int(delta * self.raw_rect.x)
        new_y = int(delta * self.raw_rect.y)
        new_width = int(delta * self.raw_rect.w)
        new_height = int(delta * self.raw_rect.h)
        if (
            (new_width != self.rect.w)
            or (new_height != self.rect.h)
            or (new_x != self.rect.x)
            or (new_y != self.rect.y)
        ):
            self.image = pygame.transform.scale(self.raw_image, (new_width, new_height))
            self.rect = pygame.Rect(new_x, new_y, new_width, new_height)


    def resize_collision_rects(self):
        resize_rects(self.collision_rects, self.raw_collision_rects, self.game_context.current_wall.delta)


    def change_collision_rects(self, json_collisions_path, wall_id_str):
        collisions_data = load_json_file(json_collisions_path) # load the json file containing all the collision rects for all the objects on the wall
        new_collision_rects = []
        for obj in collisions_data:
            if obj == self.name:
                for rect in collisions_data[obj]:
                    new_collision_rects.append(rect)

        if self.default_wall == wall_id_str:
            new_collision_rects.insert(0,self.default_collision)


        converted_collision_rects = convert_to_pygame_rect_list(new_collision_rects)
        self.collision_rects = converted_collision_rects
        if converted_collision_rects is not None:
            self.raw_collision_rects = converted_collision_rects.copy()
        else:
            self.raw_collision_rects = None

    def display_collision_rect(self):
        if self.display_collision_rect_bool:
            display_debug_rects(self.collision_rects, self.game_context.screen)

    def stash(self):
        if self.default_collision is None:
            print(f"stash error: the object {self.name} has it's default_collision argument set to None. Unable to find the default collision")
            return
        save_wall = self.game_context.current_wall
        save_room_id = self.game_context.current_room_id
        save_wall_id = self.game_context.current_wall_id

        self.game_context.current_wall = self.game_context.room_list[int(self.default_wall[0])-1][int(self.default_wall[1])-1]
        self.game_context.current_room_id = int(self.default_wall[0])-1
        self.game_context.current_wall_id = int(self.default_wall[1])-1


        custom_event = pygame.event.Event(
                MOUSEBUTTONDOWN,
                {
                    "pos": (self.default_collision[0], self.default_collision[1]),
                    "button": 1
                },
        )
        self.change_collision_rects(self.game_context.current_wall.json_collisions_path, self.default_wall)
        self.game_context.inventory.drop_current_object(custom_event, force=True)
        self.game_context.current_wall = save_wall
        self.game_context.current_room_id = save_room_id
        self.game_context.current_wall_id = save_wall_id

    def draw(self):
        self.game_context.screen.blit(self.image, self.rect)

    def initialize(self):
        pass

    def update(self, event):
        pass

    def handle_click_selection(self, event):
        pass

    def handle_click(self, event):
        if self != self.game_context.inventory.current_object:
            self.game_context.drop_current_object(event)
            return True
        return False

    def swap_display(self):
        pass
