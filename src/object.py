import pygame
from pathlib import Path
from utils import get_collision_rects, convert_to_pygame_rect_list

class Game_object(pygame.sprite.Sprite):

    def __init__(self,
                 game_context,
                 object_name : str,
                 image_path : str,
                 rect : pygame.Rect,
                 collisions : list[pygame.Rect],
                 collision_index : int = -1,
                 movable : bool = True,
                 displayed : bool = True
                 ):
        super().__init__()

        self.name = object_name
        self.game_context = game_context
        self.screen = self.game_context.screen

        self.image_path = Path(image_path)
        self.image = pygame.image.load(Path(self.game_context.root_dir / self.image_path))
        self.raw_image = self.image

        parts = self.image_path.parts
        self.image_id = (Path(*parts[-7:])).as_posix()
        self.image_name = str(self.image_path.name)

        self.collision_rects = collisions
        self.raw_collision_rects = self.collision_rects.copy()
        self.collision_rect_id = collision_index # which collision rect the object is in

        self.rect = rect
        self.raw_rect = self.rect
        if self.collision_rect_id != -1 :
            self.valid_rect = self.collision_rects[self.collision_rect_id]
        else:
            self.valid_rect = self.rect.copy()
        self.displayed = displayed
        self.movable = movable
        self.interactible = False


    def replace(self):
        self.raw_rect.center = self.valid_rect.center


    def drop_in_collision_rect(self, collision_index):
        self.raw_rect.center = self.raw_collision_rects[collision_index].center
        self.valid_rect = self.raw_collision_rects[collision_index]
        self.collision_rect_id = collision_index
        #print(f"Dropped {self.name} in collision rect {collision_index}")


    def drop_at_pos(self, x, y) -> bool: # try to fit the object in one of the collision rects, returns True if it fits, False otherwise
            #print(f"Trying to drop {self.name} at ({x}, {y})")
            return_code = False
            point_rect = pygame.Rect(int(x), int(y), 1, 1)
            collision_index = point_rect.collidelist(self.collision_rects)
            if collision_index != -1:
                self.drop_in_collision_rect(collision_index)
                return_code = True

            else:
                self.replace()

            return return_code


    def resize_image (self):
        delta = self.game_context.current_wall.delta
        self.image = pygame.transform.scale(self.raw_image,
            (int(delta * self.raw_rect.w), int(delta * self.raw_rect.h))
        )
        self.rect = pygame.Rect(delta * self.raw_rect.x, delta * self.raw_rect.y, delta * self.raw_rect.w, delta * self.raw_rect.h)


    def resize_collision_rects(self):
        delta = self.game_context.current_wall.delta
        for i in range(len(self.collision_rects)):
            raw_collision_rect = self.raw_collision_rects[i]
            self.collision_rects[i] = pygame.Rect(delta * raw_collision_rect.x, delta * raw_collision_rect.y, delta * raw_collision_rect.w, delta * raw_collision_rect.h)


    def change_collision_rects(self, collision_layers_dir):
        new_collision_rects = get_collision_rects(collision_layers_dir, self.name)
        converted_collision_rects = convert_to_pygame_rect_list(new_collision_rects)
        self.collision_rects = converted_collision_rects
        self.raw_collision_rects = converted_collision_rects.copy()


    def display_collision_rect(self):
        for rect in self.collision_rects:
            temp_surface = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
            pygame.draw.rect(temp_surface, (255, 0, 0, 128), temp_surface.get_rect())
            self.game_context.screen.blit(temp_surface, rect)


    def draw(self): # draw every entities and the non entities
        if self.displayed:
            self.game_context.screen.blit(self.image, self.rect)


    def update(self, event):
        pass


    def handle_left_click(self, event):
        self.game_context.drop_current_object(event)