import pygame

#Using .constants to make sure that everything is constant
from .constants import ROWS, COLS, SQUARE_SIZE, WHITE, BLACK, RED
from .piece import Piece

class Board:
        def __init(self):
            #The [] means that the board will be initialized as an empty list
            self.board = []
            
            #Both white and red pieces start out with 12
            self.white_left = 12 
            self.red_left = 12
            
            #Beginning of game, there are no kings
            self.white_king = 0
            self.red_king = 0
            
            #Calls method to set up the board
            self.creating_board()

        #Function rendering the checkers board on the will from using Pygame and filling it wither alternating colored square
        def drawing_squares(self,win):
            #win is windows and fill the entire window with black
            win.fill(BLACK)
            
            #Alternating colored squares
            for row in range(ROWS):
                for col in range(0 if row % 2 == 0 else 1, COLS, 2):
                  
                    #Positioning for the squares ar switched
                    position_col = col * SQUARE_SIZE
                    position_row = row * SQUARE_SIZE
                    pygame.draw.rect(win, RED, (position_col, position_row, SQUARE_SIZE, SQUARE_SIZE))
            
        def eveluating(self):
            #Evaluting the difference in the pieces
            piece_count_diff = self.white_left - self.red_left
            
            #Evaluating the difference in kings
            king_piece_diff = 0.5 * (self.white_kings - self.red_kings)
            
            #Combing the piece difference and plus the king difference
            return piece_count_diff + king_piece_diff
