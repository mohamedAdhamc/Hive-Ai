from location import Location
from game_object import GameObject
from board import Board

class Grasshopper(GameObject):
    def __init__(self, location, team):

        super().__init__(location, team)  # Call the parent class constructor


        if not isinstance(location, Location):
            raise ValueError("location must be an instance of the Location class.")
        
        self._location = location

    # def __repr__(self):
    #     return f"Grasshopper at {self.get_location()}"
    
    def get_next_possible_locations(self, board: Board):
        newLocations = []
        possible_moves = []

        loc = self.get_location()
        x = loc.get_x()
        y = loc.get_y()
        
        d = [(2,0),(-2,0),(1,1),(-1,1),(1,-1),(-1,-1)]
        for (dx,dy) in d:
            newLoc: Location = Location(x+dx,y+dy)
            if(board.get_object(newLoc) is not None):
                new_x, new_y = x, y
                while (board.get_object(Location(new_x, new_y)) is not None):
                    new_x += dx
                    new_y += dy
                newLoc = Location(new_x, new_y) 
                # check if game is not ruined (Check if the hive is still connected)
                if(board.checkIfvalid(loc, newLoc)):
                    possible_moves.append(newLoc)
                    
        return possible_moves
        
