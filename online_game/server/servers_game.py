import time
import threading
import pygame
from server_player import Player
from constants import *

MSG_LENGTH = 4


class Game(threading.Thread):
    """
    responsible for sending data to clients.
    That data is checked in many functions.
    fields definition:
    """
    xy = [(100, 100), (1100, 500), (100, 500), (1100, 100), (100, 300), (1100, 301)]
    starting_speed = [5, -5, 5, -5, 5, -5]

    # overriding of constructor
    def __init__(self, tcp_sockets, udp_sockets, num_of_clients):
        threading.Thread.__init__(self)
        self.tcp_sockets = tcp_sockets
        self.udp_sockets = udp_sockets
        self.game_on = False
        self.players = []
        self.sprites_group = None
        self.num_of_clients = num_of_clients
        self.num_of_dead_players = 0

    def run(self):  # animation loop
        """
        Overriding of Thread run method.
        Includes implementation of protocol between server/client
        Output loop- send data to clients in accordance with the game board
        """
        self.sprites_group = pygame.sprite.Group()
        self.game_on = True
        for num in range(self.num_of_clients):
            player = Player(self.xy[num], self.starting_speed[num])
            self.players.append(player)
            self.sprites_group.add(player)
        resp = "start:" + str(self.num_of_clients)
        len_resp = str(len(resp))
        resp = "".join(len_resp.zfill(NUMBER_LENGTH)) + resp
        self.send_to_all_clients(resp)
        time.sleep(2)  # for client get "start"
        i = 0
        while self.game_on:
            time.sleep(SPEED)
            self.on_update()
            for player in self.players:
                if not player.playing:
                    if player.dx != 0 and player.dy != 0:
                        self.num_of_dead_players += 1
                    player.dx = 0
                    player.dy = 0
            if self.num_of_dead_players == len(self.players):
                self.game_on = False
            if self.game_on:
                self.on_update()
                msg = "tick:"
                msg_list = []
                for player in self.players:
                    if player.new_trail:
                        msg_list.append([(str(player.x).zfill(MSG_LENGTH), str(player.y).zfill(MSG_LENGTH)),
                                        (str(player.new_trail.x).zfill(MSG_LENGTH),
                                        str(player.new_trail.y).zfill(MSG_LENGTH))])
                    else:
                        msg_list.append([(str(player.x).zfill(MSG_LENGTH), str(player.y).zfill(MSG_LENGTH)),
                                         (str(0).zfill(MSG_LENGTH),
                                          str(0).zfill(MSG_LENGTH))])
                msg += str(msg_list)
                num_str = str(len(msg))
                msg = "".join([num_str.zfill(NUMBER_LENGTH), msg])
                self.send_to_all_clients(msg)
            i += 1
        print("end game")

    def send_to_all_clients(self, response_str):
        """
        Sends message  to all players
        :param response_str: the string to send
        """
        print("send to all", response_str)
        for sock in self.tcp_sockets:
            response = response_str.encode()
            if self.game_on:
                sock.send(response)

    def on_update(self):
        """ update all game objects"""
        for player in self.players:
            player.p_update()
            self.check_playing(player)

    def check_playing(self, player):
        if player.y <= 10:
            player.y = 10
            player.playing = False
        elif player.y >= 580:
            player.y = 580
            player.playing = False
        if player.x <= 10:
            player.x = 10
            player.playing = False
        elif player.x >= 1180:
            player.x = 1180
            player.playing = False
        else:
            for other_player in self.players:
                if other_player == player:
                    trails_list = other_player.trail[0:-10]
                else:
                    trails_list = other_player.trail
                for trail in trails_list:
                    if player.y <= trail.y <= player.y + 9 or \
                            player.y <= trail.y + 4 <= player.y + 9:
                        if player.x <= trail.x <= player.x + 9 or \
                                player.x <= trail.x + 4 <= player.x + 9:
                            player.playing = False

    def update(self, socket, data):
        """
        update data for current player
        :param data: new data
        :param udp_server_socket - server socket of current player
        """
        player_id = 0
        data = data.strip()
        if data == "Bye":
            for s in self.udp_sockets:
                if s == socket:
                    self.udp_sockets[player_id].close()
                    self.tcp_sockets[player_id].close()
                    self.udp_sockets.remove(self.udp_sockets[player_id])
                    self.tcp_sockets.remove(self.tcp_sockets[player_id])
                    self.players.remove(self.players[player_id])
                player_id += 1
            if len(self.players) == 1:
                self.tcp_sockets[0].send("Bye".encode())
                self.game_on = False
        if self.players:
            if data == "start":
                for s in self.udp_sockets:
                    self.players[player_id].sp_set_dxy(data)
                    player_id += 1
            elif data == "left" or data == "right":
                for s in self.udp_sockets:
                    if s == socket:
                        self.players[player_id].sp_set_dxy(data)
                    print(self.players[player_id].dx, ", ", self.players[player_id].dy)
                    player_id += 1
