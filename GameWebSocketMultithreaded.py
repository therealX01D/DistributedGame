#CLIENT
import asyncio
import json
carID = -1
kbbtns = "NULL"
import websocket
import pygame
import threading
import keyboard
import time
import Helpers
import math
WS = None
kbtEV = threading.Event()
wsEV = threading.Event()
guiEV = threading.Event()
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


def kbthread():
    while 1:
        kbtEV.wait()
        print(f"KB THREAD..")
        global kbbtns
        kbbtns = ""
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
    kbtEV.clear()
    print('(ON MESSAGE) ..S')
    print(f"[Received From Server] {message}")

    try:
        loaded_jsn_msg = json.loads(message)
    except:
        print("NOT JSON MESSAGE : ", message)
        loaded_jsn_msg = message

    print(f"before process msgtype ({type(loaded_jsn_msg)}) => ({message})")
    if isinstance(loaded_jsn_msg, str):
        if message == "READY":
            print("I GOT 'READY' message..")

    if isinstance(loaded_jsn_msg, dict):
        print("ITS DICT")
        if "carID" in loaded_jsn_msg.keys():
            global carID
            carID = int(loaded_jsn_msg["carID"])

        elif "game" in loaded_jsn_msg.keys():
            gameStatus = loaded_jsn_msg["game"]
            print(f"[Game Status]: {gameStatus}")  # {'1' :  {'posx': p.x ,'posy': p.y ,'angle' : p.angle} ,'1' :  {'posx': p.x ,'posy': p.y ,'angle' : p.angle}}
            global GameStatus
            GameStatus = gameStatus
            print("GLOBAL GAME STATUS CHANGING ....")
            DrawImages(WIN, myimages)
            print("BEFORE UPD DISPLAY")
            pygame.display.update()  # update screen
            print("UPDATE DISPLAY")
            for key in gameStatus:
                player_id = int(key)
                print(f"key({key}) player{player_id} :> status {gameStatus[key]}")
                p_status = gameStatus[key]
                arr_players_class[player_id].x = p_status["posx"]
                arr_players_class[player_id].y = p_status["posy"]
                arr_players_class[player_id].angle = p_status["angle"]
                print(f"[player C] :{type(arr_players_class[player_id])}")
                DrawCar(WIN,arr_players_class[player_id])
                print("[[Game status changed]]")
            pygame.display.update()  # update screen
    #TODO: If there are problems when connecting lots of players
    # DUE TO LOTS OF MESSAGES FROM EVERYONE
    # .SLEEP THIS THREAD FOR A WHILE  (uncomment next line)
    #time.sleep(0.001)

    pygame.display.update()  # update screen
    print(f"(ON MESSAGE) ..E")
    print("setted GUI ev")
    kbtEV.set()


def on_error(ws, error):
    print("*Error*", error)

def on_close(wsa, close_status_code, close_msg="close"):
    #TODO : change status of username to disconnected
    print("Connection closing")
    wsa.send(close_msg)
    print("Connection closing")


# async def main(future):
def s():
    pygame.init()
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


# if __name__ == "__main__":
#     asyncio.run(main())
s()

