from location import Location
from game_object import GameObject

class QueenNotPlayedException(Exception):
    pass

class Board:
    def __init__(self):
        # white - black queen
        self._queen_played = (False, False)
        self._objects = {}
        self._turn_number = 0
        self._hands = {}
        self.initiate_game()
        
    def initiate_game(self):
        from queen import Queen
        from grass_hopper import Grasshopper
        from spider import Spider
        from ant import Ant
        from beetle import Beetle
        initial_state = {   # The initial objects in hand with each player at the beggining
            Queen: 1,
            Spider: 2,
            Beetle: 2,
            Ant: 3,
            Grasshopper: 3
        }
        self._hands[1] = self._hands[2] = initial_state # assigned to player 1 and player 2
    
    def add_object(self, game_object:GameObject):
        # check if the queen is already played in the first 4 rounds
        from queen import Queen
        if not self._queen_played[0] and not self._queen_played[1]:
            if self._turn_number > 3:
                raise QueenNotPlayedException

            elif isinstance(game_object, Queen):
                #TODO: check if it is white or black for now both are true -- done
                # mark true for the player who played queen
                self._queen_played[game_object.get_team()-1] = True

        if(self._hands[game_object.get_team()][game_object] > 0):
            self._objects[(game_object.get_location())] = game_object
            self._hands[game_object.get_team()][game_object] -= 1 # Decrease chosen object by one
        
        # number of turns that passed
        self._turn_number += 1 

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

    def check_if_hive_valid(self ,old_loc: Location, new_loc: Location):
        removed = []
        removed.append((old_loc, self._objects.pop((old_loc))))
        self._recurse_pop(new_loc, removed)

        if self._objects.keys():
            for location, insect in removed:
                self._objects[(location)] = insect
            return False

        for location, insect in removed:
            self._objects[(location)] = insect
        return True

    def _recurse_pop(self, loc: Location, removed):
        for dx, dy in [(2, 0), (-2, 0), (1, 1), (-1, 1), (1, -1), (-1, -1)]:
            new_location = Location(loc.get_x() + dx, loc.get_y() + dy)
            insect = self._objects.pop((new_location), None)
            if insect:
                removed.append((new_location, insect))
                self._recurse_pop(new_location, removed)




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
        
    
    def isSurroundedBySix(self,loc: Location):
        """
        Checks whether the object is surrounded by six other objects or no
        Args:
            loc (Location): The location of the object.

        Returns:
            bool: True if the object is surrounded by six, false otherwise.
        """
        curr_x = loc.get_x()
        curr_y = loc.get_y()
        counter = 0
        d = [(2,0),(-2,0),(1,1),(-1,1),(1,-1),(-1,-1)]
        for (dx,dy) in d:
            current_search_loc = Location(curr_x + dx, curr_y + dy)
            if self._objects.get((current_search_loc),None) is not None:
                counter = counter + 1
        
        if(counter == 6):
            return True
        else:
            return False
        
    def getPossibleDeployLocations(self, team: int):
        """Gets the possible deploy location for an object based on their team.

        Args:
            team (int): team of the object (Player 1 or 2).
        Returns:
            list: List of the possible locations at which it can deploy on the hive.
        """
        
        possible_locations = set()
        objects = dict(self._objects)
        for pos, obj in objects.items():
            obj: GameObject
            curr_x = obj.get_location().get_x()
            curr_y = obj.get_location().get_y()
            if(team == obj.get_team()):
                d = [(2,0),(-2,0),(1,1),(-1,1),(1,-1),(-1,-1)]
                for dx,dy in d:
                    current_search_loc = Location(curr_x + dx, curr_y + dy)
                    if objects.get((current_search_loc),None) is None:  # Free position neihgbouring a freindly object
                        touching_enemy = False
                        # Make sure that this position isn't touching an enemy object
                        for dx2,dy2 in d:
                            search_loc = Location(curr_x + dx + dx2, curr_y + dy + dy2)
                            if objects.get((search_loc),None) is not None:  # An object found touching this position
                                object:GameObject = objects.get(search_loc)
                                if(object.get_team() is not team):  # This Object is an enemy Object
                                    touching_enemy = True
                        if(touching_enemy is False):
                            possible_locations.add(current_search_loc)
                                    
                        
        print(possible_locations)
        return possible_locations
    
    
    def isNarrowPath(self, oldLoc: Location, newLoc: Location):
        dx, dy = newLoc - oldLoc
        # moving from left to right
        if((dx, dy) == (2, 0)):
            # check top right and bottom right
            top_right: Location = oldLoc + (1, 1)
            bottom_right: Location = oldLoc + (1, -1)
            return bool(self._objects.get(top_right, None) and self._objects.get(bottom_right, None))
        
        # moving from right to left
        if((dx, dy) == (-2, 0)):
            # check top left and bottom left
            top_left: Location = oldLoc + (-1, 1)
            bottom_left: Location = oldLoc + (-1, -1)
            return bool(self._objects.get(top_left, None) and self._objects.get(bottom_left, None))
        
        # moving to top right
        if((dx, dy) == (1, 1)):
            # check for right and top left  
            right: Location = oldLoc + (2, 0)
            top_left: Location = oldLoc + (-1, 1)
            return bool(self._objects.get(right, None) and self._objects.get(top_left, None))
        
        # moving bottom left
        if((dx, dy) == (-1, -1)):
            # check for left and bottom right
            left: Location = oldLoc + (-2, 0)
            bottom_right: Location = oldLoc + (1, -1)
            return bool(self._objects.get(left, None) and self._objects.get(bottom_right, None))
    
        # moving top left
        if((dx, dy) == (-1, 1)):
            # check for left and top right
            left: Location = oldLoc + (-2, 0)
            top_right: Location = oldLoc + (1, 1)
            return bool(self._objects.get(left, None) and self._objects.get(top_right, None))
    
        # moving bottom right
        if((dx, dy) == (1, -1)):
            # check for right and left bottom
            right: Location = oldLoc + (2, 0)
            bottom_left: Location = oldLoc + (-1, -1)
            return bool(self._objects.get(right, None) and self._objects.get(bottom_left, None))

