import socket
import time

class Game:
    def __init__(self):
        self.game_over = False
        self.clients = []
        
    def start(self):
        print("Starting server...")
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(("localhost", 9999))
        server_socket.listen(5)
        
        while not self.game_over:
            client_socket, client_address = server_socket.accept()
            print(f"Client connected from {client_address}")
            client = Player(client_socket, self)
            client.start()
            self.clients.append(client)
        
        server_socket.close()
        print("Server closed.")
        
    def send_to_all_clients(self, message):
        for client in self.clients:
            client.send(message)
        
    def game_loop(self):
        current_location = self.locations[self.players[0].location]
        self.send_to_all_clients(current_location.description)
        self.send_to_all_clients("What do you want to do?")
        
    # def move_player(self, player, direction):
    #     current_location = self.locations[player.location]
    #     if direction not in current_location.connections:
    #         return
        
    #     new_location_name = current_location.connections[direction]
    #     player.location = new_location_name
        
    #     self.send_to_all_clients(f"{player.name} is now at {self.locations[new_location_name].name}.")
    #     time.sleep(1)  # add a small delay for dramatic effect
        
    #     # check if player has reached the end of the game
    #     if player.location == "end":
    #         self.game_over = True
    #         self.send_to_all_clients("Congratulations, you have won!")
            
    #     # check if player has encountered an enemy
    #     current_location = self.locations[player.location]
    #     if current_location.enemy is not None:
    #         self.fight_enemy(player, current_location.enemy)
        
    # def fight_enemy(self, player, enemy):
    #     self.send_to_all_clients(f"You have encountered a {enemy.name}!")
    #     while True:
    #         # player's turn
    #         self.send_to_all_clients("What do you want to do?")
    #         action = player.receive().strip()
    #         if action == "attack":
    #             damage = player.attack()
    #             self.send_to_all_clients(f"You attacked the {enemy.name} for {damage} damage!")
    #             enemy.hp -= damage
    #             if enemy.hp <= 0:
    #                 self.send_to_all_clients(f"You defeated the {enemy.name}!")
    #                 current_location.enemy = None
    #                 break
    #         elif action == "run":
    #             self.send_to_all_clients("You ran away!")
    #             break
    #         else:
    #             self.send_to_all_clients("Invalid action.")
                
    #         # enemy's turn
    #         damage = enemy.attack()
    #         self.send_to_all_clients(f"The {enemy.name} attacked you for {damage} damage!")         