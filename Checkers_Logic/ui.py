import pygame
from .constants import RED, WHITE, BLUE, SQUARE_SIZE
from .board import Board

class Game:
    def __init__(self, win=None):
        self._init()
        self.win = win
        self.current_explanation = ""  # Add explanation storage

    def update(self):
        if self.win:
            self.board.draw(self.win)
            self.draw_valid_moves(self.valid_moves)
            self.draw_explanation()  # Draw explanation if the window exists
            pygame.display.update()

    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = RED
        self.valid_moves = {}
        self.current_explanation = ""

    def winner(self):
        result = self.board.winner()
        return result

    def reset(self):
        self._init()

    def select(self, row, col):
        if self.selected:
            result = self._move(row, col)
            if not result:
                self.selected = None
                self.select(row, col)

        piece = self.board.get_piece(row, col)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            valid_moves = self.board.get_valid_moves(piece)

            # Enforce multi-jumps
            multi_jump_moves = {move: skip for move, skip in valid_moves.items() if skip}
            if multi_jump_moves:
                self.valid_moves = multi_jump_moves
            else:
                self.valid_moves = valid_moves
            return True

        return False

    def _move(self, row, col):
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
            self.change_turn()
        else:
            return False

        return True

    def draw_valid_moves(self, moves):
        if self.win:
            for move in moves:
                row, col = move
                pygame.draw.circle(
                    self.win,
                    BLUE,
                    (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2),
                    15,
                )

    def draw_explanation(self):
        if self.win and self.current_explanation:
            font = pygame.font.SysFont("arial", 24)
            explanation_surface = font.render(f"Explanation: {self.current_explanation}", True, (255, 255, 255))
            self.win.blit(explanation_surface, (20, SQUARE_SIZE * 8 + 10))

    def update_explanation(self, explanation):
        self.current_explanation = explanation

    def change_turn(self):
        self.valid_moves = {}
        if self.turn == RED:
            self.turn = WHITE
        else:
            self.turn = RED

    def get_board(self):
        return self.board

    def ai_move(self, board):
        if self.board == board:
            print("AI move did not change the board.")
        self.board = board
        self.change_turn()

    def has_legal_moves(self, color):
        for piece in self.board.get_all_pieces(color):
            if self.board.get_valid_moves(piece):
                return True
        return False
