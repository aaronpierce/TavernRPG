import threading, time
from queue import Queue

class Client():
    def __init__(self, socket, address):
        self.socket = socket
        self.address = address
        self.game = None
        self.connected = True
        self.out_queue = Queue()
        self.start_tunnel()

    def send(self, message):
        self.out_queue.put(message)

    def queue(self):
        while self.connected:
            for i in range(self.out_queue.qsize()):
                self.socket.send(self.out_queue.get().encode())
            time.sleep(1)

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