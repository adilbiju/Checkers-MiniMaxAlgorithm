import sys
import types
import unittest

try:
    import pygame
except ImportError:
    sys.modules["pygame"] = types.ModuleType("pygame")

from checkers.board import Board
from checkers.constant_vals import RED, WHITE
from checkers.game import Game
from checkers.pieces import Piece
from minimax.algorithm import minimax


def empty_board():
    board = Board()
    board.board = [[0] * 8 for _ in range(8)]
    board.red_left = board.white_left = 0
    board.red_kings = board.white_kings = 0
    return board


def add_piece(board, row, col, color, king=False):
    piece = Piece(row, col, color)
    piece.king = king
    board.board[row][col] = piece
    if color == RED:
        board.red_left += 1
        board.red_kings += king
    else:
        board.white_left += 1
        board.white_kings += king
    return piece


class BoardLogicTests(unittest.TestCase):
    def test_ai_can_choose_a_move(self):
        score, next_board = minimax(Board(), 1, True, None)
        self.assertIsNotNone(next_board)
        self.assertEqual(len(next_board.get_all_pieces(WHITE)), 12)

    def test_capture_is_mandatory_for_all_pieces(self):
        board = empty_board()
        capturing = add_piece(board, 5, 2, RED)
        other = add_piece(board, 5, 6, RED)
        add_piece(board, 4, 3, WHITE)
        self.assertEqual(board.get_valid_moves(capturing), {(3, 4): [board.get_piece(4, 3)]})
        self.assertEqual(board.get_valid_moves(other), {})

    def test_three_jump_capture_removes_all_pieces(self):
        board = empty_board()
        moving = add_piece(board, 7, 0, RED)
        taken = [add_piece(board, 6, 1, WHITE),
                 add_piece(board, 4, 3, WHITE),
                 add_piece(board, 2, 5, WHITE)]
        self.assertEqual(board.get_valid_moves(moving), {(1, 6): taken})
        board.move(moving, 1, 6)
        board.remove(taken)
        self.assertEqual(board.white_left, 0)

    def test_chain_can_land_on_top_row(self):
        board = empty_board()
        moving = add_piece(board, 4, 1, RED)
        first = add_piece(board, 3, 2, WHITE)
        second = add_piece(board, 1, 4, WHITE)
        self.assertEqual(board.get_valid_moves(moving), {(0, 5): [first, second]})

    def test_king_can_reverse_during_chain(self):
        board = empty_board()
        moving = add_piece(board, 4, 1, RED, king=True)
        first = add_piece(board, 3, 2, WHITE)
        second = add_piece(board, 3, 4, WHITE)
        self.assertEqual(board.get_valid_moves(moving), {(4, 5): [first, second]})


if __name__ == "__main__":
    unittest.main()
