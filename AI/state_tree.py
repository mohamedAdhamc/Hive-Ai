from utils.board import Board
from utils.pieces.queen import Queen
from utils.pieces.ant import Ant
from utils.pieces.grass_hopper import Grasshopper
from utils.pieces.beetle import Beetle
from utils.pieces.spider import Spider
from utils.location import Location
from .state_tree_node import StateTreeNode
from .algorithms import apply_minmax, apply_alphabeta, iterative_depening

class StateTree:

    def __init__(self, _board_state, _depth):
        self._board_state = _board_state
        self._depth = _depth
        self._root = StateTreeNode()

    def build_tree(self, node):
        if node.move:
            self.play_move(node.move)
        
        if (node.depth == self._depth):
            node.evaluation = self.evaluate_board()
        else:
            next_possible_moves = self.get_next_moves(self._board_state)
            if not next_possible_moves:
                node.evaluation = self.evaluate_board()
            else:
                for move in next_possible_moves:
                    child_node = StateTreeNode(node, move, 0, node.depth + 1)
                    node.children.append(child_node)
                    self.build_tree(child_node)
        
        if node.move:
            self.reverse_move(node.move)

    def add_level(self, node):
        if node.move:
            self.play_move(node.move)
        
        if (node.depth < self._depth and node.children):
            node.evaluation = 0
            for child_node in node.children:
                self.add_level(child_node)
        else:
            node.evaluation = 0
            next_possible_moves = self.get_next_moves(self._board_state)
            for move in next_possible_moves:
                self.play_move(move)
                child_node = StateTreeNode(node, move, self.evaluate_board(), node.depth + 1)
                self.reverse_move(node.move)
                node.children.append(child_node)

        if node.move:
            self.reverse_move(node.move)

    def play_move(self, move):
        source, destination = move
        if (isinstance(source, str)):
            team = 0 if (self._board_state._turn_number % 2 == 0) else 1
            if source == "queen":
                piece = Queen(Location(destination[0], destination[1]), team)
            elif source == "ant":
                piece = Ant(Location(destination[0], destination[1]), team)
            elif source == "beetle":
                piece = Beetle(Location(destination[0], destination[1]), team)
            elif source == "grasshopper":
                piece = Grasshopper(Location(destination[0], destination[1]), team)
            elif source == "spider":
                piece = Spider(Location(destination[0], destination[1]), team)
            Board.add_object(self._board_state, piece)
        else:
            Board.move_object(self._board_state, Location(source[0], source[1]), Location(destination[0], destination[1]))

    def reverse_move(self, move):
        destination, source = move
        self._board_state._turn_number -= 1
        if (isinstance(destination, str)):
            Board.remove_object(self._board_state, Location(source[0], source[1]))
        else:
            self._board_state._turn_number -= 1
            Board.move_object(self._board_state, Location(destination[0], destination[1]), Location(source[0], source[1]))

    def evaluate_board(self):
        piece_values = {
            "Queen": 100,
            "Ant": 45,
            "Beetle": 30,
            "Grasshopper": 20,
            "Spider": 15
        }
        place_values = [100, 80, 60, 40, 20, 0]

        # self.play_move(("queen", (0,0)))
        # self.play_move(("grasshopper", (-1,-1)))
        # self.play_move(("grasshopper", (-2,-2)))
        # self.play_move(("queen", (-1,-3)))
        # self.play_move(("spider", (1,-1)))
        # self.play_move(("beetle", (2,0)))
        # self.play_move(("ant", (2,-2)))
        # self.play_move(("spider", (3,1)))
        # self.play_move(("spider", (2,2)))
        # self.play_move(("spider", (0,2)))
        # self.play_move(("beetle", (-3,-1)))
        # self.play_move(("ant", (1,-3)))

        for location, piece in self._board_state._objects.items():
            if isinstance(piece, Queen):
                if piece._team == 0:
                    white_queen_location = location
                elif piece._team == 1:
                    black_queen_location = location

        def find_distance_to_queen(piece_location, queen_location):
            y_distance = abs(queen_location.y - piece_location.y)
            distance_to_queen = (abs(queen_location.x - piece_location.x)) + y_distance
            index = max(distance_to_queen//2, y_distance) - 1
            
            if distance_to_queen == 0:
                return place_values[1]
            elif index < len(place_values):
                return place_values[index]
            else:
                return place_values[-1]
        
        score = 0
        for location, piece in self._board_state._objects.items():
            moves = piece.get_next_possible_locations(self._board_state)
            piece_value = piece_values[piece.__class__.__name__]
            for move in moves:
                if piece._team == 0:
                    score += piece_value * find_distance_to_queen(move, black_queen_location)
                elif piece._team == 1:
                    score -= piece_value * find_distance_to_queen(move, white_queen_location)

        return score

    def get_next_moves(self, board_state):

        if (board_state._turn_number == 0): #first move is always a piece in the middle
            return [("ant", (0, 0)), ("beetle", (0, 0)), ("grasshopper", (0, 0)), ("spider", (0, 0)), ("queen", (0, 0))]
        
        if (board_state._turn_number == 1): # second move is always a piece next to first piece
            return [("ant", (1, 1)), ("beetle", (1, 1)), ("grasshopper", (1, 1)), ("spider", (1, 1)), ("queen", (1, 1))]
        
        hand_pieces = []
        board_pices = []
        #loop on all hand_pieces and determine all possible locations to put them on
        #loop on all board_pices and get all possible moves for them but only if the queen is played
        return []
    
    
    def get_best_move(self, algorithm_type, time = 0, max_min = True):
        if algorithm_type == "min-max":
            result = apply_minmax(self._depth, max_min, self._root)
        elif algorithm_type == "alpha-beta":
            result = apply_alphabeta(self._depth, max_min, self._root)
        elif algorithm_type == "iterative":
            result = iterative_depening(time, max_min, self)
        for child in self._root.children:
            if result == child.evaluation:
                return child.move

if __name__== '__main__':
    board = Board()
    tree = StateTree(board, 1)
    tree.build_tree(tree._root)
    print(tree.get_best_move("iterative", 0.001))
    
    # tree.evaluate_board()
