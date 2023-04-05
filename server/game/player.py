from game.inventory import Inventory
from game.items import Weapon

import random

class Player():
    def __init__(self, game, name, location):
        self.game = game
        self.name = name
        self.alive = True
        self.location = location
        self.inventory = Inventory(self, game, [Weapon('rusty dagger')])
        self.health = 0
        self.strength = random.randint(5, 15)
        self.defense = 10
        self.mana = 100
        self.gold = 10
        self.define()

    def define(self):
        print(f'New Player {self.name} created.')

    def attack(self):
        self.game.outbound(f'You attacked a Dragon for {self.strength * 4} Damage!')

    def move(self, direction):
        if direction == 'N':
            self.location.y -= 1
        elif direction == 'S':
            self.location.y += 1
        elif direction == 'E':
            self.location.x -= 1
        elif direction == 'W':
            self.location.x += 1

    def status(self):
            left, right, bottom = 9, 9, 24
            if self.gold >= 1000:
                left += 1
                right += 1
                bottom += 2
            elif self.gold >= 100:
                left += 1
                right += 0
                bottom += 1

            text = ['\n\n' + '_' * left + 'Status' + '_' * right,
                    'Health: {}/100  Gold: {}'.format(self.health, self.gold), 
                    '¯' * bottom,
                    '']
            
            self.game.outbound('\n'.join(text))