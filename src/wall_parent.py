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
        self.root_dir = root_dir
        self.game_context = game_context
        self.background = self.create_background()
        self.original_background = self.background
        self.entities = pygame.sprite.Group()
        self.create_entities()
        self.delta_w = self.game_context.delta_w * (1080/1920)
        self.delta_h = self.game_context.delta_h * (720/1080)
        self.delta = min(self.game_context.delta_w * (1080/1920), self.game_context.delta_h * (720/1080))
        

    def clear_json(self):
        json_path = Path(self.root_dir / "images/objects_info.json")
        with open(json_path, "w", encoding="utf-8") as f:
            f.write("{}")

    def clear_cropped_objects(self):
        cropped_object_dir = Path(self.root_dir / "images/cropped_objects")
        cropped_object_paths = list(cropped_object_dir.iterdir())
        for path in cropped_object_paths:
            os.remove(path)
    
    def clear_object_layers(self):
        object_layers_dir = Path(self.root_dir / "images/object_layers")
        object_layers_path = list(object_layers_dir.iterdir())
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
    
    def create_entities(self):
        #self.clear_object_layers()
        #self.clear_cropped_objects()
        #self.clear_json()
        # 1: check if there exist a cropped object associated to the object in the cropped_objects folder and if its data is in objects_info.json
        # 2: if not we create the cropped object and save its data
        # 3: we try to find potential collision layers stored in collision_layers folder
        # 4: we create a sprite for the object and add it to the entities group
        json_path = Path(self.root_dir / "images/objects_info.json")
        objects_data = load_json_file(json_path) # load or init the JSON file

        object_layers_dir = Path(self.root_dir / "images/object_layers")
        if not object_layers_dir.exists():
            object_layers_dir.mkdir(parents=True, exist_ok=True)

        cropped_object_dir = Path(self.root_dir / "images/cropped_objects")
        if not cropped_object_dir.exists():
            cropped_object_dir.mkdir(parents=True, exist_ok=True)

        collision_layers_dir = Path(self.root_dir / "images/collision_layers")
        if not collision_layers_dir.exists():
            collision_layers_dir.mkdir(parents=True, exist_ok=True)
        
        # get all the paths in the directories
        object_layers_path = list(object_layers_dir.iterdir())
        cropped_object_paths = list(cropped_object_dir.iterdir())
        
        parts = cropped_object_dir.parts
        new_path = Path(*parts[-6:]) # relative path from src
        
        self.cleanup_data(new_path, object_layers_path, cropped_object_paths, objects_data)

        for object_path in reversed(object_layers_path): # reversed so we draw the object with the lowest layer id first
            object_name = object_path.stem[2:] # example : "vase" instead of ".../.../.../1_vase.png"
            cropped_name = f"cropped_{object_path.name}"
            json_key = (new_path / cropped_name).as_posix()
            save_path = Path(cropped_object_dir / cropped_name).as_posix() # place where we save the cropped image

            if not Path(save_path).exists() or json_key not in objects_data:
                self.create_cropped_object(object_path, save_path, json_key, objects_data)

            #TODO: optimize so we don't have to to this every time we launch the game
            collision_rects = self.get_collision_rects(collision_layers_dir, object_name) # ignore the layer index and the dash
            # create the sprite
            sprite_rect_tupple = objects_data[json_key]

            if object_name == "calculator": #TODO: change
                self.entities.add(
                    Digicode(self.game_context, f"{self.root_dir}/images/cropped_objects/cropped_5_calculator.png", pygame.Rect(sprite_rect_tupple), "1234")
                )
            elif object_name == "vase":
                self.entities.add(
                    Vase(self.game_context, save_path, pygame.Rect(sprite_rect_tupple), collision_rects)
                )
            elif object_name == "frame":
                self.entities.add(
                    Vase(self.game_context, save_path, pygame.Rect(sprite_rect_tupple), collision_rects)
                )

            elif object_name == "table":
                self.entities.add(
                    Vase(self.game_context, save_path, pygame.Rect(sprite_rect_tupple), collision_rects)
                )

            elif object_name == "connect4":
                self.entities.add(
                    Connect(self.game_context, save_path, pygame.Rect(sprite_rect_tupple), 0)
                )

        save_data_in_json(objects_data, json_path)


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


    def get_collision_rects(self, collision_layers_dir: Path, object_name: str) -> list[pygame.Rect]:
        collision_rects = []
        collision_layers_path = self.load_collision_layers_path(collision_layers_dir, object_name)
        for path in collision_layers_path:
            collision_layer = pygame.image.load(path).convert_alpha()
            rect = pygame.Rect(self.get_bounding_box(collision_layer))
            collision_rects.append(rect)
        return collision_rects


    # creates a cropped version of an image and saves its dimensions in a dictionary
    def create_cropped_object(self, raw_image_path, save_path, json_key, data_dict):
        image = pygame.image.load(raw_image_path).convert_alpha()
        bbox = self.get_bounding_box(image)
        if bbox is None:
            print(f"No visible pixels in {raw_image_path}")
            return

        x, y, w, h = bbox
        cropped_image = self.create_sub_surface(x, y, w, h, image)

        pygame.image.save(cropped_image, save_path)
        print(f"Cropped image saved to {save_path}")

        # put w, y, w, h in objects_data        
        data_dict[json_key] = bbox


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
                #pygame.draw.rect(self.game_context.screen, (0,0,0), obj.rect, 1) 
                if obj.name in ["vase"]:
                    for i in range(len(obj.collision_rects)):
                        raw_collision_rect = obj.raw_collision_rects[i]
                        obj.collision_rects[i] = pygame.Rect(self.delta * raw_collision_rect.x, self.delta * raw_collision_rect.y, self.delta * raw_collision_rect.w, self.delta * raw_collision_rect.h)


    # remove unused images in a list of cropped_object_path and the unused keys in objects_data 
    # by comparing them to the list of object_layers_path whose images are supposed to be used
    def cleanup_data(self, root_dir: Path, object_layers_path: list[Path], cropped_object_paths: list[Path], objects_data: dict):
        expected_keys = {
            (root_dir / f"cropped_{p.name}").as_posix() for p in object_layers_path
        }

        expected_cropped_name = {
            f"cropped_{p.name}" for p in object_layers_path
        }

        # delete extra keys
        for key in list(objects_data.keys()):
            if key not in expected_keys:
                del objects_data[key]
            

        # delete extra cropped images
        for cropped_path in cropped_object_paths:
            if cropped_path.name not in expected_cropped_name:
                print(f"Removing extra cropped image:  {cropped_path}")
                cropped_path.unlink()
        

    def draw_entities(self):
        for entity in self.entities:
            if entity.displayed:
                self.game_context.screen.blit(entity.image, entity.rect)
                

    def draw_background(self):
        self.game_context.screen.blit(self.background, (0, 0))


    def sort_entities_by_image_name(self):
        sprites_list = self.entities.sprites()
        sprites_list = [s for s in sprites_list if hasattr(s, "image_name")]
        sprites_list.sort(key=lambda s: s.image_name.lower())

        self.entities.empty()
        self.entities.add(*sprites_list)

    # NOTE: can be redefined in child classes
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.game_context.current_item is not None:
                self.game_context.current_item.handle_event(event)
            else:
                for obj in reversed(self.entities.sprites()): # reversed so we click the top object first
                    if obj.movable:
                        if obj.rect.collidepoint(event.pos):
                            print("collision")
                            self.game_context.current_item = obj
                            print(self.game_context.current_item.name)
                            obj.dragging = True
                            break

    # NOTE: can be redefined in child classes
    def update(self):
        self.resize_images(self.entities) # TODO: can we find a way to remove self.entities ?
        self.draw_background()
        self.draw_entities()
        self.display_collision_rects()
        mx, my = pygame.mouse.get_pos()[0] / self.delta, pygame.mouse.get_pos()[1] / self.delta
        for obj in self.entities:
            if obj.dragging:
                obj.raw_rect.x, obj.raw_rect.y = (mx - obj.raw_rect.w/2), (my - obj.raw_rect.h/2)
        self.update_current_wall()


    def update_current_wall(self):
        pass
