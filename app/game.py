import random
import logging
from fastapi import HTTPException
from algorithms import minimax

class TicTacToe:
    def __init__(self):
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.current_player = "X"  # Player starts first
        self.winner = None
        self.game_over = False

    def make_move(self, row, col):
        """Make a move on the board."""
        if self.board[row][col] != "":
            raise ValueError("Cell already occupied")
        self.board[row][col] = self.current_player
        self.winner = self.check_winner()
        self.game_over = self.winner is not None or all(self.board[r][c] != "" for r in range(3) for c in range(3))
        self.current_player = "O" if self.current_player == "X" else "X"

    def check_winner(self):
        """Check if there is a winner."""
        for i in range(3):
            if self.board[i][0] == self.board[i][1] == self.board[i][2] and self.board[i][0] != "":
                return self.board[i][0]
            if self.board[0][i] == self.board[1][i] == self.board[2][i] and self.board[0][i] != "":
                return self.board[0][i]

        if self.board[0][0] == self.board[1][1] == self.board[2][2] and self.board[0][0] != "":
            return self.board[0][0]
        if self.board[0][2] == self.board[1][1] == self.board[2][0] and self.board[0][2] != "":
            return self.board[0][2]

        return None

    def get_state(self):
        """Return the current game state."""
        return {
            "board": self.board,
            "current_player": self.current_player,
            "winner": self.winner,
            "game_over": self.game_over
        }

    def computer_easy_move(self):
        """Make an easy computer move by choosing a random empty spot."""
        if self.game_over:
            raise HTTPException(status_code=400, detail="Game is already over.")

        # Find all empty cells
        empty_cells = [(row, col) for row in range(3) for col in range(3) if self.board[row][col] == ""]
        if not empty_cells:
            raise HTTPException(status_code=400, detail="No moves left.")

        # Choose a random empty cell
        row, col = random.choice(empty_cells)
        self.make_move(row, col)
        logging.info(f"Computer made an easy move at ({row}, {col}).")

    def computer_hard_move(self):
        """Make a hard computer move using the Minimax algorithm."""
        if self.game_over:
            raise HTTPException(status_code=400, detail="Game is already over.")

        # Get the best move using Minimax
        best_move = minimax(self.board, "O")
        if best_move:
            row, col = best_move
            self.make_move(row, col)
            logging.info(f"Computer made a hard move at ({row}, {col}).")
        else:
            raise HTTPException(status_code=400, detail="No moves left.")
