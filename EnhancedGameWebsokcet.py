#CLIENT
import asyncio
import json
carID = -1

import keyboard
import websocket
import time
import pygame
EVENTTYPE = pygame.event.custom_type()

READY = 0
# username = input("ENTER : USERNAME")
username = "oa"
server = 'ws://localhost:1761'
async def on_open(ws):
    print("Connection opened")
    UN = json.dumps({"username":username})
    res = ws.send(UN)
    print(f"res of sending un {res}")
#    send_message(ws)

async def on_message(ws, message):
    print("Received message:", message)
    #RECIEVED MESSAGE : message
    try:
        loaded_jsn_msg = json.loads(message)
    except:
        print("NOT JSON MESSAGE")
    print("Received From Server:", message)
    READY = 1
    if message == "READY":
        print("I GOT 'READY' message..")
        send_message(ws)
    elif "carID" in loaded_jsn_msg.keys():
        loadedJsn = json.loads(loaded_jsn_msg)
        carID = int(loadedJsn["car"])
    elif "game" in loaded_jsn_msg.keys():
        processGameStatus(loaded_jsn_msg["game"])


async def processGameStatus(gameStatus):
    print("Processing game status.. GameWS L41")
    print(f"[Game Status]: {gameStatus}") #   {'1' :  {'posx': p.x ,'posy': p.y ,'angle' : p.angle} ,'1' :  {'posx': p.x ,'posy': p.y ,'angle' : p.angle}}
    await pygame.fastevent.post(pygame.event.Event(EVENTTYPE, message=gameStatus))

async def send_message(ws):
    # message = input("Enter a message to send: ")#
    #send user movement
    print("READY , Sending movements")
    while 1:
        message = ""
        if keyboard.is_pressed('a'):
            message = "left"
        if keyboard.is_pressed('d'):
            if(len(message)):
               message += "," + "right"
            else:
                message = "right"
        if keyboard.is_pressed('s'):
            if (len(message)):
                message += "," + "down"
            else:
                message = "down"
        if keyboard.is_pressed('w'):
            if (len(message)):
                message += "," + "up"
            else:
                message = "up"
        print("THERE")
        if(message == ""):
            message = "NULL"
        movement = json.dumps({"movement":message})
        print("MOVEMENT : ",type(movement),"->" , movement)
        res = await ws.send(message)
        print(f"res of movement un {res}")


def on_error(ws, error):
    print("Errorz:", error)

def on_close(ws):
    #TODO : change status of username to disconnected
    print("Connection closed")

# Create a WebSocket instance and connect to the server
ws = websocket.WebSocketApp(server,
                            on_open= on_open,
                            on_message= on_message,
                            on_error=on_error,
                            on_close=on_close)

# Start the WebSocket connection
while 1:
    ws.run_forever()
    print("RECONNECTING")




async def client():
    uri = server  # WebSocket server URI

    async with websockets.connect(uri) as websocket:
        while True:
            message = input("Enter message: ")  # Get user input
            await websocket.send(message)  # Send the message to the server

            response = await websocket.recv()  # Receive response from the server
            print("Received response:", response)

asyncio.run(client())