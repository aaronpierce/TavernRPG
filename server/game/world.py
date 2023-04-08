from TavernRPG.server.game.location import Location
from textwrap import dedent

import random, os
#import enemies, npc, items


class World():
    def __init__(self):
        self.start_location = None
        self.map = self._generate_map()

    def _tile(self, abbrv):
        tile_types = {
            "NT" : NormalTile,
            "FG" : FindGoldTile,
            "ST" : StartTile,
            "  " : None
        }

        return tile_types[abbrv]
    
    def _map_dsl(self):
        with open('server/resources/map.dsl.txt', 'r') as map:
            dsl = ''.join(map.readlines())
        return dsl
    
    def _validate_dsl(self, dsl):
        if dsl.count("|ST|") != 1:
             raise SyntaxError("DSL: No Starting Tile")
        # if dsl.count("|VT|") == 0:
            #  raise SyntaxError("DSL: No Victory Tile")
        lines = dsl.splitlines()
        lines = [l for l in lines if l]
        pipe_counts = [line.count("|") for line in lines]
        for count in pipe_counts:
            if count != pipe_counts[0]:
                 raise SyntaxError("DSL: Tile Count <> Pipe Count")

    def _generate_map(self):
        _map = []
        dsl = self._map_dsl()
        self._validate_dsl(dsl)

        for y, dsl_row in enumerate([x for x in dsl.splitlines() if x]):
            row = []
            dsl_cells = dsl_row.split("|")
            dsl_cells = [c for c in dsl_cells if c]
            for x, dsl_cell in enumerate(dsl_cells):
                tile_type = self._tile(dsl_cell)
                if tile_type == StartTile:
                     self.start_location = Location(x, y)
                row.append(tile_type(x, y) if tile_type else None)

            _map.append(row)
        return _map
    
    def at(self, x, y):
        if x < 0 or y < 0:
            return None
        try:
            return self.map[y][x]
        except IndexError:
            return None

class MapTile:
    def _init__(self, x, y):
        self.location = Location(x, y)

    def intro_text(self):
        raise NotImplementedError('Create a subclass instead!')

    def modify_player(self, player):
        pass


class StartTile(MapTile):
    def __init__(self, x, y):
        super().__init__()
        self.location = Location(x, y)

    def intro_text(self):
        return '''Not much to see. It appears that you can make out some faint paths around you.'''


# class EnemyTile(MapTile):
#     def __init__(self, x, y):
#         super().__init__()
#         self.x = x
#         self.y = y
#         self.enemy = enemies.enemy_spawn()
#         self.alive_text = self.enemy.alive_msg
#         self.dead_text = self.enemy.dead_msg
#         self.drop = items.drop(self.enemy.drop_table)
#         self.drop_claimed = False

#     def modify_player(self, player):
#         enemy_dmg = int(round(((self.enemy.str / 100) + 1.04) * random.randint(0, self.enemy.dmg)))
#         enemy_max = int(round(((self.enemy.str / 100) + 1.04) * self.enemy.dmg))
#         if self.enemy.is_alive():
#             player.hp -= enemy_dmg
#             if enemy_dmg == enemy_max:
#                 print('Enemy does {}* damage. You have {} HP remaining.\n'.format(enemy_dmg, player.hp))
#             else:
#                 print('Enemy does {} damage. You have {} HP remaining.\n'.format(enemy_dmg, player.hp))
#         elif not self.enemy.is_alive() and not self.drop_claimed:
#             self.drop_claimed = True
#             if isinstance(self.drop, items.Weapon) or isinstance(self.drop, items.Consumable) or isinstance(self.drop, items.Item):
#                 player.inventory.append(self.drop)
#                 print('{} was dropped by the {} and added to your inventory!\n'.format(self.drop, self.enemy))
#             elif type(self.drop) == type(int()):
#                 player.gold += self.drop
#                 print('{} Gold was dropped by the {} and added to your inventory!\n'.format(self.drop, self.enemy))

#     def intro_text(self):
#         text = self.alive_text if self.enemy.is_alive() else self.dead_text
#         return text


class NormalTile(MapTile):
    def __init__(self, x, y):
        super().__init__()
        self.location = Location(x, y)

    def intro_text(self):
        return """This is nothing interesting here."""


# class VictoryTile(MapTile):
#     def __init__(self, x, y):
#         super().__init__()
#         self.x = x
#         self.y = y

#     def modify_player(self, player):
#         player.victory = True

#     def intro_text(self):
#         return """You see a bright light in the distance...\n... it grows as you get closer.\n\nVictory is yours!!"""


# class TraderTile(MapTile):
#     def __init__(self, x, y):
#         self.trader = npc.Trader()
#         super().__init__()
#         self.x = x
#         self.y = y

#     def trade(self, player, buyer, seller):
#         while True:
#             equipped = player.most_powerful_weapon()
#             if buyer == player:
#                 player.status()
#                 print("Trader's Inventory: (Items to buy)")
#             else:
#                 player.status()
#                 print("Player\'s Inventory: (Items to sell)")
#             for i, item in enumerate(seller.inventory, 1):
#                 if seller == player and item == equipped:
#                     print('{}. {} - {} Gold +'.format(i, item.name, item.value))  # ◂
#                 else:
#                     print('{}. {} - {} Gold'.format(i, item.name, item.value))
#             user_input = input("\nChoose an item or 'Q' to exit: ")
#             if user_input in ['Q', 'q']:
#                 return
#             else:
#                 try:
#                     choice = int(user_input)
#                     to_swap = seller.inventory[choice - 1]
#                     self.swap(player, seller, buyer, to_swap)
#                 except (ValueError, IndexError):
#                     print('\nInvalid Choice!\n')

