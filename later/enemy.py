class Enemy:
    def __init__(self, name, hp, attack_power, defense_power, description):
        self.name = name
        self.hp = hp
        self.attack_power = attack_power
        self.defense_power = defense_power
        self.description = description
        
    def attack(self):
        return self.attack_power  # placeholder value, implement real combat system later