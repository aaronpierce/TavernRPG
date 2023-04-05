from game import Game
from network import Server

Server('localhost', 9999, Game).listen()

