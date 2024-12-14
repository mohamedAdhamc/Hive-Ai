from utils.location import Location

class GameObject:
    sprite = None

    def __init__(self, location: Location, team):
        if not isinstance(location, Location):
            raise ValueError("location must be an instance of the Location class.")
        self._location = location
        self._team = team


    def get_location(self):
        return self._location

    def set_location(self, location):
        if not isinstance(location, Location):
            raise ValueError("location must be an instance of the Location class.")
        self._location = location

    def get_team(self):
        return self._team

    def set_team(self, team):
        if(isinstance(team, int) and (team == 0 or team == 1)):
            self._team = team
        else:
            raise ValueError("Team should be represented as a number (1 or 2)")

    def __repr__(self):
        return f"{self.__class__.__name__} at {self.get_location()}, in team {self._team}"

    def get_next_possible_locations(self, board):
        raise NotImplementedError

    def draw(self, screen):
        if not self.sprite:
            raise TypeError("Sprite has not yet been initialized")

        # TODO: The piece location is for sure different from the window locations
        # so some calculations must be done first
        screen.blit(self.sprite, (self._location.get_x(), self._location.get_y()))
