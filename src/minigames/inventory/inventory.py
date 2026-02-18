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
                    # convert the rectangle from pygame.Rect to tuple to store them in the json
                    formated_rect = tuple(obj.raw_rect)

                    formated_collision_rects = []
                    for rect in obj.raw_collision_rects:
                        formated_collision_rects.append(tuple(rect))

                    objects_list["data"][i].append(
                        {
                            "name" : obj.name,
                            "image" : obj.image_path.as_posix(),
                            "rect" : formated_rect,
                            "collisions" : formated_collision_rects,
                            "collision_id" : obj.collision_rect_index
                        }
                    )

        save_data_in_json(objects_list, self.json_path)


    def init_images(self):
        objects_data = load_json_file(self.json_path)
        for key in objects_data:
            if key == "data":
                for i in range(len(objects_data["data"])):
                    for j in range(len(objects_data["data"][i])):
                        sprite_dict = objects_data["data"][i][j]
                        if sprite_dict:
                            name = sprite_dict["name"]
                            image = sprite_dict["image"]
                            rect = sprite_dict["rect"]
                            collisions = sprite_dict["collisions"]
                            collision_id = sprite_dict["collision_id"]

                            #convert in pygame Rect
                            rect = pygame.Rect(rect)

                            for k in range(len(collisions)):
                                collisions[k] = pygame.Rect(collisions[k])

                            object = create_object(name, self.game_context, image, rect, collisions, collision_id)
                            self.slots[i][j] = object


    def resize_objects(self):
        for i in range(len(self.slots)):
            for obj in self.slots[i]:
                if obj is not None:
                    obj.resize_image()
                    obj.resize_collision_rects()


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


    def handle_event(self, event):
        self.mouse_x, self.mouse_y = event.pos

        if (
            self.x <= self.mouse_x < self.x + self.cols * self.block_size and
            self.y <= self.mouse_y < self.y + self.rows * self.block_size
        ):
            self.col = (self.mouse_x - self.x) // self.block_size
            self.row = (self.mouse_y - self.y) // self.block_size

            if self.game_context.current_item is not None:
                self.put_in_inventory(self.row, self.col)
            else:
                self.current_item, self.slots[self.row][self.col] = self.slots[self.row][self.col], self.current_item

        elif self.current_item is not None:
            self.put_out_inventory(self.row, self.col)


    def put_in_inventory(self, row, col):
        # put objet from wall to inventory
        obj = self.game_context.current_item
        # if there is an object in the slot, it becomes the current item
        self.current_item = self.slots[row][col] #TODO: what ??
        self.slots[row][col] = obj
        if obj in self.game_context.current_wall.objects:
            self.game_context.current_wall.objects.remove(obj)
        print("Put in inventory")
        self.game_context.current_item = None
        self.current_item = None #TODO: what ??


    def put_out_inventory(self, row, col):
        obj = self.current_item
        # Mettre à jour la position de l'objet à la position actuelle de la souris
        mx, my = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
        if obj.drop(mx, my):
            self.slots[row][col] = None
            self.game_context.current_wall.objects.add(obj)
            self.game_context.current_item = None
            self.current_item = None
            print("Put out inventory")

    def resize_in_inventory(self, path):
        return pygame.transform.scale(
            pygame.image.load(path),
            (int(self.block_size * 0.9), int(self.block_size * 0.9))
        )

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

    def update_object_collision_rects(self):
        for i in range(len(self.slots)):
            for obj in self.slots[i]:
                if obj is not None:

                    current_wall_collision_dir = self.game_context.current_wall.collision_layers_dir
                    new_collision_rects = self.game_context.current_wall.get_collision_rects(current_wall_collision_dir, obj.name)

                    # convert the tupple returned by get_collision_rects into pygame.Rect
                    formated_collision_rects = []
                    for rect in new_collision_rects:
                        formated_collision_rects.append(pygame.Rect(rect))

                    obj.collision_rects = formated_collision_rects


    def display_collision_rects(self):
        for i in range(len(self.slots)):
            for obj in self.slots[i]:
                if obj is not None:
                    obj.display_collision_rect()

