import json
import os
from hashlib import sha256
from Checkers_Logic.constants import WHITE, RED, ROWS, COLS
from copy import deepcopy

class Adaptive_AI:
    def __init__(self, transposition_path="Checkers_Logic/data/transposition_table.json", depth = 4):
        self.current_depth = depth
        self.transposition_path = transposition_path
        self.transposition_table = self.load_transposition_table()

    # Load up the transosition table
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

    # Save the transposition table
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

    # Minimax algorithm with alpha-beta pruning
    def adaptive_minimax(self, position, depth, max_player, game, alpha=float('-inf'), beta=float('inf')):
        if depth == 0 or position.winner() is not None:
            eval_score = position.evaluate()
            if position.winner() == WHITE:
                return eval_score, position, "Winning move for WHITE detected."
            elif position.winner() == RED:
                return eval_score, position, "Winning move for RED detected."
            return eval_score, position, "Max depth reached with no decisive outcome."

        best_reason = ""
        if max_player:
            max_eval = float('-inf')
            best_move = None
            for piece in position.get_all_pieces(WHITE):
                valid_moves = position.get_valid_moves(piece)
                for move, skip in valid_moves.items():
                    temp_board = deepcopy(position)
                    temp_piece = temp_board.get_piece(piece.row, piece.col)
                    new_board = self.simulate_move(temp_piece, move, temp_board, game, skip)
                    evaluation, _, reason = self.adaptive_minimax(new_board, depth - 1, False, game, alpha, beta)
                    if evaluation > max_eval:
                        max_eval = evaluation
                        best_move = new_board
                        best_reason = self.generate_reason(position, new_board, WHITE, move)
                    alpha = max(alpha, max_eval)
                    if beta <= alpha:
                        break
            return max_eval, best_move, best_reason
        else:
            min_eval = float('inf')
            best_move = None
            for piece in position.get_all_pieces(RED):
                valid_moves = position.get_valid_moves(piece)
                for move, skip in valid_moves.items():
                    temp_board = deepcopy(position)
                    temp_piece = temp_board.get_piece(piece.row, piece.col)
                    new_board = self.simulate_move(temp_piece, move, temp_board, game, skip)
                    evaluation, _, reason = self.adaptive_minimax(new_board, depth - 1, True, game, alpha, beta)
                    if evaluation < min_eval:
                        min_eval = evaluation
                        best_move = new_board
                        best_reason = reason or self.generate_reason(position, new_board, RED, move)
                    beta = min(beta, min_eval)
                    if beta <= alpha:
                        break
            return min_eval, best_move, best_reason

    # this function is not used, but the hope was to be able to get the ai to adjust itself based on the player's moves
    def adjust_difficulty(self, player_move_quality):
        if player_move_quality < -0.5:  # Player made a very poor move
            self.current_depth = max(1, self.current_depth - 1)
        elif player_move_quality < 0:  # Player made a somewhat poor move
            self.current_depth = max(2, self.current_depth - 1)
        elif player_move_quality > 0.5:  # Player made a very strong move
            self.current_depth = min(6, self.current_depth + 1)
        elif player_move_quality > 0:  # Player made a somewhat strong move
            self.current_depth = min(5, self.current_depth + 1)

    # This function is used to make the AI move
    def make_adaptive_move(self, game):
        board_before = deepcopy(game.get_board())
        evaluation, new_board, reason = self.adaptive_minimax(board_before, self.current_depth, True, game)

        if new_board == board_before:
            return None, "AI could not find a valid move."

        # Save the transposition table after each move
        board_hash = self.hash_board(board_before)
        self.transposition_table[board_hash] = evaluation
        self.save_transposition_table()

        return new_board, reason
    
    def simulate_move(self, piece, move, board, game, skip):
        board.move(piece, move[0], move[1])
        if skip:
            board.remove(skip)
        return board
    
    def explain_move(self, board_before, board_after, move):
        piece = board_before.get_piece(*move)
        valid_moves = board_before.get_valid_moves(piece)
        piece_score_before = board_before.evaluate()
        piece_score_after = board_after.evaluate()

        if valid_moves[move]:
            return f"I captured a piece to gain a material advantage. Board evaluation improved from {piece_score_before} to {piece_score_after}."
        if piece.color == WHITE and move[0] == ROWS - 1:
            return f"I advanced a piece to the last row to promote it to a king. Board evaluation: {piece_score_after}."
        if piece.color == RED and move[0] == 0:
            return f"I advanced a piece to the first row to promote it to a king. Board evaluation: {piece_score_after}."
        if 2 <= move[0] <= ROWS - 3 and 2 <= move[1] <= COLS - 3:
            return f"I moved to a central position to control the board. Current evaluation: {piece_score_after}."
        if piece_score_after > piece_score_before:
            return f"I made this move to slightly improve my board position. Evaluation improved from {piece_score_before} to {piece_score_after}."
        return f"I made this move as the best available option at depth {self.current_depth}. Current evaluation: {piece_score_after}."

    # Generate a reason for the AI's move
    def generate_reason(self, board_before, board_after, color, move):
        material_gain = board_after.evaluate() - board_before.evaluate()
        piece = board_before.get_piece(*move)
        reasons = []

        # Check for capture moves
        if material_gain > 0:
            reasons.append(f"I captured an opponent's piece by moving to {move}.")

        # Check for king promotion
        if color == WHITE and move[0] == ROWS - 1:
            reasons.append(f"I promoted a piece to a king by advancing to {move}.")
        elif color == RED and move[0] == 0:
            reasons.append(f"I promoted a piece to a king by advancing to {move}.")

        # Check for central control
        if 2 <= move[0] <= ROWS - 3 and 2 <= move[1] <= COLS - 3:
            reasons.append(f"I moved to {move} to gain control of the center.")

        # Check for piece safety
        if not self.is_piece_threatened(board_after, move):
            reasons.append(f"I moved to {move} to keep my piece safe from capture.")

        # If no specific reason is found, highlight positional improvement
        if not reasons:
            reasons.append(f"I advanced my piece to {move} for a better position.")

        # Randomize reason selection to avoid repetition
        return reasons[0] if reasons else "I made this move based on the current evaluation."

    # Check if a piece is threatened by an opponent's move
    def is_piece_threatened(self, board, move):
        row, col = move
        piece = board.get_piece(row, col)

        opponent_color = WHITE if piece.color == RED else RED
        for opponent_piece in board.get_all_pieces(opponent_color):
            valid_moves = board.get_valid_moves(opponent_piece)
            for target_move, skipped in valid_moves.items():
                if move in skipped:  # If this piece is in the skip list of an opponent's valid move
                    return True
        return False
