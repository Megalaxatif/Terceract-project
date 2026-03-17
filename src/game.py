from json.decoder import JSONDecodeError
import math
import pygame
import socket
import threading
import json
import sys
import time

from room import *
from network import Network_manager
from minigames import *
from pathlib import Path
from dialogues import Dialogue

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
        self.height = self.screen.get_height()
        self.width = self.screen.get_width()
        self.fullscreen = True
        self.FPS = 60
        self.clock = pygame.time.Clock()
        self.game_running = True
        self.root_dir = (Path(__file__).resolve().parent.parent)
        self.game_data = {} # for network
        self.game_data_path = f"{self.root_dir}/data/game_data.json"
        self.event = None
        self.font = pygame.font.Font(None, 50)
        self.name = "game"
        self.current_mini_game = "menu"

        self.mouse_enabled = True
        self.network_manager = Network_manager(self)
        self.start()

        self.back_wall_R1  = Back_wall_R1(self, 0, 0)
        self.left_wall_R1  = Left_wall_R1(self, 0, 1)
        self.front_wall_R1 = Front_wall_R1(self, 0, 2)
        self.right_wall_R1 = Right_wall_R1(self, 0, 3)

        self.R1 = [self.back_wall_R1, self.left_wall_R1, self.front_wall_R1, self.right_wall_R1]

        self.back_wall_R2  = Back_wall_R2(self, 1, 0)
        self.left_wall_R2  = Left_wall_R2(self, 1, 1)
        self.front_wall_R2 = Front_wall_R2(self, 1, 2)
        self.right_wall_R2 = Right_wall_R2(self, 1, 3)

        self.R2 = [self.back_wall_R2, self.left_wall_R2, self.front_wall_R2, self.right_wall_R2]

        self.back_wall_R3  = Back_wall_R3(self, 2, 0)
        self.left_wall_R3  = Left_wall_R3(self, 2, 1)
        self.front_wall_R3 = Front_wall_R3(self, 2, 2)
        self.right_wall_R3 = Right_wall_R3(self, 2, 3)

        self.R3 = [self.back_wall_R3, self.left_wall_R3, self.front_wall_R3, self.right_wall_R3]

        self.back_wall_R4  = Back_wall_R4(self, 3, 0)
        self.left_wall_R4  = Left_wall_R4(self, 3, 1)
        self.front_wall_R4 = Front_wall_R4(self, 3, 2)
        self.right_wall_R4 = Right_wall_R4(self, 3, 3)

        self.R4 = [self.back_wall_R4, self.left_wall_R4, self.front_wall_R4, self.right_wall_R4]

        self.back_wall_R5  = Back_wall_R5(self, 4, 0)
        self.left_wall_R5  = Left_wall_R5(self, 4, 1)
        self.front_wall_R5 = Front_wall_R5(self, 4, 2)
        self.right_wall_R5 = Right_wall_R5(self, 4, 3)

        self.R5 = [self.back_wall_R5, self.left_wall_R5, self.front_wall_R5, self.right_wall_R5]

        self.room_list = [
           self.R1,
           self.R2,
           self.R3,
           self.R4,
           self.R5
        ]

        self.room_1_unlocked = True
        self.room_2_unlocked = False
        self.room_3_unlocked = False
        self.room_4_unlocked = False

        self.current_room_id = 0
        self.current_wall_id = 0
        self.current_wall = self.room_list[self.current_room_id][self.current_wall_id]
        self.current_object = None
        self.other_player_object_name = ""
        self.mini_game_menu = Menu(self)
        self.inventory = Inventory(self, 40, 615, 1, 10, 100, True) # Create inventory (it's a line here)

        self.dialogues = Dialogue(self)

    def save_game(self): # save all the game data
        if self.network_manager.is_host:
            print("save game")
            for room in self.room_list:
                for wall in room:
                    wall.save_objects_data()
            print("save inventory")
            self.inventory.save_images()


    def start(self):
        #gamemode = "s"
        gamemode = input("wanna play solo (s) or duo (d) bitch ? ")

        if gamemode == "s":
            print("launching solo...")
            self.launch_solo()

        elif gamemode == "d":
            print("launching duo...")
            #ip, port = self.listen_for_host()
            ip = input("ip of the guy: ")
            self.launch_duo(ip,self.network_manager.server_port)

        else:
            print("invalid answer, dumbass")
            sys.exit(1)

        incoming_data_thread = threading.Thread(target=self.network_manager.network_manager, daemon=True)
        incoming_data_thread.start()

    def launch_solo(self): # TODO adapt this function to make it work again
        self.network_manager.is_host = True
        self.network_manager.setup_server()


    def launch_duo(self, ip: str, port: int):
        try:
            self.network_manager.client.connect((ip, port))
        except Exception as e:
            print("launch_duo: Error 1", e)
            sys.exit(1)
        else:
            try:
                #TODO: !!! IMPORTANT !!!! this system is not stable, if the size of the package is greater than 20 KB
                # it is undefined behavior we need to use a method that give us the length of the data
                data = self.network_manager.client.recv(20480).decode("utf-8")
            except Exception as e:
                print("launch_duo: Error 2", e)
                sys.exit(1)
            else:
                try:
                    self.game_data = json.loads(data)

                except JSONDecodeError as e:
                    print("launch_duo Error 3: ", e)
                    sys.exit(1)
                else:
                    self.network_manager.is_connected = True
                    self.network_manager.is_host = False


    def switch_back_to_solo_mode(self):
        self.network_manager.is_connected = False
        self.other_player_object_name = ""
        self.network_manager.reset_client()


    def change_room(self): # change the room we are in
        # create a custom event
        mouse_x, mouse_y = pygame.mouse.get_pos()
        custom_event = pygame.event.Event(CUSTOM_DROP_EVENT, {'pos': (mouse_x, mouse_y)})

        if self.current_wall_id == FRONT_WALL and self.current_room_id < ROOM_5:
            if self.is_room_unlocked(self.current_room_id):
                self.current_room_id += 1
                self.drop_current_object(custom_event)
                self.change_current_wall()

        elif self.current_wall_id == BACK_WALL and self.current_room_id > 0:
            self.current_room_id -= 1
            self.drop_current_object(custom_event)
            self.change_current_wall()

        else:
            print("change_room : Error, impossible to go in that direction")
            return 1


    def change_wall(self, direction : str):  # change the wall we are facing

        if direction != "right" and direction != "left":
            print("change_wall : Error, invalid direction")
            return 1

        # create a custom event
        mouse_x, mouse_y = pygame.mouse.get_pos()
        custom_event = pygame.event.Event(CUSTOM_DROP_EVENT, {'pos': (mouse_x, mouse_y)})

        if direction == "right":
            self.current_wall_id = (self.current_wall_id - 1) % ROOM_5 # python is magic
        if direction == "left":
            self.current_wall_id = (self.current_wall_id + 1) % ROOM_5

        self.drop_current_object(custom_event)
        self.change_current_wall()


    def change_current_wall(self): # update the reference to the current wall
        self.current_wall = self.room_list[self.current_room_id][self.current_wall_id]
        self.recalculate_deltas()

        # change the collision rects of the objects in the inventory
        self.inventory.update_object_collision_rects()


    def update_walls(self, event): # update all walls
        for room in self.room_list:
            for wall in room:
                wall.update(event)


    def center_current_object(self): # put the center of the current object at the mouse position
        if self.current_object is not None and self.current_object.movable:
            mx, my = pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]
            x, y = mx / self.current_wall.delta, my / self.current_wall.delta
            self.current_object.raw_rect.x = x - self.current_object.raw_rect.w/2
            self.current_object.raw_rect.y = y - self.current_object.raw_rect.h/2
            #self.current_object.display_collision_rect()
            if self.network_manager.is_connected:
                self.network_manager.send_package("function", "game", "center_object", self.current_object.name, self.current_room_id, self.current_wall_id, x, y)

    # function useful for network
    def center_object(self, obj_name, room_id, wall_id, mx, my):
        src_wall = self.room_list[room_id][wall_id] # find the wall we want to take the object from
        object = None
        for obj in src_wall.objects:                # find the object we are talking about
            if obj.name == obj_name:
                object = obj
        if object is None:
            print(f"center_object error: invalid object name, the name {obj_name} was not found in room {room_id} wall {wall_id}")
            return 1

        #x, y = mx / src_wall.delta, my / src_wall.delta
        object.raw_rect.x = mx - object.raw_rect.w/2
        object.raw_rect.y = my - object.raw_rect.h/2


    def is_room_unlocked(self, room_id):
        if room_id == 0:
            return self.room_1_unlocked
        elif room_id == 1:
            return self.room_2_unlocked
        elif room_id == 2:
            return self.room_3_unlocked
        elif room_id == 3:
            return self.room_4_unlocked


    def unlock_room(self, room_id):
        if room_id == 0:
            self.room_1_unlocked = True
        elif room_id == 1:
            self.room_2_unlocked = True
        elif room_id == 2:
            self.room_3_unlocked = True
        elif room_id == 3:
            self.room_4_unlocked = True


    def select_current_object(self, event):
        for obj in reversed(self.current_wall.objects.sprites()): # reversed so we click the top object first
            if obj.displayed and obj.rect.collidepoint(event.pos):
                if obj.movable:
                    if self.network_manager.is_connected and obj.name == self.other_player_object_name:
                        return
                    self.current_object = obj
                    # send the information to the other player

                    if self.network_manager.is_connected:
                        self.network_manager.send_package("variable", "game", "other_player_object_name", obj.name)
                if obj.interactible:
                    obj.handle_left_click(event)
                return


    def drop_current_object(self, event):
        if event and self.current_object:
            self.current_object.drop_at_pos(event.pos[0], event.pos[1]) # TODO: change to return the collision rect id
            if self.network_manager.is_connected:
                self.network_manager.send_package("variable", "game", "other_player_object_name", "")
                self.network_manager.send_package(
                    "function",
                    "game",
                    "drop_object",
                    self.current_object.name,
                    self.current_room_id,
                    self.current_wall_id,
                    self.current_object.collision_rect_id
                )
            self.current_object = None


    # function useful for network
    def drop_object(self, obj_name, room_id, wall_id, collision_rect_id): # move an object on a given wall in a given room to a given collision_rect
        dest_wall = self.room_list[room_id][wall_id]                    # on which wall do we want to put it

        object = None
        for obj in dest_wall.objects:
            if obj.name == obj_name:
                object = obj
        if object is None:
            print(f"drop_object error: invalid object name, the name {obj_name} was not found in room {room_id} wall {wall_id}")
            return 1

        if collision_rect_id == -1: # we tried to move the object at a wrong position when it was at its initial position
            object.raw_rect.center = object.valid_rect.center
        else:
            object.drop_in_collision_rect(collision_rect_id)                # set the new collision rect id of the object and put it inside


    def display_room_counter(self): # for debug purposes
        text_surface = self.font.render(
            f"room number {self.current_room_id+1}",
            True,           # anti-aliasing
            (0,0,0)
        )
        x = 40
        y = 3
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
            True,           # anti-aliasing
            (0,0,0)
        )
        x = self.screen.get_width() - text_surface.get_width() - 40
        y = 3
        self.screen.blit(text_surface, (x, y))


    def recalculate_deltas(self): # recalculate the delta values when the window is resized
        self.height = self.screen.get_height()
        self.width = self.screen.get_width()
        self.delta_h = self.screen.get_height() / 720
        self.delta_w = self.screen.get_width() / 1080
        self.delta = min(self.delta_h, self.delta_w)

        self.current_wall.delta_w = self.delta_w * (1080/1920)
        self.current_wall.delta_h = self.delta_h * (720/1080)
        self.current_wall.delta = min(self.delta_w * (1080/1920), self.delta_h * (720/1080))


    def handle_basic_game_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.current_mini_game = "menu"
            elif event.key == pygame.K_LEFT:
                self.change_wall("left")
            elif event.key == pygame.K_RIGHT:
                self.change_wall("right")
            elif event.key == pygame.K_UP:
                self.change_room()
            elif event.key == pygame.K_i:
                self.inventory.displayed = not self.inventory.displayed

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            temp_inv_obj = self.inventory.current_object
            in_inventory = self.inventory.handle_left_click(event)

            if not in_inventory and not temp_inv_obj and self.current_object is None and self.inventory.current_object is None:
                self.select_current_object(event)

            elif not in_inventory and not temp_inv_obj and self.current_object is not None:
                self.current_object.handle_left_click(event)

        elif event.type == pygame.MOUSEMOTION:
            self.center_current_object()


    def handle_all_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.game_running = False
                pygame.quit()
                sys.exit()

            if event.type == pygame.WINDOWSIZECHANGED:
                self.recalculate_deltas()

            elif self.current_mini_game == "game":
                self.handle_basic_game_events(event)
                #self.current_wall.update(event)
                self.update_walls(event)
                #self.dialogues.handle_event(event)

            elif self.current_mini_game == "menu": # TODO
                pass


    def update_all(self):
        self.handle_all_events()

        self.screen.fill((0, 0, 0)) # clear the screen

        # render the current mini-game
        if self.current_mini_game == "game":
            self.current_wall.display()
            self.inventory.display()
            self.display_room_counter()
            self.display_current_object_name()
            #self.dialogues.display()

        elif self.current_mini_game == "menu":
            self.mini_game_menu.update() # TODO: separate update from display

        self.mouse_enabled = True

        pygame.display.flip()

        # limit framerate
        self.clock.tick(self.FPS)
