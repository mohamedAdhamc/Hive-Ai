import pygame
import copy
import time

from .hex_utils import (
    calculate_hex_dimensions,
    hexagon_vertices
)

from utils.board import Board
from utils.location import Location
from utils.pieces import Ant, Beetle, Grasshopper, Queen, Spider
from AI.state_tree import StateTree
from UI.constants import *

# Screen
WIDTH, HEIGHT = 1200, 800

# Colors
BACKGROUND = (255, 255, 255)  # Background
BLACK = (0, 0, 0)  # Black for Lines
RED = (255, 0, 0)
GRAY_COLOR = (90, 90, 90)
BEIGE_COLOR = (218, 194, 165)
CYAN_COLOR = (0, 255, 255)
HOVER_COLOR = (220, 220, 220)  # Light Grey When Hovered
CLICK_COLOR = (255, 0, 0)  # Red when clicked

# Hexagon attributes
HEX_GRID = 10  # Grid size
HEX_RADIUS = 30
MIN_HEX_RADIUS = 10
MAX_HEX_RADIUS = 80

HEX_WIDTH, HEX_HEIGHT, VERTICAL_SPACING, HORIZONTAL_SPACING = calculate_hex_dimensions(
    HEX_RADIUS)

CENTER_X = WIDTH / 2 - HEX_WIDTH / 2
CENTER_Y = HEIGHT / 2 - HEX_HEIGHT / 2

# Draw honeycomb pattern
def draw_hex_grid(rows, cols, hex_radius, offset_x=0, offset_y=0):
    hexagons = []
    for row in range(rows):
        for col in range(cols):
            # Horizontal offset
            x_offset = col * HORIZONTAL_SPACING + \
                (row % 2) * (HORIZONTAL_SPACING / 2) + offset_x
            # Vertical offset
            y_offset = row * VERTICAL_SPACING + offset_y
            hexagon = hexagon_vertices(x_offset, y_offset, hex_radius)
            # Store row and col instead of position
            hexagons.append((hexagon, (row, col)))
    return hexagons


