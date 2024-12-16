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
        # the beetle can move anywhere and on top of everyone
        possible_locations = []
        loc: Location = self.get_location()
        x, y = loc.get_x(), loc.get_y()
        
        # check if beetle is on top off another object => can move freely anywhere
        if(len(self.on_top_off) != 0):
            for dx, dy in [(2, 0), (-2, 0), (1, 1), (-1, 1), (-1, -1), (1, -1)]:
                new_location = Location(x + dx, y + dy)
                possible_locations.append(new_location)
            
            return possible_locations
            
        # check if object can leave its initial position
        if(not board.checkIfvalid(loc, None)):
            return []

        for dx, dy in [(2, 0), (-2, 0), (1, 1), (-1, 1), (-1, -1), (1, -1)]:
            new_location = Location(x + dx, y + dy)
            if (board.get_object(new_location) is None): # if the new location is empty, check for narrow path.
                if(not board.isNarrowPath(self.get_location(), new_location)):
                    if board.checkIfvalid(self._location, new_location):
                        possible_locations.append(new_location)
            else: 
                if(board.checkIfvalid(self._location, new_location)):
                    possible_locations.append(new_location)

        return possible_locations
