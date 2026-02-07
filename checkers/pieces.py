import pygame
from .constant_vals import RED, WHITE, SQUARE_SIZE, GREY, BLUE, YELLOW

class Piece:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.king = False
        self.x = 0
        self.y = 0
        self.check_position()


    def check_position(self):
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def make_king(self):
        self.king = True

    def move(self, row, col):
        self.row = row
        self.col = col
        self.check_position()


    def draw(self, window):
        radius = (SQUARE_SIZE//2) - 20
        pygame.draw.circle(window, GREY, (self.x, self.y), radius + 2)
        pygame.draw.circle(window, self.color, (self.x, self.y), radius)
        if self.king:
            pygame.draw.circle(window, YELLOW, (self.x, self.y), 10)

    def __repr__(self):
        return str(self.color)
        