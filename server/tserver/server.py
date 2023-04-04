import socket, threading
from textwrap import dedent
from .client import Client
from .game import Game
from .admin import Admin

class Server:
    def __init__(self, host, port, game):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen(5)
        self.connections = []
        self.game = game

    def handle(self, conn, addr):
        client = Client(conn, addr)
        client.set_game_instance(Game(client))
        self.connections.append(client)
        self.ack_connection(client)
        while client.connected:
            option = self.direct(client)
            if option == "1":
                client.game.start()
            elif option == "3":
                client.connected = False
            elif option == "4":
                Admin(self, client).start()

    def listen(self):
        print('Server is listening...')
        while True:
            conn, addr = self.sock.accept()
            t = threading.Thread(target=self.handle, args=(conn, addr))
            t.daemon = True
            t.start()

    def ack_connection(self, client):
        client.send("\nYou've connected to the server!")
        print(f"Client connected from {client.address}")

    def direct(self, client):
        self.display(client)
        return client.get()

    def display(self, client):

        logo = \
            """
                                  .                                               
                              /   ))     |\         )               ).           
                        c--. (\  ( `.    / )  (\   ( `.     ).     ( (           
                        | |   ))  ) )   ( (   `.`.  ) )    ( (      ) )          
                        | |  ( ( / _..----.._  ) | ( ( _..----.._  ( (           
            ,-.           | |---) V.'-------.. `-. )-/.-' ..------ `--) \._        
            | /===========| |  (   |      ) ( ``-.`\/'.-''           (   ) ``-._   
            | | / / / / / | |--------------------->  <-------------------------_>=-
            | \===========| |                 ..-'./\.`-..                _,,-'    
            `-'           | |-------._------''_.-'----`-._``------_.-----'         
                        | |         ``----''            ``----''                  
                        | |                                                       
                        c--'"""

        title = \
            """
                    __ __|                             _ \  _ \  __| 
                       |   _` | \ \ /  -_)   _|  \       /  __/ (_ | 
                      _| \__,_|  \_/ \___| _| _| _|   _|_\ _|  \___| 

            """
        menu = \
            """
            Select an option:
            1. - Start New Game
            2. - Load Game
            3. - Quit
            4. - Admin Panel
            -------------------
            """

        #client.send(logo)
        client.send(title)
        client.send(menu)
