from fastapi import FastAPI, HTTPException
from game import TicTacToe
import logging
import uvicorn
from logging_config import configure_logging
from file_operations import save_game_data, load_game_data  # Import functions from file_operations.py

# Initialize logging
configure_logging()

# FastAPI app
app = FastAPI()


@app.post("/new-game")
def new_game(game_mode: str):
    """
    Start a new game (POST). Parameters: game_mode ('multiplayer' or 'singleplayer').
    :param game_mode: 'multiplayer' or 'singleplayer'
    :return: 200
    """
    if game_mode not in ["multiplayer", "singleplayer"]:
        raise HTTPException(status_code=400, detail="Invalid game mode. Choose 'multiplayer' or 'singleplayer'.")

    # Create a new TicTacToe game instance
    game = TicTacToe()

    # Generate a new game ID (could use timestamp or UUID for more uniqueness)
    game_id = len(os.listdir("game_data")) + 1  # Simple sequential ID for now

    # Prepare the game state for saving
    game_data = {
        "mode": game_mode,
        "board": game.board,
        "current_player": game.current_player,
        "winner": game.winner,
        "game_over": game.game_over
    }

    # Save the game state to a JSON file
    save_game_data(game_id, game_data)

    logging.info(f"New game started with ID {game_id} in {game_mode} mode.")
    return {"message": f"New {game_mode} game started", "game_id": game_id, "state": game_data}


@app.post("/make-move")
def make_move(game_id: int, row: int, col: int):
    """
    Make a move in the game (POST).
    :param game_id: board identifier
    :param row: row to insert move
    :param col: column to insert move
    :return: 200
    """
    # Load the game state from the JSON file
    game_data = load_game_data(game_id)

    game = TicTacToe()
    game.board = game_data["board"]
    game.current_player = game_data["current_player"]
    game.winner = game_data["winner"]
    game.game_over = game_data["game_over"]

    if game_data["mode"] == "singleplayer" and game.current_player == "O":
        raise HTTPException(status_code=400, detail="It's not the player's turn.")

    # Make the move in the game
    game.make_move(row, col)

    if game_data["mode"] == "singleplayer" and not game.game_over:
        game.computer_move()

    # Save the updated game state to the JSON file
    updated_game_data = {
        "mode": game_data["mode"],
        "board": game.board,
        "current_player": game.current_player,
        "winner": game.winner,
        "game_over": game.game_over
    }
    save_game_data(game_id, updated_game_data)

    return {"message": "Move made", "state": game.get_state()}


@app.get("/state")
def get_state(game_id: int):
    """
    Get the current game state (GET).
    :param game_id: board identifier
    :return: 200
    """
    # Load the game state from the JSON file
    game_data = load_game_data(game_id)

    return {
        "board": game_data["board"],
        "current_player": game_data["current_player"],
        "winner": game_data["winner"],
        "game_over": game_data["game_over"]
    }


if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=5000)
