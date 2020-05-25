import socket               # Import socket module


class ConnectAndSend():
    def __init__(self, id):
        # Connect to the server:
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        ip = "127.0.0.1"  # Get local machine name
        port = 12345 + id  # Reserve a port for your service.
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
