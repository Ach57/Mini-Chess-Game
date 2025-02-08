def bishop_moves(position:tuple, game_state: dict)->list[tuple]:
    """
    Args:
        position (tuple): position of the piece in the board
        game_state (dict): Dictionary containing the board and turn

    Returns:
        list[tuple]: possible moves
    """
    
    x, y = position
    directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
    moves = []
    for dx, dy in directions:
        for step in range(1, 5):  # Move as far as possible
            new_x, new_y = x + dx * step, y + dy * step
            if 0 <= new_x < 5 and 0 <= new_y < 5:
                moves.append((new_x, new_y))
    return moves
    
    
