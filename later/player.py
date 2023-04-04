import threading

class Player(threading.Thread):
    def __init__(self, socket, game):
        super().__init__()
        self.socket = socket
        self.game = game
        # self.location = 
        self.name = ""
        
    def run(self):
        self.send("Welcome to the adventure game! What is your name?")
        self.name = self.receive().strip()
        self.game.send_to_all_clients(f"{self.name} has joined the game.")
        
        while not self.game.game_over:
            self.send("What do you want to do?")
            action = self.receive().strip()
            if action == "move":
                self.move()
            elif action == "quit":
                self.game_over = True
                self.game.send_to_all_clients(f"{self.name} has left the game.")
                self.socket.close()
            else:
                self.send("Invalid action.")
        
    def send(self, message):
        self.socket.sendall(message.encode())
        
    def receive(self):
        return self.socket.recv(1024).decode()
        
    # def move(self):
    #     self.send("Where do you want to go?")
    #     current_location = self.game.locations[self.location]
    #     valid_directions = list(current_location.connections.keys())
    #     self.send(f"Valid directions: {', '.join(valid_directions)}")
    #     direction = self.receive().strip()
    #     if direction not in valid_direction

    # def attack(self):
    #     return 5  # placeholder value, implement real combat system later