#     def swap(self, player, seller, buyer, item):
#         if item.value > buyer.gold:
#             print("That's too expensive")
#             return
#         seller.inventory.remove(item)
#         buyer.inventory.append(item)
#         if seller == player:
#             seller.gold = seller.gold + item.value
#         else:
#             seller.gold = seller.gold + item.value
#             buyer.gold = buyer.gold - item.value
#         print('\nTrade complete!\n')

#     def check_if_trade(self, player):
#         while True:
#             player.status()
#             print('Choose an action:\nb: Buy\ns: Sell\nq: Quit')
#             user_input = input('Action: ').lower()
#             if user_input == 'q':
#                 return
#             elif user_input == 'b':
#                 self.trade(player, buyer=player, seller=self.trader)
#             elif user_input == 's':
#                 self.trade(player, buyer=self.trader, seller=player)
#             else:
#                 print("\nInvalid Action!\n")

#     def intro_text(self):
#         return """A frail not-quit-human, not-quit-creature squats in the corner clinking his gold coins together.\nYou hear an eerie voice...\n\n'Hello stranger, up for a trade?'"""


class FindGoldTile(MapTile):
    def __init__(self, x, y):
        self.gold = random.randint(1, 50)
        self.gold_claimed = False
        super().__init__()
        self.location = Location(x, y)

    def modify_player(self, player):
        if not self.gold_claimed:
            self.gold_claimed = True
            player.gold = player.gold + self.gold
            print('++You pick up the {} Gold++\n'.format(self.gold))

    def intro_text(self):
        if self.gold_claimed:
            return """Another unremarkable part of the cave. You must forge onwards."""
        else:
            return """Someone dropped some gold. You pick it up."""


# class FindItemTile(MapTile):
#     def __init__(self, x, y):
#         self.item_claimed = False
#         super().__init__()
#         self.x = x
#         self.y = y
#         self.item = items.drop('standard', False)
#         self.claimed_text = 'An emptied chest... nothing more to find here. Better move on.'
#         self.unclaimed_text = 'You spot a partially opened chest on the ground. I wonder whats inside...'

#     def modify_player(self, player):
#         if not self.item_claimed:
#             self.item_claimed = True
#             player.inventory.append(self.item)
#             print('++{} added to inventory++\n'.format(self.item))

#     def intro_text(self):
#         text = self.unclaimed_text if not self.item_claimed else self.claimed_text
#         return text


# class BossTile(MapTile):
#     def __init__(self, x, y):
#         super().__init__()
#         self.x = x
#         self.y = y
#         self.enemy = enemies.Enemy('ancient dragon')
#         self.alive_text = 'An enormous dragon rips through the air with a loud screech and slams to the ground in front of you!!'
#         self.dead_text = 'A slain dragon lays at your feet.'
#         self.key_claimed = False
#         self.reward = items.Item('ancient key')

#     def modify_player(self, player):
#         enemy_dmg = int(round(((self.enemy.str / 100) + 1) * random.randint(0, self.enemy.dmg)))
#         if self.enemy.is_alive():
#             player.hp -= enemy_dmg
#             print('Enemy does {} damage. You have {} HP remaining.\n'.format(enemy_dmg, player.hp))
#         if not self.key_claimed and not self.enemy.is_alive():
#             self.key_claimed = True
#             player.inventory.append(self.reward)
#             print('An {} was dropped by the {} and added to your inventory!\n'.format(self.reward.name, self.enemy))

#     def intro_text(self):
#         text = self.alive_text if self.enemy.is_alive() else self.dead_text
#         return text


# class AncientChestTile(MapTile):
#     def __init__(self, x, y):
#         super().__init__()
#         self.x = x
#         self.y = y
#         self.item_claimed = False
#         self.claimed_text = 'Alas, my reward for slaying the beast has been claimed.'
#         self.unclaimed_text = 'An enormous chest sunken into the ground. You see what looks like a dragon on the face of the chest. Looks secure....'
#         self.reward = items.Weapon('ancient spear')

#     def modify_player(self, player):
#         if any(items.Item('ancient key').name in y.name for y in player.inventory) and not self.item_claimed:
#             print('This old key seems to be a snug, but perfect fit. Lets see whats inside...?\n')
#             print('You\'ve found something that looks valuable.\n')
#             print('{} was added to your inventory!\n'.format(self.reward))
#             self.item_claimed = True
#             player.inventory.append(self.reward)
#             for item in player.inventory:
#                 if item.name == 'Ancient Key':
#                     player.inventory.remove(item)
#                     break
#         elif not self.item_claimed:
#             print('The right key might open this.\n')

#     def intro_text(self):
#         text = self.claimed_text if self.item_claimed else self.unclaimed_text
#         return text

# tile_type_dict = {
#     "VT": VictoryTile,
#     "NT": NormalTile,
#     "EN": EnemyTile,
#     "ST": StartTile,
#     "FG": FindGoldTile,
#     "*T": TraderTile,
#     "FI": FindItemTile,
#     "BT": BossTile,
#     "AC": AncientChestTile,
#     "  ": None
# }
