import os
import pygame

from utils.location import Location

from .game_object import GameObject

class Ant(GameObject):
    sprite = pygame.image.load(os.path.join("assets", "Ant.png"))

    def _check_surrounding(self, board):
        surrounding = 0

        x, y = self._location.get_x(), self._location.get_y()
        for dx, dy in [(1, -1), (-1, -1), (-2, 0), (-1, 1), (1, 1), (2, 0)]:
            index = Location(x + dx, y + dy)
            piece = board.get_object(index)

            if piece:
                surrounding += 1
        # ant is surrounded no need to move

        return surrounding >= 5

    def _check_trapped(self, board):
        x, y = self._location.get_x(), self._location.get_y()
        if (
            board.get_object(Location(x - 1, y + 1)) and
            board.get_object(Location(x - 1, y - 1))
        ):
            if (board.get_object(Location(x + 2, y))):
                return True
            elif (
                board.get_object(Location(x + 1, y + 1)) and
                board.get_object(Location(x + 1, y - 1))
            ):
                return True

        elif (
            board.get_object(Location(x - 2, y)) and
            board.get_object(Location(x + 1, y - 1)) and
            board.get_object(Location(x + 1, y + 1))
        ):
            return True
        else:
            return False

    def get_next_possible_locations(self, board):
        if not board._queens_reference[self._team]:
            return []
        
        moves = []
        visited = []
        possible_moves: set[Location] = set()
        loc: Location = self.get_location()
        x, y = loc.get_x(), loc.get_y()
        
        # check if object can leave its initial position
        if(not board.checkIfvalid(loc, None)):
            return []
        
        def step_forward(current_location: Location, prev_location: Location):
            if(board.isNarrowPath(current_location, prev_location) or current_location in visited):
                return False
            
            visited.append(current_location)
            d = [(2,0),(-2,0),(1,1),(-1,1),(1,-1),(-1,-1)]
            x = current_location.get_x()
            y = current_location.get_y()
            
            # Check if current location has siblings (walking alongside the edge)
            siblings = [board.get_object(Location(x+dx, y+dy)) for dx, dy in d if board.get_object(Location(x+dx,y+dy)) is not None and board.get_object(Location(x+dx,y+dy)) is not self]
            
            if(len(siblings) == 0):
                return False
            else:
                possible_moves.add(current_location)
            
            for dx, dy in d:
                new_loc: Location = Location(x+dx,y+dy)
                if(new_loc is not prev_location):
                    if(board.get_object(new_loc) is None):
                        step_forward(new_loc, current_location)
            
        
        # start traversing
        d = [(2,0),(-2,0),(1,1),(-1,1),(1,-1),(-1,-1)]
        for (dx,dy) in d:
            newLoc: Location = Location(x+dx,y+dy)
            if(board.get_object(newLoc) is None):
                # Check if this step can be taken by the spider
                result = step_forward(newLoc, self.get_location())
            
        return list(possible_moves)
        
        
        
    
    # def get_next_possible_locations(self, board):
    #     if not board._queens_reference[self._team]:
    #         return []
    #     #TODO: Destinations that are enclosed with some patterns are not allowed,
    #     # these have to be checked yet

    #     possible_moves: set[Location] = set()
    #     loc: Location = self.get_location()
    #     x, y = loc.get_x(), loc.get_y()
        
    #     # check if object can leave its initial position
    #     if(not board.checkIfvalid(loc, None)):
    #         return []

    #     full_trap = self._check_surrounding(board)
    #     if full_trap or self._check_trapped(board):
    #         return []

    #     surrounding = [self]
    #     visited = []
    #     for piece in surrounding:
    #         if piece in visited:
    #             continue

    #         prev_location = None  
    #         x, y = piece._location.get_x(), piece._location.get_y()
    #         for dx, dy in [(1, -1), (-1, -1), (-2, 0), (-1, 1), (1, 1), (2, 0)]:
    #             new_location = Location(x + dx, y + dy)
    #             neighbour = board.get_object(new_location)
    #             if not neighbour:
    #                 if(prev_location is None):
    #                     if board.checkIfvalid(self._location, new_location):
    #                         possible_moves.add(new_location)
                                    
    #                 else:
    #                     print("narrow path?:", board.isNarrowPath(prev_location,new_location), "old loc:", prev_location, "new loc:", new_location)
    #                     if(not board.isNarrowPath(prev_location,new_location)):
    #                         if board.checkIfvalid(self._location, new_location):
    #                             possible_moves.add(new_location)
                                
    #                 prev_location = new_location
    #             else:
    #                 surrounding.append(neighbour)
    #                 prev_location = None

    #         visited.append(piece)

    #     return list(possible_moves)

    def getPossibleMoves(self, board):
        #TODO: Destinations that are enclosed with some patterns are not allowed,
        # these have to be checked yet

        possible_moves: set[Location] = set()
        x, y = self._location.get_x(), self._location.get_y()

        full_trap = self._check_surrounding(board)
        if full_trap or self._check_trapped(board):
            return []

        surrounding = [self]
        visited = []
        for piece in surrounding:
            if piece in visited:
                surrounding.remove(piece)
                continue

            x, y = piece._location.get_x(), piece._location.get_y()
            for dx, dy in [(1, -1), (-1, -1), (-2, 0), (-1, 1), (1, 1), (2, 0)]:
                new_location = Location(x + dx, y + dy)

                neighbour = board.get_object(new_location)
                if not neighbour:
                    if board.check_if_hive_valid(self._location, new_location):
                        possible_moves.add(new_location)
                else:
                    surrounding.append(neighbour)

            visited.append(piece)

        return list(possible_moves)


    def __repr__(self):
        return f"Ant at location ({self._location.get_x()}, {self._location.get_y()})"
