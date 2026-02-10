import pygame
import os
import json
from pathlib import Path
from objects.vase import Vase
from objects.digicode import Digicode
from objects.Connect4_Beta import Connect
from utils import *

class Wall:
    def __init__(self, game_context, root_dir):
        self.game_context = game_context
        self.root_dir = root_dir

        self.object_layers_dir = Path(self.root_dir / "images/object_layers")
        if not self.object_layers_dir.exists():
            self.object_layers_dir.mkdir(parents=True, exist_ok=True)

        self.cropped_object_dir = Path(self.game_context.root_dir / "assets/cropped_images")
        if not self.cropped_object_dir.exists():
            self.cropped_object_dir.mkdir(parents=True, exist_ok=True)

        self.collision_layers_dir = Path(self.root_dir / "images/collision_layers")
        if not self.collision_layers_dir.exists():
            self.collision_layers_dir.mkdir(parents=True, exist_ok=True)

        self.json_path = Path(self.root_dir / "images/objects_info.json")
        #self.clear_object_layers()
        #self.clear_cropped_objects() # TODO: to remove
        self.clear_json() # TODO: to remove also

        self.objects_data = load_json_file(self.json_path) # load or init the JSON file

        self.background = self.create_background()
        self.original_background = self.background
        self.entities = pygame.sprite.Group()
        self.create_entities()
        self.delta_w = self.game_context.delta_w * (1080/1920)
        self.delta_h = self.game_context.delta_h * (720/1080)
        self.delta = min(self.game_context.delta_w * (1080/1920), self.game_context.delta_h * (720/1080))
        

    def clear_json(self):
        with open(self.json_path, "w", encoding="utf-8") as f:
            f.write("{}")

    def clear_cropped_objects(self):
        cropped_object_paths = list(self.cropped_object_dir.iterdir())
        for path in cropped_object_paths:
            os.remove(path)
    
    def clear_object_layers(self):
        object_layers_path = list(self.object_layers_dir.iterdir())
        for path in object_layers_path:
            os.remove(path)

    def create_background(self) -> pygame.Surface:
        background_dir = Path(self.root_dir / "images/background")
        background_path = list(background_dir.iterdir()) # NOTE: we should only have one png file for the background
        background_exist =  background_path is not None # NOTE: iterdir lists the content of the folder
        background = pygame.image.load(background_path[0]) if background_exist else pygame.Surface(self.game_context.screen.get_size())
        if not background_exist: 
            background.fill((255, 0, 0))
        return background


    def init_objects_info(self):
        object_layers_path = list(self.object_layers_dir.iterdir())
        for object_path in reversed(object_layers_path): # reversed so we draw the object with the lowest layer id first
            object_name = object_path.stem[2:] # example : "vase" instead of ".../.../.../1_vase.png"
            cropped_name = f"cropped_{object_name}.png"
            save_path = Path(self.cropped_object_dir / cropped_name) # place where we save the cropped image

            #TODO: optimise this: the images are created everytime this function is called event if they already exist
            bbox = self.create_cropped_object(object_path, save_path.as_posix())

            collision_rects = self.get_collision_rects(self.collision_layers_dir, object_name)

            self.objects_data[object_name] = {}
            self.objects_data[object_name]["image"] = save_path.as_posix()
            self.objects_data[object_name]["rect"] = bbox
            self.objects_data[object_name]["collisions"] = collision_rects
            self.objects_data[object_name]["collision_id"] = -1
            
        save_data_in_json(self.objects_data, self.json_path)


    def create_entities(self):
        # case where we launched the game for the first time or we previously reset the progression
        if not self.objects_data:
            self.init_objects_info()

        for obj in self.objects_data:
            img_path = self.objects_data[obj].get("image")
            rect = pygame.Rect(self.objects_data[obj].get("rect"))
            collision_rects = self.objects_data[obj].get("collisions")
            #convert in pygame Rect
            for i in range(len(collision_rects)):
                collision_rects[i] = pygame.Rect(collision_rects[i])

            current_collision_id = self.objects_data[obj].get("collision_id")

            if obj == "calculator":
                self.entities.add(
                    Digicode(self.game_context, img_path, rect, "1234")
                )
            elif obj in ["vase", "vase2"]:
                self.entities.add(
                    Vase(self.game_context, img_path, rect, collision_rects)
                )
            elif obj == "frame":
                self.entities.add(
                    Vase(self.game_context, img_path, rect, collision_rects)
                )

            elif obj == "table":
                self.entities.add(
                    Vase(self.game_context, img_path, rect, collision_rects)
                )

            elif obj == "connect4":
                self.entities.add(
                    Connect(self.game_context, img_path, rect, 0)
                )


    def display_collision_rects(self): # debug function
        for entity in self.entities:
            if entity.name in ["vase"]:
                for rect in entity.collision_rects:
                    temp_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
                    pygame.draw.rect(temp_surface, (255, 0, 0, 128), temp_surface.get_rect())
                    self.game_context.screen.blit(temp_surface, rect)
            

    #returns the list of the paths of all the collision layers of an object
    def load_collision_layers_path(self, collision_layers_dir: Path, obj_name: str) -> list[Path]:
        collision_layers_path = list(collision_layers_dir.iterdir())

        valid_collision_layers_path = []
        all_found = False
        layer_count = 0
        while not all_found:
            layer_name = f"{obj_name}_pos{layer_count}.png"
            layer_path = Path(collision_layers_dir / layer_name)
            if layer_path in collision_layers_path:
                valid_collision_layers_path.append(layer_path)
                layer_count +=1
            else:
                all_found = True
        return valid_collision_layers_path


    def get_collision_rects(self, collision_layers_dir: Path, object_name: str) -> list[(int, int, int, int)]:
        collision_rects = []
        collision_layers_path = self.load_collision_layers_path(collision_layers_dir, object_name)
        for path in collision_layers_path:
            collision_layer = pygame.image.load(path).convert_alpha()
            rect = self.get_bounding_box(collision_layer)
            collision_rects.append(rect)
        return collision_rects


    # creates a cropped version of an image and saves its dimensions in a dictionary
    def create_cropped_object(self, raw_image_path, save_path):
        image = pygame.image.load(raw_image_path).convert_alpha()
        bbox = self.get_bounding_box(image)
        if bbox is None:
            print(f"No visible pixels in {raw_image_path}")
            return

        x, y, w, h = bbox
        cropped_image = self.create_sub_surface(x, y, w, h, image)

        pygame.image.save(cropped_image, save_path)
        print(f"Cropped image saved to {save_path}")

        return bbox


    def get_bounding_box(self, surface: pygame.Surface) -> (int, int, int, int):
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
        #print(f"x={x}, y={y}, w={w}, h={h}") #debug
        return (x, y, w, h)
        
        
    def create_sub_surface(self, x, y, w, h, surface):
        return surface.subsurface(pygame.Rect(x, y, w, h)).copy()


    def resize_images(self, objects_list):
        self.background = pygame.transform.scale(
            self.background,
            (
                int(self.original_background.get_width() * self.delta),
                int(self.original_background.get_height() * self.delta)
            )
        )  
        # changer tailles de chaque objets
        if objects_list:
            for obj in objects_list:
                obj.image = pygame.transform.scale(obj.raw_image,
                    (int(self.delta * obj.raw_rect.w), int(self.delta * obj.raw_rect.h))
                )
                obj.rect = pygame.Rect(self.delta * obj.raw_rect.x, self.delta * obj.raw_rect.y, self.delta * obj.raw_rect.w, self.delta * obj.raw_rect.h)

                # resize collision rects
                for i in range(len(obj.collision_rects)):
                    raw_collision_rect = obj.raw_collision_rects[i]
                    obj.collision_rects[i] = pygame.Rect(self.delta * raw_collision_rect.x, self.delta * raw_collision_rect.y, self.delta * raw_collision_rect.w, self.delta * raw_collision_rect.h)


    def draw_entities(self):
        for entity in self.entities:
            entity.draw()
                

    def draw_background(self):
        self.game_context.screen.blit(self.background, (0, 0))


    def sort_entities_by_image_name(self):
        sprites_list = self.entities.sprites()
        sprites_list = [s for s in sprites_list if hasattr(s, "image_name")]
        sprites_list.sort(key=lambda s: s.image_name.lower())

        self.entities.empty()
        self.entities.add(*sprites_list)


    def display(self):
        self.resize_images(self.entities)
        self.draw_background()
        self.draw_entities()
        self.display_collision_rects()

    # NOTE: can be redefined in child classes
    def update(self, event):
        for entity in self.entities:
            entity.update(event) # interactions relative to each object
