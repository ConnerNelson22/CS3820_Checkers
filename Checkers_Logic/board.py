import pygame
from .constants import BLACK, ROWS, RED, SQUARE_SIZE, COLS, WHITE
from .piece import Piece
from copy import deepcopy

class Board:
    def __init__(self):
        self.board = []
        self.red_left = self.white_left = 12
        self.red_kings = self.white_kings = 0
        self.create_board()
    
    def draw_squares(self, win):
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                pygame.draw.rect(win, RED, (row*SQUARE_SIZE, col *SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

    def evaluate(self):
        return self.white_left - self.red_left + (self.white_kings * 0.5 - self.red_kings * 0.5)

    def get_all_pieces(self, color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

        if row == ROWS - 1 or row == 0:  # Check if piece reached the end of the board
            piece.make_king()
            if piece.color == WHITE:
                self.white_kings += 1
            else:
                self.red_kings += 1

    def get_piece(self, row, col):
        return self.board[row][col]

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
        red_moves = any(self.get_valid_moves(piece) for piece in self.get_all_pieces(RED))
        white_moves = any(self.get_valid_moves(piece) for piece in self.get_all_pieces(WHITE))

        if not red_moves:
            return WHITE  # White wins
        elif not white_moves:
            return RED  # Red wins
        return None  # No winner yet

        
    
    def get_valid_moves(self, piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == RED or piece.king:
            moves.update(self._traverse_left(row - 1, max(row - 3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row - 1, max(row - 3, -1), -1, piece.color, right))
        if piece.color == WHITE or piece.king:
            moves.update(self._traverse_left(row + 1, min(row + 3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(row + 1, min(row + 3, ROWS), 1, piece.color, right))

        return moves


    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:  # Out of bounds
                break

            current = self.board[r][left]
            if current == 0:  # Empty square
                if skipped and not last:  # Invalid jump path
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped  # Add skipped pieces for this move
                else:
                    moves[(r, left)] = last

                # Recursive call for multi-jumps
                if last:  # If a piece was captured
                    next_row = max(r - 3, 0) if step == -1 else min(r + 3, ROWS)
                    moves.update(self._traverse_left(r + step, next_row, step, color, left - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, next_row, step, color, left + 1, skipped=last))
                break
            elif current.color == color:  # Same color, no jump
                break
            else:  # Opponent's piece
                last = [current]

            left -= 1

        return moves


    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:  # Out of bounds
                break

            current = self.board[r][right]
            if current == 0:  # Empty square
                if skipped and not last:  # Invalid jump path
                    break
                elif skipped:
                    moves[(r, right)] = last + skipped  # Add skipped pieces for this move
                else:
                    moves[(r, right)] = last

                # Recursive call for multi-jumps
                if last:  # If a piece was captured
                    next_row = max(r - 3, 0) if step == -1 else min(r + 3, ROWS)
                    moves.update(self._traverse_left(r + step, next_row, step, color, right - 1, skipped=last))
                    moves.update(self._traverse_right(r + step, next_row, step, color, right + 1, skipped=last))
                break
            elif current.color == color:  # Same color, no jump
                break
            else:  # Opponent's piece
                last = [current]

            right += 1

        return moves

    def simulate_move(self, piece, move, board, game, skipped):
        """
        Simulates moving a piece on the board without affecting the actual game state.
        """
        temp_board = deepcopy(board)  # Create a copy of the board
        temp_piece = temp_board.get_piece(piece.row, piece.col)  # Get the piece on the copied board
        temp_board.move(temp_piece, move[0], move[1])  # Move the piece

        if skipped:
            temp_board.remove(skipped)  # Remove skipped pieces if applicable

        return temp_board  # Return the simulated board
