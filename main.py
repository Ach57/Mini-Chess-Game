import math
import copy
import time
import sys
import threading
from pieces.king import king_moves
from pieces.queen import queen_moves
from pieces.knight import knight_moves
from pieces.pawn import pawn_moves, promote_pawn
from pieces.bishop import bishop_moves
from mini_chess_logger import MiniChessLogger


def menu() ->int:
    print(' -------------------------------')
    print('|       Mini Game Chess         |')
    print('| 1. Player Vs Player           |')
    print('| 2. Player Vs AI               |')
    print("| 3. AI Vs AI                   |")
    print("| 4. Exit                       |")
    print(' -------------------------------')
    
    is_correct = False
    while(not is_correct):
        try:
            user_input = int(input("Please entre a valid option: "))
            if user_input>4 or user_input<1:
                print('Please entre a value within the correct range\n')
            else:
                is_correct = True
        except ValueError as e:
            print('incorrect value!\n')
    
    if user_input == 4:
        print('Bye!')
        exit(0)
    return user_input

def main(user_input:int):
    if user_input == 1:
        print(' -----------------------------------------')
        print('|            Player Mode Rules             |')
        print('| Entre The maximum Allow time in Seconds  |')
        print('| Entre the maximum number of turns        |')
        print(' -----------------------------------------')
        
        is_correct = False
        while(not is_correct):
            try:
                max_time = int(input("Max time in Seconds: "))
                if max_time<0:
                    print('Lets keep it postive, shall we?\n')
                elif max_time>15:
                    print('Wohoo that\'t alot of time to think. Shrink it bit\n')
                else:
                    is_correct = True
            except ValueError:
                print('Not a number :(\n')
        
        is_correct = False
        while(not is_correct):
            try:
                max_turn = int(input("Max turn in Seconds: "))
                if max_turn<0:
                    print('Lets keep it postive, shall we?\n')
                else:
                    is_correct = True
            except ValueError:
                print('Not a number :(\n')
        
        game = MiniChess( alpha_beta=False, timeout=max_time, max_turns=max_turn)
        game.play()
        
    elif user_input == 2:
        print(' -----------------------------------------')
        print('|         Player Vs Ai Mode Rules          |')
        print('| Entre The maximum Allow time in Seconds  |')
        print('| Entre the maximum number of turns        |')
        print('| Activate alpha_beta? Yes/No              |')
        print(' -----------------------------------------')
        
        is_correct = False
        while(not is_correct):
            try:
                max_time = int(input("Max time in Seconds: "))
                if max_time<0:
                    print('Lets keep it postive, shall we?\n')
                elif max_time>15:
                    print('Wohoo that\'t alot of time to think. Shrink it bit\n')
                else:
                    is_correct = True
            except ValueError:
                print('Not a number :(\n')
        
        is_correct = False
        while(not is_correct):
            try:
                max_turn = int(input("Max turn in Seconds: "))
                if max_turn<0:
                    print('Lets keep it postive, shall we?\n')
                else:
                    is_correct = True
            except ValueError:
                print('Not a number :(\n')
        
        is_correct = False
        while(not is_correct):
            alpha_beta = str(input("Alpha beta: "))
            if alpha_beta.lower() == 'yes':
                alpha_beta = True
                is_correct = True
            elif alpha_beta.lower() == 'no':
                alpha_beta = False
                is_correct =True
            else:
                print('Incorrect Value\n')
                
    elif user_input ==3:
        print(' -----------------------------------------')
        print('|           Ai Vs Ai Mode Rules            |')
        print('| Entre The maximum Allow time in Seconds  |')
        print('| Entre the maximum number of turns        |')
        print('| Activate alpha_beta? Yes/No              |')
        print(' -----------------------------------------')
        
        is_correct = False
        while(not is_correct):
            try:
                max_time = int(input("Max time in Seconds: "))
                if max_time<0:
                    print('Lets keep it postive, shall we?\n')
                elif max_time>15:
                    print('Wohoo that\'t alot of time to think. Shrink it bit\n')
                else:
                    is_correct = True
            except ValueError:
                print('Not a number :(\n')
        
        is_correct = False
        while(not is_correct):
            try:
                max_turn = int(input("Max turn in Seconds: "))
                if max_turn<0:
                    print('Lets keep it postive, shall we?\n')
                else:
                    is_correct = True
            except ValueError:
                print('Not a number :(\n')
        
        is_correct = False
        while(not is_correct):
            alpha_beta = str(input("Alpha beta: "))
            if alpha_beta.lower() == 'yes':
                alpha_beta = True
                is_correct = True
            elif alpha_beta.lower() == 'no':
                alpha_beta = False
                is_correct =True
            else:
                print('Incorrect Value\n')
              
