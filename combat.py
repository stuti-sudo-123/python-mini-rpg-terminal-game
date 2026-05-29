import random
class Combat:
    def __init__(self,player,enemies):
        self.player=player
        self.enemies=enemies
    def run(self):
        print("\n⚔ COMBAT STARTED")
        for e in self.enemies:
            print(f"  {e.emoji} {e.name} appears!")
        while self.player.is_alive() and any(e.is_alive() for e in self.enemies):
            self._show_status()
            action = self._get_action()
            if action == "fight":
                self._player_attacks()
            elif action == "use":
                item_name = input("Use which item? > ").strip()
                success, msg = self.player.use_item(item_name)
                print(msg)
            elif action == "flee":
                if self._attempt_flee():
                    return "fled"
            if not any(e.is_alive() for e in self.enemies):
                break
            self._enemies_attack()
        if not self.player.is_alive():
            return "dead"
        return "victory"
    def _show_status(self):
        filled=int((self.player.health/self.player.max_health)*20)
        bar = "█" * filled + "░" * (20 - filled)
        print(f"{self.player.name }{bar }{self.player.health}/{self.player.max_health}")
        for e in self.enemies:
            if e.is_alive():
                print(e.emoji, e.name, e.health_bar())
    def _get_action(self):
        print("OPTIONS:")
        print('''
                1. fight
                2. use item
                3. flee
            ''')
        while True:
            choice=input("> ").strip().lower()
            if choice in ("1", "fight", "f", "attack"):
                return "fight"
            elif choice in ("2", "use", "u"):
                return "use"
            elif choice in ("3", "flee", "run", "r"):
                return "flee"
            else:
                print("Type fight, use, or flee")
    def _player_attacks(self):
        alive_enemies=[e for e in self.enemies if e.is_alive()]
        target = alive_enemies[0]   
        raw_damage = self.player.attack + random.randint(-2, 4)
        actual_damage = target.take_damage(raw_damage)
        print(f"You hit {target.emoji} {target.name} for {actual_damage} damage!")
        if not target.is_alive():
            print(f"{target.emoji} {target.name} defeated!")
    def _enemies_attack(self):
        for e in self.enemies:
            if e.is_alive():
                raw=e.attack_player()
                damage=self.player.take_damage(raw)
                print(f"{e.emoji} {e.name} hits you for {damage} damage!")
    def _attempt_flee(self):
        if random.random() < 0.5:
            print("You escaped!")
            return True
        else:
            print("You couldn't escape!")
            return False
    def distribute_rewards(self):
        total_gold=0
        all_loot=[]
        for e in self.enemies:
            gold,items=e.drop_loot()
            total_gold+=gold
            all_loot.extend(items)
        self.player.gold+=total_gold
        print(f"💰 You found {total_gold} crystals!")
        for item in all_loot:
            self.player.add_item(item)
            print(f"🎁 Found: {item['name']}")
        total_xp = sum(e.xp_reward for e in self.enemies)
        self.player.gain_xp(total_xp)
        print(f"✨ Gained {total_xp} XP")
