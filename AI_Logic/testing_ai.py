import json
import os
from hashlib import sha256
from Checkers_Logic.constants import WHITE, RED
from copy import deepcopy

class Adaptive_AI2:
    def __init__(self, transposition_path="Checkers_Logic/data/transposition_table.json", depth = 3):
        self.current_depth = depth
        self.transposition_path = transposition_path
        self.transposition_table = self.load_transposition_table()

    def load_transposition_table(self):
        # Update the path to point to AI_Logic
        self.transposition_path = "AI_Logic/transposition_table.json"

        # Ensure the directory exists
        os.makedirs(os.path.dirname(self.transposition_path), exist_ok=True)

        if not os.path.exists(self.transposition_path):
            # Create an empty JSON file if it doesn't exist
            print(f"Transposition table not found. Creating a new one at {self.transposition_path}.")
            with open(self.transposition_path, 'w') as file:
                json.dump({}, file)

        # Load the table from the file
        with open(self.transposition_path, 'r') as file:
            return json.load(file)


    def save_transposition_table(self):
        with open(self.transposition_path, 'w') as file:
            json.dump(self.transposition_table, file)

    def hash_board(self, board):
        # Create a unique hash for the board state
        board_string = "".join(
            f"{piece.row}-{piece.col}-{piece.color}-{piece.king}"
            for row in board.board
            for piece in row if piece != 0
        )
        return sha256(board_string.encode()).hexdigest()

    def adaptive_minimax(self, position, depth, max_player, game, alpha=float('-inf'), beta=float('inf')):
        if depth == 0 or position.winner() is not None:
            eval_score = position.evaluate()
            return eval_score, position

        if max_player:
            max_eval = float('-inf')
            best_move = None
            for move in self.get_all_moves(position, WHITE, game):
                evaluation = self.adaptive_minimax(move, depth - 1, False, game, alpha, beta)[0]
                if evaluation > max_eval:
                    max_eval = evaluation
                    best_move = move
                alpha = max(alpha, max_eval)
                if beta <= alpha:
                    break
            return max_eval, best_move
        else:
            min_eval = float('inf')
            best_move = None
            for move in self.get_all_moves(position, RED, game):
                evaluation = self.adaptive_minimax(move, depth - 1, True, game, alpha, beta)[0]
                if evaluation < min_eval:
                    min_eval = evaluation
                    best_move = move
                beta = min(beta, min_eval)
                if beta <= alpha:
                    break
            return min_eval, best_move

        
    def evaluate_player_move(self, board_before, board_after):
        return board_after.evaluate() - board_before.evaluate()

    def adjust_difficulty(self, player_move_quality):
        if player_move_quality < -0.5:  # Player made a very poor move
            self.current_depth = max(1, self.current_depth - 1)
        elif player_move_quality < 0:  # Player made a somewhat poor move
            self.current_depth = max(2, self.current_depth - 1)
        elif player_move_quality > 0.5:  # Player made a very strong move
            self.current_depth = min(6, self.current_depth + 1)
        elif player_move_quality > 0:  # Player made a somewhat strong move
            self.current_depth = min(5, self.current_depth + 1)

    def make_adaptive_move(self, game):
        board_before = deepcopy(game.get_board())
        value, new_board = self.adaptive_minimax(board_before, self.current_depth, True, game)
        if new_board == board_before:
            print("AI failed to find a better move. No valid moves applied.")
        else:
            print(f"AI selected a move with evaluation: {value}")
        return new_board, f"Move evaluated with outcome: {value}"

    def get_all_moves(self, board, color, game):
        
        moves = []
        for piece in board.get_all_pieces(color):
            valid_moves = board.get_valid_moves(piece)
            for move, skip in valid_moves.items():
                # Simulate the move on a temporary board
                temp_board = deepcopy(board)
                temp_piece = temp_board.get_piece(piece.row, piece.col)
                new_board = self.simulate_move(temp_piece, move, temp_board, game, skip)
                moves.append(new_board)
        return moves
    
    def simulate_move(self, piece, move, board, game, skip):
        board.move(piece, move[0], move[1])
        if skip:
            board.remove(skip)
        return board
    
    def make_adaptive_move_simulation(self, board, turn):
        """
        Simulates a move for the given player (turn) without rendering visuals.
        """
        try:
            value, new_board = self.adaptive_minimax(board, self.current_depth, turn == WHITE, None)
            if not new_board:  # No valid moves
                print("No valid moves found!")
                return board, "No move possible"
            return new_board, f"Move evaluated with outcome: {value}"
        except Exception as e:
            print(f"Error during AI move generation: {e}")
            return board, "Error in move"