class Bishop:
    def __init__(self, color:str):
        self.color   = color
        

    def get_possible_moves(self, position: tuple) ->list[tuple]:
        x, y = position
        
        moves = []
        
        for i in range(1,5):
            moves.append((x+1, y+1))
            moves.append((x+1, y-1))
            moves.append((x-1, y-1))
            moves.append((x-1, y+1))
            
        return moves

        