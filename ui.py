# ui.py
import pygame

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

def draw_board(screen):
    square_size = 100
    for row in range(8):
        for col in range(8):
            color = BLACK if (row + col) % 2 == 0 else WHITE
            pygame.draw.rect(screen, color, (col * square_size, row * square_size, square_size, square_size))