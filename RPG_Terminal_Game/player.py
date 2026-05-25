class player:
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
        while self.xp>self.xp_to_next:
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
        pass