# board.py
import pygame

RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

class Piece:
    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.king = False

    def make_king(self):
        self.king = True

    def draw(self, screen, square_size):
        radius = square_size // 2 - 10
        x = self.col * square_size + square_size // 2
        y = self.row * square_size + square_size // 2
        pygame.draw.circle(screen, self.color, (x, y), radius)
        if self.king:
            pygame.draw.circle(screen, WHITE, (x, y), radius - 5)  # Indicate king status

class Board:
    def __init__(self, screen, square_size=100):
        self.screen = screen
        self.square_size = square_size
        self.pieces = []
        self.create_board()

    def create_board(self):
        for row in range(8):
            for col in range(8):
                if (row + col) % 2 == 1:  # Only place pieces on black squares
                    if row < 3:
                        self.pieces.append(Piece(row, col, BLACK))
                    elif row > 4:
                        self.pieces.append(Piece(row, col, RED))

    def draw_pieces(self):
        for piece in self.pieces:
            piece.draw(self.screen, self.square_size)
