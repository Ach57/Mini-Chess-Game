class Knight:
    def __init__(self, color:str):
        
        self.color   = color
        
    def get_possible_moves(self, position: tuple)->list[tuple]:
        
        x,y = position
        
        moves = [
            (x + 2, y + 1), (x + 2, y - 1),
            (x - 2, y + 1), (x - 2, y - 1),
            (x + 1, y + 2), (x + 1, y - 2),
            (x - 1, y + 2), (x - 1, y - 2)
        ]
        
        return moves
        
        