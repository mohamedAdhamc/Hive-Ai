from location import Location
from board import Board
from grass_hopper import Grasshopper

# Example Usage
try:
    board = Board()
    loc1 = Location(5, 10)
    grasshopper1 = Grasshopper(loc1)
    loc2 = Location(15, 20)
    grasshopper2 = Grasshopper(loc2)

    # Add game objects to the board
    board.add_object(grasshopper1)
    board.add_object(grasshopper2)
    print(board)

    # Move a game object
    board.move_object(grasshopper1.get_location(), Location(2,1))
    print("\nAfter moving grasshopper1:")
    print(board)

    # Remove a game object
    board.remove_object(grasshopper2.get_location())
    print("\nAfter removing grasshopper2:")
    print(board)
except (ValueError, KeyError) as e:
    print(e)
