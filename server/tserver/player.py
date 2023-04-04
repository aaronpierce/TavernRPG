class Player():
    def __init__(self, game, name):
        self.game = game
        self.name = name
        self.alive = True
        self.health = 0
        self.strength = 10
        self.defense = 10
        self.mana = 100
        self.define()

    def define(self):
        print(f'New Player {self.name} created.')

    def attack(self):
        self.game.outbound(f'You attacked a Dragon for {self.strength * 4} Damage!')