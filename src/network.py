import pygame
import sys
import json
import socket
from utils import load_json_file

class Network_manager:
    def __init__(self, game_context):
        self.game_context = game_context
        self.server_port = 50000
        self.is_host = True  # by default we play in solo
        self.is_connected = False
        self.running = True  # TODO: suppress this later on, only usefull to avoid nasty errors if we quit the game through the network thread in duo mode
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.receive_buffer = ""
        self.FPS = 100
        self.clock = pygame.time.Clock()


    def network_manager(self):
        while self.running:
            if self.is_host and not self.is_connected:
                self.check_new_connection()

            # elif self.is_connected:
            #     #self.check_incoming_client_data()
            #     pass
            self.clock.tick(self.FPS)

    def setup_server(self):
        self.server.setblocking(False) # TODO: I don't remember why I put this here, do we realy need the server socket to be non-blocking ?
        self.server.bind(("", self.server_port))
        self.server.listen(1)


    def reset_client(self):
        self.client.close()
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.receive_buffer = ""


    def check_incoming_client_data(self):  # check if some data are coming either from player 1 or player 2
        try:
            #TODO: !!! IMPORTANT !!!! this system is not stable, if the size of the package is greater than 10 KB
            # it is undefined behavior we need to use a method that give us the length of the data
            raw_data = self.client.recv(4096).decode("utf-8")

            self.receive_buffer += raw_data
            #make sure that we process every line if there are multiple lines received at once
            #TODO: change this, I don't like it
            while "\n" in self.receive_buffer:
                line, self.receive_buffer = self.receive_buffer.split("\n", 1)
                if line.strip():  # ignore spaces at the end and at the beginning of the string just to be sure the line is valid when converted to json
                    data = json.loads(line)
                    self.load_data_in_memory(data)


        except BlockingIOError:  # no data
            pass

        except ConnectionResetError:  # the other player disconnected
            print("disconnected")
            if self.is_host:
                print("switching back to solo mode...")
                self.game_context.switch_back_to_solo_mode()
            else:
                # we lost connection with the host so we stop everything
                print("shuting down...")
                self.running = False  # stop the network thread
                pygame.event.post(pygame.event.Event(pygame.QUIT))  # we send a QUIT event to the main thread

        except Exception as e:
            print("check_incoming_client_data : Error ", e)


    def check_new_connection(self):  # check if someone is trying to connect
        try:
            self.client, address = self.server.accept()  # the server creates a connection with the player
            print(f"new connection established with {address}")  # debug

        except BlockingIOError:  # there is no client trying to connect
            pass

        except Exception as e:  # a real error occured
            print("check_new_connection 1 : Error ", e)

        else:  # this is only executed if the code in the try section validates
            # we will send the game data to the player
            # update the data in the json file before sending
            self.game_context.save_game()
            data = self.get_all_data()
            raw_data = json.dumps(data)  # convert json into raw text

            try:
                self.client.sendall(raw_data.encode("utf-8"))

            except Exception as e:
                print("check_new_connection 2 : Error, impossible to send the data to the player ", e)

            else:
                print("game data sent !")
                self.is_connected = True


    def get_all_data(self): # returns a list of dict containing all the wall data and the inventory data at the end
        data = {"wall_data": [], "inv_data" : {}}
        for i in range(len(self.game_context.room_list)):
            data["wall_data"].append([])
            for wall in self.game_context.room_list[i]:
                wall_data = load_json_file(wall.json_path)
                data["wall_data"][i].append(wall_data)
        inventory_data = load_json_file(self.game_context.inventory.json_path)
        data["inv_data"] = inventory_data

        return data