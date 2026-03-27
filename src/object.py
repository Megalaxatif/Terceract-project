from pathlib import Path

import pygame
from utils import convert_to_pygame_rect_list, get_collision_rects, load_json_file


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
        self.default_collision = default_collision
        self.raw_default_collision = None
        self.default_wall = default_wall
        if self.default_collision:
            self.collision_rects.insert(0,self.default_collision)
            self.raw_default_collision = self.default_collision.copy()
        self.raw_collision_rects = self.collision_rects.copy()
        self.collision_rect_id = collision_index  # which collision rect the object is in

        self.rect = rect
        self.raw_rect = self.rect
        if self.collision_rect_id != -1:
            self.valid_rect = self.collision_rects[self.collision_rect_id]
        else:
            self.valid_rect = self.rect.copy()
        self.displayed = displayed
        self.movable = movable
        #TODO: this is not clean to put something exclusively related to closet in the parent class
        self.display_collision_rect_bool = not ("obj_in_closet" in self.name) # TODO why this name ?
        self.last_inventory_pos = -1, -1

        self.in_grid = False # TODO: don't put this in the parent class wtf


    def replace(self):
        self.raw_rect.center = self.valid_rect.center


    def drop_in_collision_rect(self, collision_index):
        self.raw_rect.center = self.raw_collision_rects[collision_index].center
        self.valid_rect = self.raw_collision_rects[collision_index]
        self.collision_rect_id = collision_index
        # print(f"Dropped {self.name} in collision rect {collision_index}")

    # try to fit the object in one of the collision rects, returns True if it fits, False otherwise
    def drop_at_pos(self, x, y) -> bool:
        # print(f"Trying to drop {self.name} at ({x}, {y})")
        return_code = False
        point_rect = pygame.Rect(int(x), int(y), 1, 1)
        collision_index = point_rect.collidelist(self.collision_rects)
        if self.display_collision_rect_bool:
            if collision_index != -1:
                self.drop_in_collision_rect(collision_index)
                return_code = True
            elif self.game_context.inventory.current_object:
                return False
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
        delta = self.game_context.current_wall.delta
        ll = len(self.collision_rects)
        for i in range(ll):
            raw_collision_rect = self.raw_collision_rects[i]
            new_x = int(delta * raw_collision_rect.x)
            new_y = int(delta * raw_collision_rect.y)
            new_w = int(delta * raw_collision_rect.w)
            new_h = int(delta * raw_collision_rect.h)

            collision_rect = self.collision_rects[i]

            if (
                (new_x != collision_rect.x)
                or (new_y != collision_rect.y)
                or (new_w != collision_rect.w)
                or (new_h != collision_rect.h)
            ):
                self.collision_rects[i] = pygame.Rect(new_x, new_y, new_w, new_h)


    def change_collision_rects(self, json_collision_path, wall_id_str):
        #new_collision_rects = get_collision_rects(..., self.name)
        collisions_data = load_json_file(json_collision_path) # load the json file containing all the collision rects for all the objects on the wall
        new_collision_rects = []
        for obj in collisions_data:
            if obj == self.name:
                for rect in collisions_data[obj]:
                    new_collision_rects.append(rect)

        if self.default_wall == wall_id_str:
            if self.default_collision:
                new_collision_rects.append(self.default_collision)

        converted_collision_rects = convert_to_pygame_rect_list(new_collision_rects)
        self.collision_rects = converted_collision_rects
        self.raw_collision_rects = converted_collision_rects.copy()


    def display_collision_rect(self):
        if self.display_collision_rect_bool:
            for rect in self.collision_rects:
                temp_surface = pygame.Surface(
                    (rect.width, rect.height), pygame.SRCALPHA
                )
                pygame.draw.rect(
                    temp_surface, (255, 0, 0, 128), temp_surface.get_rect()
                )
                self.game_context.screen.blit(temp_surface, rect)


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
