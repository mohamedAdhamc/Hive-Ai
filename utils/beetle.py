from game_object import GameObject
from board import Board
from location import Location

class Beetle(GameObject):
    def get_next_possible_locations(self, board: Board):
        # the beetle can move anywhere and on top of everyone
        possible_locations = []
        x, y = self._location.get_x(), self._location.get_y()

        for dx, dy in [(2, 0), (-2, 0), (1, 1), (-1, 1), (-1, -1), (1, -1)]:
            new_location = Location(x + dx, y + dy)
            if board.get_object(new_location):
                # no need to check if it will break the hive since there is
                # an object already there
                possible_locations.append(new_location)
            elif board.check_if_hive_valid(self._location, new_location):
                possible_locations.append(new_location)

        return possible_locations

