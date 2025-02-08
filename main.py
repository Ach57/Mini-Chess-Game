import math
import copy
import time
import argparse
from pieces.king import king_moves
from pieces.queen import queen_moves
from pieces.knight import knight_moves
from pieces.pawn import  pawn_moves
from pieces.bishop import bishop_moves


class MiniChess:
    def __init__(self):
        self.current_game_state = self.init_board()

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
        
        
        player = board[current_pos[0]][current_pos[1]]
        
        if player =='.':
            return False
        
        if (player[0] =='w' and turn!= 'white') or (player[0]=='b' and turn!='black'):
            return False
        
        valid_movements =self.valid_moves(game_state)
        print((current_pos, destination))
        print(valid_movements)
        
        if(current_pos, destination) in valid_movements:
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
        # Return a list of all the valid moves.
        # Implement basic move validation
        # Check for out-of-bounds, correct turn, move legality, etc
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
                if piece==".": continue
                
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
    Modify to board to make a move

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
        game_state["board"][start_row][start_col] = '.'
        game_state["board"][end_row][end_col] = piece
        game_state["turn"] = "black" if game_state["turn"] == "white" else "white"

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
            self.display_board(self.current_game_state)
            move = input(f"{self.current_game_state['turn'].capitalize()} to move: ") # gets input move from the user 
            if move.lower() == 'exit':
                print("Game exited.")
                exit(1)
            move = self.parse_input(move)
            if not move or not self.is_valid_move(self.current_game_state, move):
                print("Invalid move. Try again.")
                continue

            self.make_move(self.current_game_state, move)

if __name__ == "__main__":
    game = MiniChess()
    game.play()



    

'''
Notes:

Everything would be okay except that there is a logic to handle between the movements 


'''