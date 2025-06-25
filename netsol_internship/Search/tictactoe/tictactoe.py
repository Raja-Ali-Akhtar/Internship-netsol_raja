"""
Tic Tac Toe Player
"""

import math
import copy
X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    countX = 0
    countO = 0
    for row in board:
        for cell in row:
            if cell == "X":
                countX += 1
            elif cell == "O":
                countO += 1
    if countX == countO:
        return "X"
    else:
        return "O"

    


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    possible_actions = set()
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                possible_actions.add((i, j))
    return possible_actions



def result(board, action):
    i, j = action
    if board[i][j] != EMPTY:
        raise Exception("Invalid move")
    new_board = copy.deepcopy(board)
    new_board[i][j] = player(board)
    return new_board

def winner(board):
    """
    Returns the winner of the game, if there is one.
    Returns "X" if X wins, "O" if O wins, else None.
    """

    for row in board:
        if row[0] == row[1] == row[2] and row[0] is not None:
            return row[0]

    for col in range(3):
        if (board[0][col] == board[1][col] == board[2][col]) and (board[0][col] is not None):
            return board[0][col]

    
    if (board[0][0] == board[1][1] == board[2][2]) and (board[0][0] is not None):
        return board[0][0]
    if (board[0][2] == board[1][1] == board[2][0]) and (board[0][2] is not None):
        return board[0][2]

    # No winner
    return None



def terminal(board):
    # Game over if there is a winner
    if winner(board) is not None:
        return True
    # Game over if no EMPTY cells
    for row in board:
        if EMPTY in row:
            return False
    return True


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    win = winner(board)
    if win == "X":
        return 1
    elif win == "O":
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    # If the board is terminal, there is no move to make
    if terminal(board):
        return None

    # Helper function to maximize score (for X)
    def max_value(state):
        if terminal(state):
            return utility(state)
        v = -math.inf
        for action in actions(state):
            v = max(v, min_value(result(state, action)))
        return v

    # Helper function to minimize score (for O)
    def min_value(state):
        if terminal(state):
            return utility(state)
        v = math.inf
        for action in actions(state):
            v = min(v, max_value(result(state, action)))
        return v

    current = player(board)
    best_action = None

    if current == "X":
        best_score = -math.inf
        for action in actions(board):
            score = min_value(result(board, action))
            if score > best_score:
                best_score = score
                best_action = action
    else:  # current == "O"
        best_score = math.inf
        for action in actions(board):
            score = max_value(result(board, action))
            if score < best_score:
                best_score = score
                best_action = action

    return best_action

