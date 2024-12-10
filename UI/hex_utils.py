import math


def calculate_hex_dimensions(radius):
    """Recalculate hexagon dimensions based on the radius."""
    hex_width = math.sqrt(3) * radius  # Width
    hex_height = 2 * radius  # Height
    # Vertical and horizontal spacing for hex pattern
    vertical_spacing = hex_height * 3 / 4
    horizontal_spacing = hex_width
    return hex_width, hex_height, vertical_spacing, horizontal_spacing

def hexagon_vertices(x, y, radius):
    vertices = []
    for i in range(6):
        angle = math.radians(60 * i - 30)
        vertex_x = x + radius * math.cos(angle)
        vertex_y = y + radius * math.sin(angle)
        vertices.append((vertex_x, vertex_y))
    return vertices

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
