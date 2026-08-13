from copy import deepcopy

from checkers.constant_vals import RED, WHITE

def minimax(position, depth, max_player, game):
    turn = WHITE if max_player else RED
    winner = position.winner(turn)
    if winner is not None:
        return (float('inf') if winner == WHITE else float('-inf')), position
    if depth == 0:
        return position.evaluate(), position
    
    if max_player:
        maxEval = float('-inf')
        best_move = None
        for move in get_all_moves(position, WHITE, game):
            evaluation = minimax(move, depth-1, False, game)[0]
            maxEval = max(maxEval, evaluation)
            if maxEval == evaluation:
                best_move = move
        return maxEval, best_move
    else:
        minEval = float('inf')
        best_move = None
        for move in get_all_moves(position, RED, game):
            evaluation = minimax(move, depth-1, True, game)[0]
            minEval = min(minEval, evaluation)
            if minEval == evaluation:
                best_move = move
        return minEval, best_move

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


