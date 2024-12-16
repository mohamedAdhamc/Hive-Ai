import os
import pygame

from utils.location import Location

from .game_object import GameObject

class Spider(GameObject):
    sprite = pygame.image.load(os.path.join("assets", "Spider.png"))

    def __init__(self, location, team):
        super().__init__(location, team)

        if not isinstance(location, Location):
            raise ValueError("location must be an instance of the Location class.")

        self._location = location

    # def __repr__(self):
    #     return f"Spider at {self.get_location()}"

    def get_next_possible_locations(self, board):
        if not board._queens_reference[self._team]:
            return []

        possible_moves = []
        moves = []
        initial_loc: Location = self.get_location()
        x = initial_loc.get_x()
        y = initial_loc.get_y()

        def moveStepForward(loc: Location , prevLoc: Location, step):
            if(board.isNarrowPath(prevLoc, loc)):
                return False
            flag = False
            x = loc.get_x()
            y = loc.get_y()
            d = [(2,0),(-2,0),(1,1),(-1,1),(1,-1),(-1,-1)]
            # check if the spider is having neighbours (Moving on edges)
            for (dx,dy) in d:
                newLoc: Location = Location(x+dx,y+dy)
                if((prevLoc.get_x(),prevLoc.get_y()) == (x+dx,y+dy) or (initial_loc.get_x(),initial_loc.get_y()) == (x+dx,y+dy)):
                    continue
                if(board.get_object(newLoc) is not None):
                    flag = True
                    break

            if(flag == False): # if not moving on edge return false
                return False

            if(step == 1): # If reached the final step with no violations return true
                moves.append(loc)
                return True

            # Test all possible moves
            for (dx,dy) in d:
                newLoc: Location = Location(x+dx,y+dy)
                if((prevLoc.get_x(),prevLoc.get_y()) == (x+dx,y+dy) or (initial_loc.get_x(),initial_loc.get_y()) == (x+dx,y+dy)):
                    continue
                if(board.get_object(newLoc) is None):
                # Check if this step can be taken by the spider
                    moveStepForward(newLoc, loc, step-1)

        d = [(2,0),(-2,0),(1,1),(-1,1),(1,-1),(-1,-1)]
        for (dx,dy) in d:
            newLoc: Location = Location(x+dx,y+dy)
            if(board.get_object(newLoc) is None):
                # Check if this step can be taken by the spider
                result = moveStepForward(newLoc, initial_loc, 3)


        for newLoc in moves:
            if(board.checkIfvalid(initial_loc, newLoc)):
                possible_moves.append(newLoc)

        return possible_moves
