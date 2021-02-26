import pygame
import time
import random

pygame.init()

display_width = 1280
display_height = 720

spacecraft_width = 48
spacecraft_height = 48

enemy_width = 80
enemy_height = 80

#colors
black = (0,0,0)
darkgray = (20,20,20)
white = (255,255,255)
red = (255,0,0)

spacecraft_image = pygame.image.load('spacecraft.png')
enemy_image = pygame.image.load('fireball.png')

gameDisplay = pygame.display.set_mode((display_width, display_height))

pygame.display.set_caption('Silver Spacecraft')

clock = pygame.time.Clock()

def spacecraft(x, y):
    gameDisplay.blit(spacecraft_image, (x,y))

def enemy(x, y):
    gameDisplay.blit(enemy_image, (x,y))

def overlap(x,y,enemy_x,enemy_y):
    x = int(x)
    y = int(y)
    enemy_x = int(enemy_x)
    enemy_y = int(enemy_y)

    spacecraft_Coordinate_x = [i for i in range(x, x + spacecraft_width)]
    spacecraft_Coordinate_y = [i for i in range(y, y + spacecraft_height)]
    enemy_Coordinate_x = [i for i in range(enemy_x, enemy_x + enemy_width)]
    enemy_Coordinate_y = [i for i in range(enemy_y, enemy_y + enemy_height)] 

    intersection_x = [item for item in spacecraft_Coordinate_x if item in enemy_Coordinate_x]
    intersection_y = [item for item in spacecraft_Coordinate_y if item in enemy_Coordinate_y]

    if len(intersection_x) and len(intersection_y):
        return True
    else:
        return False    

def text_object(text, font):
    text_surf = font.render(text, True, red)
    return text_surf, text_surf.get_rect()

def message_display(text):
    text_font = pygame.font.Font('freesansbold.ttf', 100)
    text_surf, text_rect = text_object(text, text_font)
    text_rect.center = ((display_width / 2),(display_height / 2))
    gameDisplay.blit(text_surf, text_rect)
    pygame.display.update()
    time.sleep(2)
 
def score_display(score):
    font = pygame.font.SysFont(None, 25)
    text_surf = font.render("score: " + str(score), True, white)
    gameDisplay.blit(text_surf, (0,0))
 
def crach():
    message_display('Game Over')
    game_loop()

def game_loop():
    x = display_width * 0.45
    y = display_height * 0.8

    enemy_x = round(random.randrange(0, display_width))
    enemy_y = -300
    enemy_speed = 5

    x_change = 0

    score = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5
                elif event.key == pygame.K_RIGHT:
                    x_change = +5

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0

            #print(event)
        
        x = x + x_change

        gameDisplay.fill(darkgray)
        spacecraft(x, y)
        enemy(enemy_x, enemy_y)
        enemy_y += enemy_speed

        if x > display_width - spacecraft_width or x < 0:
            crach()

        if enemy_y > display_height:
            enemy_x = round(random.randrange(0, display_width))
            enemy_y = 0 - enemy_height
            score += 1
            enemy_speed += 1

        if overlap(x,y,enemy_x,enemy_y):
            crach()    

        score_display(score)
        pygame.display.update()
        clock.tick(120)   

game_loop()