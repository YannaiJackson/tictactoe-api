def minimax(board, player):
    """Minimax algorithm to find the best move for the computer."""
    def evaluate(board):
        winner = check_winner(board)
        if winner == "O":
            return 1
        elif winner == "X":
            return -1
        elif all(board[r][c] != "" for r in range(3) for c in range(3)):
            return 0
        return None

    def check_winner(board):
        """Check if there is a winner."""
        for i in range(3):
            if board[i][0] == board[i][1] == board[i][2] and board[i][0] != "":
                return board[i][0]
            if board[0][i] == board[1][i] == board[2][i] and board[0][i] != "":
                return board[0][i]

        if board[0][0] == board[1][1] == board[2][2] and board[0][0] != "":
            return board[0][0]
        if board[0][2] == board[1][1] == board[2][0] and board[0][2] != "":
            return board[0][2]
        return None

    def minimax_rec(board, depth, is_maximizing):
        """Minimax recursion."""
        score = evaluate(board)
        if score is not None:
            return score

        if is_maximizing:
            best = -float("inf")
            for r in range(3):
                for c in range(3):
                    if board[r][c] == "":
                        board[r][c] = "O"
                        best = max(best, minimax_rec(board, depth + 1, False))
                        board[r][c] = ""
            return best
        else:
            best = float("inf")
            for r in range(3):
                for c in range(3):
                    if board[r][c] == "":
                        board[r][c] = "X"
                        best = min(best, minimax_rec(board, depth + 1, True))
                        board[r][c] = ""
            return best

    best_val = -float("inf")
    best_move = None
    for r in range(3):
        for c in range(3):
            if board[r][c] == "":
                board[r][c] = "O"
                move_val = minimax_rec(board, 0, False)
                board[r][c] = ""
                if move_val > best_val:
                    best_move = (r, c)
                    best_val = move_val
    return best_move
