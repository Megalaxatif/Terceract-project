import json
import socket
import sys
import threading
from json.decoder import JSONDecodeError
from pathlib import Path

from numpy._core.numeric import False_
import pygame
from dialogues import Dialogue
from minigames import *
from network import Network_manager
from room import *
from sound import SoundManager

ROOM_1 = 0
ROOM_2 = 1
ROOM_3 = 2
ROOM_4 = 3
ROOM_5 = 4
BACK_WALL = 0
LEFT_WALL = 1
FRONT_WALL = 2
RIGHT_WALL = 3

CUSTOM_DROP_EVENT = pygame.USEREVENT + 1


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.delta_h = 1
        self.delta_w = 1
        self.delta = 1
        self.last_delta = 1
        self.height = self.screen.get_height()
        self.width = self.screen.get_width()
        self.fullscreen = True
        self.FPS = 60
        self.clock = pygame.time.Clock()
        self.game_running = True
        self.root_dir = Path(__file__).resolve().parent.parent
        self.raw_stash = pygame.image.load(Path(f"{self.root_dir}/assets/gui/stash.png")).convert_alpha()
        self.stash = self.raw_stash
        self.stash_raw_rect = self.raw_stash.get_rect()
        self.stash_rect = self.stash_raw_rect
        self.game_data = {}  # for network
        self.game_data_path = f"{self.root_dir}/data/game_data.json"
        self.event = None
        self.font = pygame.font.Font(None, 30)
        self.name = "game"
        self.current_mini_game = "game"

        self.network_manager = Network_manager(self)
        self.sound_manager = SoundManager(self)
        self.mouse_hover_image = pygame.image.load(f"{self.root_dir}/assets/gui/mouse_hover.png").convert_alpha()
        self.mouse_hover_image = pygame.transform.scale(self.mouse_hover_image, (40, 40))

        self.launch_solo() #launch solo by default

        self.create_all_walls()

        self.exit_door_opened = True
        self.room_1_unlocked = True
        self.room_2_unlocked = True
        self.room_3_unlocked = True
        self.room_4_unlocked = True

        self.current_room_id = 0
        self.current_wall_id = 0
        self.current_wall = self.room_list[self.current_room_id][self.current_wall_id]
        self.current_object = None
        self.other_player_object_name = ""
        self.other_player_inventory_object_name = ""  # TODO
        self.other_player_inventory_object = None
        self.mini_game_menu = Menu(self)
        self.inventory = Inventory(self, 40, 615, 1, 10, 100, True)  # Create inventory (it's a line here)
        self.laboratory_game = Laboratory(self)
        self.dialogues = Dialogue(self)

        self.end_screen_reference = self.get_reference("end_screen")

        self.initialize_all_objects()


    def create_all_walls(self):
        self.back_wall_R1 = Back_wall_R1(self, 0, 0)
        self.left_wall_R1 = Left_wall_R1(self, 0, 1)
        self.front_wall_R1 = Front_wall_R1(self, 0, 2)
        self.right_wall_R1 = Right_wall_R1(self, 0, 3)

        self.R1 = [
            self.back_wall_R1,
            self.left_wall_R1,
            self.front_wall_R1,
            self.right_wall_R1,
        ]

        self.back_wall_R2 = Back_wall_R2(self, 1, 0)
        self.left_wall_R2 = Left_wall_R2(self, 1, 1)
        self.front_wall_R2 = Front_wall_R2(self, 1, 2)
        self.right_wall_R2 = Right_wall_R2(self, 1, 3)

        self.R2 = [
            self.back_wall_R2,
            self.left_wall_R2,
            self.front_wall_R2,
            self.right_wall_R2,
        ]

        self.back_wall_R3 = Back_wall_R3(self, 2, 0)
        self.left_wall_R3 = Left_wall_R3(self, 2, 1)
        self.front_wall_R3 = Front_wall_R3(self, 2, 2)
        self.right_wall_R3 = Right_wall_R3(self, 2, 3)

        self.R3 = [
            self.back_wall_R3,
            self.left_wall_R3,
            self.front_wall_R3,
            self.right_wall_R3,
        ]

        self.back_wall_R4 = Back_wall_R4(self, 3, 0)
        self.left_wall_R4 = Left_wall_R4(self, 3, 1)
        self.front_wall_R4 = Front_wall_R4(self, 3, 2)
        self.right_wall_R4 = Right_wall_R4(self, 3, 3)

        self.R4 = [
            self.back_wall_R4,
            self.left_wall_R4,
            self.front_wall_R4,
            self.right_wall_R4,
        ]

        self.back_wall_R5 = Back_wall_R5(self, 4, 0)
        self.left_wall_R5 = Left_wall_R5(self, 4, 1)
        self.front_wall_R5 = Front_wall_R5(self, 4, 2)
        self.right_wall_R5 = Right_wall_R5(self, 4, 3)

        self.R5 = [
            self.back_wall_R5,
            self.left_wall_R5,
            self.front_wall_R5,
            self.right_wall_R5,
        ]

        self.room_list = [self.R1, self.R2, self.R3, self.R4, self.R5]


    def is_obj_in_wall(self, target_name, wall_id, room_id):
        target_wall = self.room_list[room_id][wall_id]
        for object in target_wall.objects:
            if object.name == target_name:
                return True
        return False


    def quit(self):
        self.game_running = False
        self.network_manager.quit()
        pygame.quit()
        sys.exit()


    def reset_game(self):
        for room in self.room_list:
            for wall in room:
                wall.reset()
        self.inventory.reset()
        self.quit()


    def initialize_all_objects(self):  # this function finishes the initialization of the objects when all the variable
        # they would need have been created (useful for the axe for examble)
        for room in self.room_list:
            for wall in room:
                for obj in wall.objects:
                    obj.initialize()
        for line in self.inventory.slots:
            for obj in line:
                if obj:
                    obj.initialize()


    def save_game(self):  # save all the game data
        if self.network_manager.is_host:
            print("save game")
            for room in self.room_list:
                for wall in room:
                    wall.save_objects_data()
            print("save inventory")
            self.inventory.save()


    def launch_solo(self):
        self.network_manager.is_host = True
        self.network_manager.setup_server()
        incoming_data_thread = threading.Thread(target=self.network_manager.network_manager, daemon=True)
        incoming_data_thread.start()


    def launch_duo(self, ip: str, port: int):
        try:
            self.network_manager.client.connect((ip, port))
        except socket.gaierror:
            print("launch_duo: Error 4: impossible to find a valid host with the information given")
            return 4
        except Exception as e:
            print("launch_duo: Error 1", e)
            return 1
        else:
            try:
                raw_data = self.network_manager.receive_package_list()
                if not raw_data:
                    print("launch_duo: Error 5: no data to decode")
                    self.network_manager.handle_disconnection()
                    return 5

                data = raw_data[0].decode("utf-8")

            except Exception as e:
                print("launch_duo: Error 2", e)
                self.network_manager.handle_disconnection()
                return 2
            else:
                try:
                    self.game_data = json.loads(data)

                except JSONDecodeError as e:
                    print("launch_duo Error 3: ", e)
                    self.network_manager.handle_disconnection()
                    return 3
                else:
                    # just a way to make sure that we start on the exit door to avoid any crash when playing in duo
                    while self.current_wall_id != 0:
                        self.change_wall(-1)
                    while self.current_room_id != 0:
                        self.change_room()
                    self.network_manager.is_connected = True
                    self.network_manager.is_host = False
                    self.network_manager.server.close() # close the server socket definitively
                    #------- recreate all the things that depends on wether we're host or client ------
                    # recreate the walls. Since we changed is_host to False above, they will be created
                    # with the data of the other player
                    self.create_all_walls()
                    self.inventory = Inventory(self, 40, 615, 1, 10, 100, True)  # reset the inventory
                    self.initialize_all_objects()
        return 0


    def switch_back_to_solo_mode(self):
        self.network_manager.is_connected = False
        self.other_player_object_name = ""
        self.other_player_inventory_object_name = ""
        self.network_manager.reset_client()


    def change_room(self):  # change the room we are in
        # create a custom event
        mouse_x, mouse_y = pygame.mouse.get_pos()
        custom_event = pygame.event.Event(
            CUSTOM_DROP_EVENT, {"pos": (mouse_x, mouse_y)}
        )

        if self.current_wall_id == FRONT_WALL and self.current_room_id < ROOM_5:
            if self.is_room_unlocked(self.current_room_id):
                self.current_room_id += 1
                self.drop_current_object(custom_event)
                self.change_current_wall()
            else:
                self.sound_manager.play_sound("locked_door")

        elif self.current_wall_id == BACK_WALL and self.current_room_id > 0:
            self.current_room_id -= 1
            self.drop_current_object(custom_event)
            self.change_current_wall()

        elif self.current_wall_id == BACK_WALL and self.current_room_id == 0 and self.exit_door_opened:
            self.current_mini_game = "end_screen"

        else:
            print("change_room : Error, impossible to go in that direction")
            return 1
        return 0


    def change_wall(self, direction: int):  # change the wall we are facing : -1 to go right and 1 to go left

        # create a custom event
        mouse_x, mouse_y = pygame.mouse.get_pos()
        custom_event = pygame.event.Event(
            CUSTOM_DROP_EVENT, {"pos": (mouse_x, mouse_y)}
        )

        self.current_wall_id = (self.current_wall_id + direction) % 4

        self.drop_current_object(custom_event)
        self.change_current_wall()


    def change_current_wall(self):  # update the reference to the current wall
        self.current_wall = self.room_list[self.current_room_id][self.current_wall_id]
        self.recalculate_deltas()

        # change the collision rects of the objects in the inventory
        self.inventory.update_object_collision_rects()
        wall = self.current_wall.objects
        for obj in wall:
            if obj.displayed and "gray_bg" in obj.name:
                obj.swap_display()

    def update_walls(self, event):  # update all walls
        for room in self.room_list:
            for wall in room:
                wall.update(event)


    def center_current_object(
        self,
    ):  # put the center of the current object at the mouse position
        if self.current_object and self.current_object.movable:
            mx, my = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
            x, y = mx / self.current_wall.delta, my / self.current_wall.delta
            self.current_object.raw_rect.center = x, y
            # self.current_object.display_collision_rect()
            if self.network_manager.is_connected:
                self.network_manager.send_package(
                    "function",
                    "game",
                    "center_object",
                    self.current_object.name,
                    self.current_room_id,
                    self.current_wall_id,
                    x,
                    y,
                )

    # function useful for network
    def center_object(self, obj_name, room_id, wall_id, mx, my):
        src_wall = self.room_list[room_id][
            wall_id
        ]  # find the wall we want to take the object from
        object = None
        for obj in src_wall.objects:  # find the object we are talking about
            if obj.name == obj_name:
                object = obj
        if object is None:
            print(
                f"center_object error: invalid object name, the name {obj_name} was not found in room {room_id} wall {wall_id}"
            )
            return 1

        # x, y = mx / src_wall.delta, my / src_wall.delta
        object.raw_rect.center = mx, my


    def is_room_unlocked(self, room_id):
        if room_id == 0:
            return self.room_1_unlocked
        elif room_id == 1:
            return self.room_2_unlocked
        elif room_id == 2:
            return self.room_3_unlocked
        elif room_id == 3:
            return self.room_4_unlocked
        elif room_id == 4:
            return self.room_5_unlocked


    def unlock_room(self, room_id):
        if room_id == 0:
            self.room_1_unlocked = True
            if self.network_manager.is_connected:
                self.network_manager.send_package("variable", "game", "room_1_unlocked", True)
        elif room_id == 1:
            self.room_2_unlocked = True
            if self.network_manager.is_connected:
                self.network_manager.send_package("variable", "game", "room_2_unlocked", True)
        elif room_id == 2:
            self.room_3_unlocked = True
            if self.network_manager.is_connected:
                self.network_manager.send_package("variable", "game", "room_3_unlocked", True)
        elif room_id == 3:
            self.room_4_unlocked = True
            if self.network_manager.is_connected:
                self.network_manager.send_package("variable", "game", "room_4_unlocked", True)
        elif room_id == 4:
            self.room_5_unlocked = True
            if self.network_manager.is_connected:
                self.network_manager.send_package("variable", "game", "room_5_unlocked", True)


    def select_current_object(self, event):
        for obj in reversed(self.current_wall.objects.sprites()):  # reversed so we click the top object first
            if obj.displayed and obj.rect.collidepoint(event.pos):
                if obj.movable:
                    if (
                        self.network_manager.is_connected
                        and obj.name == self.other_player_object_name
                    ):
                        return
                    self.current_object = obj
                    # send the information to the other player

                    if self.network_manager.is_connected:
                        self.network_manager.send_package(
                            "variable", "game", "other_player_object_name", obj.name
                        )
                obj.handle_click_selection(event)
                return


    def drop_current_object(self, event, collisions = None):
        return_code = False
        if event and self.current_object:
            return_code = self.current_object.drop_at_pos(event.pos[0], event.pos[1], collisions)  # TODO: change to return the collision rect id
            if self.network_manager.is_connected:
                self.network_manager.send_package("variable", "game", "other_player_object_name", "")
                self.network_manager.send_package(
                    "function",
                    "game",
                    "drop_object",
                    self.current_object.name,
                    self.current_room_id,
                    self.current_wall_id,
                    self.current_object.collision_rect_id,
                )
            self.current_object = None

        elif event and self.inventory.current_object:
            if self.network_manager.is_connected:
                self.network_manager.send_package("variable", "game", "other_player_inventory_object_name", "")
            return_code = self.inventory.drop_current_object(event)  # TODO: change to return the collision rect id

        return return_code


    # function useful for network
    def drop_object(self, obj_name, room_id, wall_id, collision_rect_id):  # move an object on a given wall in a given room to a given collision_rect
        dest_wall = self.room_list[room_id][wall_id]  # on which wall do we want to put it

        object = None
        for obj in dest_wall.objects:
            if obj.name == obj_name:
                object = obj

        if object is None:
            print(f"drop_object error: invalid object name, the name {obj_name} was not found in room {room_id} wall {wall_id}")
            return 1

        if (collision_rect_id == -1):  # we tried to move the object at a wrong position when it was at its initial position
            object.raw_rect.center = object.valid_rect.center
        else:
            object.drop_in_collision_rect(collision_rect_id)  # set the new collision rect id of the object and put it inside


    def get_reference(self, name):  # returns the reference to an object in the game
        # search in the walls
        for room in self.room_list:
            for wall in room:
                for obj in wall.objects:
                    if obj.name == name:
                        return obj
        # search in the inventory
        for line in self.inventory.slots:
            for obj in line:
                if obj:
                    if obj.name == name:
                        return obj

        print(f'get_reference error: no object with name {name} found in the game, exiting')
        self.quit()


    def get_reference_large(self, name):  # returns the reference to an object in the game
        res = []
        for room in self.room_list:
            for wall in room:
                for obj in wall.objects:
                    if name in obj.name:
                        res.append(obj)
        return res


    def update_gui(self):
        if self.last_delta != self.delta:
            delta = self.delta
            self.last_delta = delta

            new_x = int(delta * self.stash_raw_rect.x)
            new_y = int(delta * self.stash_raw_rect.y)
            new_width = int(self.raw_stash.get_width() * delta)
            new_height = int(self.raw_stash.get_height() * delta)

            self.stash = pygame.transform.scale(self.raw_stash, (new_width, new_height))
            self.stash_rect = pygame.Rect(new_x, new_y, new_width, new_height)

            self.font = pygame.font.Font(None, int(30 * delta))


    def display_room_counter(self):  # for debug purposes
        room_name = "Denial"
        if self.current_room_id == 1:
            room_name = "Anger"
        elif self.current_room_id == 2:
            room_name = "Bargaining"
        elif self.current_room_id == 3:
            room_name = "Depression"
        elif self.current_room_id == 4:
            room_name = "Acceptance"

        text_surface = self.font.render(
            f"{room_name} room",
            True,  # anti-aliasing
            (255, 255, 255),
        )
        x = 0
        y = 100 * self.delta
        self.screen.blit(text_surface, (x, y))


    def display_fps(self):  # for debug purposes
        text_surface = self.font.render(
            f"FPS {int(self.clock.get_fps())}",
            True,  # anti-aliasing
            (255, 255, 255),
        )
        x = 0
        y = 125 * self.delta
        self.screen.blit(text_surface, (x, y))


    def display_current_object_name(self):
        name = ""
        if self.current_object:
            name = self.current_object.name
        elif self.inventory.current_object:
            name = self.inventory.current_object.name
        else:
            name = "None"
        text_surface = self.font.render(
            f"selected object : {name}",
            True,  # anti-aliasing
            (255, 255, 255),
        )
        x = 0
        y = 75 * self.delta
        self.screen.blit(text_surface, (x, y))


    def display_mouse_hover(self):
        pos = pygame.mouse.get_pos()
        if self.stash_rect.collidepoint(pos):
            self.screen.blit(self.mouse_hover_image, pos)
        else:
            wall = list(self.current_wall.objects)
            for obj in reversed(wall):
                if obj.displayed and obj.rect.collidepoint(pos):
                    if obj.interactible:
                        self.screen.blit(self.mouse_hover_image, pos)  # draw the cursor
                    return


    def display_gui(self):
        self.update_gui()
        self.display_room_counter()
        self.display_current_object_name()
        self.display_fps()
        self.screen.blit(self.stash, (0,0))
        self.display_mouse_hover()


    def recalculate_deltas(self):  # recalculate the delta values when the window is resized
        self.height = self.screen.get_height()
        self.width = self.screen.get_width()
        self.delta_w = self.width / 1080
        self.delta_h = self.height / 720
        self.delta = min(self.delta_h, self.delta_w)

        self.current_wall.delta_w = self.delta_w * (1080 / 1920)
        self.current_wall.delta_h = self.delta_h * (720 / 1080)
        self.current_wall.delta = min(self.current_wall.delta_w, self.current_wall.delta_h)


    def handle_keyboard_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.change_wall(1)
            elif event.key == pygame.K_RIGHT:
                self.change_wall(-1)
            elif event.key == pygame.K_UP:
                self.change_room()
            elif event.key == pygame.K_DOWN:
                self.change_room()
            elif event.key == pygame.K_i:
                self.inventory.displayed = not self.inventory.displayed
            elif event.key == pygame.K_r:
                self.reset_game()

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            temp_inv_obj = self.inventory.current_object
            in_inventory = self.inventory.handle_click(event)

            if (
                not in_inventory
                and not temp_inv_obj
                and self.current_object is None
                and self.inventory.current_object is None
            ):
                self.select_current_object(event)

            elif (
                not in_inventory
                and not temp_inv_obj
                and self.current_object is not None
            ):
                self.current_object.handle_click(event)

        elif event.type == pygame.MOUSEMOTION:
            self.center_current_object()

    # TODO change this absolutely disgusting stuff
    def handle_all_events(self, events):
        for event in events:
            if event.type == pygame.QUIT:
                self.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    swap_mini_game = True
                    if self.current_mini_game == "menu":
                        self.current_mini_game = "game"
                        self.mini_game_menu.duo_error_code = -1
                    else:
                        if self.current_mini_game == "game":
                            wall = self.current_wall.objects

                            # TODO: remove that, the function is not meant to do this
                            for obj in wall:
                                if obj.displayed and "gray_bg" in obj.name:
                                    obj.swap_display()
                                    swap_mini_game = False

                        if swap_mini_game:
                            self.current_mini_game = "menu"

            if event.type == pygame.WINDOWSIZECHANGED:
                self.recalculate_deltas()

            elif self.current_mini_game == "game":
                self.update_walls(event)
                self.handle_keyboard_event(event)
                self.dialogues.handle_event(event)

            elif self.current_mini_game == "laboratory":
                self.laboratory_game.handle_click(event)


    def update_all(self):
        events = pygame.event.get()
        self.handle_all_events(events)

        self.screen.fill((0, 0, 0))  # clear the screen

        # render the current mini-game
        if self.current_mini_game == "game":
            self.current_wall.display()
            self.inventory.display()
            self.dialogues.display()
            self.dialogues.update()
            self.display_gui()
            self.inventory.draw_current_object()


        elif self.current_mini_game == "menu":
            self.mini_game_menu.update(events)

        elif self.current_mini_game == "laboratory":
            self.laboratory_game.update()

        elif self.current_mini_game == "end_screen":
            self.end_screen_reference.resize_image()
            self.end_screen_reference.draw()

        pygame.display.flip()

        # limit framerate
        self.clock.tick(self.FPS)