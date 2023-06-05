import time

import pygame
from Helpers import *
import zmq
import json
from ReadFromDict import *
import Button as button
dictionary = read_dictionary_from_file()
def kill():
    pygame.quit()
    context = zmq.Context()
    psr = context.socket(zmq.PUSH)
    KillPort = dictionary["KillPort"]
    psr.bind("tcp://*:"+str(KillPort))
    psr.send_string("KILL ALL")

def guiP():
    import math
    import Helpers
    class AbstractCar:
        def __init__(self, max_vel, rotation_vel):
            self.img = self.IMG
            self.max_vel = max_vel
            self.vel = 0
            self.rotation_vel = rotation_vel
            self.angle = 0
            self.x, self.y = self.START_POS
            # print("START POS OF CAR",self.START_POS)
            self.acceleration = 0.05

        def rotate(self, left=False, right=False):
            self.angle += left * 2 + right * -2

        def draw(self, win):
            Helpers.blit_rotate_center(win, self.img, (self.x, self.y), self.angle)

        def move(self):
            rad = math.radians(-self.angle)
            vertical_v = -math.cos(rad) * self.vel
            horizontal_v = math.sin(rad) * self.vel
            self.x += horizontal_v
            self.y += vertical_v

        def move_forward(self):
            self.vel = min(self.vel + self.acceleration, self.max_vel)  # threshold is max_vel
            self.move()

        def move_backward(self):
            self.vel = max(self.vel - self.acceleration, -self.max_vel)  # threshold is max_vel
            self.move()

        def reduce_speed(self):
            if self.vel > 0:
                self.vel = max(self.vel - self.acceleration / 4, 0)

            if self.vel < 0:
                self.vel = min(self.vel + self.acceleration / 4, 0)
            self.move()
    ##GAME ASSETS

    GRASS = scaleImage(pygame.image.load("imgs/grass.jpg"), 2.5, 2.5)
    TRACK = pygame.image.load("imgs/track.png")
    FINISH = scaleImage(pygame.image.load("imgs/finish.png"), 0.8, 0.8)
    FINISH_POSITION = (156, 250)

    RED_CAR = scaleImage(pygame.image.load("imgs/red-car.png"), 0.3, 0.3)
    GREEN_CAR = scaleImage(pygame.image.load("imgs/green-car.png"), 0.3, 0.3)
    GREY_CAR = scaleImage(pygame.image.load("imgs/grey-car.png"), 0.3, 0.3)
    PURPLE_CAR = scaleImage(pygame.image.load("imgs/purple-car.png"), 0.3, 0.3)
    CAR_IMGS = [RED_CAR, GREEN_CAR, GREY_CAR, PURPLE_CAR]
    WIDTH, HEIGHT = TRACK.get_width(), TRACK.get_height()
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))

    myimages = [(GRASS, (0, 0)), (TRACK, (0, 0)), (FINISH, FINISH_POSITION)]

    def DrawImages(win, images):
        for image, pos in images:
            WIN.blit(image, pos)

    def DrawCar(win, player_car):
        player_car.draw(win)

    # each player in game will have this class
    class PlayerCar(AbstractCar):
        def __init__(self, max_vel, rotation_vel, CarID,
                     StartPos):
            self.CarID = CarID
            self.IMG = CAR_IMGS[CarID]
            self.START_POS = StartPos  # use self.x better
            super().__init__(max_vel, rotation_vel)  # Call the parent class constructor


    player1 = PlayerCar(4, 4, 0, (180, 260))  # RED
    player2 = PlayerCar(4, 4, 1, (170, 260))  # GREEN
    arr_players_class = [player1, player2]

    context = zmq.Context()
    puller = context.socket(zmq.PULL)
    GUIport = dictionary["GUIPort"]
    puller.connect("tcp://localhost:"+str(GUIport))
    run = True
    pygame.init()
    pygame.font.init()
    MAIN_FONT = pygame.font.SysFont("comicsans", 44)

    mic_img = pygame.image.load('imgs/mic.png').convert_alpha()
    mmic_img = pygame.image.load('imgs/MutedMic.png').convert_alpha()
    H = mic_img.get_height()*0.06
    mmic = button.Button(0, HEIGHT-H, mmic_img, 0.06)
    mic = button.Button(0, HEIGHT-H, mic_img, 0.06)
    MIC = mmic
    micMuted  = 1
    MICS = [mic,mmic]
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = 0
        if MIC.draw(WIN):
            micMuted ^= 1
            MIC = MICS[micMuted]

        pygame.display.update()  # update screen
        gameString = puller.recv_string()
        gameStatus = json.loads(gameString)
        print(f"[WS -> GUI] : {gameStatus}")
        if "winner" in gameStatus.keys() :
            #This is not a gameStatus this is the winner username
            for i in range(1000):
                print(f"Winner is {gameStatus}")
            Helpers.blit_text_center(WIN,MAIN_FONT,text=f"WINNER IS {gameStatus}")
            time.sleep(6)
            kill()


        # print(f"[GUI]{gameStatus}")
        DrawImages(WIN, myimages)
        for key in gameStatus:
            player_id = int(key)
            p_status = gameStatus[key]
            arr_players_class[player_id].x = p_status["posx"]
            arr_players_class[player_id].y = p_status["posy"]
            arr_players_class[player_id].angle = p_status["angle"]
            DrawCar(WIN, arr_players_class[player_id])


    for i in range(5):
        print("PGAME ENDED")
        print("!!! __KILL__ !!!")
    kill()


