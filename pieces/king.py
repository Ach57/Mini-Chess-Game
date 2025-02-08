class King:
    
    def __init__(self, color:str):
        self.color = color 
    
    def get_possible_moves(self,posiiton :tuple) ->list[tuple]:
        x,y = posiiton
        moves = [
            (x-1, y-1), (x-1, y) , (x-1, y+1),
            (x, y-1),               (x, y+1), 
            (x+1, y-1), (x+1, y), (x+1, y+1)
        
               ]
        return moves
    

        
    
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
        