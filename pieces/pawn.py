class Pawn:
    def __init__(self,color:str):
        self.color = color
    
    def get_possible_moves(self, position: tuple)->list[tuple]:
        
        x,y = position
        
        moves = []
        moves.append((x, y-1)) if self.color == "white" else moves.append((x, y+1))# moving forward and backward
        
        # for diagonal moves when capturing something 
        moves.append((x - 1, y + 1)) if self.color == 'white' else moves.append((x + 1, y - 1))
        moves.append((x - 1, y - 1)) if self.color == 'white' else moves.append((x + 1, y - 1))
        
        
        return moves