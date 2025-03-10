import copy
import time
from heuristics.heuristics import get_pieces_count
def minimax(self, depth, alpha, beta, maximizing_player):
        """Minimax algorithm with Alpha-Beta Pruning."""
        if depth == 0 or self.is_game_over():
            return self.ai_heuristic(get_pieces_count(self.current_game_state), self.current_game_state), None

        best_move = None
        valid_moves = self.valid_moves()

        if maximizing_player:  # White (Maximizing)
            max_eval = float('-inf')
            for move in valid_moves:
                new_state = copy.deepcopy(self)
                new_state.make_move(move)
                eval_score, _ = new_state.minimax(depth - 1, alpha, beta, False)

                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move

                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break  # Prune the search
            return max_eval, best_move

        else:  # Black (Minimizing)
            min_eval = float('inf')
            for move in valid_moves:
                new_state = copy.deepcopy(self)
                new_state.make_move(move)
                eval_score, _ = new_state.minimax(depth - 1, alpha, beta, True)

                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move

                beta = min(beta, eval_score)
                if beta <= alpha:
                    break  # Prune the search
            return min_eval, best_move