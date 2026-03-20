import pygame
from pathlib import Path
from utils import *

class Wall:
    def __init__(self, game_context, root_dir, room_id, wall_id):
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
        self.background_w = self.background.get_width()
        self.background_h = self.background.get_height()
        self.original_background = self.background
        self.original_background_w = self.original_background.get_width()
        self.original_background_h = self.original_background.get_height()
        self.objects = pygame.sprite.Group()
        self.room_id = room_id # for network
        self.wall_id = wall_id # for network
        self.wall_id_str = f"{self.room_id + 1}{self.wall_id + 1}"
        self.delta_w = self.game_context.delta_w * (1080/1920)
        self.delta_h = self.game_context.delta_h * (720/1080)
        self.delta = min(self.game_context.delta_w * (1080/1920), self.game_context.delta_h * (720/1080))
        self.create_wall_objects()

    #---------------------------INIT---------------------------------------
    def create_background(self) -> pygame.Surface:
        background_dir = Path(self.root_dir / "images/background")
        background_path = list(background_dir.iterdir())    # NOTE: we should only have one png file for the background
        background_exist =  background_path is not None     # NOTE: iterdir lists the content of the folder
        background = pygame.image.load(background_path[0]).convert() if background_exist else pygame.Surface(self.game_context.screen.get_size())
        if not background_exist:
            background.fill((255, 0, 0))
        return background


    def get_objects_data(self):
        objects_data = {}
        object_layers_path = [f for f in sorted(Path(self.object_layers_dir).iterdir())]
        for object_path in reversed(object_layers_path): # reversed so we draw the object with the lowest layer id first
            if object_path.parent == self.object_layers_dir:
                object_name = object_path.stem[2:] # example : "vase" instead of ".../.../.../1_vase.png"
            else:
                object_name = f"{object_path.parent.name}_{object_path.stem[2:]}"
            cropped_name = f"cropped_{object_name}.png"
            save_path = Path(self.cropped_object_dir / cropped_name) # place where we save the cropped image
            relative_path = Path(f"assets/cropped_images/{cropped_name}")
            bbox = create_cropped_object(object_path, save_path.as_posix())

            collision_rects = get_collision_rects(self.collision_layers_dir, object_name)

            if object_name not in ["key", "magnet", "grid"]:
                default_collision = bbox
            else:
                default_collision = None

            objects_data[object_name] = {}
            objects_data[object_name]["image"] = relative_path.as_posix()
            objects_data[object_name]["rect"] = bbox
            objects_data[object_name]["collisions"] = collision_rects
            objects_data[object_name]["collision_id"] = -1
            objects_data[object_name]["default_collision"] = default_collision
            objects_data[object_name]["default_wall_id"] = self.wall_id_str

        save_data_in_json(objects_data, self.json_path)
        return objects_data


    def create_wall_objects(self):
        objects_data = {}
        if self.game_context.network_manager.is_host:
            objects_data = load_json_file(self.json_path) # load or init the JSON file
            # case where we launched the game for the first time or we previously reset the progression
            if not objects_data:
                objects_data = self.get_objects_data()

        else:
            objects_data = self.game_context.game_data["wall_data"][self.room_id][self.wall_id]

        for key in objects_data:
            img_path = objects_data[key]["image"] # load the relative path
            rect = objects_data[key]["rect"]
            collision_rects = objects_data[key]["collisions"]
            current_collision_id = objects_data[key]["collision_id"]
            default_collision = objects_data[key].get("default_collision")
            default_wall = objects_data[key].get("default_wall_id", "")

            converted_rect = convert_to_pygame_rect(rect)
            converted_collision_rects = convert_to_pygame_rect_list(collision_rects)
            converted_default_collision = convert_to_pygame_rect(default_collision)

            object = create_object(key,
                self.game_context,
                img_path,
                converted_rect,
                converted_collision_rects,
                current_collision_id,
                converted_default_collision,
                default_wall)

            self.objects.add(object)


#-------------------------------SAVE---------------------------------
    def save_objects_data(self):
        new_obj_data = {}
        for object in self.objects:
            print(f"saving {object.name} in json")
            formated_rect = convert_to_tuple_rect(object.raw_rect)

            
            if object.default_collision:
                formated_collision_rects = convert_to_tuple_rect_list(
                    [row for row in object.raw_collision_rects if row != object.default_collision] # Erase object.default_collision
                    )
                formated_default_collision = convert_to_tuple_rect(object.default_collision)
            else:
                formated_collision_rects = convert_to_tuple_rect_list(object.raw_collision_rects)
                formated_default_collision = None
                
            new_obj_data[object.name] = {}
            new_obj_data[object.name]["image"] = object.image_path.as_posix()
            new_obj_data[object.name]["rect"] = formated_rect
            new_obj_data[object.name]["collisions"] = formated_collision_rects
            new_obj_data[object.name]["collision_id"] = object.collision_rect_id
            new_obj_data[object.name]["default_collision"] = formated_default_collision
            new_obj_data[object.name]["default_wall_id"] = object.default_wall
        save_data_in_json(new_obj_data, self.json_path)


#-----------------------RESIZE---------------------------
    def resize_wall(self):
        self.resize_background()
        for obj in self.objects:
            obj.resize_image()
            obj.resize_collision_rects()


    def resize_background(self):
        new_w = int(self.original_background_w * self.delta)
        new_h = int(self.original_background_h * self.delta)
        if (new_w != self.background_w) or (new_h != self.background_h):
            self.background = pygame.transform.scale(
                    self.original_background, (new_w, new_h)
            )
            self.background_w = new_w
            self.background_h = new_h


#--------------------DRAWING--------------------------------
    def display_collision_rects(self):
        for entity in self.objects:
            entity.display_collision_rect()

    def display_current_collision_rect(self):
        if self.game_context.current_object:
            self.game_context.current_object.display_collision_rect()
        elif self.game_context.inventory.current_object:
            self.game_context.inventory.current_object.display_collision_rect()

    def draw_objects(self):
        for obj in self.objects:
            if obj.displayed:
                obj.draw()


    def draw_background(self):
        self.game_context.screen.blit(self.background, (0, 0))


    def display(self):
        self.resize_wall()
        self.draw_background()
        self.draw_objects()
        self.display_current_collision_rect()
        #self.display_collision_rects()
#--------------------------------------------------------

    # NOTE: can be redefined in child classes
    def update(self, event):
        for obj in self.objects:
            if obj.displayed:
                obj.update(event) # interactions relative to each object
