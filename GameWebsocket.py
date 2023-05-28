#CLIENT
import asyncio
import json
message = "NULL"
import websocket
import pygame
EVENTTYPE = pygame.event.custom_type()
import threading
import keyboard
import time

def send_message(ws):
    message = ""
    print("HERE")
    if keyboard.is_pressed("a"):
        message = "left"
    print("HERE")

    if keyboard.is_pressed("d"):
        if(len(message)):
           message += "," + "right"
        else:
            message = "right"
    if keyboard.is_pressed("s"):
        if (len(message)):
            message += "," + "down"
        else:
            message = "down"
    if keyboard.is_pressed("w"):
        if (len(message)):
            message += "," + "up"
        else:
            message = "up"
    print("THERE")
    if(message == ""):
        message = "NULL"
    print(message)
    movement = json.dumps({"movement":message})
    print("MOVEMENT : ",type(movement),"->" , movement)
    time.sleep(0.01)

    ws.send(movement)



# username = input("ENTER : USERNAME")
username = "oaayoub"
server = 'ws://localhost:1761'

def on_open(ws):
    print("Connection opened")
    UN = json.dumps({"username":username})
    ws.send(UN)

def on_message(ws, message):
    print("Received message:", type(message))
    #RECIEVED MESSAGE : message
    try:
        loaded_jsn_msg = json.loads(message)
    except:
        print("NOT JSON MESSAGE")
        loaded_jsn_msg = message
    print("Received From Server:", message)
    if message == "READY":
        print("I GOT 'READY' message..")
    elif "carID" in loaded_jsn_msg.keys():
        loadedJsn = json.loads(loaded_jsn_msg)
        carID = int(loadedJsn["car"])
    elif "game" in loaded_jsn_msg.keys():
        processGameStatus(loaded_jsn_msg["game"])
    print(f"(ON MESSAGE)")
    send_message(ws)
    print("MESSAGE SENT")



def processGameStatus(gameStatus):
    print("Processing game status.. GameWS L41")
    print(f"[Game Status]: {gameStatus}") #   {'1' :  {'posx': p.x ,'posy': p.y ,'angle' : p.angle} ,'1' :  {'posx': p.x ,'posy': p.y ,'angle' : p.angle}}
    pygame.fastevent.post(pygame.event.Event(EVENTTYPE, message=gameStatus))

def on_error(ws, error):
    print("Errorz:", error)

def on_close(wsa, close_status_code, close_msg):
    #TODO : change status of username to disconnected
    print("Connection closed")


async def main(future):
    ws = websocket.WebSocketApp(server,
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    wst = threading.Thread(target=ws.run_forever)
    print("Starting WSapp")
    wst.start()

if __name__ == "__main__":
    asyncio.run(main())
