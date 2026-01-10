import pygame
import os
import json
from pathlib import Path

pygame.init()

class Wall:
    def __init__(self, game_context, background_layer_path : str | None, interactable_layers_path : list[str] | None, root_dir_child):
        #explanation:
        #background_layer_path is a path to a static image that cannot move
        #interactable_layers is a list of the path to the entities to be displayed on the wall
        self.game_context = game_context
        self.interactable_layers_path = interactable_layers_path
        self.background = pygame.image.load(background_layer_path) if background_layer_path is not None else pygame.Surface(self.game_context.screen.get_size())
        self.raw_background = self.background
        if background_layer_path is None: self.background.fill((255, 0, 0))
        self.entities = pygame.sprite.Group
        self.current_item = None
        self.delta_w = self.game_context.delta_w * (1080/1920)
        self.delta_h = self.game_context.delta_h * (720/1080)
        self.delta = min(self.game_context.delta_w * (1080/1920), self.game_context.delta_h * (720/1080))
        #self.displayed_obj = None #just to init # what ??
        
        self.dragging = False
        #self.drag_offset = pygame.Vector2(0, 0) # what ??

        # position de la table
        self.table_pos = pygame.Vector2(100, 100) # what ??

        json_path = Path(f"{self.game_context.root_dir}/data/game_data.json")

        # Charger ou initialiser le JSON
        if json_path.exists():
            with open(json_path, "r", encoding="utf-8") as f:
                try:
                    game_data = json.load(f)
                except json.JSONDecodeError:
                    game_data = {}
        else:
            game_data = {}
        
        # first we load the raw images with their path in interactable_layers_path
        if self.interactable_layers_path:

            for layer_path in self.interactable_layers_path:
                original_layer_path = layer_path  # cle du JSON

                full_path = Path(layer_path)
                if not full_path.exists():
                    print(f"Image not found: {full_path}")
                    continue

                original_name = os.path.basename(layer_path)
                cropped_name = f"cropped_{original_name}"
                save_path = Path(f"{root_dir_child}") / "images" / cropped_name

                # Si la cle not in JSON, on init
                json_key = full_path.relative_to(full_path.parents[3]).as_posix()
                if json_key not in game_data:
                    game_data[json_key] = [None, None, None, None, None, None]

                if save_path.exists() and game_data[json_key][0] != None:
                    print(f"Cropped file already exists: {save_path}, skipping...")
                    continue

                image = pygame.image.load(full_path).convert_alpha()

                bbox = self.get_bounding_box(image)
                if bbox is None:
                    print(f"No visible pixels in {original_layer_path}")
                    continue

                x, y, w, h = bbox
                cropped_image = self.create_sub_surface(x, y, w, h, image)

                # Enregistrer bbox dans le JSON
                game_data[json_key] = [x, y, w, h, x, y]

                pygame.image.save(cropped_image, save_path)
                print(f"Cropped image saved to {save_path}")
                
        #json_path.parent.mkdir(parents=True, exist_ok=True)

        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(game_data, f, indent=4, ensure_ascii=False)



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

        
    def handle_click(self, event, obj_list):
        if obj_list:
            l = len(obj_list)
            for i in range(l):
                obj = obj_list[i]
                # self.object_pos = obj.x * self.delta, obj.y * self.delta # what ??

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if obj.rect.collidepoint(event.pos):
                        print("clicked")
                        obj.dragging = not obj.dragging
                        # what ???
                        #temp_obj = self.displayed_obj.pop(i)
                        #self.displayed_obj.append(temp_obj)


    def resize_images(self, objects_list):

        self.background = pygame.transform.scale(
            self.background,
            (
                int(self.raw_background.get_width() * self.delta),
                int(self.raw_background.get_height() * self.delta)
            )
        )
        
        # changer tailles de chaque objets
        if objects_list:
            for obj in objects_list:
                obj.cropped_image = pygame.transform.scale(obj.raw_cropped_image,
                    (self.delta * obj.w, self.delta * obj.h)
                )
                obj.rect = pygame.Rect(self.delta * obj.x, self.delta * obj.y, self.delta * obj.w, self.delta * obj.h)
                #pygame.draw.rect(self.game_context.screen, (0,0,0), obj.rect, 1)
    
    def update(self):
        self.resize_images(None)
        self.game_context.screen.blit(self.background, (0, 0))
        # mx, my = pygame.mouse.get_pos()[0] / self.delta, pygame.mouse.get_pos()[1] / self.delta
        # if self.dragging:
        #     obj.x, obj.y = (mx - obj.w/2), (my - obj.h/2)
        
        # if 1 == 0: #TODO erase (not now)
        #     x, y, w, h = self.get_bounding_box(self.table_test)
        #     new_table = self.create_sub_surface(x, y, w, h, self.table_test)

        #     table_rect = new_table.get_rect(topleft=self.table_pos)
            
        #     self.handle_event(table_rect)

        #     self.game_context.screen.blit(new_table, self.table_pos)


