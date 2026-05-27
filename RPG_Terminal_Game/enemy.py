import random
ENEMY_TYPES = {
    "spore_crawler": {
        "name":    "Spore Crawler",
        "health":  30,
        "attack":  8,
        "defense": 2,
        "xp":      20,
        "gold":    (2, 6),
        "emoji":   "🍄",
        "loot":    [
            {"name": "Nano Injector", "type": "heal", "value": 25, "chance": 0.3}
        ]
    },
    "void_shade": {
        "name":    "Void Shade",
        "health":  45,
        "attack":  12,
        "defense": 4,
        "xp":      35,
        "gold":    (4, 10),
        "emoji":   "👻",
        "loot":    [
            {"name": "Nano Injector", "type": "heal", "value": 25, "chance": 0.25}
        ]
    },
    "titan_brute": {
        "name":    "Titan Brute",
        "health":  70,
        "attack":  18,
        "defense": 8,
        "xp":      55,
        "gold":    (8, 18),
        "emoji":   "🗿",
        "loot":    [
            {"name": "Plasma Cell", "type": "heal", "value": 50, "chance": 0.4}
        ]
    },
    "ancient_one": {
        "name":    "The Ancient One",
        "health":  150,
        "attack":  30,
        "defense": 15,
        "xp":      150,
        "gold":    (30, 60),
        "emoji":   "🌌",
        "loot":    [
            {"name": "Void Essence", "type": "heal", "value": 100, "chance": 0.8}
        ]
    }
}
class Enemy:
    def __init__(self,enemy_type):
        data=ENEMY_TYPES.get(enemy_type.lower())
        if not data:
            raise ValueError(f"Unknown enemy type: '{enemy_type}'")
        self.name = data["name"]
        self.health = data["health"]
        self.max_health = data["health"]  
        self.attack = data["attack"]
        self.defense = data["defense"]
        self.xp_reward = data["xp"]
        self.gold_range = data["gold"]
        self.emoji = data["emoji"]
        self.loot_table = data["loot"]
        self.type = enemy_type      
    def is_alive(self):
        return self.health>0
    def take_damage(self,amount):
        damage = max(1, amount - self.defense)
        self.health = max(0, self.health - damage)
        return damage
    def attack_player(self):
        return self.attack+random.randint(-2,3)
    def drop_loot(self):
        gold=random.randint(self.gold_range[0],self.gold_range[1])
        dropped_items=[]
        for item in self.loot_table:
            if random.random()<item["chance"]:
                drop={k:v for k,v in item.items() if k!="chance"}
                dropped_items.append(drop)
        return gold,dropped_items
    def health_bar(self):
        filled=int((self.health / self.max_health)*20)
        empty=20-filled
        bar="█" * filled + "░" * empty
        return bar + f"{ self.health}/{self.max_health}"