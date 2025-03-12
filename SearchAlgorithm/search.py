import copy
import time
from heuristics.heuristics import get_pieces_count

class SearchAlgorithm:
    def __init__(self, game, heuristic, alpha_beta=True, max_time=5):
        """
        Initializes the search algorithm.
        
        Args:
            game: The MiniChess game instance.
            heuristic: The heuristic function to evaluate board states.
            alpha_beta (bool): Whether to use Alpha-Beta Pruning (True) or Minimax (False).
            max_time (int): Maximum time allowed for the AI to make a move.
        """
        self.game = game  # Reference to the MiniChess game
        self.heuristic = heuristic  # Chosen heuristic function
        self.alpha_beta = alpha_beta  # Boolean: True for Alpha-Beta, False for Minimax
        self.max_time = max_time  # Time limit for AI move computation
        self.start_time = None  # Track the start time for time management

    def search_best_move(self, depth):
        """
        Decides whether to use Minimax or Alpha-Beta based on the `self.alpha_beta` flag.
        
        Args:
            depth (int): Maximum depth to search in the game tree.

        Returns:
            tuple: (best_score, best_move)
        """
        self.start_time = time.time()  # Start the timer

        if self.alpha_beta:
            return self.alpha_beta_pruning(depth, float('-inf'), float('inf'), True)
        else:
            return self.minimax(depth, True)

    """
    Implements the basic Minimax.

    Args:
        depth (int): How deep the search tree should go.
        maximizing_player (bool): True if maximizing (White), False if minimizing (Black).

    Returns:
        tuple: (best_score, best_move)
    """
    def minimax(self, depth, maximizing_player):
        # Check if time is up before continuing the search
        if time.time() - self.start_time >= self.max_time:
            print("AI exceeded time limit! It loses.")
            self.game.logger.log_winner(f"{'White' if maximizing_player else 'Black'} loses due to timeout.")
            exit(0)  # AI automatically loses if it takes too long

        # Base case: If depth = 0 or game is over, evaluate the board.
        if depth == 0 or self.game.is_game_over():
            return self.evaluate_state(), None

        best_move = None
        valid_moves = self.game.valid_moves(self.game.current_game_state)

        if maximizing_player:  # White (Maximizing)
            max_eval = float('-inf')
            for move in valid_moves:
                new_state = copy.deepcopy(self.game)
                new_state.make_move(new_state.current_game_state, move)

                eval_score, _ = self.minimax(depth - 1, False)  # Use `self.minimax` instead of `new_state.minimax`

                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move

            return max_eval, best_move

        else:  # Black (Minimizing)
            min_eval = float('inf')
            for move in valid_moves:
                new_state = copy.deepcopy(self.game)
                new_state.make_move(new_state.current_game_state, move)

                eval_score, _ = self.minimax(depth - 1, True)  # Use `self.minimax` instead of `new_state.minimax`

                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move

            return min_eval, best_move

    """
    Implements Alpha-Beta Pruning to optimize Minimax.
    
    Args:
        depth (int): How deep the search tree should go.
        alpha (float): Best already explored option along the path for the maximizer.
        beta (float): Best already explored option along the path for the minimizer.
        maximizing_player (bool): True if maximizing (White), False if minimizing (Black).

    Returns:
        tuple: (best_score, best_move)
    """
    def alpha_beta_pruning(self, depth, alpha, beta, maximizing_player):
        # Check if time is up before continuing the search
        if time.time() - self.start_time >= self.max_time:
            print("AI exceeded time limit! It loses.")
            self.game.logger.log_winner(f"{'White' if maximizing_player else 'Black'} loses due to timeout.")
            exit(0)  # AI automatically loses if it takes too long

        # Base case: If depth = 0 or game is over, evaluate the board.
        if depth == 0 or self.game.is_game_over():
            return self.evaluate_state(), None

        best_move = None
        valid_moves = self.game.valid_moves(self.game.current_game_state)

        if maximizing_player:  # White (Maximizing)
            max_eval = float('-inf')
            for move in valid_moves:
                new_state = copy.deepcopy(self.game)
                new_state.make_move(new_state.current_game_state, move)

                eval_score, _ = self.alpha_beta_pruning(depth - 1, alpha, beta, False)

                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move

                # Alpha-Beta Pruning Condition
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break  # Prune the remaining branches

            return max_eval, best_move

        else:  # Black (Minimizing)
            min_eval = float('inf')
            for move in valid_moves:
                new_state = copy.deepcopy(self.game)
                new_state.make_move(new_state.current_game_state, move)

                eval_score, _ = self.alpha_beta_pruning(depth - 1, alpha, beta, True)

                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move

                # Alpha-Beta Pruning Condition
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break  # Prune the remaining branches

            return min_eval, best_move

    def evaluate_state(self):
        """
        Evaluates the game state using the chosen heuristic.
        
        Returns:
            int: Heuristic score representing the favorability of the state.
        """
        return self.heuristic(get_pieces_count(self.game.current_game_state), self.game.current_game_state)
