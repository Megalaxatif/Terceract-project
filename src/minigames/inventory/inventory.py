import pygame
import sys
from pathlib import Path

root_dir = Path(__file__).resolve().parent

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)

pygame.init()

class Inventory:
    def __init__(self, game_context, x, y, rows, cols, block_size):
        self.game_context = game_context
        self.x = x
        self.y = y
        self.rows = rows
        self.cols = cols
        self.block_size = block_size
        self.slots = [[None for _ in range(cols)] for _ in range(rows)]
        self.display = False

        # load images
        self.images = {
            "temp1": pygame.transform.scale(pygame.image.load(f"{root_dir}/images/temp1.png"), (block_size*0.9, block_size*0.9)),
            "temp2": pygame.transform.scale(pygame.image.load(f"{root_dir}/images/temp2.png"), (block_size*0.9, block_size*0.9))
        }

        # Default pos
        self.slots[0][0] = "temp1"
        self.slots[1][1] = "temp2"

        self.current_item = None

    def update(self):
        self.draw_grid()
        self.draw_items()

        # for event in pygame.event.get():
            # if event.type == pygame.MOUSEBUTTONDOWN:
                # self.handle_click(event.pos)
                # print("click")

        # Display current item
        if self.current_item: # if not None
            mx, my = pygame.mouse.get_pos()
            self.game_context.screen.blit(self.images[self.current_item], (mx - 0.4*self.block_size, my - 0.4*self.block_size))

    def handle_click(self, pos):
        mouse_x, mouse_y = pos

        if not (self.x <= mouse_x < self.x + self.cols * self.block_size and
                self.y <= mouse_y < self.y + self.rows * self.block_size):
            return

        col = (mouse_x - self.x) // self.block_size
        row = (mouse_y - self.y) // self.block_size

        slot = self.slots[row][col]

        # Grab
        if self.current_item is None and slot is not None:
            self.current_item = slot
            self.slots[row][col] = None

        # Drop
        elif self.current_item is not None: # Swap them
            self.slots[row][col], self.current_item = self.current_item, self.slots[row][col]
        
        print("click inventory")

    def draw_grid(self):
        for row in range(self.rows):
            for col in range(self.cols):
                rect = pygame.Rect(self.x + col * self.block_size,
                    self.y + row * self.block_size,
                    self.block_size, self.block_size)
                pygame.draw.rect(self.game_context.screen, WHITE, rect, 2)

    def draw_items(self):
        for row in range(self.rows):
            for col in range(self.cols):
                item = self.slots[row][col]
                if item: # Not None
                    self.game_context.screen.blit(self.images[item],
                        (self.x + col * self.block_size + 0.05*self.block_size,
                        self.y + row * self.block_size + 0.05*self.block_size))
