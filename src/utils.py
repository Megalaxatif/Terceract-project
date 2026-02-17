import json
import pygame
from pathlib import Path
from objects.vase import Vase
from objects.digicode import Digicode
from objects.Connect4_Beta import Connect

def create_object(obj_name, game_context, img_path, rect, collision_rects, current_collision_id):

    if obj_name == "calculator":
        return Digicode(game_context, obj_name, img_path, rect, "1234")

    elif obj_name in ["vase", "vase2"]:
        return Vase(game_context, obj_name, img_path, rect, collision_rects, current_collision_id)

    elif obj_name == "frame":
        return Vase(game_context, obj_name, img_path, rect, collision_rects, current_collision_id)

    elif obj_name == "table":
        return Vase(game_context, obj_name, img_path, rect, collision_rects, current_collision_id)

    elif obj_name == "connect4":
        return Connect(game_context, obj_name,img_path, rect, 0)

    else:
        print("create_object error: invalid object name")


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

def create_sub_surface(
     x, y, w, h, surface):
    return surface.subsurface(pygame.Rect(x, y, w, h)).copy()
