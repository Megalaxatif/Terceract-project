import pygame
import sys
from pathlib import Path
import json
from room.objects.vase import Vase

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)

pygame.init()

class Inventory:
    def __init__(self, game_context, x, y, rows, cols, block_size, center):
        self.game_context = game_context
        self.root_dir = Path(__file__).resolve().parent
        self.raw_x = x
        self.x = int(self.raw_x * self.game_context.delta)
        self.raw_y = y
        self.y = int(self.raw_y * self.game_context.delta)
        self.rows = rows
        self.cols = cols
        self.raw_block_size = block_size
        self.block_size = int(self.raw_block_size * self.game_context.delta)
        self.slots = [[None for _ in range(cols)] for _ in range(rows)]
        self.display = False
        self.center = center
        self.last_row, self.last_col = 0, 0

        # load images
        self.images = {
            "temp1.png": [pygame.transform.scale(pygame.image.load(f"{self.root_dir}/images/temp1.png"), (block_size*0.9, block_size*0.9)), f"{self.root_dir}/images/temp1.png"],
            "temp2.png": [pygame.transform.scale(pygame.image.load(f"{self.root_dir}/images/temp2.png"), (block_size*0.9, block_size*0.9)), f"{self.root_dir}/images/temp2.png"]
        }

        # Default pos
        self.slots[0][0] = "temp1.png"
        self.slots[0][1] = "temp2.png"

        self.current_item = None

    def update(self):
        self.block_size = int(self.raw_block_size * self.game_context.delta)
        if self.center:
            mid_block = len(self.slots[0])//2 + len(self.slots[0])%2
            self.x = self.game_context.screen.get_width()//2 - mid_block * self.block_size
        else:
            self.x = int(self.raw_x * self.game_context.delta)
        self.y = int(self.raw_y * self.game_context.delta)
        
        for key in self.images:
            self.images[key][0] = self.resize_in_inventory(f"{self.root_dir}/images/{key}")
        
        self.draw_grid()
        self.draw_items()

        # Display current item
        if self.current_item: # if not None
            mx, my = pygame.mouse.get_pos()
            self.game_context.screen.blit(self.images[self.current_item][0], (mx - 0.4*self.block_size, my - 0.4*self.block_size))

    def resize_in_inventory(self, path):
        return pygame.transform.scale(pygame.image.load(path), (self.block_size*0.9, self.block_size*0.9))

    def handle_click(self, pos):
        mouse_x, mouse_y = pos

        if (self.x <= mouse_x < self.x + self.cols * self.block_size and
                self.y <= mouse_y < self.y + self.rows * self.block_size):

            col = (mouse_x - self.x) // self.block_size
            row = (mouse_y - self.y) // self.block_size

            slot = self.slots[row][col]

            # Grab
            if not self.current_item:
                if slot:
                    self.current_item = slot
                external_obj = self.game_context.current_wall.current_item
                if external_obj:
                    if not Path(f"{self.root_dir}/images/{external_obj.image_name}").exists():
                        pygame.image.save(external_obj.image, f"{self.root_dir}/images/{external_obj.image_name}")
                    self.images[external_obj.image_name] = [self.resize_in_inventory(f"{self.root_dir}/images/{external_obj.image_name}"), str(external_obj.image_path)]
                    self.slots[row][col] = external_obj.image_name
                    for sprite in self.game_context.current_wall.entities.sprites():
                        if isinstance(sprite, Vase) and sprite.image_path == external_obj.image_path:
                            self.game_context.current_wall.entities.remove(sprite)
                    self.game_context.current_wall.current_item.dragging = False
                    self.game_context.current_wall.current_item = None
                    self.game_context.current_wall.dragging = False
                else:
                    self.slots[row][col] = None
                self.last_row, self.last_col = row, col

            # Drop
            elif self.current_item: # Swap them
                self.slots[row][col], self.current_item = self.current_item, self.slots[row][col]
            
            print("click inventory")
        
        elif self.current_item != None:
            self.create_entities()
            self.game_context.current_wall.sort_entities_by_image_name()
        
    def draw_grid(self):
        for row in range(self.rows):
            for col in range(self.cols):
                rect = pygame.Rect(self.x + col * self.block_size,
                    self.y + row * self.block_size,
                    self.block_size, self.block_size)
                pygame.draw.rect(self.game_context.screen, WHITE, rect, 2)

    def draw_items(self):
        #print(self.images)
        for row in range(self.rows):
            for col in range(self.cols):
                item = self.slots[row][col]
                if item: # Not None
                    self.game_context.screen.blit(self.images[item][0],
                        ((self.x + col * self.block_size + 0.05*self.block_size),
                        (self.y + row * self.block_size + 0.05*self.block_size)))
    
    def create_entities(self):
        # put at original place if it's a non valid zone
        # self.slots[self.last_row][self.last_col], self.current_item = self.current_item, self.slots[self.last_row][self.last_col]
        
        object_path = Path(self.root_dir / f"images/{self.current_item}")
        cropped_object_dir = Path(self.game_context.current_wall.root_dir / "images/cropped_objects")
        object_layers_path = list((object_path.parent).iterdir())
        # Charger ou initialiser le JSON
        objects_data = {}
        json_path = Path(self.root_dir / "objects_info.json")
        json_path_wall = Path(self.game_context.current_wall.root_dir / "images/objects_info.json")
        if json_path.exists():
            with open(json_path, "r", encoding="utf-8") as f:
                    try:
                        objects_data = json.load(f)
                    except json.JSONDecodeError:
                        objects_data = {}
        else:
            raise Exception("create entities error : invalid path")
        
        # delete extra keys
        expected_keys = {
            f"{p.name}" for p in object_layers_path
        }

        for key in list(objects_data.keys()):
            if key not in expected_keys:
                del objects_data[key]
        
        if json_path_wall.exists():
            with open(json_path_wall, "r", encoding="utf-8") as f:
                    try:
                        objects_data_wall = json.load(f)
                    except json.JSONDecodeError:
                        objects_data_wall = {}
        else:
            raise Exception("create entities error : invalid path")
        
        cropped_name = f"cropped_{object_path.name}"
        save_path = Path(cropped_object_dir / object_path.name)
        origin_path = Path(self.images[self.current_item][1])
        if not save_path.exists() or object_path.name not in objects_data_wall:
            
            image = pygame.image.load(origin_path).convert_alpha()
            bbox = self.get_bounding_box(image)

            if bbox is None:
                print(f"No visible pixels in {object_path}")
            
            else:
                x, y, w, h = bbox

                pygame.image.save(image, save_path)
                print(f"Cropped image saved to {save_path}")

                # put x, y, w, h in objects_data
                objects_data_wall[object_path.name] = bbox
        
        if object_path.name not in objects_data:
            objects_data[object_path.name] = objects_data_wall[object_path.name]
        
        #create the sprite
        sprite_rect_tupple = objects_data[object_path.name]
        dim = (sprite_rect_tupple[0],
                sprite_rect_tupple[1],
                sprite_rect_tupple[2],
                sprite_rect_tupple[3]) 
        cropped_name = cropped_name[2:]
        if cropped_name == "table.png" or "cropped_ui_test.png" or "cropped_vase.png": #TODO: ALWAYS TRUE
            self.game_context.current_wall.entities.add(Vase(self.game_context, save_path, pygame.Rect(dim)))
        # TODO: list all the other entities possible

        #save the data in the json file
        def save_json(path, data):
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

        save_json(json_path, objects_data)
        save_json(json_path_wall, objects_data_wall) 

        del self.images[self.current_item]

        self.current_item = None

    def create_sub_surface(self, x, y, w, h, surface):
        return surface.subsurface(pygame.Rect(x, y, w, h)).copy()
    
    def get_bounding_box(self, surface):
        width, height = surface.get_size()
        pixel_array = pygame.PixelArray(surface)

        min_x = width
        min_y = height
        max_x = 0
        max_y = 0

        found = False

        for y in range(height):
            for x in range(width):
                color = surface.unmap_rgb(pixel_array[x, y])
                if color.a > 0:  # if a pixel is visible
                    found = True
                    min_x = min(min_x, x)
                    min_y = min(min_y, y)
                    max_x = max(max_x, x)
                    max_y = max(max_y, y)

        del pixel_array  # if we don't do that, the surface is locked

        if not found:
            return None
        
        x, y, w, h = min_x, min_y, max_x - min_x + 1, max_y - min_y + 1
        print(f"x={x}, y={y}, w={w}, h={h}")
        return (x, y, w, h)