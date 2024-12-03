from location import Location
from game_object import GameObject
# from grass_hopper import Grasshopper

class Board:
    def __init__(self):
        self._objects = {}

    def add_object(self, game_object:GameObject):
        self._objects[(game_object.get_location())] = game_object

    def get_object(self, location):
        """
        Get the game object at a specific position.

        Returns:
            object: The game object at the given position, or None if empty.
        """
        return self._objects.get((location), None)

    def remove_object(self, location):
        """
        Remove a game object from a specific position.
        
        Raises:
            KeyError: If there is no object at the specified position.
        """
        if not isinstance(location, Location):
            raise ValueError("location must be of Location class.")
        
        if (location) not in self._objects:
            raise KeyError(f"No object found at location.")
        del self._objects[(location)]

    def move_object(self, oldLocation, newLocation):
        """
        Move a game object from one position to another.
        
        Raises:
            KeyError: If there is no object at the source position.
        """
        if (oldLocation) not in self._objects:
            raise KeyError(f"No object found at position old location.")
        object : GameObject = self._objects.pop((oldLocation))
        object.set_location(newLocation)
        self._objects[(newLocation)] = object

    def __repr__(self):
        """
        Represent the board as a string.
        """
        return "\n".join([f"Position {pos}: {obj}" for pos, obj in self._objects.items()])
    
    def checkIfvalid(self, oldLoc: Location, newLoc: Location):
        """
        Checks if the hive is still connected after every move.
        Args:
            oldLoc (Location): Location of object before the move.
            newLoc (Location): Location of object after the move.
        Returns:
            bool: True if the hive is still connected, False otherwise.
        """
        newBoard = dict(self._objects)
        del newBoard[(oldLoc)]
        newBoard[newLoc] = 1
        print("Qabl el mas7 Board:=>",newBoard)
        visited = []
        
        # test neighbours
        def checkHive(loc: Location, prev:Location):
            visited.append(loc)
            print("location:",loc)
            curr_x = loc.get_x()
            curr_y = loc.get_y()
            d = [(2,0),(-2,0),(1,1),(-1,1),(1,-1),(-1,-1)]
            for (dx,dy) in d:
                current_search_loc = Location(curr_x + dx, curr_y + dy)
                if((curr_x + dx, curr_y + dy) == (prev.get_x(), prev.get_y()) or current_search_loc in visited):
                    continue
                print("search:",current_search_loc)
                if newBoard.get((current_search_loc),None) is not None:
                    print("found")
                    checkHive(current_search_loc, loc)
                else:
                    print("not found")
            
            del newBoard[(loc)]
                    

        checkHive(newLoc,oldLoc)
        print("ba3d el mas7 board:",newBoard)
        if(len(newBoard) == 0):
            return True
        else:
            return False
        
    
    def isSurroundedByFive(self,loc: Location):
        """
        Checks whether the object is surrounded by five other objects or no
        Args:
            loc (Location): The location of the object.

        Returns:
            bool: True if the object is surrounded by five, false otherwise.
        """
        curr_x = loc.get_x()
        curr_y = loc.get_y()
        counter = 0
        d = [(2,0),(-2,0),(1,1),(-1,1),(1,-1),(-1,-1)]
        for (dx,dy) in d:
            current_search_loc = Location(curr_x + dx, curr_y + dy)
            if self._objects.get((current_search_loc),None) is not None:
                counter = counter + 1
        
        if(counter == 5):
            return True
        else:
            return False
                

