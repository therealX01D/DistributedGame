import pygame
import time
import math
import Helpers


GRASS = Helpers.scaleImage(pygame.image.load("imgs/grass.jpg"), 2.5, 2.5)
TRACK = pygame.image.load("imgs/track.png")
FINISH= Helpers.scaleImage(pygame.image.load("imgs/finish.png"),0.9,0.9)
TRACK_BORDER = Helpers.scaleImage(pygame.image.load("imgs/track-border.png"),0.9,0.9)

RED_CAR = Helpers.scaleImage(pygame.image.load("imgs/red-car.png"),0.55,0.55)
GREEN_CAR = Helpers.scaleImage(pygame.image.load("imgs/green-car.png"),0.55,0.55)

WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

myimages = [(GRASS,(0,0)),(TRACK,(0,0)),(FINISH,(0,0))]

def DrawImages(win,images):
    for image,pos in images:
        WIN.blit(image,pos)

class AbstractCar:
    def __init__(self, max_vel, rotation_vel):
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.x, self.y = self.START_POS
        self.acceleration = 0.05

    def rotate(self, left=False, right=False):
        self.angle += left * 1 + right * -1

    def draw(self, win):
        Helpers.blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

    def move(self):
        rad = math.radians(-self.angle)
        vertical_v = -math.cos(rad)*self.vel
        horizontal_v = math.sin(rad)*self.vel
        self.x += horizontal_v
        self.y += vertical_v

    def move_forward(self):
        self.vel = min(self.vel + self.acceleration, self.max_vel) #threshold is max_vel
        self.move()

    def move_backward(self):
        self.vel = max(self.vel - self.acceleration, -self.max_vel) #threshold is max_vel
        self.move()

    def reduce_speed(self):
        if self.vel>0:
            self.vel = max(self.vel - self.acceleration / 4, 0)

        if self.vel<0:
            self.vel = min(self.vel + self.acceleration / 4, 0)
        self.move()

class PlayerCar(AbstractCar):
    IMG = RED_CAR
    START_POS = (180, 200)



def DrawCar(win,player_car):
    player_car.draw(win)

FPS = 60
pygame.display.set_caption("Racing Game!")
run = 1
clock = pygame.time.Clock()
i = 0

player_car = PlayerCar(4, 4)
while run:
    clock.tick(FPS)
    DrawImages(WIN,myimages)
    DrawCar(WIN,player_car)

    pygame.display.update() # update screen
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = 0
            break
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_car.rotate(left=1)
    if keys[pygame.K_RIGHT]:
        player_car.rotate(right=1)

    if keys[pygame.K_UP]:
        player_car.move_forward()
    if keys[pygame.K_DOWN]:
        player_car.move_backward()
    if (not keys[pygame.K_UP]) and (not keys[pygame.K_DOWN]):
        player_car.reduce_speed()


pygame.quit()