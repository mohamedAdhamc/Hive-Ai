from location import Location

class Grasshopper:
    def __init__(self, location):
        if not isinstance(location, Location):
            raise ValueError("location must be an instance of the Location class.")
        self.location = location

    def get_location(self):
        return self.location

    def update_location(self, location):
        if not isinstance(location, Location):
            raise ValueError("location must be an instance of the Location class.")
        self.location = location
