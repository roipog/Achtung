import socket
import threading
from constants import *


class ConnectAndSend():
    def __init__(self, game):
        # Connect to the server:
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((IP, TCP_PORT_NUMBER))
        # Start reading from server in separate thread
        ReadThread(self.client_socket, game).start()

    def send(self, request_str):
        # Send some messages:
        print("in send", request_str)
        request_str = request_str.strip()
        self.client_socket.send(request_str.encode())


class ReadThread(threading.Thread):

    def __init__(self, client_socket, game):
        self.client_socket = client_socket
        self.game = game
        threading.Thread.__init__(self)

    def run(self):
        try:
            while True:
                response_len = self.client_socket.recv(NUMBER_LENGTH).strip()
                try:
                    msg_len = int(response_len)
                    response = self.client_socket.recv(msg_len).strip()
                    request_str = response.decode()
                except ValueError:
                    request_str = "Bye"
                print("got from server", request_str, "|")
                self.game.use_data_from_tcp(request_str)
                if request_str == "Bye":
                    print("break")
                    break

        except ConnectionResetError:
            print("Bye")
        finally:
            self.client_socket.close()

