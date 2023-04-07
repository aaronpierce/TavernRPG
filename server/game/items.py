import random
from server.game.extras import load as _load

WEAPONS = _load('weapons')
CONSUMABLES = _load('consumables')
ITEMS = _load('non_consumables')
TABLES = _load('drop_tables')

class Weapon:
    def __init__(self, template):
        self.__dict__.update(WEAPONS[template])

    def __str__(self):
        return '{} (+{} DMG)'.format(self.name, self.damage)

class Consumable:
    def __init__(self, template):
        self.__dict__.update(CONSUMABLES[template])

    def __str__(self):
        return '{} (+{} HP)'.format(self.name, self.healing_value)

class Item:
    def __init__(self, template):
        self.__dict__.update(ITEMS[template])

    def __str__(self):
        return '{}'.format(self.name)
    
class DropTable():
    def __init__(self, table, gold=True):
        self.table = TABLES[table]
        self.gold = gold

    def drop(self):
        complete = False
        item_drop = None

        while not complete:
            pick = random.choice(self.table)

            if pick in WEAPONS:
                item_drop = Weapon(pick)
            elif pick in CONSUMABLES:
                item_drop = Consumable(pick)
            elif pick in ITEMS:
                item_drop = Item(pick)
            elif self.gold and pick == 'gold':
                item_drop = random.randrange(10, 100)
            elif not self.gold and pick == 'gold':
                continue
            complete = True

        return item_drop


# drop = random.choices(drops, weights=probabilities, k=1000)

# Code for creating override function to provide testing!

def override_generate():
    data = {}
    for item in WEAPONS:
        data[WEAPONS[item]['name']] = Weapon(item)
    for item in CONSUMABLES:
        data[CONSUMABLES[item]['name']] = Consumable(item)
    for item in ITEMS:
        data[ITEMS[item]['name']] = Item(item)
    return data


override = override_generate()