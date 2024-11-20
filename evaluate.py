import pygame
from Checkers_Logic.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE
from Checkers_Logic.ui import Game
from AI_Logic.ai import Adaptive_AI

FPS = 60
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def simulate_ai_move_as_mouse(game, ai, color):
    """
    Simulates the AI determining a move and executing it as if it clicked the mouse.
    """
    board = game.get_board()
    move, explanation = ai.make_adaptive_move(game)

    if move is None:
        print(f"AI ({'Red' if color == RED else 'White'}) cannot make a move!")
        return False

    # Locate the piece and destination
    for piece in board.get_all_pieces(color):
        valid_moves = board.get_valid_moves(piece)
        for destination, skipped in valid_moves.items():
            temp_board = board.simulate_move(piece, destination, board, game, skipped)
            if temp_board == move:
                row, col = piece.row, piece.col
                dest_row, dest_col = destination

                # Simulate mouse clicks for selecting and moving
                print(f"AI ({'Red' if color == RED else 'White'}) selects ({row}, {col})")
                game.select(row, col)
                print(f"AI ({'Red' if color == RED else 'White'}) moves to ({dest_row}, {dest_col})")
                game.select(dest_row, dest_col)
                return True

    print(f"AI ({'Red' if color == RED else 'White'}) failed to match a valid move!")
    return False

def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)
    ai = Adaptive_AI()

    while run:
        clock.tick(FPS)

        if game.turn == WHITE:  # AI's turn
            try:
                print("AI's turn:")
                if not simulate_ai_move_as_mouse(game, ai, WHITE):
                    print("AI failed to make a valid move.")
                    run = False
            except Exception as e:
                print(f"AI failed to make a move due to an error: {e}")
                game.change_turn()

        if game.winner() is not None:
            print("Winner:", game.winner())
            run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # Simulate AI for player instead of manual mouse clicks
            if game.turn == RED:  # AI for Red simulates user move
                try:
                    print("Red's turn (AI acting as player):")
                    if not simulate_ai_move_as_mouse(game, ai, RED):
                        print("AI (Red) failed to make a valid move.")
                        run = False
                except Exception as e:
                    print(f"AI (Red) failed to make a move due to an error: {e}")
                    game.change_turn()

        game.update()

    # Save the transposition table at the end of the game
    ai.save_transposition_table()
    pygame.quit()

main()
