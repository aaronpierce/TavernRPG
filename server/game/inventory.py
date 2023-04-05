class Inventory:
    def __init__(self, player, game, items=[]):
        self.game = game
        self.player = player
        self.items = items

    def display(self):
        self.game.outbound('\nInventory:')
        self.game.outbound('\n'.join([f'- {i}' for i in self.items]))