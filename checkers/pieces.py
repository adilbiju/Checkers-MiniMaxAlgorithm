import pygame
from .constant_vals import SQUARE_SIZE, GREY

class Piece:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.x = 0
        self.y = 0
        self.check_position()

    def check_position(self):
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def move(self, row, col):
        self.row = row
        self.col = col
        self.check_position()

    def draw(self, window):
        radius = (SQUARE_SIZE // 2) - 20
        pygame.draw.circle(window, GREY, (self.x, self.y), radius + 2)
        pygame.draw.circle(window, self.color, (self.x, self.y), radius)
