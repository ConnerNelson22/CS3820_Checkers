import pygame
from copy import deepcopy
from Checkers_Logic.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE
from Checkers_Logic.ui import Game
from AI_Logic.ai import Adaptive_AI

pygame.init()  # Initialize all Pygame modules

FPS = 60
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)
    ai = Adaptive_AI()

    while run:
        clock.tick(FPS)

        if game.turn == WHITE:  # AI's turn
            try:
                new_board, explanation = ai.make_adaptive_move(game)
                if new_board is None:
                    print("AI did not generate a valid move!")
                else:
                    print(f"AI move explanation: {explanation}")
                    game.ai_move(new_board)
                    game.update_explanation(explanation)  # Update the explanation display
            except Exception as e:
                print(f"AI failed to make a move due to an error: {e}")
                game.change_turn()

        if game.winner() is not None:
            print("Winner:", game.winner())
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)

        game.update()

    pygame.quit()

main()