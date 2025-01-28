import random
import logging
from fastapi import HTTPException
from algorithms import minimax

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class TicTacToe:
    def __init__(self, game_id):
        self.game_id = game_id
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.current_player = "X"  # Player X starts first
        self.winner = None
        self.game_over = False
        logging.info(f"Game {game_id} initialized. Player X starts.")

    def make_move(self, row, col):
        """Make a move on the board."""
        if self.board[row][col] != "":
            logging.warning(f"Game {self.game_id} - Attempt to make a move in an already occupied cell ({row}, {col}).")
            raise ValueError("Cell already occupied")

        self.board[row][col] = self.current_player
        logging.info(f"Game {self.game_id} - Player {self.current_player} made a move at ({row}, {col}).")

        self.winner = self.check_winner()
        self.game_over = self.winner is not None or all(self.board[r][c] != "" for r in range(3) for c in range(3))

        if self.game_over:
            if self.winner:
                logging.info(f"Game {self.game_id} - Player {self.winner} wins the game!")
            else:
                logging.info(f"Game {self.game_id} - The game ended in a draw.")
        else:
            logging.info(f"Game {self.game_id} - Next player: {self.current_player}.")

        self.current_player = "O" if self.current_player == "X" else "X"

    def check_winner(self):
        """Check if there is a winner."""
        logging.info(f"Game {self.game_id} - Checking winner...")

        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] and self.board[i][0] != "":
                logging.info(f"Game {self.game_id} - Winner found: {self.board[i][0]} (row {i})")
                return self.board[i][0]
            if self.board[0][i] == self.board[1][i] == self.board[2][i] and self.board[0][i] != "":
                logging.info(f"Game {self.game_id} - Winner found: {self.board[0][i]} (column {i})")
                return self.board[0][i]

        if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[0][0] != "":
            logging.info(f"Game {self.game_id} - Winner found: {self.board[0][0]} (diagonal top-left to bottom-right)")
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[0][2] != "":
            logging.info(f"Game {self.game_id} - Winner found: {self.board[0][2]} (diagonal top-right to bottom-left)")
            return self.board[0][2]

        logging.info(f"Game {self.game_id} - No winner found.")
        return None

    def get_state(self):
        """Return the current game state."""
        logging.info(
            f"Game {self.game_id} - Game state requested. Current state: {self.board}, Current player: {self.current_player}, Winner: {self.winner}")

        # Returning game state in a format that matches your frontend expectations
        return {
            "game_id": self.game_id,  # Ensure game_id is part of the response
            "board": self.board,  # The board array (3x3 grid)
            "winner": self.winner,  # Winner ('X', 'O', or None)
            "game_over": self.game_over,  # True if the game is over, otherwise False
        }

    def computer_easy_move(self):
        """Make an easy computer move by choosing a random empty spot."""
        if self.game_over:
            logging.warning(f"Game {self.game_id} - Attempt to make a move, but the game is already over.")
            raise HTTPException(status_code=400, detail="Game is already over.")

        # Find all empty cells
        empty_cells = [(row, col) for row in range(3) for col in range(3) if self.board[row][col] == ""]
        if not empty_cells:
            logging.warning(f"Game {self.game_id} - No empty cells available for the computer to make a move.")
            raise HTTPException(status_code=400, detail="No moves left.")

        # Choose a random empty cell
        row, col = random.choice(empty_cells)
        self.make_move(row, col)
        logging.info(f"Game {self.game_id} - Computer made an easy move at ({row}, {col}).")

    def computer_hard_move(self):
        """Make a hard computer move using the Minimax algorithm."""
        if self.game_over:
            logging.warning(f"Game {self.game_id} - Attempt to make a move, but the game is already over.")
            raise HTTPException(status_code=400, detail="Game is already over.")

        # Get the best move using Minimax
        best_move = minimax(self.board, "O")
        if best_move:
            row, col = best_move
            self.make_move(row, col)
            logging.info(f"Game {self.game_id} - Computer made a hard move at ({row}, {col}).")
        else:
            logging.warning(f"Game {self.game_id} - No valid moves available for the computer.")
            raise HTTPException(status_code=400, detail="No moves left.")
