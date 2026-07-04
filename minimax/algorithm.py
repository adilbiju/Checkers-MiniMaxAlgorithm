from copy import deepcopy

from checkers.constant_vals import RED, WHITE

def get_all_moves(board, color, game):
    moves = []

    for piece, valid_moves in board.get_all_valid_moves(color).items():
        for move, skip in valid_moves.items():
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_board = simulate_move(temp_piece, move, temp_board, game, skip)
            moves.append(new_board)

    return moves

def simulate_move(piece,move, board, game, skip):
    board.move(piece, move[0], move[1])
    if skip:
        board.remove([board.get_piece(taken.row, taken.col) for taken in skip])
    return board


