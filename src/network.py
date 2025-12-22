import pygame
import sys
import json
import socket

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

    def network_manager(self):
        while self.running:
            if self.is_host and not self.is_connected:
                self.check_new_connection()

            elif self.is_connected:
                self.check_incoming_client_data()

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
            raw_data = self.client.recv(4096).decode("utf-8")
            self.receive_buffer += raw_data
            # make sure that we process every line if there are multiple lines received at once
            #TODO: change this, I don't like it
            while "\n" in self.receive_buffer:
                line, self.receive_buffer = self.receive_buffer.split("\n", 1)
                if line.strip():  # ignore spaces at the end and at the beginning of the string just to be sure the line is valid when converted to json
                    data = json.loads(line)
                    self.game_context.load_data_in_memory(data)

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

    def check_new_connection(self):  # check if someone is trying to connect to become player 2
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
            self.game_context.save_data()
            self.game_context.load_data_from_file()
            raw_data = json.dumps(self.game_context.game_data)  # convert json into raw text

            try:
                self.client.sendall(raw_data.encode("utf-8"))
                print("game data sent !")

            except Exception as e:
                print("check_new_connection 2 : Error, impossible to send the data to the player ", e)

            else:
                self.is_connected = True
                self.game_context.player2.is_displayed = True  # the second player is now visible on the server side
