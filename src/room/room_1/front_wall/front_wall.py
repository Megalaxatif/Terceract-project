import pygame
import json
from wall_parent import Wall
from pathlib import Path
from ...objects.vase import Vase

root_dir = Path(__file__).resolve().parent

class Front_wall_R1(Wall):
    def __init__(self, game):
        super().__init__(game, f"{game.root_dir}/assets/images/next_door.png", [f"{root_dir}/images/table_test.png", f"{root_dir}/images/ui_test.png"], root_dir)
        
        self.wall_parent = Wall
        
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
        
        # Init les objets displayed sur le mur
        self.vase = Vase(f"{root_dir}/images/table_test.png", game_data[f"{root_dir.relative_to(root_dir.parents[1]).as_posix()}/images/table_test.png"])
        self.ui_test = Vase(f"{root_dir}/images/ui_test.png", game_data[f"{root_dir.relative_to(root_dir.parents[1]).as_posix()}/images/ui_test.png"])
        print(self.ui_test.cropped_image)
        
        self.interactable_obj = [self.vase, self.ui_test]
        self.displayed_obj = [self.vase, self.ui_test]
        
    def display_objects(self):
        if self.displayed_obj:
            for obj in self.displayed_obj:
                self.game_context.screen.blit(obj.cropped_image, (self.delta * obj.x, self.delta * obj.y))
        
    def update(self):
        self.resize_images(self.displayed_obj)
        self.game_context.screen.blit(self.background, (0, 0)) 
        self.display_objects()
        mx, my = pygame.mouse.get_pos()[0] / self.delta, pygame.mouse.get_pos()[1] / self.delta
        for obj in self.interactable_obj:
            if obj.dragging:
                obj.x, obj.y = (mx - obj.w/2), (my - obj.h/2)
        
        
class Table:
    def __init__(self, wall):
        pass