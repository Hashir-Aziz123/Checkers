import random
import copy
from functools import lru_cache

class AI:
    def __init__(self, board, level="easy"):
        """
        Initialize the AI.
        :param board: The board object.
        :param level: AI difficulty level - 'easy', 'medium', 'hard'.
        """
        self.board = board
        self.level = level
        self.transposition_table = {}

    def get_best_move(self):
        """
        Decide the best move based on the AI level.
        """
        all_moves = self.board.get_all_valid_moves("AI")
        if not all_moves:
            print("[DEBUG] AI: No valid moves available.")
            return None  # No valid moves available

        print(f"[DEBUG] AI: Found {len(all_moves)} valid moves.")

        if self.level == "easy":
            return self._get_heuristic_move(all_moves)
        elif self.level == "medium":
            return self._get_minimax_move(all_moves, depth=2)  # Adjust depth for complexity
        elif self.level == "hard":
            return self._get_minimax_move(all_moves, depth=4)  # Adjust depth for complexity

    def _get_random_move(self, moves):
        """
        Choose a random move.
        """
        print("[DEBUG] AI (Easy): Choosing a random move.")
        return random.choice(moves)

    def _get_heuristic_move(self, moves):
        print("[DEBUG] AI (Medium): Choosing a heuristic-based move.")
        capture_moves = [move for move in moves if self._is_capture_move(move)]

        if capture_moves:
            print(f"[DEBUG] AI: Found {len(capture_moves)} capture moves.")
            return random.choice(capture_moves)  # Randomize among captures

        print("[DEBUG] AI: No capture moves. Choosing a regular move.")
        return random.choice(moves)  # Fallback to random for other moves

    def _evaluate_board(self, board):
        """
        Evaluate the board state.
        :param board: The board object.
        :return: A numerical score representing the board's state.
        """
        score = 0
        for row in board.boardArray:
            for piece in row:
                if piece:
                    if piece.player == "AI":
                        score += 1 + (2 if piece.isKing else 0)  # Reward AI pieces
                    else:
                        score -= 1 + (2 if piece.isKing else 0)  # Penalize opponent pieces
        return score

    def _is_capture_move(self, move):
        """
        Check if a move is a capture move.
        :param move: The move to check.
        :return: True if the move is a capture move, False otherwise.
        """
        prev_pos, new_pos = move
        return abs(new_pos[0] - prev_pos[0]) == 2  # Capture moves involve jumping over an opponent piece

    def _get_minimax_move(self, moves, depth):
        """
        Get the best move using the minimax algorithm.
        :param moves: All valid moves.
        :param depth: Depth of the minimax algorithm.
        :return: The best move.
        """
        best_move = None
        best_score = float('-inf')
        alpha = float('-inf')
        beta = float('inf')

        for move in moves:
            board_copy = self._copy_board(self.board)  # Create a custom copy of the board
            board_copy.apply_move(move)
            score = self._minimax(board_copy, depth - 1, False, alpha, beta)
            
            if score > best_score:
                best_score = score
                best_move = move

            alpha = max(alpha, score)
            if alpha >= beta:
                break  # Alpha-beta pruning

        return best_move

    def _minimax(self, board, depth, is_maximizing, alpha, beta):
        """
        Minimax algorithm with alpha-beta pruning.
        :param board: The board object.
        :param depth: The current depth of the search.
        :param is_maximizing: True if the current layer is maximizing, False if minimizing.
        :param alpha: Alpha value for alpha-beta pruning.
        :param beta: Beta value for alpha-beta pruning.
        :return: The evaluation score.
        """
        board_key = self._board_to_key(board)
        if board_key in self.transposition_table:
            return self.transposition_table[board_key]

        if depth == 0 or board.is_game_over():
            score = self._evaluate_board(board)
            self.transposition_table[board_key] = score
            return score

        if is_maximizing:
            max_eval = float('-inf')
            for move in board.get_all_valid_moves("AI"):
                board_copy = self._copy_board(board)  # Create a custom copy of the board
                board_copy.apply_move(move)
                eval = self._minimax(board_copy, depth - 1, False, alpha, beta)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break  # Alpha-beta pruning
            self.transposition_table[board_key] = max_eval
            return max_eval
        else:
            min_eval = float('inf')
            for move in board.get_all_valid_moves("Player"):
                board_copy = self._copy_board(board)  # Create a custom copy of the board
                board_copy.apply_move(move)
                eval = self._minimax(board_copy, depth - 1, True, alpha, beta)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break  # Alpha-beta pruning
            self.transposition_table[board_key] = min_eval
            return min_eval

    def _copy_board(self, board):
        """
        Create a custom copy of the board without pygame surfaces.
        :param board: The board object to copy.
        :return: A new board object with the same state.
        """
        new_board = type(board)(board.window, True)  # Create a new instance of the Board class
        new_board.boardArray = [
            [self._copy_piece(piece) for piece in row]
            for row in board.boardArray
        ]
        new_board.turn = board.turn
        return new_board

    def _copy_piece(self, piece):
        """
        Create a copy of a piece.
        :param piece: The piece object to copy.
        :return: A new piece object with the same state.
        """
        if piece is None:
            return None
        new_piece = type(piece)(piece.row, piece.col, piece.player, piece.window, True)
        new_piece.isKing = piece.isKing
        return new_piece

    def _board_to_key(self, board):
        """
        Convert a board state to a hashable key for the transposition table.
        :param board: The board object.
        :return: A hashable key representing the board state.
        """
        key = []
        for row in board.boardArray:
            for piece in row:
                if piece is None:
                    key.append('0')
                else:
                    key.append(f'{piece.player[0]}{"K" if piece.isKing else "P"}')
        return ''.join(key)
