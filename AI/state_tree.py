from utils.board import Board
from utils.pieces.queen import Queen
from utils.pieces.ant import Ant
from utils.pieces.grass_hopper import Grasshopper
from utils.pieces.beetle import Beetle
from utils.pieces.spider import Spider
from utils.location import Location
from UI.constants import *
from .state_tree_node import StateTreeNode
from .algorithms import apply_minmax, apply_alphabeta, iterative_depening
from random import randint

class StateTree:

    def __init__(self, _board_state, _depth, difficulty = PLAYER_DIFFICULTY_EASY):
        self._board_state = _board_state
        self._depth = _depth
        self._root = StateTreeNode()
        self._leaves_count = 0
        self.difficulty = difficulty
        self.time = 1
        if self.difficulty == PLAYER_DIFFICULTY_MEDIUM:
            self.time = 5
        elif self.difficulty == PLAYER_DIFFICULTY_HARD:
            self.time = 10

    def build_tree(self, node):
        if node.move:
            self.play_move(node.move)

        if (node.depth == self._depth):
            node.evaluation = self.evaluate_board()
        else:
            next_possible_moves = self._board_state.get_moves_and_deploys()
            if not next_possible_moves:
                node.evaluation = self.evaluate_board()
            else:
                for move in next_possible_moves:
                    child_node = StateTreeNode(node, move, 0, node.depth + 1)
                    node.children.append(child_node)
                    self.build_tree(child_node)

        if node.move:
            self.reverse_move(node.move)

        # if (node.depth == self._depth):
        #     node.evaluation = self.evaluate_board()
        #     return

        # next_possible_moves = self._board_state.get_moves_and_deploys()

        # if not next_possible_moves:
        #     node.evaluation = self.evaluate_board()
        #     return

        # for move in next_possible_moves:
        #     next_board_state = self.play_move(node.board, move)
        #     child_node = StateTreeNode(node, move, 0, node.depth + 1, next_board_state)
        #     node.children.append(child_node)
        #     self.build_tree(child_node)

    def add_level(self, node, i = 2):
        if node.move:
            self.play_move(node.move)

        if (node.depth == self._depth):
            node.evaluation = self.evaluate_board()
        else:
            if (node.depth < self._depth - i):
                if node.children:
                    node.evaluation = 0
                    for child_node in node.children:
                        self.add_level(child_node)
            else:
                next_possible_moves = self._board_state.get_moves_and_deploys()
                evaluation = self.evaluate_board()
                if node != self._root and (not next_possible_moves or evaluation <= 0):
                    node.evaluation = evaluation
                else:
                    node.evaluation = 0
                    for move in next_possible_moves:
                        child_node = StateTreeNode(node, move, 0, node.depth + 1)
                        node.children.append(child_node)
                        self.add_level(child_node)

        if node.move:
            self.reverse_move(node.move)

        # self._root.move = None
        # nodes = [self._root]

        # while nodes:
        #     node = nodes.pop()
        #     if node.move:
        #         for _ in range(i):
        #             node.move.pop(0)
        #         for move in node.move:
        #             self.play_move(move)

        #     if (node.depth == self._depth):
        #         node.evaluation = self.evaluate_board()
        #     else:
        #         if (node.depth < self._depth - 2):
        #             if node.children:
        #                 node.evaluation = 0
        #                 for child_node in node.children:
        #                     nodes.append(child_node)
        #         else:
        #             next_possible_moves = self._board_state.get_moves_and_deploys()
        #             if not next_possible_moves:
        #                 node.evaluation = self.evaluate_board()
        #             else:
        #                 node.evaluation = 0
        #                 for move in next_possible_moves:
        #                     child_node = StateTreeNode(node, node.move + [move], 0, node.depth + 1)
        #                     node.children.append(child_node)
        #                     nodes.append(child_node)

        #     if node.move:
        #         for move in node.move:
        #             self.reverse_move(move)

    def play_move(self, move):
        source, destination = move
        destination_x = destination.get_x()
        destination_y = destination.get_y()
        if (isinstance(source, str)):
            team = 0 if (self._board_state._turn_number % 2 == 0) else 1
            if source == "Queen":
                piece = Queen(Location(destination_x, destination_y), team)
            elif source == "Ant":
                piece = Ant(Location(destination_x, destination_y), team)
            elif source == "Beetle":
                piece = Beetle(Location(destination_x, destination_y), team)
            elif source == "Grasshopper":
                piece = Grasshopper(Location(destination_x, destination_y), team)
            elif source == "Spider":
                piece = Spider(Location(destination_x, destination_y), team)
            Board.add_object(self._board_state, piece, True)
        else:
            Board.move_object(self._board_state, Location(source.get_x(), source.get_y()), Location(destination_x, destination_y), True)

    def reverse_move(self, move):
        destination, source = move
        self._board_state._turn_number -= 1
        if (isinstance(destination, str)):
            Board.remove_object(self._board_state, Location(source.get_x(), source.get_y()))
        else:
            self._board_state._turn_number -= 1
            Board.move_object(self._board_state, Location(source.get_x(), source.get_y()), Location(destination.get_x(), destination.get_y()), True)

    def find_distance_to_queen(self, piece_location, queen_location):
        place_values = [20, 12, 5, 2, 1, 0]

        y_distance = abs(queen_location.get_y() - piece_location.get_y())
        distance_to_queen = (abs(queen_location.get_x() - piece_location.get_x())) + y_distance
        index = max(distance_to_queen//2, y_distance) - 1

        if distance_to_queen == 0:
            return place_values[1]
        elif index < len(place_values):
            return place_values[index]
        else:
            return place_values[-1]


    def evaluate_board(self):
        self._leaves_count += 1
        piece_values = {
            "Queen": 10,
            "Ant": 8,
            "Beetle": 5,
            "Grasshopper": 3,
            "Spider": 2
        }

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

        if self._board_state._turn_number < 8:
            return randint(-100, 3)

        win_condition = self._board_state.check_win_condition_bool()
        if win_condition == 1:
            return float('inf')
        elif win_condition == -1:
            return float('-inf')

        queen_surrounded_score = 0
        d = [(2,0),(-2,0),(1,1),(-1,1),(1,-1),(-1,-1)]
        i = -1
        for queen in self._board_state._queens_reference:
            x = queen._location.get_x()
            y = queen._location.get_y()
            for (dx,dy) in d:
                new_location: Location = Location(x + dx, y + dy)
                if(self._board_state.get_object(new_location)):
                    queen_surrounded_score += i
            i = 1

        pieces_movement_score = 0
        for location, piece in list(self._board_state._objects.items()):
            if self.difficulty == PLAYER_DIFFICULTY_HARD:
                moves = piece.get_next_possible_locations(self._board_state)
                piece_value = piece_values[piece.__class__.__name__]
                for move in moves:
                    if piece._team == 0:
                        pieces_movement_score += piece_value * self.find_distance_to_queen(move, self._board_state._queens_reference[1]._location)
                    elif piece._team == 1:
                        pieces_movement_score -= piece_value * self.find_distance_to_queen(move, self._board_state._queens_reference[0]._location)
            else:
                piece_value = piece_values[piece.__class__.__name__]
                if piece._team == 0:
                    pieces_movement_score += piece_value * self.find_distance_to_queen(location, self._board_state._queens_reference[1]._location)
                elif piece._team == 1:
                    pieces_movement_score -= piece_value * self.find_distance_to_queen(location, self._board_state._queens_reference[0]._location)

        score = pieces_movement_score + 1000 * queen_surrounded_score
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


    def get_best_move(self, algorithm_type, max_min = True):
        if algorithm_type == AI_MODE_MINMAX:
            result = apply_minmax(self._depth, max_min, self._root)
        elif algorithm_type == AI_MODE_ALPHA_BETA:
            result = apply_alphabeta(self._depth, max_min, self._root)
        elif algorithm_type == AI_MODE_ITERATIVE:
            result = iterative_depening(self.time, max_min, self)
        for child in self._root.children:
            if result == child.evaluation:
                return child

if __name__== '__main__':
    board = Board()
    tree = StateTree(board, 1)
    tree.build_tree(tree._root)

    # tree.evaluate_board()
