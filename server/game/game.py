from TavernRPG.server.game.player import Player
from TavernRPG.server.game.world import World
from TavernRPG.server.game.extras import game_help
from collections import OrderedDict
from functools import partial
from pprint import pprint
import sys, time
class Game():
    def __init__(self, client):
        self.online = True
        self.client = client
        self.player = None
        self.world = None
        self.actions = None

    def create_player(self, location):
        #self.outbound('Enter your username:')
        self.player = Player(self, 'Dakiru', location) #self.inbound(), location)

    def create_world(self):
        self.world = World()

    def start(self):
        self.create_world()
        self.create_player(self.world.start_location)

        self.loop()

    def loop(self):
        while self.online and self.player.alive and self.client.connected:
            try:
                self.action_handler()
                self.render()
            except WindowsError as e:
                self.client.close()


    def inbound(self):
        message = self.client.get()
        return message

    def outbound(self, message):
        self.client.send(message)

    def prompt(self):
        self.outbound(f'\n{self.player.name}@player > Choose action:')
        return self.inbound().lower()
        
    def action_handler(self):
        action = None
        while not action:
            self.player.status()
            self.available_actions()
            action = self.actions.get(self.prompt())
            if action: action()
            else: self.outbound("\nInvalid action - Use '?' for help.\n")

    def available_actions(self):
        actions = OrderedDict()
        if self.player.inventory:
            self.action_builder(actions, 'i', self.player.inventory.display, 'Inventory')
        #if isinstance(world.at(self.player.location), world.TraderTile):
        #    self.action_builder(actions, 't', self.player.trade, 'Trade')
        #if (isinstance(world.at(self.player.location), world.EnemyTile) or isinstance(room, world.BossTile)) and room.enemy.is_alive():
        #    self.action_builder(actions, 'a', self.player.attack, 'Attack')
        #else:
        if self.world.at(self.player.location.x, self.player.location.y - 1):
            self.action_builder(actions, 'n', partial( self.player.move, 'N'), 'Go North')
        if self.world.at(self.player.location.x, self.player.location.y + 1):
            self.action_builder(actions, 's', partial( self.player.move, 'S'), 'Go South')
        if self.world.at(self.player.location.x + 1, self.player.location.y):
            self.action_builder(actions, 'e', partial( self.player.move, 'E'), 'Go East')
        if self.world.at(self.player.location.x - 1, self.player.location.y):
            self.action_builder(actions, 'w', partial( self.player.move, 'W'), 'Go West')
        #if self.player.hp < 100 and any(isinstance(y, items.Consumable) for y in self.player.inventory):
        #     self.action_builder(actions, 'h', self.player.heal, 'Heal')

        self.action_builder(actions, '?', game_help, '')
        self.action_builder(actions, '**!eoc!**', sys.exit, '')
        #self.action_builder(actions, '+', self.player.save, '')
        #self.action_builder(actions, '-', self.player.load, '')

        # Only Enable Override function for testing.
        #self.action_builder(actions, '~', self.player.override, '')

        self.actions = actions


    def action_builder(self, action_dict, hot_key, action, name):
        action_dict[hot_key.lower()] = action
        if hot_key not in ['~', '-', '+', '?', '**!eoc!**']:  # This is for hiding override control
            self.outbound('{}: {}'.format(hot_key, name))
        self.outbound('\n')

    def render(self):
        if self.player.alive:
            print(*self.player.location)
            self.outbound('\n' + self.world.at(*self.player.location).intro_text() + '\n')

