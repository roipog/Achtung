""" With map and player"""

import ast
from pygame.locals import *
import os, sys
from map import *
from client_player import Player
import constants
import tcp_client_socket
import udp_client_socket

MSG_LENGTH = 5


class Game:

    # class variables, revoke with 'self.' or 'Game.'
    width = 1200
    height = 600
    xy = [(100, 100), (1100, 500), (100, 501), (1100, 101), (100, 300), (1100, 301)]
    paths = ["../imgs/dot1.png", "../imgs/dot2.png", "../imgs/dot3.png",
             "../imgs/dot4.png", "../imgs/dot5.png", "../imgs/dot6.png"]

    def __init__(self):
        """ declare all game objects (as in constructor)"""
        self.running = False
        self.screen = None
        # main object
        self.players = None
        self.opponent = None
        # group of static and movable game objects
        self.sprites_group = None
        self.blocks = None
        self.id = 0
        self.on_init()
        self.tcp_client = tcp_client_socket.ConnectAndSend(self)
        self.udp_client = None
        self.num_of_clients = 0

    def on_init(self):
        """ all game objects initialization"""

        # set title
        pygame.display.set_caption("ACHTUNG")

        # https://riptutorial.com/pygame/topic/6442/creating-a-window-in-pygame---pygame-display-set-mode--
        self.screen = pygame.display.set_mode((Game.width, Game.height))
        self.blocks = []
        self.players = []
        self.sprites_group = pygame.sprite.Group()
        map = Map(self.blocks, self.sprites_group)

    def use_data_from_tcp(self, response_str):
        msg = response_str.strip()
        if msg.startswith("Wait to start"):     # we got "Wait to start:0" or "Wait to start:1"
            self.id = int(msg.split(":")[1])
            print(msg)
        elif msg.startswith("start"):
            self.num_of_clients = int(msg.split(":")[1])
            self.udp_client = udp_client_socket.ConnectAndSend(self.id)
            for num in range(self.num_of_clients):
                player = Player(self.paths[num], self.xy[num])
                self.players.append(player)
                self.sprites_group.add(player)
        elif msg == "Bye":
            self.running = False
            self.udp_client.close_socket()
        elif msg.startswith("tick"):
            msg = msg[5::]  # removes "tick:" from the msg and create the list
            msg_list = eval(msg)
            for num in range(self.num_of_clients):
                px, py = msg_list[num][0]
                tx, ty = msg_list[num][1]
                if px and py:
                    px = int(px)
                    py = int(py)
                    tx = int(tx)
                    ty = int(ty)
                    self.players[num].set_data(px, py, tx, ty)

    def on_event(self, event):
        """ callback after events """
        if event.type == QUIT:
            if self.udp_client:
                self.udp_client.send("Bye".rjust(MSG_LENGTH))
            self.running = False
        else:
            key = pygame.key.get_pressed()
            if self.udp_client:
                if key[pygame.K_SPACE]:
                    self.udp_client.send("start".rjust(MSG_LENGTH))
                elif key[pygame.K_LEFT]:
                    self.udp_client.send("left".rjust(MSG_LENGTH))
                elif key[pygame.K_RIGHT]:
                    self.udp_client.send("right".rjust(MSG_LENGTH))

    def on_update(self):
        """ update all game objects"""
        if self.players:
            for player in self.players:
                if player.new_trail:
                    self.sprites_group.add(player.new_trail)
        pygame.display.update()
        self.sprites_group.update()

    def on_render(self):
        """ draw all game objects"""
        self.screen.fill((255, 255, 255))   # white color background
        self.sprites_group.draw(self.screen)

    def on_execute(self):
        """ animation loop"""

        self.running = True
        while self.running:

            # reacts on events *****************************************
            for event in pygame.event.get():
                self.on_event(event)

            # update data **********************************************
            self.on_update()

            # drawing **************************************************
            self.on_render()

            # time in milliseconds for watch the screen ****************
            pygame.time.delay(10)

        pygame.quit()
        # sys.exit(0)


def main():
    pygame.init()
    # set pygame screen location
    os.environ['SDL_VIDEO_WINDOW_POS'] = "{},{}".format(100, 100)
    my_game = Game()
    my_game.on_execute()


if __name__ == "__main__":
    main()
