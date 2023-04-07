import socket, threading, time, os, sys

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        self.connected = True
        self.send_thread = None
        self.receive_thread = None
        self.connect()

    def setup_tunnels(self):
        self.send_thread = threading.Thread(target=self.input_processor)
        self.send_thread.daemon = False
        self.send_thread.start()

        self.receive_thread = threading.Thread(target=self.incoming_processor)
        self.receive_thread.daemon = False
        self.receive_thread.start()

    def connect(self):
        self.setup_tunnels()
        
    def shutdown(self):
        sys.exit()

    def send(self, data):
        try:
            self.sock.send(data.encode())
        except socket.error:
            self.close()

    def receive(self):
        try:
            return self.sock.recv(1024).decode()
        except socket.error:
            self.close()
        

    def close(self):
        if self.connected:
            print('Disconnecting...')
            self.connected = False
            self.sock.close()
            self.shutdown()

    def incoming_processor(self):
        while self.connected:
            message = self.receive()
            if message:
                print(message)
            time.sleep(.5)

        print('Incoming Service offline.')
    
    def input_processor(self):
        while self.connected:
            self.outbound()
        print('Outgoing Service offline.')
        

    def prompt(self):
        value = None
        while not value:
            time.sleep(1)
            value = input('>')
            

        return value

    def outbound(self):
        message = self.prompt()
        self.send(message)

if __name__ == '__main__':

    host = 'localhost'

    if os.name == 'posix':
        if os.environ.get('IS_DOCKER', False):
            host = '172.17.0.2'
        else:
            host = '157.245.248.126'

    Client(host, 9999)