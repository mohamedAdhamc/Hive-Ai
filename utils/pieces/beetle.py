import os
import pygame

from utils.location import Location

from .game_object import GameObject

class Beetle(GameObject):
    sprite = pygame.image.load(os.path.join("assets", "Beetle.png"))

    def __init__(self, location, team):
        # have a reference for the object it came on top of
        # so it can be popped safely from the board
        self.on_top_off = []

        super().__init__(location, team)

    def put_on_top_of(self, piece):
        self.on_top_off.append(piece)

    def get_next_possible_locations(self, board):
        if not board._queens_reference[self._team]:
            return []

        # the beetle can move anywhere and on top of everyone
        possible_locations = []
        x, y = self._location.get_x(), self._location.get_y()

        for dx, dy in [(2, 0), (-2, 0), (1, 1), (-1, 1), (-1, -1), (1, -1)]:
            new_location = Location(x + dx, y + dy)

            if board.check_if_hive_valid(self._location, new_location):
                possible_locations.append(new_location)

        return possible_locations
