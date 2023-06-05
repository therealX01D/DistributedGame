import time
import websocket
import json
import threading
import zmq
from ReadFromDict import *
WS = None
pusher = None
dicitonary = read_dictionary_from_file()
READY = False
username = "oaayoub"
def on_open(ws):
    print("Connection opened")
    global  username
    with open("username.pkl", "rb") as file:
        username = pickle.load(file)
    UN = json.dumps({"username":username})
    ws.send(UN)
    #TODO : Errors here for username check main GameWeb...
def on_message(ws, message): #recieve
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
            global READY
            READY = True

    if isinstance(loaded_jsn_msg, dict):
        print("ITS DICT")
        if "carID" in loaded_jsn_msg.keys():
            global carID
            carID = int(loaded_jsn_msg["carID"])

        elif "game" in loaded_jsn_msg.keys():
            gameStatus = loaded_jsn_msg["game"]
            print(f"[Game Status]: {gameStatus}")  # {'1' :  {'posx': p.x ,'posy': p.y ,'angle' : p.angle} ,'1' :  {'posx': p.x ,'posy': p.y ,'angle' : p.angle}}
            global pusher
            pusher.send_string(json.dumps(gameStatus))


    print(f"(ON MESSAGE) ..E") #

def on_error(ws, error):
    print("*Error*", error)

def on_close(wsa, close_status_code, close_msg="close"):
    #TODO : change status of username to disconnected
    print("Connection closing")
    wsa.send(close_msg)
    print("Connection closing")

def sendMovementThread():
    print("Send movement thread")
    global WS , READY
    context = zmq.Context()
    puller = context.socket(zmq.PULL)
    KeyboardPort = dicitonary["keyboardPort"]
    puller.connect("tcp://localhost:"+str(KeyboardPort))
    while True:
        movement = puller.recv_string()
        if READY:
            WS.send(movement)


def wsP():
    global pusher
    context = zmq.Context()
    pusher = context.socket(zmq.PUSH)
    GUIPort = dicitonary["GUIPort"]
    pusher.bind("tcp://*:"+str(GUIPort))
    time.sleep(1)
    server = 'ws://35.158.245.102:17611'
    ws = websocket.WebSocketApp(server,
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    wst = threading.Thread(target=ws.run_forever)
    global WS
    WS = ws
    wst.start()
    smt = threading.Thread(target=sendMovementThread)
    time.sleep(1)
    smt.start()
    # while 1:
    #     ws.run_forever()
    #     print("RECONNECTING")