import socket, threading, time

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        self.connected = True
        self.send_thread = None
        self.receive_thread = None
        self.setup_tunnels()

    def setup_tunnels(self):
        self.send_thread = threading.Thread(target=self.input_processor)
        self.send_thread.daemon = False
        self.send_thread.start()

        self.receive_thread = threading.Thread(target=self.incoming_processor)
        self.receive_thread.daemon = False
        self.receive_thread.start()

    def send(self, data):
        self.sock.send(data.encode())

    def receive(self):
        data = self.sock.recv(1024).decode()
        return data

    def close(self):
        self.sock.close()

    def incoming_processor(self):
        while self.connected:
            message = self.receive()
            if message:
                print(message)
            time.sleep(.25)
    
    def input_processor(self):
        while self.connected:
            self.outbound()
        self.close()

    def prompt(self):
        value = None
        while not value:
            value = input('')

        return value

    def outbound(self):
        try:
            message = self.prompt()
            self.send(message)

        except socket.timeout:
            self.connected = False

if __name__ == '__main__':
    Client('localhost', 9999)