class MiniChess:
    def __init__(self, alpha_beta=True, timeout=5, max_turns=100):
        self.current_game_state = self.init_board()
        self.logger = MiniChessLogger(alpha_beta, timeout, max_turns)
        self.turn_count = 0  # Track number of turns for draw condition
        self.piece_count_history = []  # Store past counts of pieces
        self.max_turns = max_turns
        self.timeout = timeout
    """
    Initialize the board

    Args:
        - None
    Returns:
        - state: A dictionary representing the state of the game
    """
    def init_board(self):
        state = {
                "board": 
                [['bK', 'bQ', 'bB', 'bN', '.'],
                ['.', '.', 'bp', 'bp', '.'],
                ['.', '.', '.', '.', '.'],
                ['.', 'wp', 'wp', '.', '.'],
                ['.', 'wN', 'wB', 'wQ', 'wK']],
                "turn": 'white',
                }
        return state

    """
    Prints the board
    
    Args:
        - game_state: Dictionary representing the current game state
    Returns:
        - None
    """
    def display_board(self, game_state):
        print()
        for i, row in enumerate(game_state["board"], start=1):
            print(str(6-i) + "  " + ' '.join(piece.rjust(3) for piece in row))
        print()
        print("     A   B   C   D   E")
        print()
        self.logger.log_board(game_state)

    """
    Check if the move is valid    
    
    Args: 
        - game_state:   dictionary | Dictionary representing the current game state
        - move          tuple | the move which we check the validity of ((start_row, start_col),(end_row, end_col))
    Returns:
        - boolean representing the validity of the move
    """
    def is_valid_move(self, game_state, move):
        current_pos, destination = move
        board = game_state['board']
        turn = game_state['turn']
        try: # for when the player enters a move completely out of the board
            player = board[current_pos[0]][current_pos[1]]
        except IndexError:
            return False

        if player =='.':
            return False
        
        if (player[0] =='w' and turn!= 'white') or (player[0]=='b' and turn!='black'):
            return False
        
        valid_movements = self.valid_moves(game_state)
        
        if (current_pos, destination) in valid_movements:
            return True
        
        return False

    """
    Returns a list of valid moves

    Args:
        - game_state:   dictionary | Dictionary representing the current game state
    Returns:
        - valid moves:   list | A list of nested tuples corresponding to valid moves [((start_row, start_col),(end_row, end_col)),((start_row, start_col),(end_row, end_col))]
    """
    def valid_moves(self, game_state):
        board = game_state['board']
        turn = game_state['turn']
        valid_moves = []
        
        movement_rules = {
            "K": king_moves,
            "Q": queen_moves,
            "B": bishop_moves,
            "N": knight_moves,
            "p": pawn_moves
        }
        for row in range(5):
            for col in range(5):
                piece = board[row][col]
                if piece == ".": continue
                
                piece_color = "white" if piece[0] =="w" else "black"
                piece_type = piece[1]
                
                if piece_color == turn:
                    move_function = movement_rules.get(piece_type, lambda position, game_state: [])
                    possible_moves = move_function((row, col), game_state)
                    
                    for move in possible_moves:
                        end_row, end_col = move
                        if 0 <= end_row < 5 and 0 <= end_col < 5:
                            valid_moves.append(((row, col), (end_row, end_col)))
                
        return valid_moves
    
    """
    Counts the total number of pieces on the board.

    Args:
        - game_state: dictionary | The current state of the game.

    Returns:
        - int: The total number of non-empty squares on the board, representing the number of active pieces.
    
    This function iterates over the board and counts all non-empty squares (i.e., any cell that does not contain '.'). 
    It is used to track the number of pieces remaining in the game, which is crucial for implementing the draw condition 
    where no captures have occurred for 10 full turns.
    """
    
    def count_pieces(self, game_state):
        count = 0
        for row in game_state["board"]:
            for cell in row:
                if cell != ".":
                    count += 1
        return count
    
    """
    Modify the board to make a move

    Args: 
        - game_state:   dictionary | Dictionary representing the current game state
        - move          tuple | the move to perform ((start_row, start_col),(end_row, end_col))
    Returns:
        - game_state:   dictionary | Dictionary representing the modified game state
    """
    def make_move(self, game_state, move):
        start = move[0]
        end = move[1]
        start_row, start_col = start
        end_row, end_col = end
        piece = game_state["board"][start_row][start_col]
        captured_piece = game_state['board'][end_row][end_col]
        
        game_state["board"][start_row][start_col] = '.'
        game_state["board"][end_row][end_col] = piece

        # Check if the king is captured:
        if captured_piece =='wK':
            print("Black wins! White's King is captured.")
            self.logger.log_winner('Black Wins! (White\'s king captured)')
            exit(0)
        elif captured_piece =='bK':
            print("White Wins! Black\'s King is captured.")
            self.logger.log_winner('White Wins! (Black\'s King captured)')
            exit(0)
        # Check for pawn promotion after the move is made
        if piece in ["wp", "bp"]:
            promote_pawn((end_row, end_col), game_state)  
        
        current_game_turn = game_state['turn']
        game_state["turn"] = "black" if game_state["turn"] == "white" else "white"
        # Update turn count every time black moves (white + black = 1 turn)
        if game_state["turn"] == "white":
            self.turn_count += 1
            piece_count = self.count_pieces(game_state)

            # Store the piece count history
            if len(self.piece_count_history) == 10:
                self.piece_count_history.pop(0)  # Keep only the last 10 turns
            
            self.piece_count_history.append(piece_count)

            # Check if the number of pieces remained the same for 10 turns
            if len(self.piece_count_history) == 10 and len(set(self.piece_count_history)) == 1:
                print("Game ended in a draw due to no captures in 10 turns.")
                self.logger.log_winner("Draw (no captures in 10 turns)")
                exit(0)

        self.logger.log_move(current_game_turn, move, valid=True)
        return game_state


    """
    Parse the input string and modify it into board coordinates

    Args:
        - move: string representing a move "B2 B3"
    Returns:
        - (start, end)  tuple | the move to perform ((start_row, start_col),(end_row, end_col))
    """
    def parse_input(self, move):
        try:
            start, end = move.split()
            start = (5-int(start[1]), ord(start[0].upper()) - ord('A'))
            end = (5-int(end[1]), ord(end[0].upper()) - ord('A'))
            return (start, end)
        except:
            return None

    def countdown(self):
        for i in range(self.timeout, 0, -1):
            sys.stdout.write(f"\rTime left: {i} seconds")
            sys.stdout.flush()
            time.sleep(1)
        sys.stdout.write("\r" + " " * 30 + "\rTime's up!")
        sys.stdout.flush()
        self.time_up = True
        return
    
    
    """
    Game loop

    Args:
        - None
    Returns:
        - None
    """
    def play(self):
        print("Welcome to Mini Chess! Enter moves as 'B2 B3'. Type 'exit' to quit.")
        while True:
            self.display_board(self.current_game_state) # Show the board
        
            move = input(f"{self.current_game_state['turn'].capitalize()} to move: ") # gets input move from the user     
            
            if move.lower() == 'exit': # Exit the game upon request
                print("Game exited.")
                exit(1)
            
            move = self.parse_input(move) # parse input 
            
            if not move or not self.is_valid_move(self.current_game_state, move):
                
                self.logger.log_move(self.current_game_state['turn'], move, valid=False)
                
                print('You can\'t make this move!')
                
                print("Invalid move. Try again.")
                
                continue

            self.make_move(self.current_game_state, move)

            if self.turn_count > self.max_turns: ## Check if the number of turns excceeded the maximum number of turns 
                print("Game ended due to max turn limit.")
                self.logger.log_winner("Draw (max turns reached)")
                break

if __name__ == "__main__":
    main(menu())




    