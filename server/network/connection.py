import threading, time, uuid
from queue import Queue

class Connection():
    def __init__(self, socket, address):
        self.socket = socket
        self.address = address
        self.id = uuid.uuid4()
        self.game = None
        self.connected = True
        self.out_queue = Queue()
        self.start_tunnel()

    
    def __str__(self):
        return f'<Connection : {self.id} {self.address}>'

    def __repr__(self):
        return f'Connection( <Socket()> , {self.address} )'

    def send(self, message):
        self.out_queue.put(message)

    def queue(self):
        while self.connected:
            for i in range(self.out_queue.qsize()):
                self.socket.send(self.out_queue.get().encode())
            time.sleep(.25)

    def get(self):
        data = self.socket.recv(1024).decode()
        if data: return data
        else: return None
    
    def start_tunnel(self):
        t = threading.Thread(target=self.queue)
        t.daemon = True
        t.start()

    def set_game_instance(self, game):
        self.game = game

    def close(self):
        print(f'Client {self.id} has diconnected from {self.address} : Player <{self.game.player.name}>.')
        self.connected = False
        self.socket.close()

    