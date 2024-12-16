import pygame, sys
from UI.HiveGame import HiveGame
from UI.constants import *
from UI.Button import Button

first_player = None
second_player = None
first_player_mode = None
second_player_mode = None
first_player_diff = None
second_player_diff = None

#difficulty menu
def difficulty_menu(player_num):
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(75).render("Select Difficulty", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(400, 100))

        EASY_BUTTON = Button(image=pygame.image.load("assets/Rect.png"), pos=(400, 250), 
                            text_input="Easy", font=get_font(65), base_color="#d7fcd4", hovering_color="White")
        MEDIUM_BUTTON = Button(image=pygame.image.load("assets/Rect.png"), pos=(400, 380), 
                            text_input="Medium", font=get_font(65), base_color="#d7fcd4", hovering_color="White")
        HARD_BUTTON = Button(image=pygame.image.load("assets/Rect.png"), pos=(400, 510), 
                            text_input="Hard", font=get_font(65), base_color="#d7fcd4", hovering_color="White")
                            

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        #hovering
        for button in [EASY_BUTTON, MEDIUM_BUTTON, HARD_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        #events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #mouse click
            global first_player_diff, second_player_diff
            if event.type == pygame.MOUSEBUTTONDOWN:
                #play button click
                if EASY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    if player_num == 1:
                        first_player_diff = PLAYER_DIFFICULTY_EASY
                        pygame.mixer.music.load('assets/menu-sound.mp3')
                        pygame.mixer.music.play(1)
                        mode_menu(2)
                        return
                    else:
                        second_player_diff = PLAYER_DIFFICULTY_EASY
                        # print("first_player, first_player_diff, second_player, second_player_diff")
                        # print(first_player, first_player_diff, second_player, second_player_diff)
                        # print("first_player, first_player_diff, second_player, second_player_diff")
                        pygame.mixer.music.load('assets/board-start.mp3')
                        pygame.mixer.music.play(1)
                        launch()
                        return
                #options button click
                if MEDIUM_BUTTON.checkForInput(MENU_MOUSE_POS):
                    if player_num == 1:
                        first_player_diff = PLAYER_DIFFICULTY_MEDIUM
                        pygame.mixer.music.load('assets/menu-sound.mp3')
                        pygame.mixer.music.play(1)
                        mode_menu(2)
                        return
                    else:
                        second_player_diff = PLAYER_DIFFICULTY_MEDIUM
                        pygame.mixer.music.load('assets/board-start.mp3')
                        pygame.mixer.music.play(1)
                        launch()
                        return
                #quit button click
                if HARD_BUTTON.checkForInput(MENU_MOUSE_POS):
                    if player_num == 1:
                        first_player_diff = PLAYER_DIFFICULTY_HARD
                        pygame.mixer.music.load('assets/menu-sound.mp3')
                        pygame.mixer.music.play(1)
                        mode_menu(2)
                        return
                    else:
                        second_player_diff = PLAYER_DIFFICULTY_HARD
                        pygame.mixer.music.load('assets/board-start.mp3')
                        pygame.mixer.music.play(1)
                        launch()
                        return
        pygame.display.update()    
#mode menu
def mode_menu(player_num):
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        Text = "Select AI's Algorithm"

        MENU_TEXT = get_font(75).render(Text, True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(400, 100))

        MINMAX_BUTTON = Button(image=pygame.image.load("assets/Rect.png"), pos=(400, 250), 
                            text_input="Min-Max", font=get_font(65), base_color="#d7fcd4", hovering_color="White")
        ALPHABETA_BUTTON = Button(image=pygame.image.load("assets/Rect.png"), pos=(400, 380), 
                            text_input="Alpha-Beta", font=get_font(65), base_color="#d7fcd4", hovering_color="White")
        ITERATIVE_BUTTON = Button(image=pygame.image.load("assets/Rect.png"), pos=(400, 510), 
                            text_input="Iterative Deepening", font=get_font(65), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        #hovering
        for button in [MINMAX_BUTTON, ALPHABETA_BUTTON, ITERATIVE_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        #events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #mouse click
            
            global first_player_mode, second_player_mode
            if event.type == pygame.MOUSEBUTTONDOWN:
                #play button click
                if MINMAX_BUTTON.checkForInput(MENU_MOUSE_POS):
                    if player_num == 1:
                        first_player_mode = AI_MODE_MINMAX
                        pygame.mixer.music.load('assets/menu-sound.mp3')
                        pygame.mixer.music.play(1)
                        player_menu(2)
                        return
                    else:
                        second_player_mode = AI_MODE_MINMAX
                        pygame.mixer.music.load('assets/menu-sound.mp3')
                        pygame.mixer.music.play(1)
                        launch()
                        return
                #options button click
                if ALPHABETA_BUTTON.checkForInput(MENU_MOUSE_POS):
                    if player_num == 1:
                        first_player_mode = AI_MODE_ALPHA_BETA
                        pygame.mixer.music.load('assets/menu-sound.mp3')
                        pygame.mixer.music.play(1)
                        player_menu(2)
                        return
                    else:
                        second_player_mode = AI_MODE_ALPHA_BETA
                        pygame.mixer.music.load('assets/board-start.mp3')
                        pygame.mixer.music.play(1)
                        launch()
                        return
                #quit button click
                if ITERATIVE_BUTTON.checkForInput(MENU_MOUSE_POS):
                    if player_num == 1:
                        first_player_mode = AI_MODE_ITERATIVE
                        pygame.mixer.music.load('assets/menu-sound.mp3')
                        pygame.mixer.music.play(1)
                        difficulty_menu(1)
                        return
                    else:
                        second_player_mode = AI_MODE_ITERATIVE
                        pygame.mixer.music.load('assets/board-start.mp3')
                        pygame.mixer.music.play(1)
                        difficulty_menu(2)
                        return

        pygame.display.update()    

def player_menu(player_num):
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        Text = "Select First Player (white)"
        if player_num == 2:
            Text = "Select Second Player (black)"

        MENU_TEXT = get_font(75).render(Text, True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(400, 100))

        HUMAN_BUTTON = Button(image=pygame.image.load("assets/Rect.png"), pos=(400, 250), 
                            text_input="Human", font=get_font(65), base_color="#d7fcd4", hovering_color="White")
        AI_BUTTON = Button(image=pygame.image.load("assets/Rect.png"), pos=(400, 400), 
                            text_input="AI", font=get_font(65), base_color="#d7fcd4", hovering_color="White")
                            

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        #hovering
        for button in [HUMAN_BUTTON, AI_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        #events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #mouse click
            
            global first_player, second_player
            if event.type == pygame.MOUSEBUTTONDOWN:
                #play button click
                if HUMAN_BUTTON.checkForInput(MENU_MOUSE_POS):
                    if player_num == 1:
                        first_player = PLAYER_TYPE_HUMAN
                        pygame.mixer.music.load('assets/menu-sound.mp3')
                        pygame.mixer.music.play(1)
                        player_menu(2)
                        return
                    else:
                        second_player = PLAYER_TYPE_HUMAN
                        pygame.mixer.music.load('assets/menu-sound.mp3')
                        pygame.mixer.music.play(1)
                        launch()
                        return
                #options button click
                if AI_BUTTON.checkForInput(MENU_MOUSE_POS):
                    if player_num == 1:
                        first_player = PLAYER_TYPE_AI
                        pygame.mixer.music.load('assets/menu-sound.mp3')
                        pygame.mixer.music.play(1)
                        mode_menu(1)
                        return
                    else:
                        second_player = PLAYER_TYPE_AI
                        pygame.mixer.music.load('assets/board-start.mp3')
                        pygame.mixer.music.play(1)
                        mode_menu(2)
                        return

        pygame.display.update()    

#main menu
def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(400, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Rect.png"), pos=(400, 250), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Rect.png"), pos=(400, 400), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        # OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Rect.png"), pos=(400, 400), 
        #                     text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        #hovering
        # for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        #events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            #mouse click
            if event.type == pygame.MOUSEBUTTONDOWN:
                #play button click
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.mixer.music.load('assets/menu-sound.mp3')
                    pygame.mixer.music.play(1)
                    player_menu(1)
                #options button click
                # if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                #     options()
                #quit button click
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()    

def launch():
    pygame.init()

    game = HiveGame([first_player, second_player], [first_player_mode, second_player_mode], [first_player_diff, second_player_diff])
    game.start_game_loop()

    pygame.quit()

if __name__ == "__main__":
    main_menu()
    #launch()
