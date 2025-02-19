from fastapi import FastAPI, HTTPException
from game import TicTacToe
from starlette.middleware.cors import CORSMiddleware
import logging

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow specific origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Store games in-memory for the sake of example
games = {}

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


@app.post("/multiplayer/new-game")
def new_multiplayer_game():
    """
    Start a new multiplayer game.
    """
    game_id = len(games) + 1
    game = TicTacToe(game_id)
    games[game_id] = {"game": game}

    logging.info(f"New multiplayer game started with game_id: {game_id}")
    return {"message": "New multiplayer game started", "game_id": game_id, "state": game.get_state()}


@app.post("/singleplayer/new-game")
def new_singleplayer_game(difficulty: str):
    """
    Start a new singleplayer game. Parameters: difficulty ('easy' or 'hard').
    """
    if difficulty not in ["easy", "hard"]:
        raise HTTPException(status_code=400, detail="Invalid difficulty. Choose 'easy' or 'hard'.")

    game_id = len(games) + 1
    game = TicTacToe(game_id)
    games[game_id] = {"game": game, "difficulty": difficulty}

    logging.info(f"New singleplayer game started with game_id: {game_id} and difficulty: {difficulty}")
    return {"message": f"New Single-player game started with difficulty: {difficulty}", "game_id": game_id, "state": game.get_state()}


@app.post("/multiplayer/make-move")
def multiplayer_make_move(game_id: int, row: int, column: int):
    """
    Make a move in multiplayer game. Parameters: game_id, row, column.
    """
    game_data = games.get(game_id)
    if not game_data:
        raise HTTPException(status_code=404, detail="Game not found.")

    logging.info(f"Making move for game_id {game_id} at position ({row}, {column})")

    game = game_data["game"]
    game.make_move(row, column)

    return {"message": "Move made", "state": game.get_state()}


@app.post("/singleplayer/make-move")
def singleplayer_make_move(game_id: int, row: int, column: int, difficulty: str):
    """
    Make a move in singleplayer game. Parameters: game_id, row, column, difficulty.
    """
    game_data = games.get(game_id)
    if not game_data:
        raise HTTPException(status_code=404, detail="Game not found.")

    logging.info(f"Making move for game_id {game_id} at position ({row}, {column}) with difficulty: {difficulty}")

    game = game_data["game"]
    game.make_move(row, column)

    # Handle the computer's move based on difficulty level
    if difficulty == "easy":
        game.computer_easy_move()
    elif difficulty == "hard":
        game.computer_hard_move()
    else:
        raise HTTPException(status_code=400, detail="Invalid difficulty. Choose 'easy' or 'hard'.")

    return {"message": "Move made", "state": game.get_state()}


@app.get("/state")
def get_state(game_id: int):
    """
    Get the current game state. Parameters: game_id.
    """
    game_data = games.get(game_id)
    if not game_data:
        raise HTTPException(status_code=404, detail="Game not found.")

    logging.info(f"Getting state for game_id {game_id}")

    return {"state": game_data["game"].get_state()}
