import json
import pygame
from pathlib import Path


#---------------------JSON-----------------------------------
#
def load_json_file(json_path: Path) -> dict:
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                print(f"load_json_file error: JSONDecodeError on {json_path.as_posix()}")
                return {}
    except Exception as e:
        print(f"load_json_file error: {e} on {json_path.as_posix}")
        return {}


def save_data_in_json(data: dict, json_path: Path):
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def clear_json(json_path):
    with open(json_path, "w", encoding="utf-8") as f:
        f.write("{}")


#----------------------CONVERSION--------------------------
def convert_to_pygame_rect(rect) -> pygame.Rect | None:
    if rect:
        return pygame.Rect(rect)
    else:
        return None


def convert_to_pygame_rect_list(rect_list) -> list[pygame.Rect]:
    pygame_rect_list = []
    for rect in rect_list:
        #print(rect_list)
        if rect:
            pygame_rect_list.append(pygame.Rect(rect))
    return pygame_rect_list


def convert_to_tuple_rect(rect) -> tuple[int, ...]:
    return tuple(rect)


def convert_to_tuple_rect_list(rect_list) -> list[tuple[int, ...]]:
    tuple_rect_list = []
    for rect in rect_list:
        tuple_rect_list.append(tuple(rect))
    return tuple_rect_list


#------------------------------------------------------------------

#returns the list of the paths of all the collision layers of an object
def load_collision_layers_path(collision_layers_dir: Path, object_name: str) -> list[Path]:
    collision_layers_path = list(collision_layers_dir.iterdir())

    valid_collision_layers_path = []
    all_found = False
    layer_count = 0
    while not all_found:
        layer_name = f"{object_name}_pos{layer_count}.png"
        layer_path = Path(collision_layers_dir / layer_name)
        if layer_path in collision_layers_path:
            valid_collision_layers_path.append(layer_path)
            layer_count +=1
        else:
            all_found = True
    return valid_collision_layers_path


def get_collision_rects(collision_layers_dir : Path, object_name: str) -> list[tuple[int, int, int, int]]: # TODO: can we move this to utils ?
    collision_rects = []
    collision_layers_path = load_collision_layers_path(collision_layers_dir, object_name)
    for path in collision_layers_path:
        collision_layer = pygame.image.load(path).convert_alpha()
        rect = get_bounding_box(collision_layer)
        collision_rects.append(rect)
    return collision_rects

# creates a cropped version of an image and return its dimentions
def create_cropped_object(raw_image_path, save_path):
    image = pygame.image.load(raw_image_path).convert_alpha()
    bbox = get_bounding_box(image)
    if bbox is None:
        print(f"No visible pixels in {raw_image_path}")
        return

    x, y, w, h = bbox
    cropped_image = create_sub_surface(x, y, w, h, image)

    pygame.image.save(cropped_image, save_path)
    print(f"Cropped image saved to {save_path}")

    return bbox


def get_bounding_box(surface: pygame.Surface) -> tuple[int, int, int, int] | None:
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


def create_sub_surface(
     x, y, w, h, surface):
    return surface.subsurface(pygame.Rect(x, y, w, h)).copy()


#---------------------CREATE OBJECT-------------------------------------
def create_object(obj_name, game_context, img_path, rect, collision_rects,
                  current_collision_id, default_collision, default_wall):
    # local import to avoid circular import
    from objects.padlock import Padlock
    from objects.padlock_door import Padlock_door
    from objects.digicode import Digicode
    from objects.Connect4_Beta import Connect
    from objects.grid.magnet import Magnet
    from objects.grid.key import Key
    from objects.grid.grid import Grid
    from objects.closet import Closet
    from objects.borne import Borne
    from objects.plank import Plank
    from objects.book import Book
    from objects.library import Library
    from objects.screwdriver import Screwdriver
    from objects.axe import Axe
    from object import Game_object

    if obj_name == "calculator":
        return Digicode(game_context, obj_name, img_path, rect, "1234")

    elif obj_name in ["vase", "vase2"]:
        return Game_object(game_context, obj_name, img_path, rect,
                      collision_rects, current_collision_id, True, True,
                      default_collision, default_wall)

    elif obj_name == "frame":
        return Game_object(game_context, obj_name, img_path, rect,
                           collision_rects, current_collision_id,
                           default_collision, default_wall)

    elif obj_name == "table":
        return Game_object(game_context, obj_name, img_path, rect,
                           collision_rects, current_collision_id, False, True,
                           default_collision, default_wall)

    elif obj_name == "connect4":
        return Connect(game_context, obj_name,img_path, rect, 0)

    elif obj_name == "magnet":
        return Magnet(game_context, obj_name, img_path, rect, collision_rects,
                      current_collision_id)

    elif obj_name == "key":
        return Key(game_context, obj_name, img_path, rect, collision_rects,
                   current_collision_id)

    elif obj_name == "clock":
        return Game_object(game_context, obj_name, img_path, rect, collision_rects,
                           current_collision_id, True, True,
                            default_collision, default_wall)

    elif obj_name == "grid_wall":
        return Grid(game_context, obj_name, img_path, rect,
                      collision_rects, current_collision_id, True)

    elif obj_name == "grid":
        return Grid(game_context, obj_name, img_path, rect,
                      collision_rects, current_collision_id, False)

    elif obj_name == "closed_closet":
        return Closet(game_context, obj_name, img_path, rect,
                      collision_rects, current_collision_id, True)

    elif obj_name == "opened_closet":
        return Closet(game_context, obj_name, img_path, rect,
                      collision_rects, current_collision_id, False)

    elif "obj_in_closet" in obj_name:

        if "screwdriver" in obj_name:
            return Screwdriver(game_context, obj_name, img_path, rect,
                        collision_rects, current_collision_id,
                        default_collision, default_wall)
        temp = Game_object(game_context, obj_name, img_path, rect,
                      collision_rects, current_collision_id, True, True,
                      default_collision, default_wall)
        temp.displayed = False
        return temp

    elif obj_name == "borne":
        return Borne(game_context, obj_name, img_path, rect,
                      collision_rects, current_collision_id)

    elif obj_name == "padlock":
        return Padlock(game_context, obj_name, img_path, rect,
                           collision_rects, current_collision_id)

    elif obj_name == "padlock_door":
        return Padlock_door(game_context, obj_name, img_path, rect,
                           collision_rects, current_collision_id)

    elif "plank" in obj_name:
        return Plank(game_context, obj_name, img_path, rect,
                      collision_rects, current_collision_id)

    elif obj_name == "library":
        return Library(game_context, obj_name, img_path, rect,
                      collision_rects, current_collision_id)

    elif obj_name == "book_closed":
        return Book(game_context, obj_name, img_path, rect,
                      collision_rects, current_collision_id, True, False)

    elif obj_name == "book_opened":
        return Book(game_context, obj_name, img_path, rect,
                      collision_rects, current_collision_id, False, False)

    elif "book_bait" in obj_name:
        return Book(game_context, obj_name, img_path, rect,
                      collision_rects, current_collision_id, False, True)
    elif obj_name == "axe":
        return Axe(game_context, obj_name, img_path, rect,
                      collision_rects, current_collision_id, default_collision, default_wall)

    else:
        return Game_object(game_context, obj_name, img_path, rect,
                           collision_rects, current_collision_id, False, True,
                            default_collision, default_wall)
        #print("create_object error: invalid object name")
