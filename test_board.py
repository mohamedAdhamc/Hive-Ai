from utils.location import Location
from utils.board import Board
from utils.pieces.grass_hopper import Grasshopper
from utils.pieces.spider import Spider
from utils.pieces.ant import Ant
from utils.pieces.queen import Queen
from utils.pieces.beetle import Beetle

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

def get_moves_for_team(board):
    # Get the team pieces using the filter function
    team_pieces = board.filter_team_pieces()
    print("team pieces:", team_pieces)
    move_pairs = []
    moves = {}
    
    # Iterate through each piece in team_pieces
    for start_location, piece in team_pieces.items():
        # Get possible destination locations for this piece
        possible_destinations = piece.get_next_possible_locations(board)
        moves[piece] = []
        
        # Add each destination as a pair of start and destination to the result list
        for destination in possible_destinations:
            moves[piece].append(destination)
            # move_pairs.append([start_location, destination])
    
        print("piece:", piece, moves[piece])
    # return move_pairs
    return moves

try:
    #test_hive_broken()
    # test_ant_movement()
    # test_beetle_movement()
    board = Board(lambda x: x)
    loc1 = Location(0, 0)
    queen1 = Queen(loc1, 0)
    loc7 = Location(1, 1)
    Queen2 = Queen(loc7, 1)
    loc8 = Location(2, 0)
    Ant1 = Ant(loc8, 0)
    loc9 = Location(3, 1)
    grasshopper = Grasshopper(loc9, 0)
    # Ant2 = Ant(loc9, team=2)

    # board.initiate_game()

    # Add game objects to the board
    board.add_object(queen1)
    board.add_object(Queen2)
    board.add_object(Ant1)
    board.add_object(grasshopper)
    print("Board:", board)
    # print(Queen2.get_next_possible_locations(board))

    # print(board.get_object(Location(2, 0)))
    # print(board)
    # deploy1 = board.getPossibleDeployLocations(2)
    # print("deploy for team 1",deploy1)
    # print(board)
    # Check possible moves
    #queen2.getPossibleMoves(board)
    # queen1.getPossibleMoves(board)
    print(get_moves_for_team(board))
    
except (ValueError, KeyError) as e:
    print(e)

