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
WS = None

def kbthread():
    while 1:
        time.sleep(0.2)
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



# username = input("ENTER : USERNAME")
username = "oaayoub"
server = 'ws://localhost:1761'
def on_open(ws):
    print("Connection opened")
    UN = json.dumps({"username":username})
    ws.send(UN)

def on_message(ws, message):
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
        time.sleep(0.4)

        print("SENT MESSAGE TO PYGAME")
    print(f"(ON MESSAGE)E")




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
    # wst = threading.Thread(target=ws.run_forever)
    # print("Starting WSapp")
    # wst.start()
    kbt = threading.Thread(target=kbthread)
    print("Starting kbthread")
    kbt.start()
    while 1:
        ws.run_forever()
        print("RECONNECTING")


if __name__ == "__main__":
    asyncio.run(main())

