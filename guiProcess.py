import pygame
from Helpers import *
import zmq
import abstractcar
import json
import eventScript



def guiP():
    carID = -1
    ##GAME ASSETS
    GRASS = scaleImage(pygame.image.load("imgs/grass.jpg"), 2.5, 2.5)
    TRACK = pygame.image.load("imgs/track.png")
    FINISH = scaleImage(pygame.image.load("imgs/finish.png"), 0.8, 0.8)
    FINISH_MASK = pygame.mask.from_surface(FINISH)
    FINISH_POSITION = (156, 250)
    TRACK_BORDER = scaleImage(pygame.image.load("imgs/track-border.png"), 1, 1)

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
    class PlayerCar(abstractcar.AbstractCar):
        IMG = RED_CAR
        START_POS = (180, 200)

        def __init__(self, max_vel, rotation_vel, CarID,
                     StartPos):  # TODO : THIS IS SSHIT AND MAY CAUSE ERROR , MAKE SURE IT WORKS RIGHT
            super().__init__(max_vel, rotation_vel)  # Call the parent class constructor
            self.CarID = CarID
            self.StartPos = StartPos
            self.IMG = CAR_IMGS[CarID]
            self.START_POS = StartPos  # use self.x better

    player1 = PlayerCar(4, 4, 0, (180, 250))  # RED
    player2 = PlayerCar(4, 4, 1, (170, 250))  # GREEN
    arr_players_class = [player1, player2]

    context = zmq.Context()
    puller = context.socket(zmq.PULL)
    puller.connect("tcp://localhost:80819")
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = 0

        pygame.display.update()  # update screen
        gameString = puller.recv_string()
        gameStatus = json.loads(gameString)
        print(f"[GUI]{gameStatus}")
        #TODO : read game status from zmq
        DrawImages(WIN, myimages)
        for key in gameStatus:
            player_id = int(key)
            p_status = gameStatus[key]
            arr_players_class[player_id].x = p_status["posx"]
            arr_players_class[player_id].y = p_status["posy"]
            arr_players_class[player_id].angle = p_status["angle"]
            DrawCar(WIN, arr_players_class[player_id])
            print(f"display updated")

    pygame.quit()
    eventScript.myevent.set()
    print("PGAME ENDED")


