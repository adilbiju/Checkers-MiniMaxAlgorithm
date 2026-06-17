import pygame

from .constant_vals import COLS, RED, ROWS, SQUARE_SIZE, WHITE, CHECK1, CHECK2
from .pieces import Piece


class Board:
    def __init__(self):
        self.board = []
        self.red_left = self.white_left = 12
        self.red_kings = self.white_kings = 0
        self.create_board()

    def draw_board(self, window):
        window.fill(CHECK2)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(window, CHECK1, (row * SQUARE_SIZE, col * SQUARE_SIZE,
                                                  SQUARE_SIZE, SQUARE_SIZE))

    def evaluate(self):
        return self.white_left - self.red_left + (self.white_kings - self.red_kings) * 0.5

    def get_all_pieces(self, color):
        return [piece for row in self.board for piece in row
                if piece != 0 and piece.color == color]

    def move(self, piece, row, col):
        self.board[piece.row][piece.col] = 0
        self.board[row][col] = piece
        piece.move(row, col)

        back_row = 0 if piece.color == RED else ROWS - 1
        if row == back_row:
            piece.make_king()
            if piece.color == WHITE:
                self.white_kings += 1
            else:
                self.red_kings += 1

    def get_piece(self, row, col):
        return self.board[row][col]

    def remove(self, pieces):
        for piece in pieces:
            if self.board[piece.row][piece.col] == 0:
                continue
            self.board[piece.row][piece.col] = 0
            if piece.color == RED:
                self.red_left -= 1
            else:
                self.white_left -= 1

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == (row + 1) % 2 and row < 3:
                    self.board[row].append(Piece(row, col, WHITE))
                elif col % 2 == (row + 1) % 2 and row > 4:
                    self.board[row].append(Piece(row, col, RED))
                else:
                    self.board[row].append(0)

    def draw(self, window):
        self.draw_board(window)
        for row in self.board:
            for piece in row:
                if piece != 0:
                    piece.draw(window)

    def _directions(self, piece):
        rows = (-1, 1) if piece.king else ((-1,) if piece.color == RED else (1,))
        return [(dr, dc) for dr in rows for dc in (-1, 1)]

    def _capture_moves(self, piece):
        moves = {}
        origin = (piece.row, piece.col)

        def occupant(row, col, current, captured):
            if (row, col) == current:
                return piece
            if (row, col) == origin or any(
                    taken.row == row and taken.col == col for taken in captured):
                return 0
            return self.board[row][col]

        def search(row, col, captured):
            continued = False
            for dr, dc in self._directions(piece):
                middle_row, middle_col = row + dr, col + dc
                landing_row, landing_col = row + 2 * dr, col + 2 * dc
                if not (0 <= middle_row < ROWS and 0 <= middle_col < COLS
                        and 0 <= landing_row < ROWS and 0 <= landing_col < COLS):
                    continue
                middle = occupant(middle_row, middle_col, (row, col), captured)
                if (middle == 0 or middle.color == piece.color
                        or occupant(landing_row, landing_col, (row, col), captured) != 0):
                    continue
                continued = True
                new_captured = captured + (middle,)
                back_row = 0 if piece.color == RED else ROWS - 1
                if not piece.king and landing_row == back_row:
                    moves[(landing_row, landing_col)] = list(new_captured)
                else:
                    search(landing_row, landing_col, new_captured)
            if not continued and captured:
                moves[(row, col)] = list(captured)

        search(piece.row, piece.col, ())
        return moves

    def get_all_valid_moves(self, color):
        pieces = self.get_all_pieces(color)
        captures = {piece: self._capture_moves(piece) for piece in pieces}
        if any(captures.values()):
            return {piece: moves for piece, moves in captures.items() if moves}

        moves = {}
        for piece in pieces:
            piece_moves = {}
            for dr, dc in self._directions(piece):
                row, col = piece.row + dr, piece.col + dc
                if 0 <= row < ROWS and 0 <= col < COLS and self.board[row][col] == 0:
                    piece_moves[(row, col)] = []
            if piece_moves:
                moves[piece] = piece_moves
        return moves

    def get_valid_moves(self, piece):
        return self.get_all_valid_moves(piece.color).get(piece, {})

    def winner(self, turn=None):
        if self.red_left <= 0:
            return WHITE
        if self.white_left <= 0:
            return RED
        return None
