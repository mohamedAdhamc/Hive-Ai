from location import Location
from game_object import GameObject
from grass_hopper import Grasshopper

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

