import socket, threading, time, os, sys

class Client:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        self.connected = False
        self.send_thread = None
        self.receive_thread = None
        self.connect()


    def setup_tunnels(self):
        self.connected = True

        self.send_thread = threading.Thread(target=self.input_processor)
        self.send_thread.daemon = False
        self.send_thread.start()

        self.receive_thread = threading.Thread(target=self.incoming_processor)
        self.receive_thread.daemon = False
        self.receive_thread.start()        

    def connect(self):
        try:
            self.setup_tunnels()
        except ConnectionRefusedError:
            print('Server is offline.')
        sys.exit()

    def send(self, data):
        try:
            self.sock.send(data.encode())
        except ConnectionResetError:
            self.connected = False

    def receive(self):
        try:
            return self.sock.recv(1024).decode()
        except socket.error:
            self.connected = False
            return None
        

    def close(self):
        if self.connected:
            print('\nDisconnecting...')
            self.connected = False
            self.sock.close()
            

    def incoming_processor(self):
        while self.connected:
            message = self.receive()
            if message:
                if message.startswith('$'):
                    self.command(message)
                else:
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
            try:
                value = input('>')
            except (EOFError, ConnectionResetError):
                self.close()
                value = '**!EOC!**'

        return value

    def outbound(self):
        message = self.prompt()
        self.send(message)

    def command(self, message):
        cmd = {'type': message.split('~')[1], 'data': message.split('~')[2]}
        if cmd['type'] == 'IDSND':
            print('Client ID: ', cmd['data'])

    def connection_lost(self, where):
        print(f'Connection Lost: Press <R> to Reconnect or <Q> to Quit. [{where}]')
        
        choice = input('> ')
        if choice.lower() == 'r':
            self.connect()
        elif choice.lower() == 'q':
            sys.exit()
        else:
            pass

if __name__ == '__main__':

    host = 'localhost'

    if os.name == 'posix':
        if os.environ.get('IS_DOCKER', False):
            host = '172.17.0.2'
        else:
            host = '157.245.248.126'

    Client(host, 9999)