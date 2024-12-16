import os
import pygame

from utils.location import Location

from .game_object import GameObject

class Queen(GameObject):
    sprite = pygame.image.load(os.path.join("assets", "Queen.png"))

    def __init__(self, location, team):
        super().__init__(location, team)

        if not isinstance(location, Location):
            raise ValueError("location must be an instance of the Location class.")

        self._location = location

    # def __repr__(self):
    #     return f"Queen at {self.get_location()}"

    def get_next_possible_locations(self, board):
        if not board._queens_reference[self._team]:
            return []

        possible_moves = []
        loc: Location = self.get_location()
        x = loc.get_x()
        y = loc.get_y()

        d = [(2,0),(-2,0),(1,1),(-1,1),(1,-1),(-1,-1)]
        for (dx,dy) in d:
            newLoc: Location = Location(x+dx,y+dy)
            if(board.get_object(newLoc) is None):
                # print("true1", newLoc)
                if(not board.isNarrowPath(loc, newLoc)): # Check if the path is not narrow
                    if(board.checkIfvalid(loc, newLoc)): # check if game is not ruined (Check if the hive is still connected)
                        possible_moves.append(newLoc)

        return possible_moves
