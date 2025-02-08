def king_moves(position:tuple, game_state:dict)->list[tuple]:
    """_summary_
    Returns all possible moves for a King.
    Args:
        position (tuple): position of the piece in the board
        game_state (dict): Dictionary containing the board and turn
    """
    
    x,  y = position
    
    directions = [(-1, -1), (-1, 0), (-1, 1),
                  (0, -1),         (0, 1),
                  (1, -1), (1, 0), (1, 1)]
    return [(x + dx, y + dy) for dx, dy in directions]


    
    
    
    
'''
(y)
|             possible moves for (0,0) = [(-1, -1),
|                                (-1, 0), (-1, 1), (0, -1),
|                                (0, 1), (1, -1), (1, 0), (1, 1)]
|
|
|
(0,0)---------------------- (x)
'''
        