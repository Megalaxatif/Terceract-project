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
        self.fullscreen = True
        self.FPS = 60
        self.clock = pygame.time.Clock()
        self.game_running = True
        self.root_dir = Path(__file__).resolve().parent.parent
        self.game_data = {}  # json file
        self.game_data_path = f"{self.root_dir}/data/game_data.json"

        self.name = "game"
        self.current_mini_game = "menu"
        
        self.mini_game_menu = Menu(self)
        self.mini_game_inventory = Inventory(self, 600, 100, 5, 3, 100)

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

        self.current_room_id = 0
        self.current_wall_id = 0 # back wall
        self.current_wall = None
        self.update_current_wall() # reference to the current wall to render
        self.network_manager = Network_manager(self)

    def save_data(self):
        # save the data in the game_data file
        if self.network_manager.is_host:
            data = {
                "player1_posX": self.player1.get_posX(),
                "player1_posY": self.player1.get_posY(),
                "player2_posX": self.player2.get_posX(),
                "player2_posY": self.player2.get_posY()
            }

            with open(self.game_data_path, "w") as file:
                json.dump(data, file, indent=4)

    def load_data_from_file(self):
        if self.network_manager.is_host:
            try:
                with open(self.game_data_path, "r") as data:
                    self.game_data = json.load(data)
            except FileNotFoundError as e:
                print("load_data_file: Error", e)
                sys.exit(1)

    def load_data_in_memory(self, data: dict):
        for key, value in data.items():
            if key == "player1_posX":
                self.player1.set_posX(value)

            elif key == "player1_posY":
                self.player1.set_posY(value)
            elif key == "player2_posX":
                self.player2.set_posX(value)
            elif key == "player2_posY":
                self.player2.set_posY(value)

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
        self.player2.is_displayed = True
        self.player1.is_displayed = True

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
        self.player2.is_displayed = False

    def get_entities(self):
        return list(self.entities)

    def is_collision(self, rect):
        return rect.collidelist(self.map.collision_rects) > -1

    #NOTE IMPORTANT TO KEEP THESE FUNCTIONS FOR THE MOVEMENT OF OBJECTS IN THE FUTURE !!

    # def move_up(self, player: Player):
    #     player.move_up()
    #     if self.network.is_connected:
    #         self.network.client.sendall(
    #             f'{{"player{player.player_id}_posY": {player.get_posY()}}}\n'.encode("utf-8")
    #         )

    # def move_down(self, player: Player):
    #     player.move_down()
    #     if self.network.is_connected:
    #         self.network.client.sendall(
    #             f'{{"player{player.player_id}_posY": {player.get_posY()}}}\n'.encode("utf-8")
    #         )

    # def move_right(self, player: Player):
    #     player.move_right()
    #     if self.network.is_connected:
    #         self.network.client.sendall(
    #             f'{{"player{player.player_id}_posX": {player.get_posX()}}}\n'.encode("utf-8")
    #         )

    # def move_left(self, player: Player):
    #     player.move_left()
    #     if self.network.is_connected:
    #         self.network.client.sendall(
    #             f'{{"player{player.player_id}_posX": {player.get_posX()}}}\n'.encode("utf-8")
    #         )

    # def move_all_directions(self, player: Player, coeff):
    #     keys = pygame.key.get_pressed()
    #     dx, dy = 0, 0

    #     if keys[pygame.K_LEFT]:
    #         dx -= 1
    #     if keys[pygame.K_RIGHT]:
    #         dx += 1
    #     if keys[pygame.K_UP]:
    #         dy -= 1
    #     if keys[pygame.K_DOWN]:
    #         dy += 1

    #     if dx != 0 or dy != 0:
    #         length = math.sqrt(dx * dx + dy * dy)
    #         dx /= length
    #         dy /= length

    #         player.old_x = player.rect.x
    #         player.old_y = player.rect.y

    #         player.update_velocity(coeff)

    #         player.precise_x += dx * player.velocity
    #         player.precise_y += dy * player.velocity

    #         player.rect.x = player.precise_x
    #         player.rect.y = player.precise_y

    #         if player.is_displayed:
    #             player.hitbox.midbottom = player.rect.midbottom

    #             if self.map.map_collision(player.hitbox):
    #                 player.rect.x = player.old_x
    #                 player.rect.y = player.old_y
    #                 player.precise_x = player.old_x
    #                 player.precise_y = player.old_y
    #             else:
    #                 for entity in self.get_entities():
    #                     if entity.npc_collision(player):
    #                         player.rect.x = player.old_x
    #                         player.rect.y = player.old_y
    #                         player.precise_x = player.old_x
    #                         player.precise_y = player.old_y

    def change_room(self):
        if self.current_wall_id == FRONT_WALL and self.current_room_id < ROOM_5:
            self.current_room_id += 1
        elif self.current_wall_id == BACK_WALL and self.current_room_id > 0:
            self.current_room_id -= 1
        else:
            print("change_room : Error, impossible to go in that direction")
            return 1
        self.update_current_wall()


    def change_wall(self, direction : str):
        if direction != "right" and direction != "left": 
            print("change_wall : Error, invalid direction")
            return 1
        elif direction == "right":
            self.current_wall_id = (self.current_wall_id - 1) % ROOM_5 # python is magic
        elif direction == "left":
            self.current_wall_id = (self.current_wall_id + 1) % ROOM_5

        self.update_current_wall()


    def update_current_wall(self):
        self.current_wall = self.room_list[self.current_room_id][self.current_wall_id]

    def handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_running = False
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.current_mini_game = "menu"
                elif event.key == pygame.K_LEFT:
                    self.change_wall("left")
                elif event.key == pygame.K_RIGHT:
                    self.change_wall("right")
                elif event.key == pygame.K_UP:
                    self.change_room()
                if event.key == pygame.K_i and self.current_mini_game == "game":
                    self.mini_game_inventory.display = not self.mini_game_inventory.display

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.mini_game_inventory.display:
                    self.mini_game_inventory.handle_click(event.pos)
                if self.current_mini_game == "game":
                    self.current_wall.handle_click(event)


    def update(self):
        self.screen.fill((0, 0, 0))
        coeff = self.clock.tick(self.FPS) / 40
        
        self.delta_h = self.screen.get_height() / 720
        self.delta_w = self.screen.get_width() / 1080
        
        self.current_wall.delta_w = self.delta_w * (1080/1920)
        self.current_wall.delta_h = self.delta_h * (720/1080)
        self.current_wall.delta = min(self.delta_w * (1080/1920), self.delta_h * (720/1080))

        self.handle_input()

        if self.current_mini_game == "game":
            #player = self.player1 if self.network.is_host else self.player2
            self.current_wall.update()

            #debug
            font = pygame.font.Font(None, 50)
            text_surface = font.render(
                f"room number {self.current_room_id+1}",
                True,           # anti-aliasing
                (0,0,0)
            )
            self.screen.blit(text_surface, (100, 50))

        elif self.current_mini_game == "menu":
            self.mini_game_menu.update()

        else:
            self.mini_game_test.update()
        
        if self.mini_game_inventory.display:
            self.mini_game_inventory.update()

        pygame.display.flip()

