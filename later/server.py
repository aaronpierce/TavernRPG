import socket
import time
import threading

class Server:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen(5)
        self.connections = []

    def handle(self, conn, addr):
        self.connections.append(conn)
        print(f"New client connected: {addr}")
        while True:
            data = conn.recv(1024).decode()
            if not data:
                break
            print(f"Received data from {addr}: {data}")
            for c in self.connections:
                if c != conn:
                    c.send(data.encode())
        conn.close()
        self.connections.remove(conn)
        print(f"Client {addr} disconnected")

    def start(self):
        while True:
            conn, addr = self.sock.accept()
            t = threading.Thread(target=self.handle, args=(conn, addr))
            t.daemon = True
            t.start()

    def send_to_all_clients(self, clients, message):
        for client in self.clients:
            client.send(message.encode())

    def send_to_client(self, client, message):
        client.send(message.encode())

    def recieve_from_client(self, client):
        data = client.recv()
        if not data:
            return None
        return data

    def ack_connection(self, client):
        self.send_to_client(client, "You've connected to the server!")
        print(f"Client connected from {client.address}")


class Game:
    def __init__(self):
        self.server = Server('localhost', 8000)
        self.clients = []

    def handle_client(self, conn, addr):
        client = Client(conn, addr)
        self.clients.append(client)

    def run(self):
        self.server.start()

        while True:
            # game logic
            # ...
            # send data to all clients
            self.server.send_to_all_clients(self.clients, data)
            
            # receive data from clients
            for c in self.clients:
                data = c.receive_from_client()
                # update game state with client data
                # ...
            
        # close connections
        for c in self.clients:
            c.close()

        self.server.sock.close()

class Client():
    def __init__(self, socket, address):
        self.socket = socket
        self.address = address

    def send(self, message):
        self.socket.send(message.encode())

    def recv(self):
        return self.socket.recieve(1024).decode()

if __name__ == '__main__':
    game = Game()
    game.start()
    