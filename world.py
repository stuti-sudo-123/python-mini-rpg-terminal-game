import copy
from enemy import Enemy
ROOMS = {

    # ── LEVEL 1 — Planet Auren — 1 room ──────
    "auren_crash": {
        "name":        "Crash Site — Planet Auren",
        "description": "Your ship lies shattered across golden sand dunes. Strange glowing symbols pulse on nearby rocks. Two pale suns hang motionless in a violet sky. A Quantum Shard glints in the wreckage — your only way forward.",
        "exits":       {},
        "enemies":     [],
        "items":       [
            {"name": "Nano Injector", "type": "heal", "value": 25},
            {"name": "Quantum Shard", "type": "teleporter", "value": 0},
        ],
        "emoji":       "🪐",
        "visited":     False,
        "level":       1,
    },

    # ── LEVEL 2 — Planet Virek — 1 room ──────
    "virek_jungle": {
        "name":        "Neon Jungle — Planet Virek",
        "description": "Towering plants pulse with blue and violet light. The air smells electric. Spore Crawlers nest between the glowing roots, launching clouds of toxic spores at anything that moves.",
        "exits":       {},
        "enemies":     ["spore_crawler", "spore_crawler"],
        "items":       [
            {"name": "Nano Injector", "type": "heal", "value": 25},
            {"name": "Quantum Shard", "type": "teleporter", "value": 0},
        ],
        "emoji":       "🌿",
        "visited":     False,
        "level":       2,
    },

    # ── LEVEL 3 — Planet Shen — 1 room ───────
    "crystal_caves": {
        "name":        "Crystal Caves — Planet Shen",
        "description": "Enormous crystals jut from the cave walls, each humming a different frequency. Ancient alien carvings cover every surface. Void Shades phase in and out of the crystal walls.",
        "exits":       {},
        "enemies":     ["void_shade", "void_shade"],
        "items":       [
            {"name": "Nano Injector", "type": "heal", "value": 25},
            {"name": "Quantum Shard", "type": "teleporter", "value": 0},
        ],
        "emoji":       "💎",
        "visited":     False,
        "level":       3,
    },

    # ── LEVEL 4 — Planet Morvak — 1 room ─────
    "acid_swamps": {
        "name":        "Acid Swamps — Planet Morvak",
        "description": "Toxic green fog rolls across bubbling pools of acid. The sky is permanently overcast, the colour of a bruise. A Titan Brute wades through the swamp toward you, its crystal armour hissing where the acid touches it.",
        "exits":       {},
        "enemies":     ["titan_brute"],
        "items":       [
            {"name": "Plasma Cell", "type": "heal", "value": 50},
            {"name": "Quantum Shard", "type": "teleporter", "value": 0},
        ],
        "emoji":       "🧪",
        "visited":     False,
        "level":       4,
    },

    # ── LEVEL 5 — Planet Elyon — 1 room ──────
    "sky_citadel": {
        "name":        "Sky Citadel — Planet Elyon",
        "description": "Ruins of an alien civilisation float on islands of rock suspended in pale clouds. Two Titan Brutes guard the central platform, their crystal armour catching the light of three distant moons.",
        "exits":       {},
        "enemies":     ["titan_brute", "titan_brute"],
        "items":       [
            {"name": "Plasma Cell", "type": "heal", "value": 50},
            {"name": "Quantum Shard", "type": "teleporter", "value": 0},
        ],
        "emoji":       "🏛",
        "visited":     False,
        "level":       5,
    },

    # ── LEVEL 6 — Planet Draak — 1 room ──────
    "volcanic_core": {
        "name":        "Volcanic Core — Planet Draak",
        "description": "The heart of a living volcano. Lava falls from the ceiling like waterfalls. The rock walls glow orange. Void Shades flicker between the lava streams while a Titan Brute stands guard at the centre.",
        "exits":       {},
        "enemies":     ["void_shade", "void_shade", "titan_brute"],
        "items":       [
            {"name": "Plasma Cell", "type": "heal", "value": 50},
            {"name": "Quantum Shard", "type": "teleporter", "value": 0},
        ],
        "emoji":       "🌋",
        "visited":     False,
        "level":       6,
    },

    # ── LEVEL 7 — Planet Kryos — 2 rooms ─────
    "frozen_wastes": {
        "name":        "Frozen Wastes — Planet Kryos",
        "description": "A blizzard tears across a flat expanse of white. Visibility is near zero. Frozen alien soldiers stand like statues in the ice — until you get close enough. Head east to find shelter.",
        "exits":       {"east": "ice_sanctum"},
        "enemies":     ["void_shade", "titan_brute"],
        "items":       [
            {"name": "Plasma Cell", "type": "heal", "value": 50},
        ],
        "emoji":       "❄️",
        "visited":     False,
        "level":       7,
    },
    "ice_sanctum": {
        "name":        "Ice Sanctum — Planet Kryos",
        "description": "A cathedral of ice deep beneath the frozen surface. Every surface reflects your image back at you — slightly wrong. Two Titan Brutes guard the Quantum Shard. Beyond this, only the Void.",
        "exits":       {"west": "frozen_wastes"},
        "enemies":     ["titan_brute", "titan_brute"],
        "items":       [
            {"name": "Void Essence", "type": "heal", "value": 100},
            {"name": "Quantum Shard", "type": "teleporter", "value": 0},
        ],
        "emoji":       "🧊",
        "visited":     False,
        "level":       7,
    },

    # ── LEVEL 8 — The Void Nexus — 3 rooms ───
    "void_entrance": {
        "name":        "Void Entrance — The Threshold",
        "description": "Reality fractures at the edges. The floor beneath you is made of solidified darkness. Stars drift past at eye level. Two Ancient Shades — evolved Void Shades warped by the Nexus — block your path east.",
        "exits":       {"east": "void_heart"},
        "enemies":     ["void_shade", "void_shade", "void_shade"],
        "items":       [
            {"name": "Void Essence", "type": "heal", "value": 100},
        ],
        "emoji":       "🌑",
        "visited":     False,
        "level":       8,
    },
    "void_heart": {
        "name":        "Void Heart — The In-Between",
        "description": "The centre of nothing. No sound exists here — your footsteps, your breathing, your heartbeat all vanish into silence. Titan Brutes warped by void energy patrol the darkness. You can feel The Ancient One watching.",
        "exits":       {"west": "void_entrance", "east": "void_nexus"},
        "enemies":     ["titan_brute", "titan_brute", "void_shade"],
        "items":       [
            {"name": "Void Essence", "type": "heal", "value": 100},
        ],
        "emoji":       "🕳️",
        "visited":     False,
        "level":       8,
    },
    "void_nexus": {
        "name":        "The Void Nexus — End of Everything",
        "description": "Pure darkness. No floor, no ceiling, no walls — just infinite black space punctuated by drifting stars. In the centre floats The Ancient One, an entity older than the universe itself. It has been waiting. Its eyes open.",
        "exits":       {"west": "void_heart"},
        "enemies":     ["ancient_one"],
        "items":       [],
        "emoji":       "🌌",
        "visited":     False,
        "level":       8,
        "is_boss":     True,
    },
}
LEVEL_START_ROOMS=[
    "auren_crash",
    "virek_jungle",
    "crystal_caves",
    "acid_swamps",
    "sky_citadel",
    "volcanic_core,"
    "frozen_wastes",
    "void_entrance"
]
class World:
    def __init__(self):
        self.rooms=copy.deepcopy(ROOMS)
        self.current_level=1
        self._spawn_enemies()
    def _spawn_enemies(self):
        for room in self.rooms.values():
            room["enemy_objects"]=[Enemy(e) for e in room["enemies"]]
    def get_room(self,room_id):
        return self.rooms.get(room_id)
    def get_live_enemies(self,room_id):
        room=self.rooms.get(room_id)
        if not room:
            return []
        return [e for e in room["enemy_objects"] if e.is_alive()]
    def mark_visited(self,room_id):
        room=self.rooms.get(room_id)
        if not room:
            return 
        room["visited"]=True
    def take_item(self,room_id,item_name):
        room=self.rooms.get(room_id)
        item=next((i for i in room["items"] if i["name"].lower()==item_name.lower()),None)
        if not item :
            return None, f"No item with {item_name} name"
        if item["type"]=="teleporter":
            if self.get_live_enemies(room_id):
                return None,"Kill all enemies first"
            else:
                room["items"].remove(item)
                return item, "teleporter_activated"
        else:
            room["items"].remove(item)
            return item, "picked_up"
    def next_level(self):
        self.current_level+=1
        if self.current_level>len(LEVEL_START_ROOMS):
            return "game_complete"
        return LEVEL_START_ROOMS[self.current_level-1]
    def to_dict(self):
        room_data={}
        for room_id, room in self.rooms.items():
            room_data[room_id]={
            "visited":        room["visited"],
            "items":          room["items"],
            "enemies_alive": [e.type for e in self.get_live_enemies(room_id)]
            }
        return {
                "current_level": self.current_level,
                "rooms": room_data
            }
    def from_dict(self,data):
        self.current_level=data["current_level"]
        for room_id,room in self.rooms.items():
            room_data=data["rooms"][room_id]
            room["visited"]=room_data["visited"]
            room["enemy_objects"]=[Enemy(e) for e in room_data["enemies_alive"]]
            room["items"]= room_data["items"]
