from pieces.king import king_moves
from pieces.queen import queen_moves
from pieces.knight import knight_moves
from pieces.pawn import pawn_moves, promote_pawn
from pieces.bishop import bishop_moves
from Logger.mini_chess_logger import MiniChessLogger
from heuristics.heuristics import e0, e1, e2  # Import heuristics
from SearchAlgorithm.search import SearchAlgorithm  # Import the AI search class

def menu() -> int:
    """Displays the menu and returns the selected option."""
    print(' -------------------------------')
    print('|       Mini Game Chess         |')
    print('| 1. Player Vs Player           |')
    print('| 2. Player Vs AI               |')
    print('| 3. AI Vs Player               |')
    print("| 4. AI Vs AI                   |")
    print("| 5. Exit                       |")
    print(' -------------------------------')
    while True:
        try:
            user_input = int(input("Please enter a valid option: "))
            if 1 <= user_input <= 5:
                return user_input
            else:   
                print("Invalid choice. Choose between 1-5.")
        except ValueError:
            print("Please enter a number.")

def main(user_input: int):
    """Main function to start the game based on user selection."""
    
    if user_input == 1:
        print(' -----------------------------------------')
        print('|         Player Vs Player Mode           |')
        print('| Enter the maximum number of turns       |')
        print(' -----------------------------------------')

        while True:
            try:
                max_turns = int(input("Max turns: "))
                if max_turns > 0:
                    break
                else:
                    print("Please enter a positive number for turns.")
            except ValueError:
                print("Invalid input. Please enter an integer.")

        game = MiniChess(alpha_beta=False, timeout=float("inf"), max_turns=max_turns, player1_type="Human", player2_type="Human")
        game.player_vs_player_play()

    elif user_input in [2, 3, 4]:  # AI-related game modes
        print(' -----------------------------------------')
        print('|            AI Mode Rules                |')
        print('| Enter the maximum allowed time (in sec) |')
        print('| Enter the maximum number of turns       |')
        print('| Define the heuristic: e0, e1, e2        |')
        print('| Enable alpha-beta? (yes/no)             |')
        print(' -----------------------------------------')

        while True:
            try:
                max_time = int(input("Max time (seconds): "))
                if max_time > 0:
                    break
                else:
                    print("Please enter a positive number for time.")
            except ValueError:
                print("Invalid input. Please enter an integer.")

        while True:
            try:
                max_turns = int(input("Max turns: "))
                if max_turns > 0:
                    break
                else:
                    print("Please enter a positive number for turns.")
            except ValueError:
                print("Invalid input. Please enter an integer.")
        
        heuristic_map = {"e0": e0, "e1": e1, "e2": e2}
        
        if user_input ==4:
            heuristic_str1 = input("AI_1: Heuristic (e0, e1, e2): ").lower()
            while heuristic_str1 not in heuristic_map:
                heuristic_str1 = input("Invalid heuristic. Choose from (e0, e1, e2): ").lower()
            
            heuristic1 = heuristic_map[heuristic_str1]
            
            heuristic_str2 = input("AI_2: Heuristic (e0, e1, e2): ").lower()
            while heuristic_str2 not in heuristic_map:
                heuristic_str2 = input("Invalid heuristic. Choose from (e0, e1, e2): ").lower()
            
            heuristic2 = heuristic_map[heuristic_str2]
            
            alpha_beta =  input("AI_1: Enable Alpha-Beta? (yes/no): ").lower()
            alpha_beta = alpha_beta in ["yes", "y"]
            
            heuristic = [heuristic1, heuristic2]
            
            game = MiniChess(alpha_beta=alpha_beta, timeout=max_time, max_turns=max_turns, heuristic=heuristic, player1_type="AI", player2_type="AI")
            game.Ai_vs_Ai_play(heuristic)
            
        else:
            heuristic_str = input("Heuristic (e0, e1, e2): ").lower()

            while heuristic_str not in heuristic_map:
                heuristic_str = input("Invalid heuristic. Choose from (e0, e1, e2): ").lower()

            heuristic = heuristic_map[heuristic_str]  # Map to actual function

            alpha_beta = input("Enable Alpha-Beta? (yes/no): ").lower()
            alpha_beta = alpha_beta in ["yes", "y"]
            
            if user_input == 2:
                game = MiniChess(alpha_beta=alpha_beta, timeout=max_time, max_turns= max_turns, heuristic=heuristic, player1_type="Human", player2_type="AI")
                game.player_vs_Ai_play(heuristic)
            elif user_input == 3:
                game = MiniChess(alpha_beta=alpha_beta, timeout=max_time, max_turns=max_turns, heuristic=heuristic, player1_type="AI", player2_type="Human")
                game.Ai_vs_player_play()
                
    elif user_input == 5:
        print("Goodbye!")
        exit(0)


