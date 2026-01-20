import pygame
import os
import json
from pathlib import Path
from room.objects.vase import Vase
from room.objects.digicode import Digicode

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
        

    def create_background(self) -> pygame.Surface:
        background_dir = Path(self.root_dir / "images/background")
        background_path = list(background_dir.iterdir()) # NOTE: we should only have one png file for the background
        background_exist =  background_path is not None # NOTE: iterdir lists the content of the folder
        background = pygame.image.load(background_path[0]) if background_exist else pygame.Surface(self.game_context.screen.get_size())
        if not background_exist: 
            background.fill((255, 0, 0))
        return background
    
    def create_entities(self):
        # 1: for each object in object_layers directory check if there exist a croped object associated in the croped_objects directory and it's data in objects_info.json
        # 2: if not we create the object and we write it's property in objects_info.json
        # 3: when all the cropped object are here we create a sprite for each of them and we put them in entities

        object_layers_dir = Path(self.root_dir / "images/object_layers")
        cropped_object_dir = Path(self.root_dir / "images/cropped_objects")
        object_layers_path = list(object_layers_dir.iterdir())

        # load le JSON
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
        
        parts = cropped_object_dir.parts
        new_path = Path(*parts[-6:])
        
        # delete extra keys
        expected_keys = {
            (new_path / f"cropped_{p.name}").as_posix() for p in object_layers_path
        }

        for key in list(objects_data.keys()):
            if key not in expected_keys:
                del objects_data[key]
        
        # delete extra cropped images
        expected_cropped_filenames = {
            f"cropped_{p.name}" for p in object_layers_path
        }

        for cropped_file in cropped_object_dir.iterdir():
            if not cropped_file.is_file():
                continue

            if cropped_file.name not in expected_cropped_filenames or not cropped_file.name.startswith("cropped_"):
                print(f"Removing extra cropped image: {cropped_file}")
                cropped_file.unlink()

        for object_path in object_layers_path:
            cropped_name = f"cropped_{object_path.name}"
            new_cropped_path = (new_path / cropped_name).as_posix()
            save_path = Path(cropped_object_dir / cropped_name)

            if not save_path.exists() or new_cropped_path not in objects_data:
                print(new_cropped_path not in objects_data)
                image = pygame.image.load(object_path).convert_alpha()
                bbox = self.get_bounding_box(image)

                if bbox is None:
                    print(f"No visible pixels in {object_path}")
                    continue

                x, y, w, h = bbox
                cropped_image = self.create_sub_surface(x, y, w, h, image)

                pygame.image.save(cropped_image, save_path)
                print(f"Cropped image saved to {save_path}")

                # put x, y, w, h in objects_data
                objects_data[new_cropped_path] = bbox

            # create the sprite
            sprite_rect_tupple = objects_data[new_cropped_path]
            name = object_path.name[2:]

            if name == "calculator.png": #TODO: change
                self.entities.add(
                    Digicode(self.game_context, f"{self.root_dir}/images/cropped_objects/cropped_5_calculator.png", (pygame.Rect(sprite_rect_tupple)[0], pygame.Rect(sprite_rect_tupple)[1]), "1234")
                )
            else:
                self.entities.add(
                    Vase(self.game_context, save_path, pygame.Rect(sprite_rect_tupple))
                )

        # save JSON
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(objects_data, f, indent=4, ensure_ascii=False)


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
        
        
    def create_sub_surface(self, x, y, w, h, surface):
        return surface.subsurface(pygame.Rect(x, y, w, h)).copy()

        
    def handle_click(self):
        clicked = False
        event = self.game_context.event
        if self.game_context.mouse_enabled:
            for obj in reversed(self.entities.sprites()):
                if event and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and obj.rect.collidepoint(event.pos) and not clicked:
                    clicked = True
                    if obj.name == "vase":
                        if not self.dragging or obj.dragging:
                            print("object clicked")
                            self.dragging = not self.dragging
                            obj.dragging = not obj.dragging # NOTE: dangerous because dragging is only defined in Vase
                            if obj.dragging:
                                self.current_item = obj
                            else:
                                self.current_item = None

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

    def update(self):
        self.resize_images(self.entities) # TODO: can we find a way to remove self.entities ?
        self.draw_background()
        self.draw_entities()
        mx, my = pygame.mouse.get_pos()[0] / self.delta, pygame.mouse.get_pos()[1] / self.delta
        for obj in self.entities:
            if obj.name in ["vase"] and obj.dragging:
                obj.raw_rect.x, obj.raw_rect.y = (mx - obj.raw_rect.w/2), (my - obj.raw_rect.h/2)
        self.update_current_wall()
        #self.resize_images(None)
        #self.draw_background()
        # mx, my = pygame.mouse.get_pos()[0] / self.delta, pygame.mouse.get_pos()[1] / self.delta
        # if self.dragging:
        #     obj.x, obj.y = (mx - obj.w/2), (my - obj.h/2)
        
        # if 1 == 0: #TODO erase (not now)
        #     x, y, w, h = self.get_bounding_box(self.table_test)
        #     new_table = self.create_sub_surface(x, y, w, h, self.table_test)

        #     table_rect = new_table.get_rect(topleft=self.table_pos)
            
        #     self.handle_event(table_rect)

        #     self.game_context.screen.blit(new_table, self.table_pos)
        
    def update_current_wall(self):
        pass