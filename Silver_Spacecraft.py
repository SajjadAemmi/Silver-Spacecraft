import pygame
import time
import random
from gpiozero import DistanceSensor

pygame.init()

#colors
white = (255,255,255)
red = (255,0,0)


class Enemy:
    def __init__(self):
        self.width = 48
        self.height = 48
        self.image = pygame.image.load('enemy.png')
        self.x_pos = Game.width
        self.y_pos = random.randint(0, Game.height - self.height)
        self.speed = 20
        self.area = Game.display.blit(self.image, (self.x_pos, self.y_pos))

    def draw(self):
        self.area = Game.display.blit(self.image, (self.x_pos, self.y_pos))

    def move(self):
        self.x_pos -= self.speed


class Spacecraft:

    def __init__(self):
        self.width = 48
        self.height = 48
        self.image = pygame.image.load('spacecraft.png')
        self.x_pos = 100
        self.y_pos = Game.height / 2
        self.speed = 32
        self.area = Game.display.blit(self.image, (self.x_pos, self.y_pos))

    def draw(self):
        self.area = Game.display.blit(self.image, (self.x_pos, self.y_pos))

    def move(self):
        self.y_pos -= self.y_direction * self.speed
        self.y_pos = min(self.y_pos, Game.height - self.height)
        self.y_pos = max(self.y_pos, 0)


class Game:

    width = 640
    height = 480
    display = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Silver SpaceCraft')
    background = pygame.image.load('galaxy.jpg')
    point_sound = pygame.mixer.Sound("sfx_point.wav")
    game_over_sound = pygame.mixer.Sound("sfx_hit.wav")
    pygame.mixer.music.load('music.mp3')
    pygame.mixer.music.set_volume(0.2)
    sensor = DistanceSensor(echo=23, trigger=24, queue_len=5)    

    @staticmethod
    def play():
        pygame.mixer.music.play()
        spacecraft = Spacecraft()
        enemy = Enemy()
        clock = pygame.time.Clock()
        score = 0
        sensor_distance = 0
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            # print('Distance to nearest object is', Game.sensor.distance, 'm')
            sensor_distance_pre = sensor_distance
            sensor_distance = Game.sensor.distance

            if sensor_distance - sensor_distance_pre < -0.001:
                spacecraft.y_direction = -1
            elif sensor_distance - sensor_distance_pre > 0.001:
                spacecraft.y_direction = 1
            else:
                spacecraft.y_direction = 0

            spacecraft.move()
            enemy.move()

            Game.display.blit(Game.background, (0, 0))
            spacecraft.draw()
            enemy.draw()

            if enemy.x_pos < 0:
                enemy = Enemy()
                Game.point_sound.play()
                score += 1

            if spacecraft.area.colliderect(enemy.area):
                Game.game_over_sound.play()
                Game.message_display('Game Over')
                Game.play()

            Game.score_display(score)
            pygame.display.update()
            clock.tick(10)

    @staticmethod
    def text_object(text, font):
        text_surf = font.render(text, True, red)
        return text_surf, text_surf.get_rect()

    @staticmethod
    def message_display(text):
        text_font = pygame.font.Font('freesansbold.ttf', 100)
        text_surf, text_rect = Game.text_object(text, text_font)
        text_rect.center = ((Game.width / 2), (Game.height / 2))
        Game.display.blit(text_surf, text_rect)
        pygame.display.update()
        time.sleep(2)

    @staticmethod
    def score_display(score):
        font = pygame.font.SysFont(None, 25)
        text_surf = font.render("score: " + str(score), True, white)
        Game.display.blit(text_surf, (0,0))


if __name__ == '__main__':
    Game.play()
