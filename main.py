import pygame
from ui import draw_board
from board import Board

pygame.init()
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption('Checkers Game')
board = Board(screen)
selected_piece = None  # Track the currently selected piece
valid_moves = []  # Store valid moves for the selected piece

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Get the position of the click
            pos = pygame.mouse.get_pos()
            row, col = pos[1] // board.square_size, pos[0] // board.square_size

            if selected_piece:
                # Move the selected piece if clicked on a valid move
                if (row, col) in valid_moves:
                    selected_piece.row, selected_piece.col = row, col
                    selected_piece = None  # Deselect the piece after moving
                    valid_moves = []  # Reset valid moves after moving
                else:
                    selected_piece = None  # Deselect if invalid move
            else:
                # Select a piece if clicked on one
                for piece in board.pieces:
                    if piece.row == row and piece.col == col:
                        selected_piece = piece
                        valid_moves = [(row + 1, col + 1), (row + 1, col - 1)]  # Placeholder valid moves
                        break

    # Draw board and pieces
    draw_board(screen)
    board.draw_pieces()

    # Highlight selected piece and valid moves
    if selected_piece:
        pygame.draw.circle(screen, (0, 255, 0), ((selected_piece.col * board.square_size) + board.square_size // 2,
                                                 (selected_piece.row * board.square_size) + board.square_size // 2), board.square_size // 2 - 5, 3)
        for move in valid_moves:
            pygame.draw.circle(screen, (0, 255, 255), (move[1] * board.square_size + board.square_size // 2,
                                                       move[0] * board.square_size + board.square_size // 2), 15)

    pygame.display.flip()

pygame.quit()
