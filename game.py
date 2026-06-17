from player import Player
from world import World
from combat import Combat
from save_system import save_game , load_game,save_exists,delete_save
class Game:
    def __init__(self):
        self.player=None
        self.world=None
        self.running=False
    def start(self):
        self._show_title()
        choice=self._main_menu()
        if choice=="new":
            self._new_game()
        elif choice=="load":
            self._load_game()
        else:
            return
        self.running=True
        self._game_loop()
    def _show_title(self):
        print("=" * 50)
        print("     ⚡ VOID WALKER ⚡")
        print("=" * 50)
    def _main_menu(self):
        while True:
            print("\nMain Menu:")
            print("1. New Game")
            print("2. Load Game" if save_exists() else "2. Load Game (no save found)")
            print("3. Quit")
            choice = input("> ").strip().lower()
            if choice in ("1", "new"):
                return "new"
            elif choice in ("2", "load") and save_exists():
                return "load"
            elif choice in ("3", "quit", "q"):
                return "quit"
            else:
                print("Enter a valid choice.")
    def _new_game(self):
        name = input("Enter your name, Void Walker: ").strip() or "Kael"
        self.player = Player(name)
        self.world = World()
        print(f"\nWelcome, {self.player.name}. Your journey begins...")
    def _load_game(self):
        player_data,world_data=load_game()
        self.player=Player.from_dict(player_data)
        self.world = World()
        self.world.from_dict(world_data)
        print(f"Welcome back, {self.player.name}.")
    def _game_loop(self):
        self._look_at_room()
        while self.running and self.player.is_alive():
            raw=input("\n> ").strip().lower()
            if not raw:
                continue
            self._handle_command(raw)
    def _handle_command(self,raw):
        parts=raw.split()
        cmd=parts[0]
        args=parts[1:] if len(parts)>1 else []
        if cmd in ("go", "move") and args:
            self._move(args[0])
        elif cmd in ("n", "north"):   self._move("north")
        elif cmd in ("s", "south"):   self._move("south")
        elif cmd in ("e", "east"):    self._move("east")
        elif cmd in ("w", "west"):    self._move("west")
        elif cmd == "look":           self._look_at_room()
        elif cmd == "take" and args:  self._take_item(" ".join(args))
        elif cmd == "use" and args:   self._use_item(" ".join(args))
        elif cmd == "stats":          self.player.show_stats()
        elif cmd in ("inv", "inventory"): self.player.show_inventory()
        elif cmd == "save":           save_game(self.player, self.world)
        elif cmd in ("help", "h"):    self._show_help()
        elif cmd in ("quit", "q"):    self._quit()
        else: print("Unknown command. Type help.")
    def _look_at_room(self):
        room=self.world.get_room(self.player.current_room)
        self.world.mark_visited(self.player.current_room)
        print(f"\n{room['emoji']} {room['name']}")
        print(room['description'])
        if room["items"]:
            print("Items: "+ ", ".join(i["name"] for i in room["items"]))
        enemies=self.world.get_live_enemies(self.player.current_room)
        if enemies:
            print("Enemies: " + ", ".join(f"{e.emoji} {e.name}" for e in enemies))
        if room['exits']:
            print("Exits: " + ", ".join(room['exits'].keys()))
        else:
            print("No exits — find the Quantum Shard to teleport.")
    def _move(self,direction):
        room=self.world.get_room(self.player.current_room)
        if direction not in room['exits']:
                print(f"You can't go {direction} from here.")
                return
        if self.world.get_live_enemies(self.player.current_room):
            print("Defeat all enemies before moving!")
            return        
        self.player.current_room=room['exits'][direction]
        self._look_at_room()
        self._check_for_combat()
    def _take_item(self,item_name):
        item,signal=self.world.take_item(self.player.current_room,item_name)
        if not item:
            print(signal)
            return
        if signal=="teleporter_activate":
            print("⚡ Quantum Shard acquired! Teleporting...")
            next_room=self.world.next_level()
            if next_room=="game_complete":
                self._victory()
                return
            self.player.current_room=next_room
            self._look_at_room()
            self._check_for_combat()
        else:
            self.player.add_item(item)
            print(f"✅ Picked up {item['name']}.") 
    def _use_item(self,item_name):
        success,msg=self.player.use_item(item_name)
        print(msg)
    def _check_for_combat(self):
        enemies=self.world.get_live_enemies(self.player.current_room)
        if not enemies:
            return
        combat=Combat(self.player,enemies)
        result=combat.run()
        if result == "victory":
            print("\n🏆 All threats eliminated!")
            combat.distribute_rewards()
            self._check_win()
        elif result == "dead":
            self._game_over()
        elif result == "fled":
            print("You retreated!")
    def _check_win(self):
        if self.player.current_room == "void_nexus":
            if not self.world.get_live_enemies("void_nexus"):
                self._victory()
    def _game_over(self):
        print("\n💀 GAME OVER")
        print(f"{self.player.name} has fallen in the void.")
        delete_save()
        self.running = False
    def _victory(self):
        print("\n🌌 YOU WIN!")
        print(f"{self.player.name} has defeated The Ancient One!")
        print(f"Level reached: {self.player.level}")
        print(f"Crystals collected: {self.player.gold}")
        delete_save()
        self.running = False
    def _quit(self):
        answer = input("Save before quitting? (y/n) > ").strip().lower()
        if answer == "y":
            save_game(self.player, self.world)
        print("Farewell, Void Walker.")
        self.running = False
    def _show_help(self):
        print("\n── COMMANDS ─────────────────────")
        print("go <direction>   move between rooms")
        print("n/s/e/w          shortcut movement")
        print("look             describe current room")
        print("take <item>      pick up an item")
        print("use <item>       use from inventory")
        print("stats            show your stats")
        print("inv              show inventory")
        print("save             save game")
        print("quit             quit game")
        print("─────────────────────────────────")
if __name__ == "__main__":
    game = Game()
    game.start()