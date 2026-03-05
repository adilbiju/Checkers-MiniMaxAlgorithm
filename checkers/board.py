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
