import math
import pygame
import socket
import threading
import json
import sys
import time

from player import Player
from entities import Entities
from map import Map
from network import Network_manager
from minigames import *
from pathlib import Path


root_dir = Path(__file__).resolve().parent.parent


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.fullscreen = True
        self.FPS = 60
        self.clock = pygame.time.Clock()
        self.game_running = True

        self.game_data = {}  # json file
        self.game_data_path = f"{root_dir}/data/game_data.json"

        self.players = pygame.sprite.Group()
        self.entities = pygame.sprite.Group()

        self.name = "game"
        self.current_mini_game = "menu"
        
        # init minigames
        self.mini_game_test = Test(self)
        self.mini_game_menu = Menu(self)

        self.player1 = Player(
            None,
            None,
            f"{root_dir}/assets/images/blue-brown-frog-single.png",
            1,
            displayed=False
        )
        self.player2 = Player(
            None,
            None,
            f"{root_dir}/assets/images/robot-single.png",
            2,
            displayed=False
        )

        self.players.add(self.player1)
        self.players.add(self.player2)

        self.entities.add(
            Entities(
                200,
                200,
                self.game_data.get("player2_sprite"),
                3,
                displayed=True,
                mini_game_access=self.mini_game_test
            )
        )

        self.map = Map(self, f"{root_dir}/map/map-sewadge.tmx")
        self.network = Network_manager(self)

    def save_data(self):
        # save the data in the game_data file
        if self.network.is_host:
            data = {
                "player1_posX": self.player1.get_posX(),
                "player1_posY": self.player1.get_posY(),
                "player2_posX": self.player2.get_posX(),
                "player2_posY": self.player2.get_posY()
            }

            with open(self.game_data_path, "w") as file:
                json.dump(data, file, indent=4)

    def load_data_from_file(self):
        if self.network.is_host:
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

    def broadcast_host(self, port):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        message = f"GAME_HOST:{port}".encode()

        while True:
            s.sendto(message, ("<broadcast>", 50001))
            time.sleep(1)

    def listen_for_host(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(("", 50001))

        data, addr = s.recvfrom(1024)
        msg = data.decode()

        if msg.startswith("GAME_HOST"):
            port = int(msg.split(":")[1])
            host_ip = addr[0]
            return host_ip, port

    def start(self):
        gamemode = "s" #input("wanna play solo (s) or duo (d) bitch ? ")

        if gamemode == "s":
            print("launching solo...")
            self.launch_solo()

        elif gamemode == "d":
            print("launching duo...")
            ip, port = self.listen_for_host()
            self.launch_duo(ip, port)

        else:
            print("invalid answer, dumbass")
            sys.exit(1)

        self.load_data_in_memory(self.game_data)

        incoming_data_thread = threading.Thread(
            target=self.network.network_manager,
            daemon=True
        )
        incoming_data_thread.start()

    def launch_solo(self):
        self.load_data_from_file()
        self.player1.is_displayed = True
        self.network.setup_server()

    def launch_duo(self, ip: str, port: int):
        self.player2.is_displayed = True
        self.player1.is_displayed = True

        try:
            self.network.client.connect((ip, port))
        except Exception as e:
            print("launch_duo: Error", e)
            sys.exit(1)
        else:
            try:
                data = self.network.client.recv(4096).decode("utf-8")
            except Exception as e:
                print("launch_duo: Error", e)
            else:
                self.game_data = json.loads(data)
                self.network.is_connected = True
                self.network.is_host = False

    def switch_back_to_solo_mode(self):
        self.network.is_connected = False
        self.network.reset_client()
        self.player2.is_displayed = False

    def get_entities(self):
        return list(self.entities)

    def is_collision(self, rect):
        return rect.collidelist(self.map.collision_rects) > -1

    def move_up(self, player: Player):
        player.move_up()
        if self.network.is_connected:
            self.network.client.sendall(
                f'{{"player{player.player_id}_posY": {player.get_posY()}}}\n'.encode("utf-8")
            )

    def move_down(self, player: Player):
        player.move_down()
        if self.network.is_connected:
            self.network.client.sendall(
                f'{{"player{player.player_id}_posY": {player.get_posY()}}}\n'.encode("utf-8")
            )

    def move_right(self, player: Player):
        player.move_right()
        if self.network.is_connected:
            self.network.client.sendall(
                f'{{"player{player.player_id}_posX": {player.get_posX()}}}\n'.encode("utf-8")
            )

    def move_left(self, player: Player):
        player.move_left()
        if self.network.is_connected:
            self.network.client.sendall(
                f'{{"player{player.player_id}_posX": {player.get_posX()}}}\n'.encode("utf-8")
            )

    def move_all_directions(self, player: Player, coeff):
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0

        if keys[pygame.K_LEFT]:
            dx -= 1
        if keys[pygame.K_RIGHT]:
            dx += 1
        if keys[pygame.K_UP]:
            dy -= 1
        if keys[pygame.K_DOWN]:
            dy += 1

        if dx != 0 or dy != 0:
            length = math.sqrt(dx * dx + dy * dy)
            dx /= length
            dy /= length

            player.old_x = player.rect.x
            player.old_y = player.rect.y

            player.update_velocity(coeff)

            player.precise_x += dx * player.velocity
            player.precise_y += dy * player.velocity

            player.rect.x = player.precise_x
            player.rect.y = player.precise_y

            if player.is_displayed:
                player.hitbox.midbottom = player.rect.midbottom

                if self.map.map_collision(player.hitbox):
                    player.rect.x = player.old_x
                    player.rect.y = player.old_y
                    player.precise_x = player.old_x
                    player.precise_y = player.old_y
                else:
                    for entity in self.get_entities():
                        if entity.npc_collision(player):
                            player.rect.x = player.old_x
                            player.rect.y = player.old_y
                            player.precise_x = player.old_x
                            player.precise_y = player.old_y

    def update(self):
        self.screen.fill((0, 0, 0))
        coeff = self.clock.tick(self.FPS) / 40

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_running = False
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.current_mini_game = "menu"

        if self.current_mini_game == "game":
            player = self.player1 if self.network.is_host else self.player2
            self.move_all_directions(player, coeff)

            self.screen.fill((0, 0, 0))
            self.map.group.center(player.rect.center)
            self.map.group.draw(self.screen)

            for entity in self.get_entities():
                if entity.is_entity_displayed():
                    self.screen.blit(entity.sprite, (entity.get_posX(), entity.get_posY()))
                    entity.npc_interact(player, self.screen, self, entity.mini_game_access)

        elif self.current_mini_game == "menu":
            self.mini_game_menu.update()

        else:
            self.mini_game_test.update()

        pygame.display.flip()

