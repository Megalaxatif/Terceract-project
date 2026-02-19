import pygame
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

        clear_json(self.json_path) # TODO: to remove also

        self.background = self.create_background()
        self.original_background = self.background
        self.objects = pygame.sprite.Group()
        self.create_wall_objects()
        self.delta_w = self.game_context.delta_w * (1080/1920)
        self.delta_h = self.game_context.delta_h * (720/1080)
        self.delta = min(self.game_context.delta_w * (1080/1920), self.game_context.delta_h * (720/1080))


#---------------------------INIT---------------------------------------
    def create_background(self) -> pygame.Surface:
        background_dir = Path(self.root_dir / "images/background")
        background_path = list(background_dir.iterdir()) # NOTE: we should only have one png file for the background
        background_exist =  background_path is not None # NOTE: iterdir lists the content of the folder
        background = pygame.image.load(background_path[0]) if background_exist else pygame.Surface(self.game_context.screen.get_size())
        if not background_exist:
            background.fill((255, 0, 0))
        return background


    def get_objects_data(self):
        objects_data = {}
        object_layers_path = list(self.object_layers_dir.iterdir())
        for object_path in reversed(object_layers_path): # reversed so we draw the object with the lowest layer id first
            object_name = object_path.stem[2:] # example : "vase" instead of ".../.../.../1_vase.png"
            cropped_name = f"cropped_{object_name}.png"
            save_path = Path(self.cropped_object_dir / cropped_name) # place where we save the cropped image
            relative_path = Path(f"assets/cropped_images/{cropped_name}")
            bbox = create_cropped_object(object_path, save_path.as_posix())

            #collision_rects = get_collision_rects(self.collision_layers_dir, object_name)

            objects_data[object_name] = {}
            objects_data[object_name]["image"] = relative_path.as_posix()
            objects_data[object_name]["rect"] = bbox
            #objects_data[object_name]["collisions"] = collision_rects
            objects_data[object_name]["collision_id"] = -1

        save_data_in_json(objects_data, self.json_path)
        return objects_data


    def create_wall_objects(self):
        objects_data = load_json_file(self.json_path) # load or init the JSON file
        # case where we launched the game for the first time or we previously reset the progression
        if not objects_data:
            objects_data = self.get_objects_data()

        for key in objects_data:
            img_path = objects_data[key]["image"] # load the relative path
            rect = objects_data[key]["rect"]
            formated_rect = convert_to_pygame_rect(rect)
            #collision_rects = objects_data[key]["collisions"]

            current_collision_id = objects_data[key]["collision_id"]
            # #convert in pygame Rect
            # for i in range(len(collision_rects)):
            #     collision_rects[i] = pygame.Rect(collision_rects[i])
            collision_rects = get_collision_rects(self.collision_layers_dir, key)

            object = create_object(key, self.game_context, img_path, formated_rect, collision_rects, current_collision_id)
            self.objects.add(object)


#-------------------------------SAVE---------------------------------
    def save_objects_data(self):
        new_obj_data = {}
        for object in self.objects:
            print(f"saving {object.name} in json")
            # convert the rectangle from pygame.Rect to tuple to store them in the json
            formated_rect = convert_to_tuple_rect(object.raw_rect)

            # formated_collision_rects = []
            # for rect in object.raw_collision_rects:
            #     formated_collision_rects.append(tuple(rect))

            new_obj_data[object.name] = {}
            new_obj_data[object.name]["image"] = object.image_path.as_posix()
            new_obj_data[object.name]["rect"] = formated_rect
            #new_obj_data[object.name]["collisions"] = formated_collision_rects
            new_obj_data[object.name]["collision_id"] = object.collision_rect_index
        save_data_in_json(new_obj_data, self.json_path)


#-----------------------RESIZE---------------------------
    def resize_all(self):
        self.resize_background()
        for obj in self.objects:
            obj.resize_image()
            obj.resize_collision_rects()


    def resize_background(self):
        self.background = pygame.transform.scale(
            self.background,
            (
                int(self.original_background.get_width() * self.delta),
                int(self.original_background.get_height() * self.delta)
            )
        )

#--------------------DRAWING--------------------------------
    def display_collision_rects(self):
        for entity in self.objects:
            entity.display_collision_rect()


    def draw_objects(self):
        for obj in self.objects:
            obj.draw()


    def draw_background(self):
        self.game_context.screen.blit(self.background, (0, 0))


    def display(self):
        self.resize_all()
        self.draw_background()
        self.draw_objects()
        self.display_collision_rects()
#--------------------------------------------------------

    # NOTE: can be redefined in child classes
    def update(self, event):
        for obj in self.objects:
            obj.update(event) # interactions relative to each object
