import pygame
from .constant_vals import RED, WHITE, BLUE, SQUARE_SIZE
from .board import Board
class Game:
    def __init__(self, window):
        self._init()
        self.window = window

    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = RED
        self.valid_moves = {}

    def reset(self):
        self._init()

    def winner(self):
        return self.board.winner(self.turn)
    
    def change_turn(self):
        self.valid_moves = {}
        if self.turn == RED:
            self.turn = WHITE
        else:
            self.turn = RED

    def get_board(self):
        return self.board
    
