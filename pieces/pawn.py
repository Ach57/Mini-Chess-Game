def pawn_moves(position, game_state):
    """
    Args:
        position (tuple): position of the piece in the board
        game_state (dict): Dictionary containing the board and turn

    Returns:
        list[tuple]: possible moves
    """
    x, y = position
    board = game_state["board"]
    turn = game_state["turn"]
    direction = 1 if turn == "white" else -1
    moves = []

    if 0 <= y + direction < 5 and board[y + direction][x] == ".":
        moves.append((x, y + direction))

    for dx in [-1, 1]:
        if 0 <= x + dx < 5 and 0 <= y + direction < 5:
            if board[y + direction][x + dx] != ".":
                moves.append((x + dx, y + direction))

    return moves
