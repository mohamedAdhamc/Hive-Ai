from location import Location

class GameObject:
    def __init__(self, location, color):
        if not isinstance(location, Location):
            raise ValueError("location must be an instance of the Location class.")
        self._location = location
        self._color = color # or team

    def get_location(self):
        return self._location

    def set_location(self, location):
        if not isinstance(location, Location):
            raise ValueError("location must be an instance of the Location class.")
        self._location = location

    def get_next_possible_locations(self, board):
        raise NotImplementedError


