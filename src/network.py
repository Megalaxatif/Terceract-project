from json.decoder import JSONDecodeError
import pygame
import sys
import json
import socket
from utils import *


class Network_manager:
    def __init__(self, game_context):
        self.game_context = game_context
        self.server_port = 50000
        self.is_host = True  # by default we play in solo
        self.is_connected = False
        self.running = True  # TODO: suppress this later on, only usefull to avoid nasty errors if we quit the game through the network thread in duo mode
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.settimeout(30)
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.receive_buffer = b""
        self.FPS = 100
        self.clock = pygame.time.Clock()


    def network_manager(self):
        while self.running:
            if self.is_host and not self.is_connected:
                self.check_new_connection()

            elif self.is_connected:
                 self.check_incoming_client_data()

            self.clock.tick(self.FPS)


    def setup_server(self):
        self.server.setblocking(False) # TODO: I don't remember why I put this here, do we realy need the server socket to be non-blocking ?
        self.server.bind(("", self.server_port))
        self.server.listen(1)


    def reset_client(self):
        self.client.close()
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.settimeout(30)
        self.receive_buffer = b""


    def check_incoming_client_data(self):  # check if some data are coming either from player 1 or player 2
        raw_data = self.receive_package()
        if raw_data:
            # we received the whole package
            try:
                raw_data = raw_data.decode("utf-8")
                data = json.loads(raw_data)

            except JSONDecodeError as e:
                print(f"check_incoming_client_data error: impossible to decode the following package :\n{raw_data}\nfull error: {e}")

            else:
                package_type = data["type"]
                location = data["location"]
                name = data["name"]
                args = data["args"]

                match location:
                    case "game":
                        location = self.game_context
                    case "inventory":
                        location = self.game_context.inventory
                    case "magnet":
                        location = self.get_reference("magnet")
                    case "key":
                        location = self.get_reference("key")

                    case _: # TODO
                        print("check_incoming_client_data error: the location you gave is not taken in charge for the moment, you need to code it you lazy bastard")
                        return

                if location is None:
                    print(f"check_incoming_client_data error: no object with name {name} found in the game")
                    return

                if package_type == "function":
                    target_function = None
                    try:
                        target_function = getattr(location, name)

                    except AttributeError:
                        print(f"check_incoming_client_data error: impossible to find the function {name} located in {location}")

                    else:
                        if callable(target_function):
                            try:
                                target_function(*args)
                            except Exception as e:
                                print(f"check_incoming_client_data error: the function call of {name} located in {location} with the arguments {args} is invalid and resulted in an error:\n{e}")

                        else:
                            print(f"check_incoming_client_data error: the function {name} located in {location} is not callable")


                elif package_type == "variable":
                    try:
                        setattr(location, name, args[0])

                    except Exception as e:
                        print(f"check_incoming_client_data error: the variable {name} located in {location} couldn't be set to the value {args[0]} because of an error:\n{e}")

                else:
                    print(f"check_incoming_client_data error: the package type {package_type} is not taken in charge")


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
            raw_data = json.dumps(data) + "\n" # convert json into raw text

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


    def send_package(self, package_type : str, location : str, name : str, *args):
        if package_type not in ["variable", "function"]:
            print(f"send_package error: Invalid package type, you gave \"{package_type}\" but the function only accepts \"variable\" or \"function\"")
            return 1

        if package_type == "variable" and len(args) != 1:
            print("send_package error: you gave 0 or more than 1 arguments for a\"variable\" package type")
            return 2

        package = {
            "type" : package_type,
            "location" : location,
            "name" : name,
            "args" : args
        }
        package = json.dumps(package) + "\n"
        self.client.sendall(package.encode("utf-8"))
        return 0


    def receive_package(self):
        self.client.settimeout(30)
        package = b""

        while b"\n" not in self.receive_buffer:
            try:
                chunk = self.client.recv(4096)

                if not chunk:
                    self.handle_disconnection()
                    return b""

                self.receive_buffer += chunk

            except BlockingIOError:  # no data
                pass

            except ConnectionResetError:
                self.handle_disconnection()
                return b""

            except Exception as e:
                print("receive_package : Error ", e)
                return b""

        package, self.receive_buffer = self.receive_buffer.split(b"\n", 1)
        return package


    def get_reference(self, name):
        for room in self.game_context.room_list:
            for wall in room:
                for obj in wall.objects:
                    if obj.name == name:
                        return obj
        return None


    def handle_disconnection(self):
        print("disconnected")
        if self.is_host:
            print("switching back to solo mode...")
            self.game_context.switch_back_to_solo_mode()
        else:
            # we lost connection with the host so we stop everything
            print("shuting down...")
            self.running = False  # stop the network thread
            pygame.event.post(pygame.event.Event(pygame.QUIT))  # we send a QUIT event to the main thread