class HiveGame:
    def __init__(self, players, players_modes, players_diff):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.hexagons = draw_hex_grid(HEX_GRID, HEX_GRID, HEX_RADIUS)
        self.offset_x = 0
        self.offset_y = 0
        self.selected_piece = [None, None]
        self.hands = []

        self.players = players
        self.players_modes = players_modes
        self.players_diff = players_diff
        self.current_player = 0

        # all rect structures are for click detection
        self.pieces_rect = []
        self.possible_selections_rect = {}
        self.next_possible_locations = []
        self.possible_deploy_locations = []
        self.piece_to_be_moved = None
        self.drawn_locations = []

        self.init_piece_holder()

        # create a board
        self.board = Board(self.win_callback, self.create_alert_window)

        self.human_move = [(None, None), (None, None)]
        self.tree = [None, None]

        if self.players[0] != PLAYER_TYPE_HUMAN:
            self.tree[0] = StateTree(self.board, 1)
            self.tree[0].build_tree(self.tree[0]._root)
        if self.players[1] != PLAYER_TYPE_HUMAN:
            self.tree[1] = StateTree(self.board, 1)
            self.tree[1].build_tree(self.tree[1]._root)

        pygame.display.set_caption("Hive Game")

    def win_callback(self, team):
        self.running = False
        won = "WHITE" if team == 0 else "BLACK"
        print(f"{won} team won")
        self.create_alert_window(f"{won} team won", 'Close')

    def check_game_events(self):
        global HEX_RADIUS, HEX_WIDTH, HEX_HEIGHT, VERTICAL_SPACING, HORIZONTAL_SPACING

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEMOTION:
                # Update the offset to drag the grid
                if event.buttons[0]:
                    self.offset_x += event.rel[0]
                    self.offset_y += event.rel[1]
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # Zoom in/out with mouse wheel
                #if event.button == 4:  # Scroll Up
                #    if HEX_RADIUS < MAX_HEX_RADIUS:
                #        HEX_RADIUS += 5  # Increase radius
                #elif event.button == 5:  # Scroll Down
                #    if HEX_RADIUS > MIN_HEX_RADIUS:
                #        HEX_RADIUS -= 5  # Decrease radius\

                # clear last mouse click event
                # self.next_possible_locations = []

                self.check_piece_hand_selection(mouse_pos)
                piece_flag = self.check_piece_click(mouse_pos)
                self.check_clicked_possible_place(mouse_pos, piece_flag)
                # self.piece_to_be_moved = None



    def prompt_ai_for_play(self):
        start_time = time.time()
        skip = False
        for child_node in self.tree[self.current_player]._root.children:
            try:
                if child_node.move == self.human_move[self.current_player - 1]:
                    child_node.move = None
                    self.tree[self.current_player]._root = child_node
                    break
            except Exception:
                pass
        else:
            build_start_time = time.time()
            self.tree[self.current_player] = StateTree(self.board, 2)
            self.tree[self.current_player].build_tree(self.tree[self.current_player]._root)
            skip = True
        # self.tree[self.current_player]._root.print_tree()

        self.tree[self.current_player]._board_state._objects = copy.deepcopy(self.board._objects)

        if not skip:
            build_start_time = time.time()
            self.tree[self.current_player]._leaves_count = 0
            self.tree[self.current_player]._depth += 2
            self.tree[self.current_player].add_level(self.tree[self.current_player]._root)

        print("leaves count: ", self.tree[self.current_player]._leaves_count)
        print("bulid time: ", time.time() - build_start_time)

        chosen_node = self.tree[self.current_player].get_best_move(self.players_modes[self.current_player], self.players_diff[self.current_player], self.current_player == 0)
        self.tree[self.current_player]._root = chosen_node
        source, destination = chosen_node.move
        destination_x = destination.get_x()
        destination_y = destination.get_y()

        # the ai is thinking
        time.sleep(1)
        if (isinstance(source, str)):
            team = 0 if (self.board._turn_number % 2 == 0) else 1
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
            Board.add_object(self.board, piece)
        else:
            Board.move_object(self.board, Location(source.get_x(), source.get_y()), Location(destination_x, destination_y))
        self.current_player = self.board._turn_number % 2
        print("total time: ", time.time() - start_time)


    def start_game_loop(self):
        global HEX_RADIUS, HEX_WIDTH, HEX_HEIGHT, VERTICAL_SPACING, HORIZONTAL_SPACING

        self.running = True
        while self.running:
            self.screen.fill(BACKGROUND)
            self.draw_possible_deploy_locations()
            self.draw_hand()

            if self.players[self.current_player] == PLAYER_TYPE_HUMAN:
                self.check_game_events()
            else:
                self.prompt_ai_for_play()

            if self.piece_to_be_moved: # highlight the piece that is selected
                pygame.draw.polygon(
                    self.screen, RED,
                    hexagon_vertices(CENTER_X + self.piece_to_be_moved._location.get_x() * HORIZONTAL_SPACING / 2, CENTER_Y + self.piece_to_be_moved._location.get_y() * VERTICAL_SPACING, HEX_RADIUS), 3
                )
                # self.piece_to_be_moved = None

            for piece in self.board._objects.values():
                x, y = piece._location.get_x(), piece._location.get_y()
                correct_x = x * HORIZONTAL_SPACING / 2
                correct_y = y * VERTICAL_SPACING

                p_width, p_height = piece.sprite.get_width(), piece.sprite.get_height()
                color = GRAY_COLOR if piece._team == 1 else BEIGE_COLOR

                # offset will be accounted for later
                # self.pieces_rect.clear()
                if(not piece.get_location() in self.drawn_locations):
                    self.pieces_rect.append((pygame.draw.polygon(
                        self.screen, color,
                        hexagon_vertices(correct_x + CENTER_X, correct_y + CENTER_Y, HEX_RADIUS)
                    ), piece))
                    self.drawn_locations.append(piece.get_location())

                pygame.draw.polygon(
                    self.screen, color,
                    hexagon_vertices(correct_x + CENTER_X, correct_y + CENTER_Y, HEX_RADIUS)
                )

                pygame.draw.polygon(
                    self.screen, BLACK,
                    hexagon_vertices(CENTER_X + correct_x, CENTER_Y + correct_y, HEX_RADIUS), 3
                )
                self.screen.blit(piece.sprite, (CENTER_X + correct_x - p_width / 2, CENTER_Y + correct_y - p_height / 2))

            self._draw_hex_from_list(CYAN_COLOR, self.next_possible_locations)

            HEX_WIDTH, HEX_HEIGHT, VERTICAL_SPACING, HORIZONTAL_SPACING = calculate_hex_dimensions(
                HEX_RADIUS
            )

            player_color = "White" if self.current_player == 0 else "Black"
            turn_text = f"Current Turn: {player_color}"
            font = pygame.font.SysFont(None, 36)
            text_surface = font.render(turn_text, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(self.screen.get_width() // 2, 20))  # 20 pixels from the top
            self.screen.blit(text_surface, text_rect)

            pygame.display.flip()

    def init_piece_holder(self):
        # two times one for yellow team one for black team and it has to
        # done this way so it does net get takon as a shallow copy
        self.hands.append([
            Ant, Ant, Ant,
            Beetle, Beetle,
            Grasshopper, Grasshopper, Grasshopper,
            Queen, Spider, Spider
        ])
        self.hands.append([
            Ant, Ant, Ant,
            Beetle, Beetle,
            Grasshopper, Grasshopper, Grasshopper,
            Queen, Spider, Spider
        ])
        self.piece_rects = []

        # I got them by trial and error so don't ask me
        self.holder_width = WIDTH * 3/4 + 20
        self.holder_height = HEIGHT * 1/4 + 10
        self.pieces_holder_border = pygame.rect.Rect((WIDTH * 3/4, HEIGHT * 1/4), (WIDTH * 1/4 + 5, 125))
        self.pieces_holder = pygame.rect.Rect((WIDTH * 3/4 + 5, HEIGHT * 1/4 + 5), (WIDTH * 1/4, 125 - 10))

        # one collision detection box work for both players
        for index, piece in enumerate(self.hands[0]):
            x = self.holder_width + (index % 4 * 40)
            y = self.holder_height + (index // 4) * 35
            self.piece_rects.append(piece.sprite.get_rect().move(x, y))


    def draw_hand(self):
        weird_brown_color = (210, 189, 150)
        pygame.draw.rect(self.screen, (10, 10, 10), self.pieces_holder_border, border_radius = 5)
        pygame.draw.rect(self.screen, weird_brown_color, self.pieces_holder, border_radius = 5)

        team = self.board._turn_number % 2
        for index, piece in enumerate(self.hands[team]):
            if not piece:
                continue

            x = self.holder_width + (index % 4 * 40)
            y = self.holder_height + (index // 4) * 35
            self.screen.blit(piece.sprite, (x, y))

    def draw_possible_deploy_locations(self):
        if self.selected_piece[0]:
            team = self.board._turn_number % 2
            self._draw_hex_from_list(CYAN_COLOR, self.board.getPossibleDeployLocations(team))

    def check_piece_click(self, mouse_pos):
        # stop if there is a turn currently being played
        # if self.next_possible_locations:
            # return

        # stop any movement if queen has not yet been played
        if not self.board._queens_reference[self.board.turn()]:
            return

        piece_flag = False
        print("pieces rect: ", self.pieces_rect)
        for piece_hex, piece in self.pieces_rect:
            # print("hex: ",piece_hex, "piece:", piece)
            if piece_hex.scale_by(0.8).collidepoint(mouse_pos):
                piece_flag = True
                team = self.board._turn_number % 2
                if team == piece._team:
                    # add the current location as the first element so when moving the piece
                    # it can be easily selected
                    # update next possible locations and piece to be moved
                    self.piece_to_be_moved = piece
                    self.next_possible_locations = list(piece.get_next_possible_locations(self.board))
                    # self.next_possible_locations.extend(piece.get_next_possible_locations(self.board))
                    break

        return piece_flag


    def check_clicked_possible_place(self, mouse_pos, piece_flag):
        possible_new_place_flag = False
        for location, rect in self.possible_selections_rect.items():
            if rect.collidepoint(mouse_pos):
                possible_new_place_flag = True
                piece_class, piece_index = self.selected_piece[0], self.selected_piece[1]

                if piece_class:
                    self.human_move[self.current_player] = (piece_class.__name__, location)
                    team = self.board._turn_number % 2
                    piece = piece_class(location, team)
                    self.board.add_object(piece)
                    self.hands[team][piece_index] = None
                    self.selected_piece = [None, None]
                    break
                else:
                    self.human_move[self.current_player] = (self.piece_to_be_moved._location, location)
                    old_location = self.piece_to_be_moved.get_location()
                    self.board.move_object(self.piece_to_be_moved._location, location)
                    self.next_possible_locations.clear()
                    # clear the pieces rect
                    self.pieces_rect.clear()
                    print("Old location:", old_location)
                    self.drawn_locations.clear()
                    self.piece_to_be_moved = None

        # while clearing after every fram is not the most optimum
        # but it is the simplest and what works for now
        self.possible_selections_rect.clear()
        self.current_player = self.board._turn_number % 2

        if(possible_new_place_flag == False and not piece_flag):
            self.next_possible_locations.clear()
            self.piece_to_be_moved = None


    def check_piece_hand_selection(self, mouse_pos):
        team = self.board._turn_number % 2
        hand_selection_flag = False
        for index, (piece_rect, piece) in enumerate(zip(self.piece_rects, self.hands[team])):
            if not piece:
                continue

            if piece_rect.collidepoint(mouse_pos):
                hand_selection_flag = True
                self.selected_piece = [piece, index]

        if(hand_selection_flag):
           self.next_possible_locations = []
           self.piece_to_be_moved = None

    def _draw_hex_from_list(self, color, hex_list):
        for location in hex_list:
            x, y = location.get_x(), location.get_y()
            self.possible_selections_rect[location] = pygame.draw.polygon(
                self.screen, color,
                hexagon_vertices(CENTER_X + x * HORIZONTAL_SPACING / 2, CENTER_Y + y * VERTICAL_SPACING, HEX_RADIUS)
            )
            pygame.draw.polygon(
                self.screen, BLACK,
                hexagon_vertices(CENTER_X + x * HORIZONTAL_SPACING / 2, CENTER_Y + y * VERTICAL_SPACING, HEX_RADIUS), 3
            )

    def create_alert_window(self, message, btn_string):
        padding = 20  # Padding around text and button
        button_height = 30
        button_width = 100
        line_spacing = 5

        font = pygame.font.Font(None, 28)

        # Split the message into lines that fit within the screen width
        words = message.split(' ')
        lines = []
        current_line = ""
        for word in words:
            test_line = f"{current_line} {word}".strip()
            test_surface = font.render(test_line, True, (0, 0, 0))
            if test_surface.get_width() <= self.screen.get_width() - 2 * padding:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        if current_line:
            lines.append(current_line)

        # Calculate alert dimensions based on text and button size
        text_width = max(font.render(line, True, (0, 0, 0)).get_width() for line in lines)
        text_height = sum(font.render(line, True, (0, 0, 0)).get_height() for line in lines) + (len(lines) - 1) * line_spacing
        alert_width = max(text_width, button_width) + 2 * padding
        alert_height = text_height + button_height + 3 * padding

        # Position the alert at the top of the screen
        alert_x = (self.screen.get_width() - alert_width) // 2
        alert_y = (self.screen.get_height() - alert_height) // 2  # Fixed distance from the top of the window

        # Create alert surface
        alert_surface = pygame.Surface((alert_width, alert_height))
        alert_surface.fill((230, 230, 230))

        # Render text centered horizontally and placed vertically within the alert
        text_y = padding
        for line in lines:
            text_surface = font.render(line, True, (0, 0, 0))
            text_rect = text_surface.get_rect(center=(alert_width // 2, text_y + text_surface.get_height() // 2))
            alert_surface.blit(text_surface, text_rect)
            text_y += text_surface.get_height() + line_spacing

        # Create button
        button_x = (alert_width - button_width) // 2
        button_y = alert_height - button_height - padding
        button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

        # Render button text
        button_text = font.render(btn_string, True, (0, 0, 0))
        button_text_rect = button_text.get_rect(center=button_rect.center)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    adjusted_pos = (mouse_pos[0] - alert_x, mouse_pos[1] - alert_y)

                    if button_rect.collidepoint(adjusted_pos):
                        return

            self.screen.blit(alert_surface, (alert_x, alert_y))

            # Draw button
            pygame.draw.rect(alert_surface, (200, 200, 200), button_rect)
            pygame.draw.rect(alert_surface, (0, 0, 0), button_rect, 2)
            alert_surface.blit(button_text, button_text_rect)

            pygame.display.flip()
