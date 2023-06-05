#await pauses exec of co-routine
import websockets
import asyncio
import pygame
import Helpers
import math
import json
import socket
# max_players = int(input("ENTER NUMBER OF MAX PLAYERS"))
max_players = int(input("ENTER MAX_PLAYERS"))
curr_players  =0
IPADDRESS = "0.0.0.0"
print("IP ADDRESS" , IPADDRESS)


PORT = 17611
connected_clients_IPs = set()
connected_clients_UNs = set()
connected_clients_WSs = set()
users = set()
IP__username = {}
username__id = {}
id__username = {}
GS = None
GameWinner = None
##PYGAME ASSETS
RED_CAR = Helpers.scaleImage(pygame.image.load("imgs/red-car.png"),0.3,0.3)
GREEN_CAR = Helpers.scaleImage(pygame.image.load("imgs/green-car.png"),0.3,0.3)
GREY_CAR = Helpers.scaleImage(pygame.image.load("imgs/grey-car.png"),0.3,0.3)
PURPLE_CAR = Helpers.scaleImage(pygame.image.load("imgs/purple-car.png"),0.3,0.3)
CAR_IMGS = [RED_CAR,GREEN_CAR,GREY_CAR,PURPLE_CAR]

GRASS = Helpers.scaleImage(pygame.image.load("imgs/grass.jpg"), 2.5, 2.5)
TRACK = pygame.image.load("imgs/track.png")
FINISH= Helpers.scaleImage(pygame.image.load("imgs/finish.png"),0.9,0.9)
TRACK_BORDER = Helpers.scaleImage(pygame.image.load("imgs/track-border.png"),1,1)
TRACK_BORDER_MASK = pygame.mask.from_surface(TRACK_BORDER)


FINISH = pygame.image.load("imgs/finish.png")
FINISH_MASK = pygame.mask.from_surface(FINISH)
FINISH_POSITION = (140, 250)

class AbstractCar:
    def __init__(self, max_vel, rotation_vel):
        self.img = self.IMG
        self.max_vel = max_vel
        self.vel = 0
        self.rotation_vel = rotation_vel
        self.angle = 0
        self.x, self.y = self.START_POS
        self.acceleration = 0.1

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
        self.vel = max(self.vel - self.acceleration, -self.max_vel/2) #threshold is max_vel
        self.move()

    def reduce_speed(self):
        if self.vel>0:
            self.vel = max(self.vel - self.acceleration / 2, 0)

        if self.vel<0:
            self.vel = min(self.vel + self.acceleration / 2, 0)
        self.move()
    def collide(self,mask,x=0,y=0):
        car_mask =  pygame.mask.from_surface(self.img)
        offset = (int(self.x - x),int(self.y - y))
        poi = mask.overlap(car_mask,offset)
        return poi

    def reset(self):
        self.x, self.y = self.START_POS
        self.angle = 0
        self.vel = 0


#each player in game will have this class
class PlayerCar(AbstractCar):
    def __init__(self, max_vel, rotation_vel, CarID,
                 StartPos):
        self.CarID = CarID
        self.IMG = CAR_IMGS[CarID]
        self.START_POS = StartPos
        super().__init__(max_vel, rotation_vel)  # Call the parent class constructor
    def bounce(self):
        self.vel = -self.vel/1.6
        self.move()

player1 = PlayerCar(4,4,0,(180,240))
player2 = PlayerCar(4,4,1,(170,210))
arr_players_class = [player1,player2]
##END: PYGAME ASSETS


#each player has class of his car position and color
EVENTTYPE = pygame.event.custom_type()

