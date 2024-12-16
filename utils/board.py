from .location import Location
from .pieces.game_object import GameObject
from .pieces import Queen, Beetle, Ant, Spider, Grasshopper

class QueenNotPlayedException(Exception):
    def __init__(self, message="The queen must be played within the first four turns."):
        self.message = message
        super().__init__(self.message)

class Board:
    def __init__(self, win_callback, alert_callback):
        # white - black queen
        self._queen_played = [False, False]
        self._queens_reference = [None, None]
        self._objects = {}
        self._turn_number = 0
        self.win_callback = win_callback
        self.alert_callback = alert_callback
        self._hands = {}
        self.initiate_game()

    def get_board_representation(self):
        
        board_representation = [None] * 23
        pointers = {
            "Queen": [0, 11],
            "Ant": [1, 12],
            "Grasshopper": [4, 15],
            "Beetle": [7, 18],
            "Spider": [9, 20]
        }

        for location, piece in self._objects.items():
            pointer = pointers[piece.__class__.__name__][piece._team]
            board_representation[pointer] = location
            pointers[piece.__class__.__name__][piece._team] += 1

        board_representation[22] = self._turn_number % 2
        return board_representation

    def turn(self):
        """
        Determines whose turn it is to play.
        Returns:
            bool: True if it's the first player's turn (even turn number),
            False if it's the second player's turn (odd turn number).
        """
        return self._turn_number % 2 == 0


    def filter_team_pieces(self):
        if(self.turn()):
            team_number=0
        else:
            team_number=1
        # Filter out pieces where the team attribute matches the provided team_number
        team_pieces = {location: piece for location, piece in self._objects.items() if piece.get_team() == team_number}
        return team_pieces
        

    def get_moves_and_deploys(self):
        combined_results = []

        if self.check_win_condition_bool():
            return combined_results

        team_number = 0 if self.turn() else 1
        available_pieces = self._hands[team_number]

        deploy_locations = self.getPossibleDeployLocations(team_number)
        flag=1

        if (self._turn_number == 6 and team_number == 0) or (self._turn_number == 7 and team_number == 1):
            if available_pieces.get(Queen, 0) > 0:  # If Queen is still in hand
                flag=0
                for location in deploy_locations:
                    combined_results.append(('Queen', location))
        
        if(flag):
            team_pieces = self.filter_team_pieces()

            for location, piece in team_pieces.items():
                possible_destinations = piece.get_next_possible_locations(self)

                for destination in possible_destinations:
                    combined_results.append((location, destination))

            for piece_type, count in available_pieces.items():
                if count > 0:
                    for location in deploy_locations:
                        combined_results.append((piece_type.__name__, location))

        return combined_results

    def initiate_game(self):
       
       # The initial objects in hand with each player at the beggining
        self._hands[0] = {   
            Queen: 1,
            Spider: 2,
            Beetle: 2,
            Ant: 3,
            Grasshopper: 3
        }
        self._hands[1] = {
            Queen: 1,
            Spider: 2,
            Beetle: 2,
            Ant: 3,
            Grasshopper: 3
        }
     

    def add_object(self, game_object: GameObject):
        """
        Add a game object to the board. Validates placement rules before committing changes.
        
        Ensures that:
        1. Queen must be played within the first 4 moves for each player
        2. If 4 moves pass without playing the queen, the next move MUST be a queen
        """
        try:
            current_team = game_object.get_team()
            
            if not self._queen_played[current_team]:
                team_moves = sum(1 for loc, piece in self._objects.items() if piece.get_team() == current_team)
                
                if team_moves >= 3 and not isinstance(game_object, Queen):
                    raise QueenNotPlayedException(f"Player {current_team + 1} must play their queen by the 4th move")

            if isinstance(game_object, Queen):
                self._queen_played[current_team] = True
                self._queens_reference[current_team] = game_object

            self._objects[game_object.get_location()] = game_object
            self._hands[game_object.get_team()][game_object.__class__] -= 1
            self._turn_number += 1

            if self._turn_number > 7:
                self.check_win_condition()
                
            print("Board state: ", self._objects)

            return True  

        except QueenNotPlayedException as e:
            self.alert_callback(str(e)) 
            return False


    def check_win_condition(self):
        d = [(2, 0), (-2, 0), (1, 1), (-1, 1), (1, -1), (-1, -1)]

        for dx, dy in d:
            test_location = self._queens_reference[0]._location
            if not self.get_object(test_location.create_from_self(dx, dy)):
                break
        else:
            self.win_callback(1)
            return

        for dx, dy in d:
            test_location = self._queens_reference[1]._location
            if not self.get_object(test_location.create_from_self(dx, dy)):
                break
        else:
            self.win_callback(0)
            return

    def check_win_condition_bool(self):
        d = [(2, 0), (-2, 0), (1, 1), (-1, 1), (1, -1), (-1, -1)]

        if self._queens_reference[0]:
            for dx, dy in d:
                test_location = self._queens_reference[0]._location
                if not self.get_object(test_location.create_from_self(dx, dy)):
                    break
            else:
                return 1

        if self._queens_reference[1]:
            for dx, dy in d:
                test_location = self._queens_reference[1]._location
                if not self.get_object(test_location.create_from_self(dx, dy)):
                    break
            else:
                return -1
        
        return 0

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

        game_object = self.get_object(location)

        if isinstance(game_object, Queen):
            self._queen_played[game_object.get_team()] = False
            self._queens_reference[game_object._team] = None

        self._hands[game_object.get_team()][game_object.__class__] += 1 # increase chosen object by one
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

        if isinstance(object, Beetle):
            if object.on_top_off:
                bottom_object = object.on_top_off.pop()
                bottom_object.set_location(oldLocation)
                self._objects[(oldLocation)] = bottom_object
            piece_at_location = self._objects.pop((newLocation), None)
            if piece_at_location:
                object.put_on_top_of(piece_at_location)

        object.set_location(newLocation)
        self._objects[(newLocation)] = object

        self._turn_number += 1
        if self._turn_number > 7:
            self.check_win_condition()
        
        print("Board state:", self._objects)

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
        visited = []

        # test neighbours
        def checkHive(loc: Location, prev:Location):
            visited.append(loc)
            curr_x = loc.get_x()
            curr_y = loc.get_y()
            d = [(2,0),(-2,0),(1,1),(-1,1),(1,-1),(-1,-1)]
            for (dx,dy) in d:
                current_search_loc = Location(curr_x + dx, curr_y + dy)
                if((curr_x + dx, curr_y + dy) == (prev.get_x(), prev.get_y()) or current_search_loc in visited):
                    continue
                if newBoard.get((current_search_loc),None) is not None:
                    checkHive(current_search_loc, loc)
            
            del newBoard[(loc)]


        checkHive(newLoc,oldLoc)
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

        d = [(2,0),(-2,0),(1,1),(-1,1),(1,-1),(-1,-1)]

        possible_locations = set()
        objects = dict(self._objects)
        for pos, obj in objects.items():
            obj: GameObject
            curr_x = obj.get_location().get_x()
            curr_y = obj.get_location().get_y()
            if(team == obj.get_team()):
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
        
        if self._turn_number == 0:
            possible_locations.add(Location(0, 0))
        elif self._turn_number == 1:
            for dx, dy in d:
                possible_locations.add(Location(dx, dy))

        return possible_locations
                           
                        
    
    
    def isNarrowPath(self, oldLoc: Location, newLoc: Location):
        diff = newLoc - oldLoc
        dx, dy = diff.get_x(), diff.get_y()
        # moving from left to right
        if((dx, dy) == (2, 0)):
            # check top right and bottom right
            top_right: Location = oldLoc + Location(1, 1)
            bottom_right: Location = oldLoc + Location(1, -1)
            return bool(self.get_object((top_right)) and self.get_object((bottom_right)))
        
        # moving from right to left
        if((dx, dy) == (-2, 0)):
            # check top left and bottom left
            top_left: Location = oldLoc + Location(-1, 1)
            bottom_left: Location = oldLoc + Location(-1, -1)
            return bool(self.get_object(top_left) and self.get_object(bottom_left))
        
        # moving to top right
        if((dx, dy) == (1, -1)):
            # check for right and top left  
            right: Location = oldLoc + Location(2, 0)
            top_left: Location = oldLoc + Location(-1, -1)
            return bool(self.get_object(right) and self.get_object(top_left))
        
        # moving bottom left
        if((dx, dy) == (-1, 1)):
            # check for left and bottom right
            left: Location = oldLoc + Location(-2, 0)
            bottom_right: Location = oldLoc + Location(1, 1)
            return bool(self.get_object(left) and self.get_object(bottom_right))
    
        # moving top left
        if((dx, dy) == (-1, -1)):
            # check for left and top right
            left: Location = oldLoc + Location(-2, 0)
            top_right: Location = oldLoc + Location(1, -1)
            return bool(self.get_object(left) and self.get_object(top_right))
    
        # moving bottom right
        if((dx, dy) == (1, 1)):
            # check for right and left bottom
            right: Location = oldLoc + Location(2, 0)
            bottom_left: Location = oldLoc + Location(-1, 1)
            return bool(self.get_object(right) and self.get_object(bottom_left))


