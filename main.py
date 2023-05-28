import time
import math
import Helpers
import threading
import asyncio
import pygame
# import server
import json
import GameWebsocket
import GameWebSocketMultithreaded
#TODO: get all players from server and update the game accordingly each player will have class iniated at the start of the game

##SERVER THREAD INIT
def start_server(loop, future):
    print("Server Thread Started")
    loop.run_until_complete(GameWebSocketMultithreaded.main(future))

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
##
pygame.init()
pygame.fastevent.init()
##

##PYGAME INIT END


##GAME ASSETS
GRASS = Helpers.scaleImage(pygame.image.load("imgs/grass.jpg"), 2.5, 2.5)
TRACK = pygame.image.load("imgs/track.png")
FINISH= Helpers.scaleImage(pygame.image.load("imgs/finish.png"),0.9,0.9)
TRACK_BORDER = Helpers.scaleImage(pygame.image.load("imgs/track-border.png"),0.9,0.9)

RED_CAR = Helpers.scaleImage(pygame.image.load("imgs/red-car.png"),0.3,0.3)
GREEN_CAR = Helpers.scaleImage(pygame.image.load("imgs/green-car.png"),0.3,0.3)
GREY_CAR = Helpers.scaleImage(pygame.image.load("imgs/grey-car.png"),0.3,0.3)
PURPLE_CAR = Helpers.scaleImage(pygame.image.load("imgs/purple-car.png"),0.3,0.3)
CAR_IMGS = [RED_CAR,GREEN_CAR,GREY_CAR,PURPLE_CAR]
WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

myimages = [(GRASS,(0,0)),(TRACK,(0,0)),(FINISH,(0,0))]

def DrawImages(win,images):
    for image,pos in images:
        WIN.blit(image,pos)

def DrawCar(win,player_car):
    player_car.draw(win)

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

#each player in game will have this class
class PlayerCar(AbstractCar):
    IMG = RED_CAR
    START_POS = (180, 200)
    def __init__(self, max_vel, rotation_vel, CarID,StartPos):     #TODO : THIS IS SSHIT AND MAY CAUSE ERROR , MAKE SURE IT WORKS RIGHT
        super().__init__( max_vel, rotation_vel)  # Call the parent class constructor
        self.CarID = CarID
        self.StartPos = StartPos
        IMG = CAR_IMGS[CarID]
        START_POS = StartPos #use self.x better



# pygame.display.set_caption("Racing Game!")
run = 1
clock = pygame.time.Clock()
i = 0


player1 = PlayerCar(4,4,0,(180,250)) #RED
player2 = PlayerCar(4,4,1,(170,250)) #GREEN
arr_players_class = [player1,player2]

##GAME ASSETS END #######

##GAME MAIN LOOP

while run:
    DrawImages(WIN, myimages)
    pygame.display.update()  # update screen
    print("MAIN START")
    REDUCE = True
    for event in pygame.event.get():
        print("EV MSG" , event.message)
        if event.type == pygame.QUIT:
            run = 0
            break
        elif event.type == GameWebsocket.EVENTTYPE:
            print("GOT EVENT ",event.message)
            GameStatus = event.message #   {'1' :  {'posx': p.x ,'posy': p.y ,'angle' : p.angle} ,'1' :  {'posx': p.x ,'posy': p.y ,'angle' : p.angle}}
            LoadedGameStatus = json.loads(GameStatus)
            for key in LoadedGameStatus:
                player_id = int(key)
                p_status = LoadedGameStatus[str(player_id)]
                arr_players_class[player_id].x = p_status["posx"]
                arr_players_class[player_id].y = p_status["posy"]
                arr_players_class[player_id].angle = p_status["angle"]

    print("Main before sleep")
    time.sleep(0.1)

print("Stoping Server event loop")
stop_server(loop, future)
print("Waiting for termination")
thread.join()
print("Shutdown pygame")
pygame.quit()
