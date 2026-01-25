import pygame
import sys
from pathlib import Path
import json
from objects.vase import Vase
from objects.digicode import Digicode


BLACK = (0, 0, 0)
WHITE = (200, 200, 200)

pygame.init()


class Inventory:
    def __init__(self, game_context, x, y, rows, cols, block_size, center):
        self.game_context = game_context
        self.root_dir = Path(__file__).resolve().parent

        self.raw_x = x
        self.x = int(self.raw_x * self.game_context.delta)
        self.raw_y = y
        self.y = int(self.raw_y * self.game_context.delta)

        self.rows = rows
        self.cols = cols

        self.raw_block_size = block_size
        self.block_size = int(self.raw_block_size * self.game_context.delta)

        self.slots = [[None for _ in range(cols)] for _ in range(rows)]
        self.display = False
        self.center = center

        self.last_row, self.last_col = 0, 0
        self.mouse_x, self.mouse_y = 0, 0

        # load images
        self.images = {}

        for name in ["temp1.png", "temp2.png"]:
            final_path = self.ensure_inventory_image(name)

            inventory_key = f"src/minigames/inventory/images/{name}"

            self.images[inventory_key] = [
                pygame.transform.scale(
                    pygame.image.load(final_path),
                    (int(block_size * 0.9), int(block_size * 0.9))
                ),
                str(final_path)
            ]

        # Default pos
        self.slots[0][0] = "src/minigames/inventory/images/temp1.png"
        self.slots[0][1] = "src/minigames/inventory/images/temp2.png"

        self.current_item = None

        self.init_images()


    def ensure_inventory_image(self, filename):
        origin_path = self.root_dir / "images" / "origin" / filename
        target_path = self.root_dir / "images" / filename

        if not origin_path.exists():
            raise FileNotFoundError(f"Image source manquante : {origin_path}")

        if not target_path.exists():
            target_path.parent.mkdir(parents=True, exist_ok=True)
            image = pygame.image.load(origin_path).convert_alpha()
            pygame.image.save(image, target_path)
            print(f"Image inventaire created : {target_path}")

        return target_path


    def init_images(self):
        json_path = Path(self.root_dir / "objects_info.json")
        objects_data = self.open_json(json_path)

        # delete extra keys
        expected_keys = {
            p for p in self.images
        }

        for key in list(objects_data.keys()):
            if key not in expected_keys:
                del objects_data[key]

        for key in list(self.images):
            save_path = Path(Path(self.game_context.root_dir) / key).as_posix()

            if key not in objects_data:
                image = pygame.image.load(save_path).convert_alpha()
                bbox = 0, 0, image.get_width(), image.get_height()
                pygame.image.save(image, save_path)
                print(f"Cropped image saved to {save_path}")

                # put x, y, w, h in objects_data
                objects_data[key] = bbox

        # delete extra images
        self.delete_extra_images(objects_data)

        # save the data in the json file
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(objects_data, f, indent=4, ensure_ascii=False)


    def update(self):
        self.block_size = int(self.raw_block_size * self.game_context.delta)

        if self.center:
            mid_block = len(self.slots[0]) // 2 + len(self.slots[0]) % 2
            self.x = self.game_context.screen.get_width() // 2 - mid_block * self.block_size
        else:
            self.x = int(self.raw_x * self.game_context.delta)

        self.y = int(self.raw_y * self.game_context.delta)

        for key in self.images:
            self.images[key][0] = self.resize_in_inventory(
                (Path(self.game_context.root_dir) / key).as_posix()
            )

        self.draw_grid()
        self.draw_items()

        json_path = Path(self.root_dir / "objects_info.json")

        # Display current item
        if self.current_item:  # if not None
            mx, my = pygame.mouse.get_pos()
            self.game_context.screen.blit(
                self.images[self.current_item][0],
                (mx - 0.4 * self.block_size, my - 0.4 * self.block_size)
            )


    def resize_in_inventory(self, path):
        return pygame.transform.scale(
            pygame.image.load(path),
            (self.block_size * 0.9, self.block_size * 0.9)
        )


    def handle_event(self):
        pos = self.game_context.event.pos
        self.mouse_x, self.mouse_y = pos

        # Area in inventory
        if (
            self.x <= self.mouse_x < self.x + self.cols * self.block_size and
            self.y <= self.mouse_y < self.y + self.rows * self.block_size
        ):
            col = (self.mouse_x - self.x) // self.block_size
            row = (self.mouse_y - self.y) // self.block_size

            slot = self.slots[row][col]

            if not self.current_item:
                if slot:
                    self.current_item = slot

                external_obj = self.game_context.current_item

                # Put object in inventory
                if external_obj:
                    self.put_object_in_inventory(external_obj, row, col)

                # Take object from inventory
                else:
                    self.slots[row][col] = None

                self.last_row, self.last_col = row, col

            # Swap object in inventory
            elif self.current_item:
                self.slots[row][col], self.current_item = (
                    self.current_item,
                    self.slots[row][col]
                )

            print("click inventory")

        # Drop object out of inventory
        elif self.current_item != None:
            self.inventory_drop()
            self.game_context.current_wall.sort_entities_by_image_name()


    def put_object_in_inventory(self, external_obj, row, col):
        wall_save_path = f"{self.root_dir}/images/{external_obj.image_name}"
        inventory_save_path = f"src/minigames/inventory/images/{external_obj.image_name}"

        if not Path(wall_save_path).exists():
            pygame.image.save(external_obj.image, wall_save_path)  # put image in inventory directory

        self.images[inventory_save_path] = [
            self.resize_in_inventory(wall_save_path),
            str(wall_save_path)
        ]

        self.slots[row][col] = inventory_save_path

        json_path = Path(self.root_dir / "objects_info.json")
        json_path_wall = Path(self.game_context.current_wall.root_dir / "images/objects_info.json")

        objects_data = self.open_json(json_path)
        objects_data_wall = self.open_json(json_path_wall)

        cropped_object_dir = Path(self.game_context.current_wall.root_dir / "images/cropped_objects")
        object_path = Path(Path(self.game_context.root_dir) / external_obj.image_id)
        save_path = Path(cropped_object_dir / object_path.name)
        origin_path = Path(self.images[inventory_save_path][1])

        image = pygame.image.load(origin_path).convert_alpha()
        bbox = (
            objects_data_wall[external_obj.image_id][0],
            objects_data_wall[external_obj.image_id][1],
            image.get_width(),
            image.get_height()
        )

        x, y, w, h = bbox

        if save_path.exists():
            save_path.unlink()

        del objects_data_wall[external_obj.image_id]

        # put x, y, w, h in objects_data
        objects_data[inventory_save_path] = bbox

        if inventory_save_path not in objects_data:
            objects_data[inventory_save_path] = objects_data_wall[external_obj.image_id]

        print(self.images)

        self.save_json(json_path, objects_data)
        self.save_json(json_path_wall, objects_data_wall)

        for sprite in self.game_context.current_wall.entities.sprites():
            if isinstance(sprite, Vase) and sprite.image_path == external_obj.image_path:
                self.game_context.current_wall.entities.remove(sprite)

        self.game_context.dragging = False
        self.game_context.current_item = None
        self.game_context.dragging = False


    def inventory_drop(self):
        object_path = Path(Path(self.game_context.root_dir) / self.current_item)
        cropped_object_dir = Path(self.game_context.current_wall.root_dir / "images/cropped_objects")
        object_layers_path = list((object_path.parent).iterdir())

        # load le JSON
        json_path = Path(self.root_dir / "objects_info.json")
        json_path_wall = Path(self.game_context.current_wall.root_dir / "images/objects_info.json")

        objects_data = self.open_json(json_path)
        objects_data_wall = self.open_json(json_path_wall)

        parts = cropped_object_dir.parts
        new_path_cropped = (Path(*parts[-6:]) / object_path.name).as_posix()

        if self.current_item != str(self.current_item):
            self.current_item = (self.current_item).as_posix()

        save_path = Path(cropped_object_dir / object_path.name)
        origin_path = Path(self.images[f"src/minigames/inventory/images/{object_path.name}"][1])

        image = pygame.image.load(origin_path).convert_alpha()
        delta = self.game_context.current_wall.delta

        bbox = (
            int(self.mouse_x / self.game_context.current_wall.delta - (image.get_width() / delta) / 2),
            int(self.mouse_y / delta - (image.get_height() / delta) / 2),
            int(image.get_width() / delta),
            int(image.get_height() / delta)
        )

        x, y, w, h = bbox

        pygame.image.save(image, save_path)
        print(f"Image saved to {save_path}")

        objects_data_wall[new_path_cropped] = bbox

        # create the sprite
        sprite_rect_tupple = objects_data_wall[new_path_cropped]
        dim = (
            sprite_rect_tupple[0],
            sprite_rect_tupple[1],
            sprite_rect_tupple[2],
            sprite_rect_tupple[3]
        )

        name_without_layer = object_path.name
        
        if name_without_layer == "table.png" or "cropped_ui_test.png" or "cropped_vase.png":  # TODO: ALWAYS TRUE
            self.game_context.current_wall.entities.add(
                Vase(self.game_context, save_path, pygame.Rect(dim), [])
            )

        del objects_data[self.current_item]

        # save the data in the json file
        self.save_json(json_path, objects_data)
        self.save_json(json_path_wall, objects_data_wall)

        del self.images[self.current_item]

        self.delete_extra_images(objects_data)

        self.current_item = None
        self.game_context.mouse_enabled = False


    def delete_extra_images(self, objects_data):
        json_image_keys = set(objects_data.keys())
        object_dir = Path(self.root_dir / "images")

        for image_file in object_dir.iterdir():
            if not image_file.is_file():
                continue

            if image_file.suffix.lower() != ".png":
                continue

            src_index = image_file.parts.index("src")
            relative_path = Path(*image_file.parts[src_index:]).as_posix()

            if relative_path not in self.images:
                print(f"Removing extra inventory image: {relative_path}")
                image_file.unlink()


    def draw_grid(self):
        for row in range(self.rows):
            for col in range(self.cols):
                rect = pygame.Rect(
                    self.x + col * self.block_size,
                    self.y + row * self.block_size,
                    self.block_size,
                    self.block_size
                )
                pygame.draw.rect(self.game_context.screen, WHITE, rect, 2)


    def draw_items(self):
        # print(self.images)
        for row in range(self.rows):
            for col in range(self.cols):
                item = self.slots[row][col]
                if item:  # Not None
                    self.game_context.screen.blit(
                        self.images[item][0],
                        (
                            self.x + col * self.block_size + 0.05 * self.block_size,
                            self.y + row * self.block_size + 0.05 * self.block_size
                        )
                    )


    def create_sub_surface(self, x, y, w, h, surface):
        return surface.subsurface(pygame.Rect(x, y, w, h)).copy()


    def save_json(self, path, data):
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)


    def open_json(self, path):
        if path.exists():
            with open(path, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = {}
                return data
        else:
            raise Exception("open_json error : invalid path")