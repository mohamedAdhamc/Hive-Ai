from board import Board
from game_object import GameObject
from location import Location
from state_tree_node import StateTreeNode
from algorithms import apply_minmax, apply_alphabeta, iterative_depening

class StateTree:

    def __init__(self, _board_state, _depth):
        self._board_state = _board_state
        self._depth = _depth
        self._root = StateTreeNode()

    def build_tree(self, node):
        if node.move:
            self.play_move(node.move)
        
        next_possible_moves = self.get_next_moves(self._board_state)
        for move in next_possible_moves:
            child_node = StateTreeNode(node, move, 0, node.depth+1)
            node.children.append(child_node)
            if (node.depth < self._depth - 1):
                self.build_tree(child_node)
            else:
                child_node.evaluation = self.evaluate_board()
        
        if node.move:
            self.reverse_move(node.move)

    def add_level(self, node):
        if node.move:
            self.play_move(node.move)
        
        if (node.depth < self._depth):
            node.evaluation = 0
            for child_node in node.children:
                self.add_level(child_node)
        else:
            node.evaluation = 0
            next_possible_moves = self.get_next_moves(self._board_state)
            for move in next_possible_moves:
                child_node = StateTreeNode(node, move, self.evaluate_board(), node.depth+1)
                node.children.append(child_node)

        if node.move:
            self.reverse_move(node.move)

    def play_move(self, move):
        source, destination = move
        if (isinstance(source, str)):
            color = "white" if (self._board_state._turn_number % 2 == 0) else "black"
            piece = GameObject(Location(destination[0], destination[1]), color)
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
        return 5

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

    @staticmethod
    def build_test_tree():
        values = [-50, 21, -21, -17, -35, 24, 36, -30, -17, 16, 12, -24, 43, -24, -4, 35, -49, -47, -2, 13, 22, -47, 5, 26, -8, 25, -2]
        board = Board()
        tree = StateTree(board)
        tree._root.depth = 0 
        tree._root.move = 'a0'
        child1 = StateTreeNode(tree._root, 'b1', 0, 1)
        child2 = StateTreeNode(tree._root, 'b2', 0, 1)
        child3 = StateTreeNode(tree._root, 'b3', 0, 1)
        tree._root.children = [child1, child2, child3]
        i = 0
        for child in tree._root.children:
            child1 = StateTreeNode(child, 'c' + str(3*i+1), 0, 2)
            child2 = StateTreeNode(child, 'c' + str(3*i+2), 0, 2)
            child3 = StateTreeNode(child, 'c' + str(3*i+3), 0, 2)
            child.children = [child1, child2, child3]
            j = 0
            for subchild in child.children:
                child1 = StateTreeNode(subchild, 'd' + str(9*i+3*j+1), values[9*i+3*j], 3)
                child2 = StateTreeNode(subchild, 'd' + str(9*i+3*j+2), values[9*i+3*j+1], 3)
                child3 = StateTreeNode(subchild, 'd' + str(9*i+3*j+3), values[9*i+3*j+2], 3)
                subchild.children = [child1, child2, child3]
                j += 1
            i += 1
        return tree._root

if __name__== '__main__':
    board = Board()
    tree = StateTree(board, 1)
    tree.build_tree(tree._root)
    print(tree.get_best_move("iterative", 0.001))
    # tree._root.print_tree()
    # tree.add_level(tree._root)
    # tree._root.print_tree()

    # this is how to instantiate the test tree that have a result of 21
    # root = StateTree.build_test_tree()
    # root.print_tree()
    