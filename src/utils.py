import json
import pygame
from pathlib import Path

def load_json_file(json_path: Path):
    if json_path.exists():
        with open(json_path, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {}
    else:
        raise Exception("load_json_file error : invalid path")
        return {}

def save_data_in_json(data: dict, json_path: Path):
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)