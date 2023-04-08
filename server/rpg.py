from TavernRPG.server.game import Game
from TavernRPG.server.network import Server

import os

class RPG:
    def __init__(self):
        self.host = 'localhost'
        self.port = 9999
        self.server = Server
        self.game = Game

        self.set_host()

    def set_host(self):
        if os.name == 'posix':
            if os.environ.get('IS_DOCKER', False):
                self.host = '172.17.0.2'
            else:
                self.host = '157.245.248.126'

    def start(self):
        self.server(self.host, self.port, self.game).listen()