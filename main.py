import pygame
from UI.HiveGame import HiveGame


def launch():
    pygame.init()

    game = HiveGame()
    game.start_game_loop()

    pygame.quit()

if __name__ == "__main__":
    launch()
