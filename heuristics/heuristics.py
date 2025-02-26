def get_pieces_count(game_state: dict) ->dict:
    """_summary_
    Returns the number of pieces in a dictionary 
    Args:
        game_state (dict): game board 

    Returns:
        dict: number of pieces in a Dictionary
    """
    output_dict = {
        'black': {
                'K':0,
                'Q': 0,
                'B': 0,
                'N': 0,
                'p':0
            },
        'white':{
            'K':0,
            'Q': 0,
            'B': 0,
            'N': 0,
            'p':0
        }
    }
    board = game_state['board']# get the board
    
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] =='.':
                continue
            if board[row][col][0] =='b':
                output_dict['black'][board[row][col][1]]+=1
            else:
                output_dict['white'][board[row][col][1]]+=1
        
    return output_dict

def e0(pieces_count: dict) -> int:
    """_summary_
    e0: Purely materialistic evaluation based on the count of each type of piece.
    Args:
        pieces_count (dict): dictionary contianing the piece count of black and white

    Returns:
        int: heuristic count
    """
    
    # Values for each piece type
    piece_values = {
        'p': 1,    # Pawn value
        'B': 3,    # Bishop value
        'N': 3,    # Knight value
        'Q': 9,    # Queen value
        'K': 999   # King value
    }

    # Get the pieces count for black and white
    black_values = pieces_count['black']
    white_values = pieces_count['white']

    # Calculate the total score for black and white
    black_count = sum(black_values[piece] * piece_values[piece] for piece in piece_values)
    white_count = sum(white_values[piece] * piece_values[piece] for piece in piece_values)

    # Return the difference (positive value favors white, negative favors black)
    return white_count - black_count


def e1(pieces_count: dict, game_state:dict) ->int:
    """_summary_
    e1: Material balance with added positional value. The position of pieces affects their overall score.
    Args:
        pieces_count (dict): _description_
        game_state (dict): _description_

    Returns:
        int: _description_
    """
    position_bonus = { # Requires adjustment
    'p': {  # Pawn positions
        'black': [(1, 2), (1, 3)],  
        'white': [(3, 0), (3, 1), (3, 2)],  
    },
    'B': {  # Bishop positions
        'black': [(0, 2)],  
        'white': [(4, 1)],  
    },
    'N': {  # Knight positions
        'black': [(0, 3)],  
        'white': [(4, 0)],  
    },
    'Q': {  # Queen positions
        'black': [(0, 1)],  
        'white': [(4, 2)],  
    },
    'K': {  # King positions
        'black': [(0, 0)],  
        'white': [(4, 4)],  
    },
}
    
    def calculate_position_bonus(piece:str, color:str, game_state:dict) ->int:
        """_summary_
        addes bonus points based on where each piece exists on the board
        Args:
            piece (str): ['p','B','N','Q','K']
            color (str): ['black','white']
            game_state (dict): dictionary

        Returns:
            int: 1|0
        """
        
        bonus = 0
        board = game_state['board']
        favorable_position = position_bonus.get(piece, {}).get(color, [])
        
        for row, col in favorable_position:
            piece_at_position = board[row][col]
            if piece_at_position[0] == piece:
                bonus+=1
        
        return bonus
        
    score = e0(pieces_count)    
    
    for piece in ['p','B','N','Q','K']:
        for color in ['black','white']:
            position_score = calculate_position_bonus(piece, color, game_state)
            score+= position_score
    
    return score


if __name__=="__main__":
    game_state = {
                "board": 
                [['bK', 'bQ', 'bB', 'bN', '.'],
                ['.', '.', 'bp', 'bp', '.'],
                ['', '.', '.', '.', '.'],
                ['.', 'wp', 'wp', '.', '.'],
                ['.', 'wN', 'wB', 'wQ', 'wK']],
                "turn": 'white',
                }
    
    #print(e0(get_pieces_count(game_state)))
    
    #print(e1(get_pieces_count(game_state), game_state))
    print(game_state['board'][0][2])
    
    
    