class MiniChess:
    def __init__(self, alpha_beta=True, timeout=5, max_turns=100, heuristic=None, player1_type="Human", player2_type="Human"):
        """
        Initializes the MiniChess game.
        
        Args:
            alpha_beta (bool): Whether to use Alpha-Beta pruning (True) or Minimax (False).
            timeout (int): Maximum time allowed for AI to return a move.
            max_turns (int): Maximum number of turns before the game ends.
            heuristic (function or None): The heuristic function to use for AI evaluation.
                                          This should be None for Player vs Player mode.
            player1_type (str): "Human" or "AI" (indicates whether Player 1 is a human or AI).
            player2_type (str): "Human" or "AI" (indicates whether Player 2 is a human or AI).
        """
        heuristic_map = {e0: "e0", e1: "e1", e2:"e2"}
        self.current_game_state = self.init_board()
        
        if player1_type=="AI" and player2_type=="AI":
            self.logger = MiniChessLogger(alpha_beta=alpha_beta, timeout=timeout, max_turns=max_turns, player1_type=player1_type, player2_type=player2_type, heuristic1=heuristic_map[heuristic[0]], heuristic2=heuristic_map[heuristic[1]])
        else:
            if player1_type=="Human" and player2_type =="Human":
                self.logger = MiniChessLogger(alpha_beta, timeout, max_turns, player1_type, player2_type, heuristic1=None, heuristic2=None)
            elif player1_type =="AI" and player2_type =="Human":
                self.logger = MiniChessLogger(alpha_beta, timeout, max_turns, player1_type, player2_type, heuristic1=heuristic_map[heuristic], heuristic2=None)
            elif player1_type=="Human" and player2_type =="AI":
                self.logger = MiniChessLogger(alpha_beta, timeout, max_turns, player1_type, player2_type, heuristic1=None, heuristic2=heuristic_map[heuristic])
        
        self.turn_count = 0  # Track number of turns for draw condition
        self.piece_count_history = [] 
        self.max_turns = max_turns
        self.timeout = timeout
        self.heuristic = heuristic
        self.alpha_beta = alpha_beta  
        self.player1_type = player1_type
        self.player2_type = player2_type
        


    def is_game_over(self):
        """Checks if the game is over (if either King is captured)."""
        board = self.current_game_state["board"]
        white_king = any("wK" in row for row in board)
        black_king = any("bK" in row for row in board)

        return not white_king or not black_king  # Game over if either king is missing

    def init_board(self):
        """Sets up the initial board state."""
        return {
            "board": [['bK', 'bQ', 'bB', 'bN', '.'],
                      ['.', '.', 'bp', 'bp', '.'],
                      ['.', '.', '.', '.', '.'],
                      ['.', 'wp', 'wp', '.', '.'],
                      ['.', 'wN', 'wB', 'wQ', 'wK']],
            "turn": 'white'
        }

    def display_board(self, game_state):
        """Prints the current board state."""
        print()
        for i, row in enumerate(game_state["board"], start=1):
            print(str(6-i) + "  " + ' '.join(piece.rjust(3) for piece in row))
        print("\n     A   B   C   D   E\n")
        self.logger.log_board(game_state)

    def is_valid_move(self, game_state, move):
        """Checks if a move is valid."""
        return move in self.valid_moves(game_state)

    def valid_moves(self, game_state):
        """Returns all valid moves for the current player."""
        board = game_state['board']
        turn = game_state['turn']
        moves = []
        movement_rules = {"K": king_moves, "Q": queen_moves, "B": bishop_moves, "N": knight_moves, "p": pawn_moves}
        
        for r in range(5):
            for c in range(5):
                piece = board[r][c]
                if piece != "." and piece[0] == turn[0]:  # Match color
                    move_fn = movement_rules.get(piece[1], lambda pos, gs: [])
                    for move in move_fn((r, c), game_state):
                        moves.append(((r, c), move))

        return moves

    def make_move(self, game_state, move):
        """Executes a move and handles game updates."""
        start, end = move
        piece = game_state["board"][start[0]][start[1]]
        game_state["board"][start[0]][start[1]] = '.'
        game_state["board"][end[0]][end[1]] = piece

        if piece in ["wp", "bp"]:
            promote_pawn(end, game_state)

        if not any("bK" in row for row in game_state["board"]):
            self.display_board(self.current_game_state)
            print("White Wins!")
            self.logger.log_winner("White")
            exit(0)
        elif not any("wK" in row for row in game_state["board"]):
            self.display_board(self.current_game_state)
            print("Black Wins!")
            self.logger.log_winner("Black")
            exit(0)

        game_state["turn"] = "black" if game_state["turn"] == "white" else "white"

    def ai_make_move(self, game_state, move):
        """Executes a move and handles game updates."""
        start, end = move
        piece = game_state["board"][start[0]][start[1]]
        game_state["board"][start[0]][start[1]] = '.'
        game_state["board"][end[0]][end[1]] = piece

        if piece in ["wp", "bp"]:
            promote_pawn(end, game_state)

        game_state["turn"] = "black" if game_state["turn"] == "white" else "white"
    
    def parse_input(self, move:str):
        """Converts player input into board coordinates."""
        try:
            start, end = move.split()
            return ((5-int(start[1]), ord(start[0])-65), (5-int(end[1]), ord(end[0])-65))
        except:
            return None

    def player_vs_player_play(self):
        """Handles a human vs. human game loop."""
        self.logger.start_logging()
        while True:
            self.display_board(self.current_game_state)
            move = input(f"{self.current_game_state['turn'].capitalize()} to move: ").upper()
            if move.lower() =="exit":
                print("Exiting the game!")
                self.logger.log_info("Game exited!")
                exit(0)
            move = self.parse_input(move)
            
            if move and self.is_valid_move(self.current_game_state, move):
                self.make_move(self.current_game_state, move)
                self.logger.log_move(player=self.current_game_state['turn'], move=move)
            else:
                print("Invalid move.")
                self.logger.log_move(player=self.current_game_state['turn'], move=move, valid=False)

    def player_vs_Ai_play(self, heuristic):
        """Handles a human vs. AI game loop."""
        self.search_algorithm = SearchAlgorithm(game=self, heuristic = heuristic,alpha_beta= self.alpha_beta, max_time = self.timeout, maximizier=False)  #  Creating an instance of the searchAlgorithm Class

        #Game Starts here
        while True:
            self.display_board(self.current_game_state) # Dislay board 
            
            if self.current_game_state["turn"] == "white": # Human Starts with white turn
                
                move = input("White Your move: ").upper()
                if move.lower() =="exit": # Exit game when they type exit
                    print("Exiting the game!")
                    self.logger.log_info("Game exited!")
                    exit(0)
                    
                move = self.parse_input(move) # Get the move using parse_input
            else:    
                move = self.search_algorithm.search_best_move(3) # Make AI move
                print(f"Black AI Move: {move}")

            if move and self.is_valid_move(self.current_game_state, move):
                if self.player1_type =="Human":
                    self.logger.log_move(player=self.current_game_state['turn'], move=move)
                if self.player2_type =="AI":
                    self.logger.log_move()
                self.make_move(self.current_game_state, move)
            else:
                print("Invalid move.")

    def Ai_vs_player_play(self):
        """Handles an AI vs. Human game loop."""
        self.search_algorithm = SearchAlgorithm(self, self.heuristic, self.alpha_beta, self.timeout, maximizier=True)  # ✅ Ensure AI is initialized
        while True:
            self.display_board(self.current_game_state)
            if self.current_game_state["turn"] == "white":  # AI moves first
                move = self.search_algorithm.search_best_move(3)
                print(f"AI Move: {move}")
            else:  # Human plays
                move = input("Black move: ").upper()
                
                if move.lower() =="exit":
                    print("Exiting the game!")
                    self.logger.log_info("Game exited!")
                    exit(0)
                
                move = self.parse_input(move)

            if move and self.is_valid_move(self.current_game_state, move):
                self.make_move(self.current_game_state, move)
            else:
                print("Invalid move.")
                
    def Ai_vs_Ai_play(self, heuristic):
        """Handles an AI vs. AI game loop."""
        self.search_algorithm = SearchAlgorithm(self, self.alpha_beta, self.timeout)  # ✅ Ensure AI is initialized
        
        while True:
            self.display_board(self.current_game_state)
            if self.current_game_state['turn'] =="white":
                self.search_algorithm.heuristic = heuristic[0]
                self.search_algorithm.alpha_beta = self.alpha_beta[0]
                move = self.search_algorithm.search_best_move(3)
            else:
                self.search_algorithm.heuristic = heuristic[1]
                self.search_algorithm.alpha_beta = self.alpha_beta[1]
                move = self.search_algorithm.search_best_move(3)
                
            if move:
                self.make_move(self.current_game_state, move)
            else:
                print(f"{self.current_game_state['turn']} AI has no valid moves. Game over.")
                break

if __name__ == "__main__":
    main(menu())
