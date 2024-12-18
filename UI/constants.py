import pygame

# WARNING: Changing the dimensions might cause bugs
WIDTH, HEIGHT = 800, 600
FPS = 60

pygame.init()
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Othello')
CLOCK = pygame.time.Clock()
BG = pygame.image.load("assets/Background.png")
SMALL_BUTTON_IMAGE = pygame.image.load("assets/SmallGreyRect.png")


MARGIN = 0.04 * HEIGHT
TOP_BAR_HEIGHT = 0.12 * HEIGHT
BOARD_SIZE_PIXELS = HEIGHT - 3 * MARGIN - TOP_BAR_HEIGHT
BOARD_START_Y = 2 * MARGIN + TOP_BAR_HEIGHT
BOARD_START_X = (WIDTH - BOARD_SIZE_PIXELS - SMALL_BUTTON_IMAGE.get_rect().width)/2
BOARD_END_X = BOARD_START_X + BOARD_SIZE_PIXELS
BOARD_BUTTON_CENTER = BOARD_END_X + (WIDTH - BOARD_END_X)//2

class Colors:
    BACKGROUND = (35, 35, 35)
    TOP_BAR = (125, 125, 125)
    BOARD = (0, 145, 100)


PLAYER_TYPE_HUMAN = "Human"
PLAYER_TYPE_AI = "AI"
AI_MODE_MINMAX = "Min-Max"
AI_MODE_ALPHA_BETA = "Alpha-Beta"
AI_MODE_ITERATIVE = "Iterative"

PLAYER_DIFFICULTY_EASY = "Easy"
PLAYER_DIFFICULTY_MEDIUM = "Medium"
PLAYER_DIFFICULTY_HARD = "Hard"

def get_font(size):
    return pygame.font.Font(None, size)