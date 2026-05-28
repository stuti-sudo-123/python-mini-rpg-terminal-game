import os
import json
from player import Player
from world import World

SAVE_FILE="save.json"

def save_game(player,world):
    player_data=player.to_dict()
    world_data=world.to_dict()
    data={
        "player": player_data,
        "world": world_data
    }
    with open(SAVE_FILE,"w") as f:
        json.dump(data,f,indent=2)
    print("💾 Game saved.")
def load_game():
    with open(SAVE_FILE,"r") as f:
        data=json.load(f)
    return data["player"],data["world"]
def save_exists():
    return os.path.exists(SAVE_FILE)
def delete_save():
    if save_exists():
        os.remove(SAVE_FILE)
        
