import pygame
import time
import math
import Helpers
import threading
import asyncio
import pygame
import server


##SERVER THREAD INIT
def start_server(loop, future):
    print("Server Thread Started")
    loop.run_until_complete(server.main(future))

def stop_server(loop, future):
    print("SERVER THREAD CLOSING")
    loop.call_soon_threadsafe(future.set_result, None)


loop = asyncio.get_event_loop() #create event loop if it dosen't exist
#Or get it if it exists
#Event loop won't run until we tell it to do
#NOTE : If it wasn't already running
future = loop.create_future() #Future represents the result of an asynchronous operation.
# It is a placeholder for a value that may not be available yet

thread = threading.Thread(target=start_server, args=(loop, future))
#create thread with the given event loop that won't run here but run at server
#Also we have future of that loop
print("STARTING SERVER THREAD")
thread.start() #start server thread


##Server Thread END####

##init pygame
pygame.init()
pygame.fastevent.init()
##PYGAME INIT END


##GAME ASSETS
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
        self.angle += left * 2 + right * -2

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

class OnlineCar(AbstractCar):
    IMG = GREEN_CAR
    START_POS = (150, 200)



def DrawCar(win,player_car):
    player_car.draw(win)

FPS = 60
pygame.display.set_caption("Racing Game!")
run = 1
clock = pygame.time.Clock()
i = 0

player_car = PlayerCar(4, 4)
Online_car = OnlineCar(4, 4)
##GAME ASSETS END #######

##GAME MAIN LOOP
while run:
    clock.tick(FPS)
    DrawImages(WIN,myimages)
    DrawCar(WIN,player_car)
    DrawCar(WIN,Online_car)
    # REDUCE = 1
    pygame.display.update() # update screen

    REDUCE = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = 0
            break
        elif event.type == server.EVENTTYPE:
            mssg = event.message
            print("whole message from C: ", mssg)
            array = mssg.split(",")
            print("splitted msg" , array)
            if "left" in array:
                Online_car.rotate(left=1)
            if "right" in array:
                Online_car.rotate(right=1)

            if "up" in array:
                Online_car.move_forward()
                REDUCE  = False
            if "down" in array:
                Online_car.move_backward()
                REDUCE  = False


    if REDUCE:
        Online_car.reduce_speed()
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
    DrawCar(WIN,player_car)
    DrawCar(WIN,Online_car)

print("Stoping Server event loop")
stop_server(loop, future)
print("Waiting for termination")
thread.join()
print("Shutdown pygame")
pygame.quit()
