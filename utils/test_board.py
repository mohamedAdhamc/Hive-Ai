from location import Location
from board import Board
from grass_hopper import Grasshopper
from spider import Spider
from ant import Ant
from queen import Queen
from beetle import Beetle

def test_hive_broken():
    print("---------------------Testing Hive breaking move--------------------")
    board = Board()
    locations = [
            Location(0, 0), Location(2, 0), Location(1, 1),
            Location(2, 2), Location(0, 2)
    ]
    
    for location in locations:
        insect = Grasshopper(location, 0)
        board.add_object(insect)

    if board.check_if_hive_valid(locations[0], Location(3, 3)):
        print("Hive is valid after move")
    else:
        print("Invalid move will break hive")

def test_ant_movement():
    print("---------------------testing ant movement---------------------------")
    board = Board()
    locations = [
            Location(0, 0), Location(2, 0), Location(1, 1),
            Location(2, 2), Location(0, 2)
    ]
    
    queen = Queen(locations[0], 0)
    board.add_object(queen)
    
    for location in locations[1:]:
        namla = Ant(location, 0)
        board.add_object(namla)

    print(board.get_object(locations[-1]).get_next_possible_locations(board))

def test_beetle_movement():
    print("---------------------testing beetle movement---------------------------")
    board = Board()
    locations = [
            Location(0, 0), Location(2, 0), Location(1, 1),
            Location(2, 2), Location(0, 2)
    ]
    
    queen = Queen(locations[0], 0)
    board.add_object(queen)
    
    for location in locations[1:]:
        beetle = Beetle(location, 0)
        board.add_object(beetle)
    
    print("Possible locations for beetle:")
    print(board.get_object(locations[-1]).get_next_possible_locations(board))


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
    #test_hive_broken()
    # test_ant_movement()
    # test_beetle_movement()
    board = Board()
    loc1 = Location(0, 0)
    queen1 = Queen(loc1, team=1)
    loc2 = Location(2, 0)
    grasshopper1 = Grasshopper(loc2, team=1)
    loc3 = Location(1, -1)
    grasshopper2 = Grasshopper(loc3, 1)
    loc4 = Location(-1, 1)
    spider = Spider(loc4, team=1)
    loc5 = Location(3, 1)
    spider2 = Spider(loc5, team=2)
    loc6 = Location(1, 3)
    queen2 = Queen(loc6, team=2)
    # loc7 = Location(1, 3)
    # spider3 = Spider(loc7, team=2)

    board.initiate_game()

    # Add game objects to the board
    board.add_object(queen1)
    board.add_object(grasshopper1)
    board.add_object(grasshopper2)
    board.add_object(spider)
    # board.add_object(spider2)
    # board.add_object(queen2)
    # print(board.get_object(Location(2, 0)))
    # print(board)
    deploy1 = board.getPossibleDeployLocations(2)
    print(deploy1)
    # Check possible moves
    # queen1.getPossibleMoves(board)
    # queen1.getPossibleMoves(board)
    
except (ValueError, KeyError) as e:
    print(e)

