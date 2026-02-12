# que handle click appele dans game, update = draw

import pygame
import sys
from pathlib import Path
import json
from objects.vase import Vase
from objects.digicode import Digicode
from utils import *

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)


class Inventory:
    def __init__(self, game_context, x, y, rows, cols, block_size, center):
        self.game_context = game_context
        self.root_dir = Path(__file__).resolve().parent
        self.json_path = Path(self.root_dir / "objects_info.json")

        self.entities = pygame.sprite.Group()

        self.raw_x = x
        self.x = int(self.raw_x * self.game_context.delta)
        self.raw_y = y
        self.y = int(self.raw_y * self.game_context.delta)

        self.rows = rows
        self.cols = cols

        self.raw_block_size = block_size
        self.block_size = int(self.raw_block_size * self.game_context.delta)

        self.slots = [[None for _ in range(cols)] for _ in range(rows)]
        self.slots_entities = [[None for _ in range(cols)] for _ in range(rows)]

        self.center = center

        self.last_row, self.last_col = 0, 0
        self.mouse_x, self.mouse_y = 0, 0

        # load images
        self.current_item = None

        self.init_images()


    def save_images(self):
        objects_data = load_json_file(self.json_path)

        objects_list = {"data": []}
        for i in range(len(self.slots)):
            obj = self.slots[i]
            if obj == None:
                objects_list["data"].append(None)
            else:
                objects_list["data"].append({})
                objects_list["data"][i]["image"] = obj.image_path.as_posix()
                objects_list["data"][i]["rect"] = obj.rect
                objects_list["data"][i]["collisions"] = obj.collision_rects
                objects_list["data"][i]["collision_id"] = obj.current_collision_id
        save_data_in_json(objects_list)


    def init_images(self):
        objects_data = load_json_file(self.json_path)
        for obj in objects_data:
            


    def draw(self):
        self.block_size = int(self.raw_block_size * self.game_context.delta)

        if self.center:
            mid_block = len(self.slots_entities[0]) // 2 + len(self.slots_entities[0]) % 2
            self.x = self.game_context.screen.get_width() // 2 - mid_block * self.block_size
        else:
            self.x = int(self.raw_x * self.game_context.delta)

        self.y = int(self.raw_y * self.game_context.delta)

        self.draw_grid()
        self.draw_items()
        self.draw_current_item()


    def handle_click(self, event):
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
        self.current_item = self.slots[row][col]
        self.slots[row][col] = obj
        if obj in self.game_context.current_wall.entities:
            self.game_context.current_wall.entities.remove(obj)
        self.entities.add(obj)
        print("Put in inventory")
        self.game_context.current_item = None
        self.current_item = None

    def put_out_inventory(self, row, col):
        obj = self.current_item
        # Mettre à jour la position de l'objet à la position actuelle de la souris
        mx, my = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
        if obj.drop(mx, my):
            self.slots[row][col] = None
            if obj in self.entities:
                self.entities.remove(obj)
            self.game_context.current_wall.entities.add(obj)
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

