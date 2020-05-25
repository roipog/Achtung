
import socket
import select
import servers_game
from my_constants import *
import sys


def tcp_connection_loop(sockets_for_animation, num_of_clients):
    """
    Add server socket to list
    :param sockets_for_animation: the list that will contain all Output sockets
    """

    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Address Family : AF_INET (this is IP version 4 or IPv4 - 32 bit address - 4 byte address)
    # Type : SOCK_STREAM (this means connection oriented TCP protocol)
    # Connection means a reliable "stream" of data. The TCP packets have an "order" or "sequence"
    # Apart from SOCK_STREAM type of sockets there is another type called SOCK_DGRAM which indicates the UDP protocol.
    # Other sockets like UDP , ICMP , ARP dont have a concept of "connection". These are non-connection based
    # communication. Which means you keep sending or receiving packets from anybody and everybody.

    # Helps to system forget server after 1 second
    tcp_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        # bind socket to localhost and  PORT_NUMBER
        tcp_server_socket.bind((IP, TCP_PORT_NUMBER))

        # become a server socket
        tcp_server_socket.listen(1)
        print("Server for output(animation loop) is listening")
        # connection loop
        j = 0
        while j < num_of_clients:

            tcp_client_socket, client_address = tcp_server_socket.accept()  # Connected point. Server wait for client
            ip, port = client_address
            print("Received connection from ip= ", ip, "port= ", port)
            sockets_for_animation.append(tcp_client_socket)

            resp = "Wait to start: " + str(j)
            num_str = str(len(resp))
            resp = "".join([num_str.zfill(NUMBER_LENGTH), resp])
            tcp_client_socket.send(resp.encode())

            j += 1
    except Exception as e:
        print(e.args)

    finally:
        tcp_server_socket.close()


def receive(server_socket):
    try:
        data, client_address = server_socket.recvfrom(LENGTH)
        # print(str(data))
        data = data.decode()
        data = data.strip()
        print("message From: " + str(client_address) + "  " + data)
        return data, client_address
    except Exception as e:

        print("3:", e.args)
        return None


def main():
    """
    connection loop
    every client has two threads and two sockets
    one for Input and one for Output
    """
    num_of_clients = int(input("enter num of players"))
    while num_of_clients > 6 or num_of_clients < 1:
        num_of_clients = int(input("enter num of players"))
    # Set up the server:
    sockets_for_animation = []
    inputs = []

    tcp_connection_loop(sockets_for_animation, num_of_clients)

    try:
        for i in range(num_of_clients):
            udp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            udp_server_socket.bind((IP, UDP_PORT_NUMBER+i))
            inputs.append(udp_server_socket)

        game = servers_game.Game(sockets_for_animation, inputs, num_of_clients)
        game.setDaemon(True)
        game.start()
        running = True
        print("Server Started.")
        while running:
            readable, writable, exceptional = select.select(inputs, [], inputs, 1)
            for udp_server_socket in readable:
                request = None
                try:

                    request, address = receive(udp_server_socket)

                    # print(request)
                except ConnectionResetError as e:
                    request = None
                    print("1:", e.args)
                if request:
                    print("request: ", request)
                    game.update(udp_server_socket, request)
                    if request == "Bye":
                        print("break")
                        running = False
                        break

        # new_game.join(0)    # close new_game thread

    # except Exception as e:
    #     print("2:", e.args)

    finally:
        for i in range(len(inputs)):
            inputs[i].close()


if __name__ == '__main__':
    main()
