from location import Location
from game_object import GameObject
from queen import Queen


class QueenNotPlayedException(Exception):
    pass

class Board:
    def __init__(self):
        # white - black queen
        self._queen_played = (False, False)
        self._objects = {}
        self._turn_number = 0

    def add_object(self, game_object:GameObject):
        # check if the queen is already played in the first 4 rounds
        if not self._queen_played[0] and not self._queen_played[1]:
            if self._turn_number > 3:
                raise QueenNotPlayedException

            elif isinstance(game_object, Queen):
                #TODO: check if it is white or black for now both are true
                self._queen_played = (True, True)

        self._objects[(game_object.get_location())] = game_object
        
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

