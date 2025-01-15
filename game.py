import random
from typing import Optional
from fastapi import HTTPException
import logging


# Define the TicTacToe class
class TicTacToe:
    def __init__(self):
        # Initialize the game board with empty cells
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.current_player = "X"  # X always starts
        self.winner: Optional[str] = None
        self.game_over = False

    def make_move(self, row: int, col: int):
        if self.game_over:
            raise HTTPException(status_code=400, detail="Game is already over.")
        if not (0 <= row < 3 and 0 <= col < 3):
            raise HTTPException(status_code=400, detail="Invalid board position.")
        if self.board[row][col] != "":
            raise HTTPException(status_code=400, detail="Cell is already occupied.")

        # Place the current player's mark on the board
        self.board[row][col] = self.current_player
        logging.info(f"Player {self.current_player} made a move at ({row}, {col}).")

        # Check if this move wins the game
        if self.check_winner(row, col):
            self.winner = self.current_player
            self.game_over = True
            logging.info(f"Player {self.current_player} wins!")
        elif all(cell != "" for row in self.board for cell in row):
            # If the board is full and there's no winner, it's a tie
            self.game_over = True
            logging.info("The game is a tie.")
        else:
            # Switch to the next player
            self.current_player = "O" if self.current_player == "X" else "X"

    def computer_move(self):
        if self.game_over:
            raise HTTPException(status_code=400, detail="Game is already over.")

        # Find all empty cells
        empty_cells = [(row, col) for row in range(3) for col in range(3) if self.board[row][col] == ""]
        if not empty_cells:
            raise HTTPException(status_code=400, detail="No moves left.")

        # Choose a random empty cell
        row, col = random.choice(empty_cells)
        self.make_move(row, col)
        logging.info(f"Computer made a move at ({row}, {col}).")

    def check_winner(self, row: int, col: int) -> bool:
        # Check the row, column, and diagonals
        player = self.current_player
        return (
            all(self.board[row][c] == player for c in range(3)) or
            all(self.board[r][col] == player for r in range(3)) or
            (row == col and all(self.board[i][i] == player for i in range(3))) or
            (row + col == 2 and all(self.board[i][2 - i] == player for i in range(3)))
        )

    def get_state(self):
        return {
            "board": self.board,
            "current_player": self.current_player,
            "winner": self.winner,
            "game_over": self.game_over,
        }
