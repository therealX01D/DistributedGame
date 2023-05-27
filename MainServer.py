#await pauses exec of co-routine
import websockets
import asyncio
import pygame
import Helpers
import math
import json
# max_players = int(input("ENTER NUMBER OF MAX PLAYERS"))
max_players = 1
curr_players  =0
IPADDRESS = "localhost"
PORT = 1761
connected_clients_IPs = set()
connected_clients_WSs = set()
users = set()
IP__username = {}
username__id = {}
##PYGAME ASSETS
RED_CAR = Helpers.scaleImage(pygame.image.load("imgs/red-car.png"),0.3,0.3)
GREEN_CAR = Helpers.scaleImage(pygame.image.load("imgs/green-car.png"),0.3,0.3)
GREY_CAR = Helpers.scaleImage(pygame.image.load("imgs/grey-car.png"),0.3,0.3)
PURPLE_CAR = Helpers.scaleImage(pygame.image.load("imgs/purple-car.png"),0.3,0.3)
CAR_IMGS = [RED_CAR,GREEN_CAR,GREY_CAR,PURPLE_CAR]


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
    def __init__(self, max_vel, rotation_vel, CarID,StartPos):
        super().__init__( max_vel, rotation_vel)  # Call the parent class constructor
        self.CarID = CarID
        self.StartPos = StartPos
        IMG = CAR_IMGS[CarID]
        START_POS = StartPos #use self.x better
player1 = PlayerCar(4,4,0,(180,250))
player2 = PlayerCar(4,4,1,(170,250))
arr_players_class = [player1,player2]
##END: PYGAME ASSETS


#each player has class of his car position and color
EVENTTYPE = pygame.event.custom_type()

# handler processes the message and sends "Success" back to the client
async def handler(websocket, path):
    print("inside Handeler")
    #websocket is the client websocket
    async for message in websocket:
        global curr_players
        #if recieved message is a new connection
        registered_before = (websocket.remote_address[0] in connected_clients_IPs) #TODO : later make it with username
        print(f"{websocket.remote_address , connected_clients_IPs}")
        try:
            loaded_jsn_mssg = json.loads(message)
        except:
            loaded_jsn_mssg = message
        print(f"loaded_mssg{loaded_jsn_mssg} , currplayer{curr_players} , maxPlayer{max_players}" )
        if curr_players<max_players and not registered_before:
            connected_clients_WSs.add(websocket)
            print(f"GAME NOT READY YET , {curr_players}/{max_players} joined")
            connected_clients_IPs.add(websocket.remote_address[0])
            username = loaded_jsn_mssg["username"]
            print(f" dict{loaded_jsn_mssg} : username is :{loaded_jsn_mssg['username']}")
            IP = websocket.remote_address[0]
            print(f"IP address is {type(IP)}")
            IP__username[IP] = username
            username__id[username] = curr_players
            playerCarId = json.dumps({"carID": str(curr_players)})
            websocket.send(playerCarId)
            curr_players=curr_players+1
            #add player to the game
            if curr_players == max_players:
                print(" Broadcasting 'READY'....")
                await broadcast("READY")

        elif curr_players>=max_players and not registered_before:
            print(f"GAME READY AND YOU ARE NOT INVITED :( ")
            ER_MSG = json.dumps({"ERROR" : "GameFull!"})
            websocket.send(ER_MSG)
        elif curr_players>=max_players and registered_before:
            print(f"GAME READY AND RECIEVED SOMETHING FROM OLD USER :/ , {message}")
            if type(loaded_jsn_mssg) == str:
                print("MESSAGE IS A STRING ?? " , loaded_jsn_mssg)
                processMovement(websocket,loaded_jsn_mssg)
            elif "movement" in loaded_jsn_mssg.keys():
                movs = loaded_jsn_mssg["movement"]
                print("IT's a movement :) ")
                print(f"type {type(movs)} , {movs}")
                processMovement(websocket,movs)
            elif "username" in loaded_jsn_mssg.keys():
                    await websocket.send("READY")


def processMovement(ws,message):
    print("processing movement.. UwU")
    print(f"[Received From Client]: {message}")

    #change game status
    IP = ws.remote_address[0]
    mover_username = IP__username[IP]
    mover_car_id = username__id[mover_username]
    mover_player_car = arr_players_class[mover_car_id]
    movements = message.split(",")
    REDUCE = True
    if "left" in movements:
        mover_player_car.rotate(left=1)
    if "right" in movements:
        mover_player_car.rotate(right=1)

    if "up" in movements:
        mover_player_car.move_forward()
        REDUCE = False
    if "down" in movements:
        mover_player_car.move_backward()
        REDUCE = False
    if not REDUCE:
        mover_player_car.reduce_speed()
    print("processed movement")
    print("GOING TO prepare game status")
    prepareGameStatus()

async def broadcast(message):
    # Iterate over all connected clients and send the message
    print("inside BROADCASTING message..")
    for client in connected_clients_WSs:
        try:
            await client.send(message)
        except:
            print(f"client ({client.remote_address}) no longer available removing it")
            connected_clients_WSs.remove(client)



def prepareGameStatus():
    # Iterate over all connected clients and send the message
    print("BROADCASTING GAME STATUS ")
    cnt = 0
    playerStatus = {}
    for i in range(max_players):
        p = arr_players_class[i]
        playerStatus[str(i)] = {'posx': p.x ,'posy': p.y ,'angle' : p.angle}

    gameStatus = {'game' : playerStatus}
    DumpedGameStatus = json.dumps(gameStatus)
    print(f"gamestaus ready to broadcast : {gameStatus}")
    #send game status to everyone

    broadcast(DumpedGameStatus)
    print("Broadcasted game status")


startServer = websockets.serve(handler, IPADDRESS, PORT)

async def main():
    async with websockets.serve(handler, "localhost", PORT):
        await asyncio.Future()  # run forever

asyncio.run(main())