import time
import keyboard
import json
import zmq
from ReadFromDict import *

def kbP():
    # print("keyboard Process started..")
    context = zmq.Context()
    pusher = context.socket(zmq.PUSH)
    puller = context.socket(zmq.PULL)
    PortsDictionary = read_dictionary_from_file()
    keyboardPort = PortsDictionary["keyboardPort"]
    KBaccPort = PortsDictionary["KBaccPort"]
    pusher.bind("tcp://*:"+str(keyboardPort))
    puller.connect("tcp://localhost:"+str(KBaccPort))
    print("KB WAITING")
    puller.recv_string()
    print("KB LOOP READY")
    while 1:
        global kbbtns
        kbbtns = ""
        if keyboard.is_pressed("a"):
            kbbtns = "l"

        if keyboard.is_pressed("d"):
            if(len(kbbtns)):
               kbbtns += "," + "r"
            else:
                kbbtns = "r"
        if keyboard.is_pressed("s"):
            if (len(kbbtns)):
                kbbtns += "," + "d"
            else:
                kbbtns = "d"
        if keyboard.is_pressed("w"):
            if (len(kbbtns)):
                kbbtns += "," + "u"
            else:
                kbbtns = "u"
        if(kbbtns == ""):
            kbbtns = "NULL"
        movement = json.dumps({"movement":kbbtns})
        ###print("MOVEMENT : ", movement)
        pusher.send_string(movement)
        time.sleep(0.025)