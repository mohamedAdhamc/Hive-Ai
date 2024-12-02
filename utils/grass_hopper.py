from location import Location
from game_object import GameObject

class Grasshopper(GameObject):
    def __init__(self, location):

        super().__init__(location)  # Call the parent class constructor

        if not isinstance(location, Location):
            raise ValueError("location must be an instance of the Location class.")
        
        self._location = location

    def __repr__(self):
        return f"Grasshopper at {self.get_location()}"
    
    def get_next_possible_locations(self):
        #if there is an element above us
        return