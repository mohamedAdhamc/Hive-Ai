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
        #TODO: Destinations that are enclosed with some patterns are not allowed,
        # these have to be checked yet

        possible_moves: set[Location] = set()
        loc: Location = self.get_location()
        x, y = loc.get_x(), loc.get_y()
        
        # check if object can leave its initial position
        if(not board.checkIfvalid(loc, None)):
            return []

        full_trap = self._check_surrounding(board)
        if full_trap or self._check_trapped(board):
            return []

        surrounding = [self]
        visited = []
        for piece in surrounding:
            if piece in visited:
                continue

            x, y = piece._location.get_x(), piece._location.get_y()
            for dx, dy in [(1, -1), (-1, -1), (-2, 0), (-1, 1), (1, 1), (2, 0)]:
                new_location = Location(x + dx, y + dy)

                neighbour = board.get_object(new_location)
                if not neighbour:
                    if(not board.isNarrowPath(self.get_location(),new_location)):
                        if board.checkIfvalid(self._location, new_location):
                            possible_moves.add(new_location)
                else:
                    surrounding.append(neighbour)

            visited.append(piece)

        return list(possible_moves)
    
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