# handler processes the message and sends "Success" back to the client
async def handler(ws, path):
    print("inside Handeler")
    #websocket is the client websocket
    async for message in ws:
        global curr_players
        #if recieved message is a new connection
        registered_before = (ws.remote_address[0] in connected_clients_IPs)
        connected_clients_WSs.add(ws)
        print(f"{ws.remote_address , connected_clients_IPs}")
        try:
            if not (type(message) == dict):
                loaded_jsn_mssg = json.loads(message)
        except:
            loaded_jsn_mssg = message

        if type(loaded_jsn_mssg) == str and message =='close':
            connected_clients_WSs.remove(ws)
            break


        print(f"loaded_mssg{loaded_jsn_mssg} , currplayer{curr_players} , maxPlayer{max_players}" )
        if curr_players<max_players and not registered_before:
            connected_clients_WSs.add(ws)
            print(f"GAME NOT READY YET , {curr_players}/{max_players} joined")
            connected_clients_IPs.add(ws.remote_address[0])
            username = loaded_jsn_mssg["username"]
            print(f"username is :{loaded_jsn_mssg['username']}")
            IP = ws.remote_address[0]
            IP__username[IP] = username
            username__id[username] = curr_players
            id__username[curr_players] = username
            print(f"{username} : given ID :{curr_players} ")
            playerCarId = json.dumps({"carID": curr_players})
            curr_players=curr_players+1
            await ws.send(playerCarId)
            #add player to the game
            if curr_players == max_players:
                print(" Broadcasting 'READY'....")
                await broadcast("READY")
                #TODO : SEND OTHER PLAYERS IPs for voice chat

        elif curr_players>=max_players and not registered_before:
            print(f"GAME READY AND YOU ARE NOT INVITED :( ")
            ER_MSG = json.dumps({"ERROR": "GameFull!"})
            ws.send(ER_MSG)



        elif curr_players>=max_players and registered_before:
            carid = username__id[IP__username[ws.remote_address[0]]]
            print(f"GAME READY /RECIEVED FROM ID: {carid} -> {message}")
            if type(loaded_jsn_mssg) == str:
                loaded_jsn_mssg = {'movement' : loaded_jsn_mssg}
            if "movement" in loaded_jsn_mssg.keys():
                movs = loaded_jsn_mssg["movement"]
                print("IT's a movement")
                processMovement(carid,movs)
                prepareGameStatus()
                if GameWinner == None:
                    await ws.send(json.dumps(GS))
                else :
                    await ws.send(json.dumps({"winner" : GameWinner}))


            elif "username" in loaded_jsn_mssg.keys():
                    await ws.send("READY")


def processMovement(id,message):
    print("processing movement.. ")
    #change game status
    # global arr_players_class
    print(f"curr xy{arr_players_class[id].x}, {arr_players_class[id].y}" )
    mover_player_car = arr_players_class[id]
    movements = message.split(",")
    print("moves = ",movements)
    REDUCE = True
    if "l" in movements:
        mover_player_car.rotate(left=1)
    if "r" in movements:
        mover_player_car.rotate(right=1)

    if "u" in movements:
        mover_player_car.move_forward()
        REDUCE = False
    if "d" in movements:
        mover_player_car.move_backward()
        REDUCE = False
    if  REDUCE or message=="NULL":
        mover_player_car.reduce_speed()

    if mover_player_car.collide(TRACK_BORDER_MASK) != None :
        mover_player_car.bounce()
    finish_poi_collide = mover_player_car.collide(FINISH_MASK, *FINISH_POSITION)
    if finish_poi_collide != None:
        if finish_poi_collide[1] == 0:
            mover_player_car.bounce()
        else:
            mover_player_car.reset()
            global GameWinner
            GameWinner = id__username[id]
    print(f"new xy{arr_players_class[id].x}, {arr_players_class[id].y}" )

    print("processed movement")
    print("GOING TO prepare game status")

def prepareGameStatus():
    # Iterate over all connected clients and send the message
    global  arr_players_class
    playerStatus = {}
    for i in range(max_players):
        p = arr_players_class[i]
        playerStatus[str(i)] = {'posx': p.x ,'posy': p.y ,'angle' : p.angle}
    print("Prepared ... ")

    gameStatus = {'game' : playerStatus}
    print(f"gamestaus ready to broadcast : {gameStatus}")
    global GS
    GS = gameStatus


async def broadcast(message):
    # Iterate over all connected clients and send the message
    print("inside BROADCASTING message..")
    for client in connected_clients_WSs:
        try:
            await client.send(message)
            print("EXSTING CLIENT message sent succeffly to ", client.remote_address)
        except:
            print(f"OLD client client ({client.remote_address}) no longer available removing it")
            connected_clients_WSs.remove(client)
    print("FINISHED BROADCASTING")


startServer = websockets.serve(handler, IPADDRESS, PORT)

async def main():
    async with websockets.serve(handler, IPADDRESS, PORT):
        await asyncio.Future()  # run forever

asyncio.run(main())