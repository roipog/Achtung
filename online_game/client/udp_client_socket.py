import socket               # Import socket module
from constants import *


class ConnectAndSend():
    def __init__(self, id):
        # Connect to the server:
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ip = IP  # Get local machine name
        port = UDP_PORT_NUMBER + id  # Reserve a port for your service.
        self.address = (ip, port)

    def send(self, request_str):
        try:
            # Send some messages:
            request_str = request_str.strip()
            # print('Sending...', request_str, len(request_str))
            self.client_socket.sendto(request_str.encode(), self.address)
        except Exception as e:
            print("5:", e)
            pass

    def close_socket(self):
        self.client_socket.close()
