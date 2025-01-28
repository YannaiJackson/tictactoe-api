import json
import os
from fastapi import HTTPException

# Directory to store game data
GAME_DATA_DIR = "game_data"

# Ensure the directory exists
os.makedirs(GAME_DATA_DIR, exist_ok=True)


def save_game_data(game_id: int, game_data: dict):
    """Save the game state to a JSON file."""
    file_path = os.path.join(GAME_DATA_DIR, f"game_{game_id}.json")
    with open(file_path, "w") as f:
        json.dump(game_data, f, indent=4)


def load_game_data(game_id: int) -> dict:
    """Load the game state from a JSON file."""
    file_path = os.path.join(GAME_DATA_DIR, f"game_{game_id}.json")
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Game ID not found.")
    with open(file_path, "r") as f:
        return json.load(f)
