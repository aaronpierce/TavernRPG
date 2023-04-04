
class Location:
    def __init__(self, x, y, name, description):
        self.x = x
        self.y = y
        self.name = name
        self.description = description
        self.connections = {}
        self.enemy = None
        
    def generate_map(self, width, height):
        self.width = width
        self.height = height
        
        # create the locations
        for x in range(width):
            for y in range(height):
                location = Location(f"{x},{y}", f"You are at ({x},{y}).")
                self.locations.append(location)
                
                # randomly generate enemies
                if random.random() < 0.1:
                    enemy_type = random.choice(["goblin", "troll"])
                    enemy = Enemy(enemy_type, 10, 2, 5, f"A {enemy_type} lurks here.")
                    location.enemy = enemy
                    self.enemies.append(enemy)
                
                # randomly generate connections
                if x > 0:
                    if random.random() < 0.5:
                        location.connections["west"] = f"{x-1},{y}"
                        self.get_location(f"{x-1},{y}").connections["east"] = f"{x},{y}"
                if y > 0:
                    if random.random() < 0.5:
                        location.connections["north"] = f"{x},{y-1}"
                        self.get_location(f"{x},{y-1}").connections["south"] = f"{x},{y}"