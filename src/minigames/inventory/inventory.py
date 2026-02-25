import pygame
from pathlib import Path
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

        self.slots : list[list[Game_object]] | list = [[None for _ in range(cols)] for _ in range(rows)]
        self.slots_entities = [[None for _ in range(cols)] for _ in range(rows)] # what ??

        self.center = center

        self.last_row, self.last_col = 0, 0
        self.mouse_x, self.mouse_y = 0, 0

        # load images
        self.current_item = None

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

                    objects_list["data"][i].append(
                        {
                            "name" : obj.name,
                            "image" : obj.image_path.as_posix(),
                            "rect" : converted_rect
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
                            converted_rect = convert_to_pygame_rect(rect)

                            collision_rects = get_collision_rects(collision_layers_dir, name)
                            converted_collision_rects = convert_to_pygame_rect_list(collision_rects)
                            object = create_object(name, self.game_context, image, converted_rect, converted_collision_rects, -1)
                            self.slots[i][j] = object


    def resize_objects(self):
        for i in range(len(self.slots)):
            for obj in self.slots[i]:
                if obj is not None:
                    obj.resize_image()
                    obj.resize_collision_rects()


    def update_object_collision_rects(self):
        collision_layers_dir = self.game_context.current_wall.collision_layers_dir
        for i in range(len(self.slots)):
            for obj in self.slots[i]:
                if obj is not None:
                    obj.change_collision_rects(collision_layers_dir)


    def display(self):
        self.block_size = int(self.raw_block_size * self.game_context.delta)

        if self.center:
            mid_block = len(self.slots_entities[0]) // 2 + len(self.slots_entities[0]) % 2
            self.x = self.game_context.screen.get_width() // 2 - mid_block * self.block_size
        else:
            self.x = int(self.raw_x * self.game_context.delta)

        self.y = int(self.raw_y * self.game_context.delta)

        self.resize_objects()
        self.display_collision_rects()
        self.draw_grid()
        self.draw_items()
        self.draw_current_item()


    def handle_left_click(self, event):
        self.mouse_x, self.mouse_y = event.pos

        if (
            self.x <= self.mouse_x < self.x + self.cols * self.block_size and
            self.y <= self.mouse_y < self.y + self.rows * self.block_size
        ):
            self.col = (self.mouse_x - self.x) // self.block_size
            self.row = (self.mouse_y - self.y) // self.block_size

            if self.game_context.current_item is not None:
                self.store_current_item(self.row, self.col)
            else:
                self.current_item, self.slots[self.row][self.col] = self.slots[self.row][self.col], self.current_item

        elif self.current_item is not None:
            self.drop_current_item(self.row, self.col)


    def store_current_item(self, row, col):
        obj = self.game_context.current_item
        if self.slots[row][col] is None:

            self.slots[row][col] = obj
            self.game_context.current_wall.objects.remove(obj)
            if self.game_context.network_manager.is_connected:
                #send the information to the other player
                self.game_context.network_manager.send_package(
                    "function",
                    "inventory",
                    "inventory_store_item",
                    row,
                    col,
                    obj.name,
                    self.game_context.current_room_id,
                    self.game_context.current_wall_id
                )
            self.game_context.current_item = None
            self.current_item = None #TODO: what ??


    def drop_current_item(self, row, col):
        obj = self.current_item
        if obj is None:
            print("drop_current_item error: current_item is None")
            return -1
        # Mettre à jour la position de l'objet à la position actuelle de la souris
        mx, my = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
        if obj.drop_at_pos(mx, my):

            if self.game_context.network_manager.is_connected:
                #send the information to the other player
                self.game_context.network_manager.send_package(
                    "function",
                    "inventory",
                    "inventory_drop_item",
                    obj.name,
                    self.game_context.current_room_id,
                    self.game_context.current_wall_id,
                    obj.collision_rect_id
                )

            self.slots[row][col] = None
            self.game_context.current_wall.objects.add(obj)
            self.game_context.current_item = None
            self.current_item = None

#-------------------------NETWORK-------------------------------------

    # function useful for network
    def inventory_store_item(self, row, col, obj_name, room_id, wall_id):
        src_wall = self.game_context.room_list[room_id][wall_id]                            # find the wall we want to take the object from
        object = None
        for obj in src_wall.objects:                                                        # find the object we are talking about
            if obj.name == obj_name:
                object = obj
        if object is None:
            print(f"inventory_store_item error: invalid object name, the name {obj_name} was not found in room {room_id} wall {wall_id}")
            return 1

        if self.slots[row][col] is not None: # find a new column on the row to store the object if there was already an object in the slot
            full = True
            for i in range(self.cols):
                if self.slots[row][i] is None:
                    full = False
                    col = i
                    break
            if full:
                print(f"inventory_store_item error: impossible to store the item {obj_name} because the inventory is full") # this case should never happen
                return 2

        self.slots[row][col] = object                                                       # put the object in inventory
        object.change_collision_rects(self.game_context.current_wall.collision_layers_dir)  # change its collision rects
        src_wall.objects.remove(object)                                                     # remove the object from the wall


    # function useful for network
    def inventory_drop_item(self, obj_name, room_id, wall_id, collision_rect_id):
        obj = None
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
            print(f"inventory_drop_item error: impossible to find the object {obj_name} in the inventory")
            return -1

        dest_wall = self.game_context.room_list[room_id][wall_id]                   # on which wall do we want to put it
        dest_wall.objects.add(obj)                                                  # add the object on the wall
        obj.change_collision_rects(dest_wall.collision_layers_dir)                  # update its collision rects
        obj.drop_in_collision_rect(collision_rect_id)                               # put it in the right collision rect
        self.slots[row][col] = None                                                 # remove it from inventory

#-------------------------------------------------------------------

    def draw_grid(self):
        for row in range(self.rows):
            for col in range(self.cols):
                rect = pygame.Rect(
                    self.x + col * self.block_size,
                    self.y + row * self.block_size,
                    self.block_size,
                    self.block_size
                )
                pygame.draw.rect(self.game_context.screen, WHITE, rect, 2)


    def draw_items(self):
        for row in range(self.rows):
            for col in range(self.cols):
                item = self.slots[row][col]
                if item and item != self.current_item:
                    # Redimensionner le sprite du sprite
                    scaled_image = pygame.transform.scale(
                        item.image,
                        (int(self.block_size * 0.9), int(self.block_size * 0.9))
                    )
                    self.game_context.screen.blit(
                        scaled_image,
                        (
                            self.x + col * self.block_size + 0.05 * self.block_size,
                            self.y + row * self.block_size + 0.05 * self.block_size
                        )
                    )


    def draw_current_item(self):
        if self.current_item:  # if not None
            mx, my = pygame.mouse.get_pos()
            scaled_image = pygame.transform.scale(
                self.current_item.image,
                (int(self.block_size * 0.9), int(self.block_size * 0.9))
            )
            self.game_context.screen.blit(
                scaled_image,
                (mx - 0.4 * self.block_size, my - 0.4 * self.block_size)
            )


    def display_collision_rects(self):
        for i in range(len(self.slots)):
            for obj in self.slots[i]:
                if obj is not None:
                    obj.display_collision_rect()

