# Tic-Tac-Toe with Minimax and Alpha-Beta Pruning
# CAP4630 - Artificial Intelligence
# Nickie Dorilus

def print_board(board):
    """Pretty-print the Tic-Tac-Toe board."""
    print()
    print(f" {board[0]} | {board[1]} | {board[2]} ")
    print("---+---+---")
    print(f" {board[3]} | {board[4]} | {board[5]} ")
    print("---+---+---")
    print(f" {board[6]} | {board[7]} | {board[8]} ")
    print()


def check_winner(board):
    """
    Check if someone has won.
    Returns "X" if X wins, "O" if O wins, or None otherwise.
    """
    winning_lines = [
        (0, 1, 2),  # rows
        (3, 4, 5),
        (6, 7, 8),
        (0, 3, 6),  # columns
        (1, 4, 7),
        (2, 5, 8),
        (0, 4, 8),  # diagonals
        (2, 4, 6)
    ]

    for a, b, c in winning_lines:
        if board[a] != " " and board[a] == board[b] == board[c]:
            return board[a]  # "X" or "O"

    return None  # no winner yet


def is_draw(board):
    """Return True if the board is full and there is no winner."""
    return " " not in board and check_winner(board) is None


def minimax(board, depth, is_maximizing, ai_player, human_player, alpha, beta):
    """
    Minimax algorithm with Alpha-Beta pruning.

    board        : current board state (list of 9 cells)
    depth        : how deep we are in the game tree
    is_maximizing: True if it's AI's turn, False if it's human's turn
    ai_player    : "X" or "O" (the AI's symbol)
    human_player : "X" or "O" (the human's symbol)
    alpha, beta  : alpha-beta pruning values

    Returns a score from the AI's point of view:
        + (positive) if the position is good for AI
        - (negative) if the position is good for human
        0 if it's a draw.
    """

    winner = check_winner(board)

    # Base cases: someone won or it's a draw.
    if winner == ai_player:
        # AI wins -> positive score, faster wins are better (10 - depth)
        return 10 - depth
    if winner == human_player:
        # Human wins -> negative score, slower losses are better (depth - 10)
        return depth - 10
    if is_draw(board):
        return 0

    if is_maximizing:
        # AI's turn: try to maximize the score
        best_score = -float("inf")

        for i in range(9):
            if board[i] == " ":
                board[i] = ai_player
                score = minimax(board, depth + 1, False,
                                ai_player, human_player, alpha, beta)
                board[i] = " "  # undo move

                if score > best_score:
                    best_score = score

                # Alpha-Beta pruning update
                if best_score > alpha:
                    alpha = best_score
                if beta <= alpha:
                    # Cut off: opponent will avoid this path
                    break

        return best_score

    else:
        # Human's turn: try to minimize the score
        best_score = float("inf")

        for i in range(9):
            if board[i] == " ":
                board[i] = human_player
                score = minimax(board, depth + 1, True,
                                ai_player, human_player, alpha, beta)
                board[i] = " "  # undo move

                if score < best_score:
                    best_score = score

                # Alpha-Beta pruning update
                if best_score < beta:
                    beta = best_score
                if beta <= alpha:
                    # Cut off
                    break

        return best_score


def find_best_move(board, ai_player, human_player):
    """
    Try all possible moves for the AI and pick the one
    with the best minimax score.
    """
    best_score = -float("inf")
    best_move_index = None

    for i in range(9):
        if board[i] == " ":
            # Try move
            board[i] = ai_player
            score = minimax(board, 0, False,
                            ai_player, human_player,
                            -float("inf"), float("inf"))
            # Undo move
            board[i] = " "

            if score > best_score:
                best_score = score
                best_move_index = i

    return best_move_index


def get_human_move(board):
    """
    Ask the human to choose a move (1-9).
    Validate input and make sure the chosen cell is empty.
    """
    while True:
        move_str = input("Choose your move (1-9): ").strip()

        if move_str.isdigit():
            move = int(move_str) - 1  # convert 1-9 to 0-8

            if 0 <= move <= 8:
                if board[move] == " ":
                    return move
                else:
                    print("That spot is already taken. Try again.")
            else:
                print("Your move must be between 1 and 9.")
        else:
            print("Please type a number from 1 to 9.")


def main():
    print("Welcome to Tic-Tac-Toe with Minimax + Alpha-Beta!")
    print("Board positions are numbered like this:")

    # Show a demo board with numbers so player knows the positions.
    demo_board = [str(i + 1) for i in range(9)]
    print_board(demo_board)

    # Ask player to choose X or O
    while True:
        human_player = input("Do you want to be X or O? ").upper().strip()
        if human_player in ("X", "O"):
            break
        print("Please type X or O.")

    ai_player = "O" if human_player == "X" else "X"
    print(f"You are {human_player}. The AI is {ai_player}.")

    # Ask who goes first
    while True:
        first = input("Do you want to go first? (y/n): ").lower().strip()
        if first in ("y", "n"):
            break
        print("Please type y or n.")

    human_turn = (first == "y")

    # Create empty board
    board = [" "] * 9

    # Game loop
    while True:
        print_board(board)

        # Check if someone already won or if it's a draw
        winner = check_winner(board)
        if winner is not None or is_draw(board):
            break

        if human_turn:
            print("Your turn.")
            move = get_human_move(board)
            board[move] = human_player
        else:
            print("AI is thinking...")
            move = find_best_move(board, ai_player, human_player)
            board[move] = ai_player

        human_turn = not human_turn  # switch turns

    # Game over: show final board and result
    print_board(board)
    winner = check_winner(board)

    if winner == human_player:
        print("You win! 🎉")
    elif winner == ai_player:
        print("AI wins! 🤖 (it's unbeatable!)")
    else:
        print("It's a draw!")


if __name__ == "__main__":
    main()
