import pygame
import random
import os
import time

# Initiation
pygame.init()
pygame.mixer.init()

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
violet = (143, 0, 255)
golden = (255, 215, 0)

# Creating a Window
screen_width = 1200
screen_length = 700
gameWindow = pygame.display.set_mode((screen_width, screen_length), pygame.RESIZABLE)
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 55)

# BG Image
himg = pygame.image.load("bg.jpg")
himg = pygame.transform.scale(himg, (screen_width, screen_length)).convert_alpha()
bgimg = pygame.image.load("bg2.jpg")
bgimg = pygame.transform.scale(bgimg, (screen_width, screen_length)).convert_alpha()
goimg = pygame.image.load("snake.jpg")
goimg = pygame.transform.scale(goimg, (screen_width, screen_length)).convert_alpha()

# Game Window
pygame.display.set_caption("Snake.ers")
pygame.display.update()

# Text display
def text_screen(text, color, x, y):
    screen_text = font.render(text, True, color)
    gameWindow.blit(screen_text, [x, y])

# Snake ploting
def snake_plot(gameWindow, color, snk_list, snake_size):
    for x, y in snk_list:
        pygame.draw.rect(gameWindow, color, [x, y, snake_size, snake_size])

# Home Screen
def welcome():
    exit_game = False
    pygame.mixer.music.load("nagin.mp3")
    pygame.mixer.music.play()
    while not exit_game:
        # gameWindow.fill(white)
        gameWindow.blit(himg, (0, 0))
        text_screen("Snake", green, 720, 250)
        text_screen(".ers", red, 840, 250)
        text_screen("Tap Space to play", blue, 665, 310)
        text_screen("Created by", violet, 900, 0)
        text_screen("Anish Dey", red, 975, 40)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pygame.mixer.music.load("start.mp3")
                    pygame.mixer.music.play()
                    # gameWindow.fill(white)
                    gameWindow.blit(bgimg, (0, 0))
                    pygame.display.update()
                    time.sleep(0.4)
                    # pygame.mixer.music.load("bg.mp3")
                    # pygame.mixer.music.play()
                    game_loop()

# Game loop
def game_loop():
    # Game Specific Variables
    exit_game = False
    game_over = False
    snake_x = 45
    snake_y = 55
    snake_size = 30
    disp_x = 0
    disp_y = 0
    init_disp = 5
    food_p_x = random.randint(60, 1140)
    food_p_y = random.randint(60, 640)
    food_size = 20
    score = 0
    snk_list = []
    snk_length = 1
    if not os.path.exists("hiscore.txt"):
        with open("hiscore.txt", "w") as f:
            f.write("0")
    with open("hiscore.txt", "r") as f:
        highscore = f.read()
    fps = 30

    # If food was circle, work in progress
    # food_rad = 15

    while not exit_game:
        if game_over:
            gameWindow.blit(goimg, (0, 0))
            with open("hiscore.txt", "w") as f:
                f.write(str(highscore))
            # gameWindow.fill(white)
            text_screen("Game Over!", red, 200, 250)
            text_screen("Tap Enter to restart", blue, 200, 290)
            text_screen("Score: " + str(score) + "   High Score: " + str(highscore), black, 200, 350)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        game_loop()

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT:
                        disp_x += init_disp
                        disp_y = 0

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        disp_x += -init_disp
                        disp_y = 0

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        disp_y += -init_disp
                        disp_x = 0

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        disp_y += +init_disp
                        disp_x = 0

            # If food was circle, work in progress
            # if (abs(snake_x - food_p_x) < 6 or abs(snake_x - food_p_x) < -6) and (abs(snake_y - food_p_y) < 6 or abs(snake_x - food_p_x) < -6):
                #     score += 5
                #     food_p_x = random.randint(60, 1140)
                #     food_p_y = random.randint(60, 640)

            snake_x += disp_x
            snake_y += disp_y

            if abs(snake_x - food_p_x) < 20 and abs(snake_y - food_p_y) < 20:
                score += 5
                pygame.mixer.music.load("beep.wav")
                pygame.mixer.music.play()
                # pygame.mixer.music.load("bg.mp3")
                # pygame.mixer.music.play()
                food_p_x = random.randint(60, 1140)
                food_p_y = random.randint(60, 640)
                snk_length += 8
                if score > int(highscore):
                    highscore = score

            # gameWindow.fill(white)

            gameWindow.blit(bgimg, (0, 0))
            text_screen("Score: " + str(score) + "     High Score: " + str(highscore), blue, 5, 5)

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)

            if len(snk_list) > snk_length:
                del snk_list[0]

            if head in snk_list[:-1]:
                pygame.mixer.music.load("go.mp3")
                pygame.mixer.music.play()
                time.sleep(1)
                game_over = True

            if snake_x < 0 or snake_y < 0 or snake_x > screen_width or snake_y > screen_length:
                pygame.mixer.music.load("go.mp3")
                pygame.mixer.music.play()
                time.sleep(1)
                game_over = True

            # pygame.draw.rect(gameWindow, green, [snake_x, snake_y, snake_size, snake_size])

            snake_plot(gameWindow, golden, snk_list, snake_size)

            pygame.draw.rect(gameWindow, red, [food_p_x, food_p_y, food_size, food_size])

            # If food was circle, work in progress
            # pygame.draw.circle(gameWindow, red, [food_p_x, food_p_y], food_rad)

        pygame.display.update()
        clock.tick(fps)

    pygame.quit()
    quit()

welcome()
