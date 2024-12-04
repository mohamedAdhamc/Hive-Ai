import pygame
import math

pygame.init()

# Screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hive Game")

# Colors
BACKGROUND = (255, 255, 255)  # Background
BLACK = (0, 0, 0)  # Black for Lines
HOVER_COLOR = (220, 220, 220)  # Light Grey When Hovered
CLICK_COLOR = (255, 0, 0)  # Red when clicked

# Hexagon attributes
HEX_GRID = 10  # Grid size
HEX_RADIUS = 30
MIN_HEX_RADIUS = 10
MAX_HEX_RADIUS = 80

def calculate_hex_dimensions(radius):
    """Recalculate hexagon dimensions based on the radius."""
    hex_width = math.sqrt(3) * radius  # Width
    hex_height = 2 * radius  # Height
    # Vertical and horizontal spacing for hex pattern
    vertical_spacing = hex_height * 3 / 4  
    horizontal_spacing = hex_width  
    return hex_width, hex_height, vertical_spacing, horizontal_spacing

HEX_WIDTH, HEX_HEIGHT, VERTICAL_SPACING, HORIZONTAL_SPACING = calculate_hex_dimensions(HEX_RADIUS)

# Vertices of a hexagon
def hexagon_vertices(x, y, radius):
    vertices = []
    for i in range(6):
        angle = math.radians(60 * i - 30)
        vertex_x = x + radius * math.cos(angle)
        vertex_y = y + radius * math.sin(angle)
        vertices.append((vertex_x, vertex_y))
    return vertices

# Draw honeycomb pattern
def draw_hex_grid(rows, cols, hex_radius, offset_x=0, offset_y=0):
    hexagons = []
    for row in range(rows):
        for col in range(cols):
            # Horizontal offset
            x_offset = col * HORIZONTAL_SPACING + (row % 2) * (HORIZONTAL_SPACING / 2) + offset_x
            # Vertical offset
            y_offset = row * VERTICAL_SPACING + offset_y
            hexagon = hexagon_vertices(x_offset, y_offset, hex_radius)
            hexagons.append((hexagon, (row, col)))  # Store row and col instead of position
    return hexagons

# Check for click inside
def point_in_hexagon(px, py, hexagon):
    n = len(hexagon)
    inside = False
    x, y = px, py
    p1x, p1y = hexagon[0]
    for i in range(n + 1):
        p2x, p2y = hexagon[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside

def main():
    global HEX_RADIUS, HEX_WIDTH, HEX_HEIGHT, VERTICAL_SPACING, HORIZONTAL_SPACING
    running = True

    # Track states of hexes row and col
    hex_states = {}

    hexagons = draw_hex_grid(HEX_GRID, HEX_GRID, HEX_RADIUS)  # Choose grid size and hex size
    offset_x, offset_y = 0, 0  # Offset for dragging the grid

    clicked_this_frame = False  # Flag to track if click is processed yet

    while running:
        screen.fill(BACKGROUND)

        # Mouse 
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        # Hovering and clicking
        for hexagon, (row, col) in hexagons:
            hex_key = (row, col)  # Use grid indices 
            if point_in_hexagon(mouse_pos[0], mouse_pos[1], hexagon):
                pygame.draw.polygon(screen, HOVER_COLOR, hexagon)  # Highlight on hovering
                pygame.draw.polygon(screen, BLACK, hexagon, 2)  # Black outline
                if mouse_pressed[0] and not clicked_this_frame:  # Left mouse click and not processed yet
                    # If it was not clicked before, color it and store the state
                    if hex_key not in hex_states:
                        hex_states[hex_key] = CLICK_COLOR  # red
                    pygame.draw.polygon(screen, hex_states[hex_key], hexagon)  # Fill with stored color in state
                    pygame.draw.polygon(screen, BLACK, hexagon, 2)  # Black outline
                    print(f"Hexagon clicked at ({row}, {col})")
                    clicked_this_frame = True  # processed
            else:
                # Draw the hexagon with its current state (color)
                if hex_key in hex_states:
                    pygame.draw.polygon(screen, hex_states[hex_key], hexagon)  # Use the stored colors
                else:
                    pygame.draw.polygon(screen, BACKGROUND, hexagon)  # Default white color
                pygame.draw.polygon(screen, BLACK, hexagon, 2)  # Black outline

        # Reset flag
        if not mouse_pressed[0]:
            clicked_this_frame = False

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEMOTION:
                # Update the offset to drag the grid
                if event.buttons[0]:
                    offset_x += event.rel[0]
                    offset_y += event.rel[1]
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Zoom in/out with mouse wheel
                if event.button == 4:  # Scroll Up
                    if HEX_RADIUS < MAX_HEX_RADIUS:
                        HEX_RADIUS += 5  # Increase radius
                elif event.button == 5:  # Scroll Down
                    if HEX_RADIUS > MIN_HEX_RADIUS:
                        HEX_RADIUS -= 5  # Decrease radius

        # Recalculate hexagon dimensions
        HEX_WIDTH, HEX_HEIGHT, VERTICAL_SPACING, HORIZONTAL_SPACING = calculate_hex_dimensions(HEX_RADIUS)

        # Redraw grid with new offset
        hexagons = draw_hex_grid(HEX_GRID, HEX_GRID, HEX_RADIUS, offset_x, offset_y)

        pygame.display.flip()

# Run
if __name__ == "__main__":
    main()

pygame.quit()
