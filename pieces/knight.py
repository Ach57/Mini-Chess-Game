def knight_moves(position:tuple, game_state):
    """
    Args:
        position (tuple): position of the piece in the board
        game_state (dict): Dictionary containing the board and turn

    Returns:
        list[tuple]: possible moves
    """
    x, y = position
    moves = [(x + dx, y + dy) for dx, dy in [
        (2, 1), (2, -1), (-2, 1), (-2, -1),
        (1, 2), (1, -2), (-1, 2), (-1, -2)
    ]]
    return moves
