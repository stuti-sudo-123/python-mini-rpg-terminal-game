from player import Player
from world import World
from enemy import Enemy
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
            pass
            

