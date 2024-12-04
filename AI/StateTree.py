import copy
from utils.board import Board
from utils.game_object import GameObject
from utils.location import Location

STATE_TREE_DEPTH = 4

class StateTree:

    def __init__(self, _board_state):
        self._board_state = _board_state
        self.root = StateTreeNode()

    def build_tree(self):

        nodes_to_search = [self.root]

        while (len(nodes_to_search) > 0):
            current_node = nodes_to_search.pop(0)
            current_board_state = copy.deepcopy(self._board_state)
            next_possible_moves = []

            for move in current_node.moves:
                self.play_move(current_board_state, move)

            next_possible_moves = self.get_next_moves(current_board_state)
            evaluation = self.evaluate_board(current_board_state)
            
            for move in next_possible_moves:
                node_moves = current_node.moves + [move]
                node = StateTreeNode(current_node, node_moves, evaluation, current_node.depth+1)
                current_node.children.append(node)
                if (current_node.depth < STATE_TREE_DEPTH):
                    nodes_to_search.append(node)

    def get_next_moves(self, board_state):

        if (board_state._turn_number == 0): #first move is always a piece in the middle
            return [("ant", (0, 0)), ("beetle", (0, 0)), ("grass_hopper", (0, 0)), ("spider", (0, 0)), ("queen", (0, 0))]
        
        if (board_state._turn_number == 1): # second move is always a piece next to first piece
            return [("ant", (1, 1)), ("beetle", (1, 1)), ("grass_hopper", (1, 1)), ("spider", (1, 1)), ("queen", (1, 1))]
        
        hand_pieces = []
        board_pices = []
        #loop on all hand_pieces and determine all possible locations to put them on
        #loop on all board_pices and get all possible moves for them but only if the queen is played
        return []

    def play_move(self, board, move):
        source, destination = move
        if (isinstance(source, str)):
            color = "white" if (board._turn_number % 2 == 0) else "black"
            piece = GameObject(Location(destination[0], destination[1]), color)
            Board.add_object(board, piece)
        else:
            Board.move_object(board, Location(source[0], source[1]), Location(destination[0], destination[1]))

    def evaluate_board(self, board):
        pass


class StateTreeNode:
    
    def __init__(self, parent = None, moves = [], evaluation = 0, depth = 0):
        self.evaluation = evaluation
        self.moves = moves
        self.children = []
        self.parent = parent
        self.depth = depth

    def print_tree(self):
        if self.children == []:
            print("|   " * (self.depth-1) + "|-> ", end="")
            print(self.moves[-1])
            return
        if self.depth > 0:
            print("|   " * (self.depth-1) + "|-> ", end="")
            print(self.moves[-1])
        for child in self.children:
            child.print_tree()


if __name__== '__main__':
    board = Board()
    tree = StateTree(board)
    tree.build_tree()
    tree.root.print_tree()

