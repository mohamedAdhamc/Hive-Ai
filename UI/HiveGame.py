import pygame
import math

pygame.init()

#Screen
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Hive Game")

#Colors
BACKGROUND = (255, 223, 85) #Honeycomb Golden Background
BLACK = (0, 0, 0)   #Black for Lines
HOVER_COLOR = (220, 220, 220)  #Light Grey When Hovered
CLICK_COLOR = (255, 0, 0)  #Red when clicked

#Hexagon attributes
HEX_RADIUS = 40
HEX_WIDTH = math.sqrt(3) * HEX_RADIUS  #Width
HEX_HEIGHT = 2 * HEX_RADIUS  #Height
VERTICAL_SPACING = HEX_HEIGHT * 3/4  #For honeycomb pattern
HORIZONTAL_SPACING = HEX_WIDTH  #horizontal spacing

#Vertices of a hexagon
def hexagon_vertices(x, y, radius):
    vertices = []
    for i in range(6):
        angle = math.radians(60 * i - 30) 
        vertex_x = x + radius * math.cos(angle)
        vertex_y = y + radius * math.sin(angle)
        vertices.append((vertex_x, vertex_y))
    return vertices

#draw honeycomb pattern
def draw_hex_grid(rows, cols, hex_radius):
    hexagons = []
    for row in range(rows):
        for col in range(cols):
            #Horizontal offset
            x_offset = col * HORIZONTAL_SPACING + (row % 2) * (HORIZONTAL_SPACING / 2)  #Stagger every second row
            #Vertical offset
            y_offset = row * VERTICAL_SPACING
            hexagon = hexagon_vertices(x_offset, y_offset, hex_radius)
            hexagons.append((hexagon, (x_offset, y_offset)))
    return hexagons

#check if a point is inside a hexagon
def point_in_hexagon(point, hexagon):
    polygon = pygame.draw.polygon(screen, BACKGROUND, hexagon)
    return polygon.collidepoint(point)

def main():
    running = True
    hexagons = draw_hex_grid(20, 20, HEX_RADIUS)  #choose grid size

    while running:
        screen.fill(BACKGROUND)

        #mouse position
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()

        #Check if mouse is hovering over a hexagon
        for hexagon, (hx, hy) in hexagons:
            if point_in_hexagon(mouse_pos, hexagon):
                pygame.draw.polygon(screen, HOVER_COLOR, hexagon)  #Highlight on hover
                pygame.draw.polygon(screen, BLACK, hexagon, 2)  #Black outline
                if mouse_pressed[0]:  #Left mouse click
                    pygame.draw.polygon(screen, CLICK_COLOR, hexagon)  #Red fill on click
                    pygame.draw.polygon(screen, BLACK, hexagon, 2)  #Black outline
                    print(f"Hexagon clicked at ({hx}, {hy})")
            else:
                pygame.draw.polygon(screen, BACKGROUND, hexagon)  #BACKGROUND fill
                pygame.draw.polygon(screen, BLACK, hexagon, 2)  #Black outline

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()

#Run 
if __name__ == "__main__":
    main()

pygame.quit()
