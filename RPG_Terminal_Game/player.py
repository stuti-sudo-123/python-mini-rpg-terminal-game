class Player:
    def __init__(self,name):
        self.name=name
        self.health=100
        self.max_health=100
        self.attack = 15
        self.defense = 5
        self.level = 1
        self.xp = 0
        self.xp_to_next = 50
        self.gold = 10
        self.inventory = []
        self.current_room = "entrance"
    def take_damage(self,amount):
        damage=max(1,amount-self.defense)
        self.health=max(0,self.health-damage)
        return damage
    def is_alive(self):
        return self.health>0
    def heal(self,amount):
        healed=min(self.max_health-self.health,amount)
        self.health+=healed
        return healed
    def gain_xp(self,amount):
        self.xp+=amount
        leveled_up=False
        while self.xp>=self.xp_to_next:
            self.xp-=self.xp_to_next
            self.level_up()
            leveled_up=True
        return leveled_up
    def level_up(self):
        self.level += 1
        self.max_health += 20
        self.health = self.max_health
        self.attack += 5
        self.defense += 2
        self.xp_to_next = int(self.xp_to_next * 1.5)
        print(f"⭐ LEVEL UP! You are now level {self.level}!")
    def add_item(self,item):
        self.inventory.append(item)
    def use_item(self,item_name):
        item = next((i for i in self.inventory if i["name"].lower()==item_name.lower()),
                    None)
        if not item:
            return False,f"You do not have {item_name}"
        if item["type"]=="heal":
            healed=self.heal(item["value"])
            self.inventory.remove(item)
            return True,f"Used {item_name} and Restored {healed} HP"
        return False, "You can't use that here."
    def show_stats(self):
        print(f"── {self.name} ───────────────────")
        print(f"Level:   {self.level}")
        print(f"HP:      {self.health}/{self.max_health}")
        print(f"XP:      {self.xp}/{self.xp_to_next}")
        print(f"Attack:  {self.attack}")
        print(f"Defense: {self.defense}")
        print(f"Gold:    {self.gold}")
        print(f"Items:   {len(self.inventory)}")
    def to_dict(self):
        return {
            "name": self.name,
            "health": self.health,
            "max_health": self.max_health,
            "attack": self.attack,
            "defense": self.defense,
            "level": self.level,
            "xp": self.xp,
            "xp_to_next": self.xp_to_next,
            "gold": self.gold,
            "inventory": self.inventory,
            "current_room": self.current_room,
        }
    @classmethod
    def from_dict(cls,data):
        p=cls(data["name"])
        p.health = data["health"]
        p.max_health = data["max_health"]
        p.attack = data["attack"]
        p.defense = data["defense"]
        p.level = data["level"]
        p.xp = data["xp"]
        p.xp_to_next = data["xp_to_next"]
        p.gold = data["gold"]
        p.inventory = data["inventory"]
        p.current_room = data["current_room"]
        return p        
