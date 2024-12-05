from location import Location
from game_object import GameObject
from board import Board

class Queen(GameObject):
    def __init__(self, location, team):
        super().__init__(location, team)
        
        if not isinstance(location, Location):
            raise ValueError("location must be an instance of the Location class.")
        
        self._location = location
    
    # def __repr__(self):
    #     return f"Queen at {self.get_location()}"
    
    def getPossibleMoves(self, board:Board):
        print("checking board:", board, "\n")
        possible_moves = []
        loc: Location = self.get_location()
        x = loc.get_x()
        y = loc.get_y()
        
        d = [(2,0),(-2,0),(1,1),(-1,1),(1,-1),(-1,-1)]
        for (dx,dy) in d:
            newLoc: Location = Location(x+dx,y+dy)
            print("Chcekcing for:", newLoc)
            print("Chcekcing board:", board)
            print(board.get_object(newLoc))
            if(board.get_object(newLoc) is None):
                
                if(not board.isNarrowPath(loc, newLoc)): # Check if the path is not narrow
                    if(board.checkIfvalid(loc, newLoc)): # check if game is not ruined (Check if the hive is still connected)
                        possible_moves.append(newLoc)
                    
        print("Possible Moves", possible_moves)
        return possible_moves
        
            
        
 
