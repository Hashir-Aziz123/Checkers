import random

class AI:
    def __init__(self, board, level="easy"):
        """
        Initialize the AI.
        :param board: The board object.
        :param level: AI difficulty level - 'easy', 'medium', 'hard'.
        """
        self.board = board
        self.level = level

    def get_best_move(self):
        """
        Decide the best move based on the AI level.
        """
        all_moves = self.board.get_all_valid_moves("player1")
        if not all_moves:
            print("[DEBUG] AI: No valid moves available.")
            return None  # No valid moves available

        print(f"[DEBUG] AI: Found {len(all_moves)} valid moves.")

        if self.level == "easy":
            return self._get_random_move(all_moves)
        elif self.level == "medium":
            return self._get_heuristic_move(all_moves)
        elif self.level == "hard":
            return self._get_minimax_move(all_moves, depth=4)  # Adjust depth for complexity

    def _get_random_move(self, moves):
        """
        Choose a random move.
        """
        print("[DEBUG] AI (Easy): Choosing a random move.")
        return random.choice(moves)

    def _get_heuristic_move(self, moves):
        """
        Choose a move based on simple heuristics:
        - Prioritize moves that capture opponent pieces.
        - Otherwise, prefer moves that advance pieces.
        """
        print("[DEBUG] AI (Medium): Choosing a heuristic-based move.")
        capture_moves = [move for move in moves if self._is_capture_move(move)]

        if capture_moves:
            print(f"[DEBUG] AI: Found {len(capture_moves)} capture moves.")
            return random.choice(capture_moves)  # Randomize among captures

        print("[DEBUG] AI: No capture moves. Choosing a regular move.")
        return random.choice(moves)  # Fallback to random for other moves

    def _get_minimax_move(self, moves, depth):
        """
        Choose the best move using the Minimax algorithm with depth control.
        :param moves: All possible moves for the AI.
        :param depth: Depth of the Minimax search.
        """
        print("[DEBUG] AI (Hard): Choosing a Minimax-based move.")
        best_score = float('-inf')
        best_move = None

        for move in moves:
            # Apply the move temporarily
            self.board.apply_move(move)
            score = self._minimax(self.board, depth - 1, False)
            # Undo the move
            self.board.undo_move(move)

            if score > best_score:
                best_score = score
                best_move = move

        print(f"[DEBUG] AI: Minimax chose a move with score {best_score}.")
        return best_move

    def _minimax(self, board, depth, is_maximizing):
        """
        Minimax algorithm for evaluating board states.
        :param board: The board object.
        :param depth: Depth to search.
        :param is_maximizing: Whether this is the maximizing player's turn.
        :return: Evaluation score of the board.
        """
        if depth == 0 or board.is_game_over():
            return self._evaluate_board(board)

        all_moves = board.get_all_valid_moves("player1" if is_maximizing else "player2")
        if is_maximizing:
            best_score = float('-inf')
            for move in all_moves:
                board.apply_move(move)
                score = self._minimax(board, depth - 1, False)
                board.undo_move(move)
                best_score = max(best_score, score)
            return best_score
        else:
            best_score = float('inf')
            for move in all_moves:
                board.apply_move(move)
                score = self._minimax(board, depth - 1, True)
                board.undo_move(move)
                best_score = min(best_score, score)
            return best_score

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
                    if piece.player == "player1":
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