class Queen:
    def __init__(self, color: str):
        self.color = color
        
    def get_possible_moves(self, position:tuple)->list[tuple]:
        x,y = position
        
        moves =  []
        
        # Horizontal and vertical moves
        for i in range( 1,5):
            moves.append((x+i, y))
            moves.append((x-i, y))
            moves.append(x, y+i)
            moves.append((x, y - i))
        
        # for diagonal moves:
        for i in range (1, 5):
            moves.append((x+i, y+i))
            moves.append((x+i, y-i))
            moves.append((x-i, y+i))
            moves.append((x-i, y-i))
        return moves