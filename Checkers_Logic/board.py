# PLEASE NOTE THAT THIS WHOLE CODE IS FROM https://github.com/techwithtim/Python-Checkers-AI AND ALSO HAS A YOUTUBE VIDEO ON IT
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
                             # else the red king is increment by 1
                    else:
                        self.red_kings += 1 

        #Getting the pieces and location of the 
        def get_pieces(self, row, col):
                return self.board[row][col]

        #Function for creating the board
        def create_board(self):
                for row in range(ROWS):
                    self.board.append([])
                    for col in range(COLS):
                        if col % 2 == ((row +  1) % 2):
                                if row < 3:
                                        self.board[row].append(Piece(row, col, WHITE))
                                elif row > 4:
                                        self.board[row].append(Piece(row, col, RED))
                                else:
                                        self.board[row].append(0)
                        else:
                            self.board[row].append(0)
        def draw(self, win):
                self.draw_squares(win)
                for row in range(ROWS):
                    for col in range(COLS):
                        piece = self.board[row][col]
                        if piece != 0:
                            piece.draw(win)

        def remove(self, pieces):
                for piece in pieces:
                    self.board[piece.row][piece.col] = 0
                    if piece != 0:
                        if piece.color == RED:
                            self.red_left -= 1
                        else:
                            self.white_left -= 1
    
    def winner(self):
        if self.red_left <= 0:
            return WHITE
        elif self.white_left <= 0:
            return RED
        
        return None 
    
    def get_valid_moves(self, piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == RED or piece.king:
            moves.update(self._traverse_left(row -1, max(row-3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row -1, max(row-3, -1), -1, piece.color, right))
        if piece.color == WHITE or piece.king:
            moves.update(self._traverse_left(row +1, min(row+3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(row +1, min(row+3, ROWS), 1, piece.color, right))
    
        return moves

    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break
            
            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last
                
                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self._traverse_left(r+step, row, step, color, left-1,skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, left+1,skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]
            left -= 1
        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break
            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r,right)] = last + skipped
                else:
                    moves[(r, right)] = last
                
                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self._traverse_left(r+step, row, step, color, right-1,skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, right+1,skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1
        
        return moves
