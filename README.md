
# Tic-Tac-Toe Game Backend - Python API

## Overview
This FastAPI-based Python API serves as the backend for a Tic-Tac-Toe game. It supports both multiplayer and singleplayer game modes. The API allows players to create new games, make moves, and view the game state. In the singleplayer mode, the AI can play against the user, using either a random move (easy difficulty) or a minimax algorithm (hard difficulty). The API is designed to handle the core game logic and includes error handling and logging functionality.

## Installation Steps

### 1. Clone the repository:
```bash
git clone https://github.com/YannaiJackson/tictactoe-api.git
cd tictactoe-api
```

### 2. Install dependencies:
```bash
pip install -r requirements.txt
```

### 3. Run the API:
```bash
python main.py
```
The API will start running at `http://127.0.0.1:5000`.

---

## API Endpoints

### 1. **Create a New Multiplayer Game**
**Endpoint:**  
`POST /multiplayer/new-game`

**Response:**
```json
{
  "message": "New multiplayer game started",
  "game_id": 1,
  "state": {
    "board": [["", "", ""], ["", "", ""], ["", "", ""]],
    "current_player": "X",
    "winner": null,
    "game_over": false
  }
}
```

---

### 2. **Create a New Singleplayer Game**
**Endpoint:**  
`POST /singleplayer/new-game`

**Request Body:**
```json
{
  "difficulty": "easy" // Options: "easy", "hard"
}
```

**Response:**
```json
{
  "message": "New singleplayer game started difficulty: easy",
  "game_id": 1,
  "state": {
    "board": [["", "", ""], ["", "", ""], ["", "", ""]],
    "current_player": "X",
    "winner": null,
    "game_over": false
  }
}
```

---

### 3. **Make a Move in Multiplayer Game**
**Endpoint:**  
`POST /multiplayer/make-move`

**Request Body:**
```json
{
  "game_id": 1,
  "row": 0,
  "column": 1
}
```

**Response:**
```json
{
  "message": "Move made",
  "state": {
    "board": [["", "X", ""], ["", "", ""], ["", "", ""]],
    "current_player": "O",
    "winner": null,
    "game_over": false
  }
}
```

---

### 4. **Make a Move in Singleplayer Game**
**Endpoint:**  
`POST /singleplayer/make-move`

**Request Body:**
```json
{
  "game_id": 1,
  "row": 0,
  "column": 0
}
```

**Response:**
```json
{
  "message": "Move made",
  "state": {
    "board": [["X", "", ""], ["", "O", ""], ["", "", ""]],
    "current_player": "X",
    "winner": null,
    "game_over": false
  }
}
```

---

### 5. **Get Game State**
**Endpoint:**  
`GET /state`

**Query Parameters:**
- `game_id`: The unique ID of the game.

**Response:**
```json
{
  "board": [["X", "", ""], ["", "O", ""], ["", "", ""]],
  "current_player": "X",
  "winner": null,
  "game_over": false
}
```

---

## Running Tests

To run unit tests, make sure you have `pytest` installed:
```bash
pip install pytest
```

Then, run the tests with:
```bash
pytest tests/
```

Tests are organized into modules that cover different aspects of the game functionality, including multiplayer and singleplayer modes, making moves, and fetching game states.

---

## Contributing
Contributions are welcome! Feel free to open an issue or submit a pull request. When contributing, please follow these guidelines:
- Ensure that all new code is well-tested.
- Ensure that your changes are documented.

Please ensure that your contributions are aligned with the overall structure and quality of the project. All pull requests will be reviewed, and feedback will be provided.
