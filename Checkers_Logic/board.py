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

        def get_all_pieces(self, color):
        #Initialzing an empty list
        pieces = []

        # Iterates over each row that contains multiple piece element
        for row in self.board:
             # Each piece in that row
            for piece in row:
                # If the piece is not empty then that piece represents that color
                if piece != 0 and piece.color == color:
                     # When condition is met, piece will be added to the pieces list
                    pieces.append(piece)
        return pieces

        
        def move(self, piece, row, col):

        #Swap Positions on the board
        #self.board[piece.row][piece.col] current position on the board
        # self.board[row][col] is the target position
        # then swap back
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        #Updating the pieces location
        piece.move(row, col)

        #Update kings count by color
        #Check for promotion to king
        # if the piece is the (ROWS - 1) last row or row == 0 is the opposite
        if row == ROWS - 1 or row == 0:
             #Then make the piece a king
            piece.make_king()
            # If the color piece is white
            if piece.color == WHITE:
                #Then that white king piece increments by 1
                self.white_kings += 1
             # else the red king is incremennt by 1
            else:
                self.red_kings += 1 
