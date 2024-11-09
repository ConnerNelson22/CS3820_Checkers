import pygame
from ui import draw_board
from board import Board

pygame.init()
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption('Checkers Game')
board = Board(screen)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    draw_board(screen)  # Draw checkerboard
    board.draw_pieces()  # Draw pieces on the board
    pygame.display.flip()

pygame.quit()
