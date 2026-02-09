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

pygame.init()


class Inventory:
    def __init__(self, game_context, x, y, rows, cols, block_size, center):
        self.game_context = game_context
        self.root_dir = Path(__file__).resolve().parent
        self.entities = pygame.sprite.Group()
        self.current_entity = None

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

        self.display = False
        self.center = center

        self.last_row, self.last_col = 0, 0
        self.mouse_x, self.mouse_y = 0, 0

        # load images
        self.current_item = None

        self.init_images()


    def init_images(self):
        pass


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

        # Display current item
        if self.current_item:  # if not None
            self.game_context.dragging = True
            mx, my = pygame.mouse.get_pos()
            self.game_context.screen.blit(
                self.images[f"{self.current_item}"][0],
                (mx - 0.4 * self.block_size, my - 0.4 * self.block_size)
            )

    def handle_click(self, event):
        
        if (
            self.x <= self.mouse_x < self.x + self.cols * self.block_size and
            self.y <= self.mouse_y < self.y + self.rows * self.block_size
        ):
            col = (self.mouse_x - self.x) // self.block_size
            row = (self.mouse_y - self.y) // self.block_size

            slot = self.slots[row][col]

            if self.current_item:
                pass

    def put_in_inventory(self, obj):
        pass

    def put_out_inventory(self, obj):
        pass

    def resize_in_inventory(self, path):
        return pygame.transform.scale(
            pygame.image.load(path),
            (self.block_size * 0.9, self.block_size * 0.9)
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
                if item:  # Not None
                    self.game_context.screen.blit(
                        self.images[item][0],
                        (
                            self.x + col * self.block_size + 0.05 * self.block_size,
                            self.y + row * self.block_size + 0.05 * self.block_size
                        )
                    )

