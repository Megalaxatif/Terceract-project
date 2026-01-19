import pygame
import os
import json
from pathlib import Path
from room.objects.vase import Vase

class Wall:
    def __init__(self, game_context, root_dir):
        #explanation:
        #background_layer_path is a path to a static image that cannot move
        #interactable_layers is a list of the path to the objects to be displayed on the wall
        self.root_dir = root_dir
        self.game_context = game_context
        self.background = self.create_background()
        self.original_background = self.background
        self.entities = pygame.sprite.Group()
        self.create_entities()
        self.current_item = None
        self.dragging = False
        self.delta_w = self.game_context.delta_w * (1080/1920)
        self.delta_h = self.game_context.delta_h * (720/1080)
        self.delta = min(self.game_context.delta_w * (1080/1920), self.game_context.delta_h * (720/1080))

    def clear_json(self):
        json_path = Path(self.root_dir / "images/objects_info.json")
        with open(json_path, "w", encoding="utf-8") as f:
            f.write("{}")

    def clear_cropped_objects(self):
        cropped_object_dir = Path(self.root_dir / "images/cropped_objects")
        cropped_object_path = list(cropped_object_dir.iterdir())
        for path in cropped_object_path:
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
        object_layers_dir = Path(self.root_dir / "images/object_layers")
        cropped_object_dir = Path(self.root_dir / "images/cropped_objects")
        object_layers_path = list(object_layers_dir.iterdir())

        # load or init the JSON file
        objects_data = {}
        json_path = Path(self.root_dir / "images/objects_info.json")
        if json_path.exists():
            with open(json_path, "r", encoding="utf-8") as f:
                    try:
                        objects_data = json.load(f)
                    except json.JSONDecodeError:
                        objects_data = {}
        else:
            raise Exception("create entities error : invalid path")

        for object_path in reversed(object_layers_path): # reversed so we draw the object with the lowest layer id first
            layer_id = object_path.name[0]
            cropped_name = f"{layer_id}_cropped_{object_path.name[2:]}"
            save_path = Path(cropped_object_dir / cropped_name)

            if not save_path.exists() or str(save_path) not in objects_data:
                self.create_cropped_object(object_path, save_path, objects_data)
    
            # extract the collision rectangles of the object if they exist
            #TODO: optimize so we don't have to to this every time we launch the game
            collision_layers_path = self.load_collision_layers_path(object_path.stem[2:]) # remove the id and the underscore
            collision_rects = []
            for path in collision_layers_path:
                collision_layer = pygame.image.load(path).convert_alpha()
                rect = pygame.Rect(self.get_bounding_box(collision_layer))
                collision_rects.append(rect)


            #create the sprite
            sprite_rect_tupple = objects_data[str(save_path)]
            if object_path.stem[2:] == "table" or "cropped_ui_test" or "cropped_vase": #TODO: ALWAYS TRUE
                self.entities.add(Vase(self.game_context, save_path, pygame.Rect(sprite_rect_tupple), collision_rects))
            # TODO: list all the other entities possible

        #save the data in the json file
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(objects_data, f, indent=4, ensure_ascii=False) 


    def display_collision_rects(self): # debug function
        for entity in self.entities:
            for rect in entity.collision_rects:
                temp_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
                pygame.draw.rect(temp_surface, (255, 0, 0, 128), temp_surface.get_rect())
                self.game_context.screen.blit(temp_surface, rect)
            

    def load_collision_layers_path(self, obj_name): #returns the list of the paths of all the collision layers of an object
        collision_layers_dir = Path(self.root_dir / "images/collision_layers")
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


    def create_cropped_object(self, raw_image_path, save_path, data_dict): # creates a cropped version of an image and saves its dimensions in a dictionary
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
        data_dict[str(save_path)] = bbox


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

        
    def handle_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.current_item is not None:
                collision_index = self.current_item.rect.collidelist(self.current_item.collision_rects)
                if collision_index != -1:
                    self.current_item.raw_rect.center = self.current_item.collision_rects[collision_index].center
                    self.current_item.valid_rect = self.current_item.collision_rects[collision_index]
                else:
                    self.current_item.raw_rect.center = self.current_item.valid_rect.center
                self.current_item.dragging = False # NOTE: dangerous because dragging is only defined in Vase
                self.current_item = None
            else:
                for obj in reversed(self.entities.sprites()): # reversed so we click the top object first
                    if obj.rect.collidepoint(event.pos):
                        self.current_item = obj
                        obj.dragging = True # NOTE: dangerous because dragging is only defined in Vase
                        break


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

                for i in range(len(obj.collision_rects)):
                    raw_collision_rect = obj.raw_collision_rects[i]
                    obj.collision_rects[i] = pygame.Rect(self.delta * raw_collision_rect.x, self.delta * raw_collision_rect.y, self.delta * raw_collision_rect.w, self.delta * raw_collision_rect.h)

        
    def draw_entities(self):
        self.entities.draw(self.game_context.screen)

    def draw_background(self):
        self.game_context.screen.blit(self.background, (0, 0))

    def update(self):
        self.resize_images(self.entities) # TODO: can we find a way to remove self.entities ?
        self.draw_background()
        self.draw_entities()
        self.display_collision_rects()
        mx, my = pygame.mouse.get_pos()[0] / self.delta, pygame.mouse.get_pos()[1] / self.delta
        for obj in self.entities:
            if obj.dragging:
                obj.raw_rect.x, obj.raw_rect.y = (mx - obj.raw_rect.w/2), (my - obj.raw_rect.h/2)