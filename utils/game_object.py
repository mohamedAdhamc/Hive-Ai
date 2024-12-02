from location import Location

class GameObject:
    def __init__(self, location):
        if not isinstance(location, Location):
            raise ValueError("location must be an instance of the Location class.")
        self._location = location

    def get_location(self):
        return self._location

    def set_location(self, location):
        if not isinstance(location, Location):
            raise ValueError("location must be an instance of the Location class.")
        self._location = location


