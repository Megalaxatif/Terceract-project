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

ROOM_1 = 0
ROOM_2 = 1
ROOM_3 = 2
ROOM_4 = 3
ROOM_5 = 4

BACK_WALL = 0
LEFT_WALL = 1
FRONT_WALL = 2
RIGHT_WALL = 3

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.delta_h = 1
        self.delta_w = 1
        self.delta = 1
        self.fullscreen = True
        self.FPS = 60
        self.clock = pygame.time.Clock()
        self.game_running = True
        self.root_dir = (Path(__file__).resolve().parent.parent)
        self.game_data = {}  # json file
        self.game_data_path = f"{self.root_dir}/data/game_data.json"
        self.event = None
        self.name = "game"
        self.current_mini_game = "menu"

        self.mouse_enabled = True

        self.back_wall_R1  = Back_wall_R1(self)
        self.left_wall_R1  = Left_wall_R1(self)
        self.front_wall_R1 = Front_wall_R1(self)
        self.right_wall_R1 = Right_wall_R1(self)

        self.R1 = [self.back_wall_R1, self.left_wall_R1, self.front_wall_R1, self.right_wall_R1]

        self.back_wall_R2  = Back_wall_R2(self)
        self.left_wall_R2  = Left_wall_R2(self)
        self.front_wall_R2 = Front_wall_R2(self)
        self.right_wall_R2 = Right_wall_R2(self)

        self.R2 = [self.back_wall_R2, self.left_wall_R2, self.front_wall_R2, self.right_wall_R2]

        self.back_wall_R3  = Back_wall_R3(self)
        self.left_wall_R3  = Left_wall_R3(self)
        self.front_wall_R3 = Front_wall_R3(self)
        self.right_wall_R3 = Right_wall_R3(self)

        self.R3 = [self.back_wall_R3, self.left_wall_R3, self.front_wall_R3, self.right_wall_R3]

        self.back_wall_R4  = Back_wall_R4(self)
        self.left_wall_R4  = Left_wall_R4(self)
        self.front_wall_R4 = Front_wall_R4(self)
        self.right_wall_R4 = Right_wall_R4(self)

        self.R4 = [self.back_wall_R4, self.left_wall_R4, self.front_wall_R4, self.right_wall_R4]

        self.back_wall_R5  = Back_wall_R5(self)
        self.left_wall_R5  = Left_wall_R5(self)
        self.front_wall_R5 = Front_wall_R5(self)
        self.right_wall_R5 = Right_wall_R5(self)

        self.R5 = [self.back_wall_R5, self.left_wall_R5, self.front_wall_R5, self.right_wall_R5]


        self.room_list = [
           self.R1,
           self.R2,
           self.R3,
           self.R4,
           self.R5
        ]

        #self.change_current_wall() # reference to the current wall to render
        self.current_room_id = 0
        self.current_wall_id = 0 # back wall
        self.current_wall = self.room_list[self.current_room_id][self.current_wall_id]
        self.current_item = None
        self.network_manager = Network_manager(self)
        self.mini_game_menu = Menu(self)
        self.inventory = Inventory(self, 40, 615, 1, 10, 100, True) # Create inventory (it's a line here)


    def save_game(self): # save all the game data
        print("save game")
        for room in self.room_list:
            for wall in room:
                wall.save_objects_data()
        print("save inventory")
        self.inventory.save_images()


    def start(self): # TODO: adapt this function to make it work again
        gamemode = "s" #input("wanna play solo (s) or duo (d) bitch ? ")

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

        #self.load_data_in_memory(self.game_data)

        #incoming_data_thread = threading.Thread(
         #   target=self.network.network_manager,
          #  daemon=True
        #)
        #incoming_data_thread.start()

    def launch_solo(self): # TODO adapt this function to make it work again
        #self.load_data_from_file()
        #self.player1.is_displayed = True
        #self.network.setup_server()
        pass

    def launch_duo(self, ip: str, port: int):
        try:
            self.network_manager.client.connect((ip, port))
        except Exception as e:
            print("launch_duo: Error", e)
            sys.exit(1)
        else:
            try:
                data = self.network_manager.client.recv(4096).decode("utf-8")
            except Exception as e:
                print("launch_duo: Error", e)
            else:
                self.game_data = json.loads(data)
                self.network_manager.is_connected = True
                self.network_manager.is_host = False

    def switch_back_to_solo_mode(self):
        self.network_manager.is_connected = False
        self.network_manager.reset_client()


    def change_room(self): # change the room we are in
        if self.current_wall_id == FRONT_WALL and self.current_room_id < ROOM_5:
            self.current_room_id += 1
        elif self.current_wall_id == BACK_WALL and self.current_room_id > 0:
            self.current_room_id -= 1
        else:
            print("change_room : Error, impossible to go in that direction")
            return 1

        self.current_item = None
        self.change_current_wall()


    def change_wall(self, direction : str):  # change the wall we are facing
        if direction != "right" and direction != "left":
            print("change_wall : Error, invalid direction")
            return 1
        elif direction == "right":
            self.current_wall_id = (self.current_wall_id - 1) % ROOM_5 # python is magic
        elif direction == "left":
            self.current_wall_id = (self.current_wall_id + 1) % ROOM_5

        self.current_item = None
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


    def center_current_item(self): # put the center of the current item at the mouse position
        if self.current_item is not None and self.current_item.movable:
            mx, my = pygame.mouse.get_pos()[0] / self.current_wall.delta, pygame.mouse.get_pos()[1] / self.current_wall.delta
            self.current_item.raw_rect.x = mx - self.current_item.raw_rect.w/2
            self.current_item.raw_rect.y = my - self.current_item.raw_rect.h/2


    def select_current_item(self, event):
        for obj in reversed(self.current_wall.objects.sprites()): # reversed so we click the top object first
            if obj.rect.collidepoint(event.pos):
                self.current_item = obj
                break


    def drop_current_item(self, event):
        self.current_item.drop_at_pos(event.pos[0], event.pos[1])
        self.current_item = None


    def display_room_counter(self): # for debug purposes
        font = pygame.font.Font(None, 50)
        text_surface = font.render(
            f"room number {self.current_room_id+1}",
            True,           # anti-aliasing
            (0,0,0)
        )
        self.screen.blit(text_surface, (100, 50))


    def recalculate_deltas(self): # recalculate the delta values when the window is resized
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

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

            self.inventory.handle_left_click(event)

            if self.current_item is None and self.inventory.current_item is None:
                self.select_current_item(event)

            elif self.current_item is not None and self.current_item.movable:
                self.drop_current_item(event)


        elif event.type == pygame.MOUSEMOTION:
            self.center_current_item()


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
                self.update_walls(event)

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

        elif self.current_mini_game == "menu":
            self.mini_game_menu.update() # TODO: separate update from display

        self.mouse_enabled = True

        pygame.display.flip()
