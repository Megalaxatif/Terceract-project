from pathlib import Path

import pygame
from object import Game_object
from utils import *

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)


class Inventory:
    def __init__(self, game_context, x, y, rows, cols, block_size, center):
        self.game_context = game_context
        self.root_dir = Path(__file__).resolve().parent
        self.json_path = Path(self.root_dir / "objects_info.json")

        self.raw_x = x
        self.x = int(self.raw_x * self.game_context.delta)
        self.raw_y = y
        self.y = int(self.raw_y * self.game_context.delta)

        self.rows = rows
        self.cols = cols

        self.raw_block_size = block_size
        self.block_size = int(self.raw_block_size * self.game_context.delta)

        self.slots: list[list[Game_object]] | list = [
            [None for _ in range(cols)] for _ in range(rows)
        ]
        self.slots_entities = [
            [None for _ in range(cols)] for _ in range(rows)
        ]  # what ??

        self.center = center

        self.last_row, self.last_col = 0, 0
        self.mouse_x, self.mouse_y = 0, 0

        # load images
        self.current_object = None
        self.displayed = True

        self.init_images()

    def save_images(self):
        objects_list = {"data": [[]]}
        for i in range(len(self.slots)):
            objects_list["data"].append([])
            for obj in self.slots[i]:
                if not obj:
                    objects_list["data"][i].append(None)
                else:
                    converted_rect = convert_to_tuple_rect(obj.raw_rect)
                    converted_default_collision = None
                    if obj.default_collision:
                        converted_default_collision = convert_to_tuple_rect(
                            obj.default_collision
                        )

                    objects_list["data"][i].append(
                        {
                            "name": obj.name,
                            "image": obj.image_path.as_posix(),
                            "rect": converted_rect,
                            "default_collision": converted_default_collision,
                            "default_wall_id": obj.default_wall,
                        }
                    )
        save_data_in_json(objects_list, self.json_path)

    def init_images(self):
        objects_data = {}
        if self.game_context.network_manager.is_host:
            objects_data = load_json_file(self.json_path)
        else:
            objects_data = self.game_context.game_data["inv_data"]

        collision_layers_dir = self.game_context.current_wall.collision_layers_dir
        for key in objects_data:
            if key == "data":
                for i in range(len(objects_data["data"])):
                    for j in range(len(objects_data["data"][i])):
                        sprite_dict = objects_data["data"][i][j]
                        if sprite_dict:
                            name = sprite_dict["name"]
                            image = sprite_dict["image"]
                            rect = sprite_dict["rect"]
                            default_collision = sprite_dict["default_collision"]
                            default_wall = sprite_dict["default_wall_id"]

                            converted_rect = convert_to_pygame_rect(rect)
                            converted_default_collision = None
                            if default_collision:
                                converted_default_collision = convert_to_pygame_rect(default_collision)
                            collision_rects = get_collision_rects(collision_layers_dir, name)
                            converted_collision_rects = convert_to_pygame_rect_list(collision_rects)
                            object = create_object(
                                name,
                                self.game_context,
                                image,
                                converted_rect,
                                converted_collision_rects,
                                -1,
                                converted_default_collision,
                                default_wall,
                            )

                            self.slots[i][j] = object
        self.update_object_collision_rects()

    def resize_objects(self):
        for i in range(len(self.slots)):
            for obj in self.slots[i]:
                if obj is not None:
                    obj.resize_image()
                    obj.resize_collision_rects()


    def update_object_collision_rects(self):
        json_collisions_path = self.game_context.current_wall.json_collisions_path
        wall_id_str = self.game_context.current_wall.wall_id_str
        for i in range(len(self.slots)):
            for obj in self.slots[i]:
                if obj:
                    obj.change_collision_rects(json_collisions_path, wall_id_str)


    def display(self):
        if (
            not self.game_context.other_player_inventory_object_name
        ):  # TODO make an update() method
            self.game_context.other_player_inventory_object = None

        if self.displayed:
            self.block_size = int(self.raw_block_size * self.game_context.delta)

            if self.center:
                mid_block = (
                    len(self.slots_entities[0]) // 2 + len(self.slots_entities[0]) % 2
                )
                self.x = (
                    self.game_context.screen.get_width() // 2
                    - mid_block * self.block_size
                )
            else:
                self.x = int(self.raw_x * self.game_context.delta)

            self.y = int(self.raw_y * self.game_context.delta)

            self.resize_objects()
            self.draw_grid()
            self.draw_objects()
        if self.game_context.other_player_inventory_object:
            self.draw_other_player_current_object()
        if self.current_object:
            self.draw_current_object()
            # self.display_collision_rects()

    def handle_click(self, event):
        if self.displayed:
            self.mouse_x, self.mouse_y = event.pos

            if (
                self.x <= self.mouse_x < self.x + self.cols * self.block_size
                and self.y <= self.mouse_y < self.y + self.rows * self.block_size
            ):
                col = (self.mouse_x - self.x) // self.block_size
                row = (self.mouse_y - self.y) // self.block_size

                if self.game_context.other_player_inventory_object:
                    obj = self.game_context.other_player_inventory_object
                    if obj.last_inventory_pos != (row, col):
                        if self.game_context.current_object is not None:
                            self.store_current_object(row, col)
                        else:
                            self.swap_object(row, col)
                        return True
                else:
                    if self.game_context.current_object is not None:
                        self.store_current_object(row, col)
                    else:
                        self.swap_object(row, col)
                    return True
                return True

            elif self.current_object is not None:
                interaction_made = self.current_object.handle_click(event) # True if made
                if not interaction_made:
                    self.drop_current_object(event)
        elif self.current_object is not None:
            self.drop_current_object(event)
        return False

    def store_current_object(self, row, col):
        obj = self.game_context.current_object
        if self.slots[row][col] is None and obj.movable:
            self.slots[row][col] = obj
            self.game_context.current_wall.objects.remove(obj)
            if self.game_context.network_manager.is_connected:
                # send the information to the other player
                self.game_context.network_manager.send_package(
                    "function",
                    "inventory",
                    "inventory_store_object",
                    row,
                    col,
                    obj.name,
                    self.game_context.current_room_id,
                    self.game_context.current_wall_id,
                )
            # TODO: make a function
            self.game_context.current_object = None
            if self.game_context.network_manager.is_connected:
                self.game_context.network_manager.send_package(
                    "variable", "game", "other_player_object_name", ""
                )
            self.current_object = None

    def drop_current_object(self, event):
        obj = self.current_object
        if obj is None:
            print("inventory.drop_current_object error: current_object is None")
            return False
        obj.handle_click_selection(event)
        # Mettre à jour la position de l'objet à la position actuelle de la souris
        mx, my = event.pos[0], event.pos[1]
        return_code = obj.drop_at_pos(mx, my)
        if return_code:
            if self.game_context.network_manager.is_connected:
                # send the information to the other player
                self.game_context.network_manager.send_package(
                    "function",
                    "inventory",
                    "inventory_drop_object",
                    obj.name,
                    self.game_context.current_room_id,
                    self.game_context.current_wall_id,
                    obj.collision_rect_id,
                )
            self.game_context.current_wall.objects.add(obj)
            self.current_object = None
            if self.game_context.network_manager.is_connected:
                self.game_context.network_manager.send_package("variable", "game", "other_player_object_name", "")
            self.current_object = None

        else:
            row, col = self.current_object.last_inventory_pos
            if (row == -1) or (col == -1):
                print("drop_current_object (inventory) error: (row == -1) or (col == -1)")
                return False
            self.swap_object(row, col)
        return return_code


    def swap_object(self, row, col):
        obj_name = ""
        if self.current_object is not None:
            obj_name = self.current_object.name

        if self.game_context.network_manager.is_connected:
            self.game_context.network_manager.send_package(
                "function", "inventory", "inventory_swap_object", row, col, obj_name
            )

        if self.slots[row][col]:
            if self.current_object:
                (
                    self.current_object.last_inventory_pos,
                    self.slots[row][col].last_inventory_pos,
                ) = (
                    self.slots[row][col].last_inventory_pos,
                    self.current_object.last_inventory_pos,
                )
            else:
                self.slots[row][col].last_inventory_pos = row, col
        if self.current_object:
            self.current_object.last_inventory_pos = row, col

        self.current_object, self.slots[row][col] = (
            self.slots[row][col],
            self.current_object,
        )

    # -------------------------NETWORK-------------------------------------

    # function useful for network
    def inventory_store_object(self, row, col, obj_name, room_id, wall_id):
        src_wall = self.game_context.room_list[room_id][
            wall_id
        ]  # find the wall we want to take the object from
        object = None
        for obj in src_wall.objects:  # find the object we are talking about
            if obj.name == obj_name:
                object = obj
        if object is None:
            print(
                f"inventory_store_object error: invalid object name, the name {obj_name} was not found in room {room_id} wall {wall_id}"
            )
            return 1

        if (
            self.slots[row][col] is not None
        ):  # find a new column on the row to store the object if there was already an object in the slot
            full = True
            for i in range(self.cols):
                if self.slots[row][i] is None:
                    full = False
                    col = i
                    break
            if full:
                print(
                    f"inventory_store_object error: impossible to store the object {obj_name} because the inventory is full"
                )  # this case should never happen
                return 2

        self.slots[row][col] = object  # put the object in inventory
        dest_wall_id = f"{self.game_context.current_room_id + 1}{self.game_context.current_wall_id + 1}"
        object.change_collision_rects(
            self.game_context.current_wall.json_collisions_path, dest_wall_id
        )  # change its collision rects
        src_wall.objects.remove(object)  # remove the object from the wall

    # function useful for network
    def inventory_drop_object(
        self, obj_name, dest_room_id, dest_wall_id, collision_rect_id
    ):
        obj = self.game_context.other_player_inventory_object
        row = 0
        col = 0
        for i in range(self.rows):
            for j in range(self.cols):
                current_obj = self.slots[i][j]
                if current_obj is not None:
                    if current_obj.name == obj_name:
                        obj = current_obj
                        row = i
                        col = j

        if obj is None:
            print(
                f"inventory_drop_object error: impossible to find the object {obj_name} in the inventory"
            )
            return -1

        dest_wall = self.game_context.room_list[dest_room_id][dest_wall_id]  # on which wall do we want to put it
        dest_wall.objects.add(obj)  # add the object on the wall
        dest_wall_id_str = f"{dest_room_id + 1}{dest_wall_id + 1}"
        obj.change_collision_rects(
            dest_wall.json_collisions_path, dest_wall_id_str
        )  # update its collision rects
        obj.drop_in_collision_rect(
            collision_rect_id
        )  # put it in the right collision rect                                               # remove it from inventory
        self.slots[row][col] = None
        self.game_context.other_player_inventory_object = None

    def inventory_swap_object(self, row, col, obj_name):
        current_obj = self.game_context.other_player_inventory_object

        if self.slots[row][col]:
            if current_obj:
                (
                    current_obj.last_inventory_pos,
                    self.slots[row][col].last_inventory_pos,
                ) = (
                    self.slots[row][col].last_inventory_pos,
                    current_obj.last_inventory_pos,
                )
            else:
                self.slots[row][col].last_inventory_pos = row, col
        if current_obj:
            current_obj.last_inventory_pos = row, col

        current_obj, self.slots[row][col] = self.slots[row][col], current_obj
        self.game_context.other_player_inventory_object = current_obj

        self.game_context.other_player_inventory_object_name = None
        if current_obj:
            self.game_context.other_player_inventory_object_name = (
                self.game_context.other_player_inventory_object.name
            )

    # -------------------------------------------------------------------

    def draw_grid(self):
        for row in range(self.rows):
            for col in range(self.cols):
                rect = pygame.Rect(
                    self.x + col * self.block_size,
                    self.y + row * self.block_size,
                    self.block_size,
                    self.block_size,
                )
                pygame.draw.rect(self.game_context.screen, WHITE, rect, 2)

    def draw_objects(self):
        for row in range(self.rows):
            for col in range(self.cols):
                object = self.slots[row][col]
                if object and object != self.current_object:
                    # Redimensionner le sprite du sprite
                    scaled_image = pygame.transform.scale(
                        object.image,
                        (int(self.block_size * 0.9), int(self.block_size * 0.9)),
                    )
                    self.game_context.screen.blit(
                        scaled_image,
                        (
                            self.x + col * self.block_size + 0.05 * self.block_size,
                            self.y + row * self.block_size + 0.05 * self.block_size,
                        ),
                    )

    def draw_current_object(self):
        if self.current_object:  # if not None
            mx, my = pygame.mouse.get_pos()
            scaled_image = pygame.transform.scale(
                self.current_object.image,
                (int(self.block_size * 0.9), int(self.block_size * 0.9)),
            )
            self.game_context.screen.blit(
                scaled_image, (mx - 0.4 * self.block_size, my - 0.4 * self.block_size)
            )
            if self.game_context.network_manager.is_connected:
                self.game_context.network_manager.send_package(
                    "function",
                    "inventory",
                    "center_object_inventory",
                    self.current_object.name,
                    mx,
                    my,
                )

    def center_object_inventory(self, obj_name, mx, my):
        object = self.game_context.other_player_inventory_object
        if object is None:
            print(
                f"center_object error: invalid object name, the name {obj_name} was not found in the inventory"
            )
            return 1

        object.rect.x = mx * self.game_context.delta
        object.rect.y = my * self.game_context.delta

    def draw_other_player_current_object(self):
        obj = self.game_context.other_player_inventory_object
        pos = obj.rect.x, obj.rect.y

        if obj is None or pos is None:
            return

        mx, my = pos
        scaled_image = pygame.transform.scale(
            obj.image, (int(self.block_size * 0.9), int(self.block_size * 0.9))
        )
        self.game_context.screen.blit(
            scaled_image, (mx - 0.4 * self.block_size, my - 0.4 * self.block_size)
        )

    def display_collision_rects(self):
        for i in range(len(self.slots)):
            for obj in self.slots[i]:
                if obj is not None:
                    obj.display_collision_rect()
