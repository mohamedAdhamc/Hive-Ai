from location import Location
from board import Board
from grass_hopper import Grasshopper
from queen import Queen
from spider import Spider

# Example Usage
# try:
#     board = Board()
#     loc1 = Location(5, 10)
#     grasshopper1 = Grasshopper(loc1)
#     loc2 = Location(15, 20)
#     grasshopper2 = Grasshopper(loc2)

#     # Add game objects to the board
#     board.add_object(grasshopper1)
#     board.add_object(grasshopper2)
#     print(board)

#     # Move a game object
#     board.move_object(grasshopper1.get_location(), Location(2,1))
#     print("\nAfter moving grasshopper1:")
#     print(board)

#     # Remove a game object
#     board.remove_object(grasshopper2.get_location())
#     print("\nAfter removing grasshopper2:")
#     print(board)
# except (ValueError, KeyError) as e:
#     print(e)
    
    

# Sherif testing

try:
    board = Board()
    loc1 = Location(0, 0)
    queen1 = Queen(loc1, team=1)
    loc2 = Location(2, 0)
    grasshopper1 = Grasshopper(loc2)
    loc3 = Location(1, -1)
    grasshopper2 = Grasshopper(loc3)
    loc4 = Location(-1, 1)
    spider = Spider(loc4, team=1)
    loc5 = Location(3, 1)
    spider2 = Spider(loc5, team=1)

    # Add game objects to the board
    board.add_object(queen1)
    board.add_object(grasshopper1)
    board.add_object(grasshopper2)
    board.add_object(spider)
    board.add_object(spider2)
    # print(board.get_object(Location(2, 0)))
    # print(board)
    
    # Check possible moves
    # queen1.getPossibleMoves(board)
    queen1.getPossibleMoves(board)
    
except (ValueError, KeyError) as e:
    print(e)
