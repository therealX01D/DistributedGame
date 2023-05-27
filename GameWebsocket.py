#CLIENT
import asyncio
import json
carID = -1
message = ""
import pynput
import websocket
import time
import pygame
from pynput import keyboard
import rel
EVENTTYPE = pygame.event.custom_type()
import threading

# import keyboard  # using module keyboard
from pynput.keyboard import Listener




def on_press(key):
    message = ""
    if keyboard.is_pressed('a'):
        message = "left"
    if keyboard.is_pressed('d'):
        if (len(message)):
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
    if (message == ""):
        message = "NULL"
    message


def getButtons():
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
    if(message == ""):
        message = "NULL"
    message
    movement = json.dumps({"movement":message})
    print("MOVEMENT : ",type(movement),"->" , movement)
    ws.send(movement)


# username = input("ENTER : USERNAME")
username = "oa"
server = 'ws://localhost:1761'
def on_open(ws):
    print("Connection opened")
    UN = json.dumps({"username":username})
    ws.send(UN)

def on_message(ws, message):
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
        # send_message(ws) #TODO : undo
    elif "carID" in loaded_jsn_msg.keys():
        loadedJsn = json.loads(loaded_jsn_msg)
        carID = int(loadedJsn["car"])
    elif "game" in loaded_jsn_msg.keys():
        processGameStatus(loaded_jsn_msg["game"])


def processGameStatus(gameStatus):
    print("Processing game status.. GameWS L41")
    print(f"[Game Status]: {gameStatus}") #   {'1' :  {'posx': p.x ,'posy': p.y ,'angle' : p.angle} ,'1' :  {'posx': p.x ,'posy': p.y ,'angle' : p.angle}}
    pygame.fastevent.post(pygame.event.Event(EVENTTYPE, message=gameStatus))

def send_message(ws):
    # message = input("Enter a message to send: ")#
    #send user movement
    # while 1:
    print("READY , Sending movements")

    # message = getButtons()
    #Key = getButtons()
    movement = json.dumps({"movement":message})
    print("MOVEMENT : ",type(movement),"->" , movement)

    ws.send(movement)

def on_error(ws, error):
    print("Errorz:", error)

def on_close(wsa, close_status_code, close_msg):
    #TODO : change status of username to disconnected
    print("Connection closed")

# Create a WebSocket instance and connect to the server
ws = websocket.WebSocketApp(server,
                            on_open= on_open,
                            on_message= on_message,
                            on_error=on_error,
                            on_close=on_close)



# Start the WebSocket connection

ws.run_forever(dispatcher=rel,reconnect=0.5)  # Set dispatcher to automatic reconnection, 0.5 second reconnect delay if connection closed unexpectedly
listener = keyboard.Listener(
    on_press=on_press,
    )
listener.start()
print("RECONNECTING")


##
# async def main(future):
#     async with websockets.serve(handler, IPADDRESS, PORT):
#         await future  # run forever
#
# if __name__ == "__main__":
#     asyncio.run(main())