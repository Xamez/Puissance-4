import pygame
import os
import sys
import random

os.environ['SDL_VIDEO_CENTERED'] = '0'

pygame.init()

# VARS
clock = pygame.time.Clock()
font = pygame.font.Font('font/Qanelas-Black.ttf', 60)
WIDTH = 910
HEIGTH = 880

player = random.randint(1, 2)
start_player = player

game_state = "start"

board = [[0 for y in range(6)] for x in range(7)]
screen = pygame.display.set_mode((WIDTH, HEIGTH))
pygame.display.set_caption("Puissance 4")

# LOAD ASSETS

surface_background = pygame.image.load("assets/background.png")
rect_background = surface_background.get_rect()

surface_win_background = pygame.image.load("assets/win_background.png")
rect_win_background = surface_win_background.get_rect()

surface_red_coin = pygame.image.load("assets/red.png")
rect_red_coin = surface_red_coin.get_rect()

surface_yellow_coin = pygame.image.load("assets/yellow.png")
rect_yellow_coin = surface_yellow_coin.get_rect()


# FUNCTIONS

def display_backgroud(list):
    if len(list) == 0:
        for x in range(7):
            for y in range(6):
                screen.blit(surface_background, (rect_background.width * x,
                                                 100 + rect_background.width * y))  # rect_background.width = rect_background.height
    else:
        for pos in list:
            col, row = pos
            screen.blit(surface_win_background,
                        (rect_win_background.width * col, 100 + rect_win_background.width * row))

    pygame.draw.line(screen, (255, 255, 255), (0, 100), (WIDTH, 100), 5)  # draw little white line


def get_case(x):
    column = get_column(x)
    return column, get_row(column)


def get_column(x):
    return x // rect_background.width


def get_row(column):
    for index in range(len(board[column])):
        if board[column][5 - index] < 1:
            return 5 - index  # 5 - X to start from the bottom


def draw_coin(x):
    col, row = get_case(x)
    if row is None:
        return False
    if board[col][row] == 0:
        board[col][row] = player % 2 + 1
        if player % 2 + 1 == 1:
            screen.blit(surface_yellow_coin, (rect_yellow_coin.width * col, rect_yellow_coin.width * row + 100))
        if player % 2 + 1 == 2:
            screen.blit(surface_red_coin, (rect_red_coin.width * col, rect_red_coin.width * row + 100))

        # DEBUG
        # surface_text = font.render(str(col) + "," + str(row), True, (255, 255, 255))
        # rect_text = surface_text.get_rect(center=(rect_yellow_coin.width * col + rect_yellow_coin.width // 2,
        #                                          rect_yellow_coin.width * row + 100 + rect_yellow_coin.width // 2))
        # screen.blit(surface_text, rect_text)

        return True
    return False


def check_win():

    # check equality
    if (player == 43 and start_player == 1) or player == 44:
        return "nobody"


    value = player % 2 + 1
    color = "yellow" if value == 1 else "red"

    # check rows
    for row in range(3):
        for col in range(5):
            if board[col][row] == value and board[col][row + 1] == value and board[col][row + 2] == value and \
                    board[col][row + 3] == value and board[col][row] != 0:

                display_backgroud([(col, row), (col, row + 1), (col, row + 2), (col, row + 3)]) # highlight the background boxes

                return color

    # check columns
    for row in range(6):
        for col in range(2):
            if board[col][row] == value and board[col + 1][row] == value and board[col + 2][row] == value and \
                    board[col + 3][row] == value and board[col][row] != 0:

                display_backgroud([(col, row), (col + 1, row), (col + 2, row), (col + 3, row)])  # highlight the background boxes
                return color

    # check diagonales
    for row in range(3, 6):
        for col in range(0, 4):
            if board[col][row] == value and board[col + 1][row - 1] == value and board[col + 2][row - 2] == value and \
                    board[col + 3][row - 3] == value and board[col][row] != 0:
                display_backgroud([(col, row), (col + 1, row - 1), (col + 2, row - 2), (col + 3, row - 3)]) # highlight the background boxes

                return color

    return "run"


def drawText(text):

    pygame.draw.rect(screen, (30, 30, 30), (0, 0, WIDTH, 100)) # erase previous text

    surface_text = font.render(text, True, (0, 0, 0))
    rect_text = surface_text.get_rect(center=(WIDTH // 2, HEIGTH // 18))

    surface_text2 = font.render(text, True, (255, 255, 255)) # create a fake shadow
    rect_text2 = surface_text.get_rect(center=(WIDTH // 2 - 3, (HEIGTH // 18) - 3))

    screen.blit(surface_text, rect_text)
    screen.blit(surface_text2, rect_text2)


def reset():
    screen.fill((30, 30, 30))
    display_backgroud([])


reset() # display background and grid

while True:

    if game_state == "run":
        game_state = check_win()
        drawText("Au {} de jouer !".format("Jaune" if player % 2 == 1 else "Rouge"))

    if game_state == "start":
        drawText("Cliquez pour jouer !")
    if game_state == "nobody":
        drawText("Égalité ! Cliquez pour rejouer.")
    if game_state == "red":
        drawText("Les rouges ont gagné !")
    if game_state == "yellow":
        drawText("Les jaunes ont gagné !")

    for event in pygame.event.get():

        if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
            if game_state == "run":
                x, y = pygame.mouse.get_pos()
                if y >= 100: # grid start at 100px from the top
                    player += 1
                    if draw_coin(x) is False:
                        player -= 1
            else:
                reset()
                board = [[0 for y in range(6)] for x in range(7)]
                player = random.randint(1, 2)
                start_player = player
                game_state = "run"

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    clock.tick(60)
