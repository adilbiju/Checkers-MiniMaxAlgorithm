
import pygame
from checkers.constant_vals import WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE
from checkers.board import Board
from checkers.game import Game

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Checkers")

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)


    while (run):
        clock.tick(FPS)

        if game.winner() is not None:
            print(game.winner())
            break


        for ins in pygame.event.get():
            if ins.type == pygame.QUIT:
                run = False

            if ins.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)

        game.update()
    pygame.quit()

main()


