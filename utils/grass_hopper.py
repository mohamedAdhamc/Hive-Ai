from location import Location
from game_object import GameObject
from board import Board

class Grasshopper(GameObject):
    def __init__(self, location):

        super().__init__(location)  # Call the parent class constructor

        if not isinstance(location, Location):
            raise ValueError("location must be an instance of the Location class.")
        
        self._location = location

    def __repr__(self):
        return f"Grasshopper at {self.get_location()}"
    
    def get_next_possible_locations(self, board:Board):
        newLocations = []
        possible_moves = []

        loc = self.get_location()
        x = loc.get_x()
        y = loc.get_y()
        
        d = [(2,0),(-2,0),(1,1),(-1,1),(1,-1),(-1,-1)]
        for (dx,dy) in d:
            newLoc: Location = Location(x+dx,y+dy)
            if(board.get_object(newLoc) is None):
                # check if game is not ruined (Check if the hive is still connected)
                if(board.checkIfvalid(loc, newLoc)):
                    if(not board.isSurroundedByFive(newLoc)):
                        possible_moves.append(newLoc)
                    
        return possible_moves
        
        # #if there is an element above and right
        # if (Board.get_object(Location(x+1, y+1)) is not None):
        #     new_x = x
        #     new_y = y
        #     while (Board.get_object(Location(x+1, y+1)) is not None):
        #         new_x += 1
        #         new_y += 1
        #     newLocations.append(Location(new_x,new_y))
            

        # #if there is an element above and left
        # if (Board.get_object(Location(x-1, y+1)) is not None):
        #     new_x = x
        #     new_y = y
        #     while (Board.get_object(Location(x-1, y+1)) is not None):
        #         new_x -= 1
        #         new_y += 1
        #     newLocations.append(Location(new_x,new_y))

        # #if there is an element bottom and right
        # if (Board.get_object(Location(x+1, y-1)) is not None):
        #     new_x = x
        #     new_y = y
        #     while (Board.get_object(Location(x+1, y-1)) is not None):
        #         new_x += 1
        #         new_y -= 1
        #     newLocations.append(Location(new_x, new_y))

        # #if there is an element bottom and left
        # if (Board.get_object(Location(x-1, y-1)) is not None):
        #     new_x = x
        #     new_y = y
        #     while (Board.get_object(Location(x-1, y-1)) is not None):
        #         new_x -= 1
        #         new_y -= 1
        #     newLocations.append(Location(new_x, new_y))

        # #if there is an element to the right
        # if (Board.get_object(Location(x+2, y)) is not None):
        #     new_x = x + 2
        #     new_y = y
        #     while (Board.get_object(Location(x-1, y-1)) is not None):
        #         new_x += 2
        #     newLocations.append(Location(new_x, new_y))

        # #if there is an element to the left
        # if (Board.get_object(Location(x-2, y)) is not None):
        #     new_x = x - 2
        #     new_y = y
        #     while (Board.get_object(Location(x-1, y-1)) is not None):
        #         new_x -= 2
        #     newLocations.append(Location(new_x, new_y))

        return newLocations