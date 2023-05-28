#CLIENT
import asyncio
import json
carID = -1
kbbtns = "NULL"
import websocket
import pygame
EVENTTYPE = pygame.event.custom_type()
import threading
import keyboard
import time
import Helpers
import math
WS = None
kbtEV = threading.Event()
wsEV = threading.Event()
GameStatus = None
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

player1 = PlayerCar(4,4,0,(180,250)) #RED
player2 = PlayerCar(4,4,1,(170,250)) #GREEN
arr_players_class = [player1,player2]

##END OF ASSETS
# def GUI():
#     run = 1
#     while run:
#         print("MAIN START")
#         DrawImages(WIN, myimages)
#         pygame.display.update()  # update screen
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 run = 0
#                 break
#         global GameStatus
#
#         for key in GameStatus:
#             player_id = int(key)
#             p_status = GameStatus[key]
#             arr_players_class[player_id].x = p_status["posx"]
#             arr_players_class[player_id].y = p_status["posy"]
#             arr_players_class[player_id].angle = p_status["angle"]
#         pygame.display.update()  # update screen
#
#     pygame.quit()

def kbthread():
    while 1:
        kbtEV.wait()
        # time.sleep(0.2)
        print(f"KBTHREAD")
        global kbbtns
        kbbtns = ""
        print("INSIDE kbthread")
        if keyboard.is_pressed("a"):
            kbbtns = "left"

        if keyboard.is_pressed("d"):
            if(len(kbbtns)):
               kbbtns += "," + "right"
            else:
                kbbtns = "right"
        if keyboard.is_pressed("s"):
            if (len(kbbtns)):
                kbbtns += "," + "down"
            else:
                kbbtns = "down"
        if keyboard.is_pressed("w"):
            if (len(kbbtns)):
                kbbtns += "," + "up"
            else:
                kbbtns = "up"
        print("THERE")
        if(kbbtns == ""):
            kbbtns = "NULL"
        print(kbbtns)
        movement = json.dumps({"movement":kbbtns})
        print("MOVEMENT : ",type(movement),"->" , movement)
        WS.send(movement)
        kbtEV.clear()


# username = input("ENTER : USERNAME")
username = "oaayoub"
server = 'ws://localhost:1761'
def on_open(ws):
    print("Connection opened")
    UN = json.dumps({"username":username})
    ws.send(UN)

def on_message(ws, message):
    wsEV.wait()
    print('(ON MESSAGE)S')
    print("recieved message :::: " , message)

    try:
        loaded_jsn_msg = json.loads(message)
    except:
        print("NOT JSON MESSAGE : ", message)
        loaded_jsn_msg = message

    if message == "READY":
        print("I GOT 'READY' message..")

    elif "carID" in loaded_jsn_msg.keys():
        loadedJsn = json.loads(loaded_jsn_msg)
        global carID
        carID = int(loadedJsn["car"])

    elif "game" in loaded_jsn_msg.keys():
        gameStatus = loaded_jsn_msg["game"]
        print(f"[Game Status]: {gameStatus}")  # {'1' :  {'posx': p.x ,'posy': p.y ,'angle' : p.angle} ,'1' :  {'posx': p.x ,'posy': p.y ,'angle' : p.angle}}
        PygameMessage  = json.dumps(gameStatus)
        pygame.fastevent.post(pygame.event.Event(EVENTTYPE, message=PygameMessage)) #TODO : GAME DOSEN't READ IT (cant reach main)
        print("SENT MESSAGE TO PYGAME")
        time.sleep(0.04)

    print(f"(ON MESSAGE)E")
    wsEV.clear()


def on_error(ws, error):
    print("Error11:", error)

def on_close(wsa, close_status_code, close_msg="close"):
    #TODO : change status of username to disconnected
    print("Connection closing")
    wsa.send(close_msg)
    print("Connection closing")


async def main(future):


    global WS
    ws = websocket.WebSocketApp(server,
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    WS = ws
    wst = threading.Thread(target=ws.run_forever)
    print("Starting WSapp")
    wst.start()
    kbt = threading.Thread(target=kbthread)
    print("Starting kbthread")
    kbt.start()
    # pygamethread = threading.Thread(target=GUI())
    # pygamethread.start()

    while 1:
        ws.run_forever()
        print("RECONNECTING")


if __name__ == "__main__":
    asyncio.run(main())

