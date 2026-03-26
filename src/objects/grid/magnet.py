from pathlib import Path

import pygame
from object import Game_object
from objects.grid.grid import Grid
from utils import convert_to_pygame_rect_list, get_collision_rects


class Magnet(Game_object):
    def __init__(
        self,
        game_context,
        object_name: str,
        image_path: str,
        rect: pygame.Rect,
        collisions: list[pygame.Rect],
        collision_index: int = -1,
    ):
        super().__init__(
            game_context, object_name, image_path, rect, collisions, collision_index, True, False
        )
        self.initial_pos = self.rect.x, self.rect.y
        self.grid_displayed = False
        # self.interactible = True
        self.key_given = False
        self.default_collision = self.collision_rects[-1]
        self.raw_default_collision = self.raw_collision_rects[-1]
        self.final_collision = self.collision_rects[-2]
        self.collision_rects_wall = self.collision_rects[:-2].copy()
        self.in_grid = False

    def display_collision_rect(self):
        if self.display_collision_rect_bool:
            if self.default_collision:
                temp_surface = pygame.Surface(
                    (
                        self.default_collision.width
                        * self.game_context.current_wall.delta,
                        self.default_collision.height
                        * self.game_context.current_wall.delta,
                    ),
                    pygame.SRCALPHA,
                )
                pygame.draw.rect(
                    temp_surface, (255, 0, 0, 128), temp_surface.get_rect()
                )
                temp_rect = [
                    v * self.game_context.current_wall.delta
                    for v in self.default_collision
                ]
                self.game_context.screen.blit(temp_surface, temp_rect)

    def drop_in_collision_rect(self, collision_index):
        if self.raw_default_collision:
            self.raw_rect.center = self.raw_default_collision.center
            self.valid_rect = self.raw_default_collision
        self.collision_rect_id = collision_index
        # print(f"Dropped {self.name} in collision rect {collision_index}")

    def drop_at_pos(
        self, x, y
    ) -> bool:  # try to fit the object in one of the collision rects, returns True if it fits, False otherwise
        # print(f"Trying to drop {self.name} at ({x}, {y})")
        return_code = False
        point_rect = pygame.Rect(int(x), int(y), 1, 1)
        temp_rect = pygame.Rect(
            [
                int(v * self.game_context.current_wall.delta)
                for v in self.default_collision
            ]
        )
        print(temp_rect)
        collision_index = point_rect.collidelist([temp_rect])
        if self.display_collision_rect_bool:
            if collision_index != -1:
                self.drop_in_collision_rect(collision_index)
                return_code = True
            elif self.game_context.inventory.current_object:
                return False
            else:
                self.replace()

        return return_code

    def update(self, event):
        # TODO : seuls pb restants : rectangles de collision visibles, clé apparait pas a l'arrivee, l'aimant se pose encore dans les rects autres
        # print(f"Ongoing: {self.ongoing} / key given : {self.key_given} / mousebuttonup : {event.type == pygame.MOUSEBUTTONUP}"

        if self.in_grid:
            pos = (
                pygame.mouse.get_pos()[0] / self.game_context.current_wall.delta,
                pygame.mouse.get_pos()[1] / self.game_context.current_wall.delta,
            )
            point_rect = pygame.Rect(pos[0], pos[1], 1, 1)

            if (
                point_rect.collidelist(self.collision_rects_wall) != -1
            ) and self == self.game_context.current_object:
                self.game_context.current_object = None
                self.raw_rect.x, self.raw_rect.y = (
                    self.initial_pos
                )  # ca remet magnet à sa place de départ

    def handle_click(self, event):
        pos = (
            event.pos[0],
            event.pos[1],
        )

        print("handle click")

        start_rect = pygame.Rect(
            [
                int(v * self.game_context.current_wall.delta)
                for v in self.default_collision
            ]
        )
        end_rect = pygame.Rect(
            [
                int(v * self.game_context.current_wall.delta)
                for v in self.final_collision
            ]
        )

        if self.in_grid:
            if end_rect.collidepoint(pos):
                self.key_given = True  # give the key
                self.displayed = False

                for obj in self.game_context.current_wall.objects:
                    if obj.name == "key":
                        obj.key_given = (
                            True  # ca fait apparaitre la clé à l'arrivée (marche pas)
                        )
                        obj.displayed = True

                self.game_context.drop_current_object(event)

            elif not end_rect.collidepoint(pos) and not start_rect.collidepoint(pos):
                self.raw_rect.x, self.raw_rect.y = self.initial_pos
                self.game_context.drop_current_object(event)

            print(end_rect)
            print(pos)

        elif (
            self == self.game_context.inventory.current_object
            and start_rect.collidepoint(pos)
        ):
            print("here")
            wall = self.game_context.current_wall.objects
            for obj in wall:
                if isinstance(obj, Grid) and not obj.on_wall and obj.displayed:
                    self.in_grid = True
                    print(self.in_grid)

        if not start_rect.collidepoint(pos):
            self.raw_rect.x, self.raw_rect.y = self.initial_pos
            self.game_context.drop_current_object(event)
            print(pos)
            print(start_rect)

        else:
            wall = self.game_context.current_wall.objects
            temp = None
            for obj in wall:
                if isinstance(obj, Grid) and not obj.on_wall:
                    temp = obj.displayed
            if temp:
                self.in_grid = True
