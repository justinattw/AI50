"""
Tic Tac Toe Player

week0 project for 'cs50 introduction to artificial intelligence'
https://cs50.harvard.edu/ai/2020/projects/0/tictactoe/
"""
import copy
import math

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
    """
    Returns player who has the next turn on a board.
    """
    if turns_taken(board) % 2 == 0:
        return X
    else:
        return O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    moves = set()

    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == EMPTY:
                moves.add((row, col))

    return moves


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    row, col = action
    change_board = copy.deepcopy(board)  # Copy original board as not to alter it

    change_board[row][col] = player(change_board)
    return change_board


def winner(board):
    """
    Returns the winner of the game, if there is one.
    """
    if player_has_won(X, board):
        return X
    elif player_has_won(O, board):
        return O
    else:
        return None


def player_has_won(p, board):
    return (p == board[0][0] == board[0][1] == board[0][2] or  # if three in a row
            p == board[1][0] == board[1][1] == board[1][2] or
            p == board[2][0] == board[2][1] == board[2][2] or
            p == board[0][0] == board[1][0] == board[2][0] or  # if three in a column
            p == board[0][1] == board[1][1] == board[2][1] or
            p == board[0][2] == board[1][2] == board[2][2] or
            p == board[0][0] == board[1][1] == board[2][2] or  # if three diagonally
            p == board[2][0] == board[1][1] == board[0][2])


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    return turns_taken(board) == 9 or winner(board) is not None


def turns_taken(board):
    return 9 - sum([row.count(EMPTY) for row in board])


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    if winner(board) == X:
        return 1
    elif winner(board) == O:
        return -1
    else:
        return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """
    if terminal(board):
        return None

    if player(board) == X:
        _, move = max_value(board)
    else:
        _, move = min_value(board)

    return move


def max_value(board, alpha=-math.inf, beta=math.inf):

    v = -math.inf
    move = None

    if terminal(board):
        return utility(board), move

    actions_board = actions(board)
    for action in actions_board:
        min_v, _ = min_value(result(board, action), alpha, beta)
        alpha = max(alpha, min_v)
        if min_v > v:
            v = min_v
            move = action
        if alpha >= beta:
            break

    return v, move


def min_value(board, alpha=-math.inf, beta=math.inf):

    v = math.inf
    move = None

    if terminal(board):
        return utility(board), move

    actions_board = actions(board)
    for action in actions_board:
        max_v, _ = max_value(result(board, action), alpha, beta)
        beta = min(beta, max_v)
        if max_v < v:
            v = max_v
            move = action
        if alpha >= beta:
            break

    return v, move


