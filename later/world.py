        self.locations = [
            [Location(0, 0, "start", "You are at the start of your journey."),
             Location(1, 0, "forest", "You are in a dark forest."),
             Location(2, 0, "beach", "You are on a sunny beach."),
             Location(3, 0, "mountain", "You are on a rugged mountain.")],
            [Location(0, 1, "cave", "You are in a dark cave."),
             Location(1, 1, "field", "You are in a vast field."),
             Location(2, 1, "river", "You are next to a rushing river."),
             Location(3, 1, "desert", "You are in a scorching desert.")],
            [Location(0, 2, "town", "You are in a small town."),
             Location(1, 2, "village", "You are in a peaceful village."),
             Location(2, 2, "castle", "You are in a grand castle."),
             Location(3, 2, "dungeon", "You are in a dark dungeon.")],
            [Location(0, 3, "swamp", "You are in a murky swamp."),
             Location(1, 3, "jungle", "You are in a dense jungle."),
             Location(2, 3, "ruins", "You are in ancient ruins."),
             Location(3, 3, "end", "You have reached the end of your journey!")]
        ]
        self.enemies = {
            "goblin": Enemy("goblin", 10, 2, 5, "A small and fierce goblin."),
            "troll": Enemy("troll", 20, 5, 10, "A large and strong troll.")
        }