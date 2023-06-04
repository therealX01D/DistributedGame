import time
import keyboard
import json
import zmq

def kbP():
    print("keyboard Process started..")
    context = zmq.Context()
    pusher = context.socket(zmq.PUSH)
    pusher.bind("tcp://*:80801")
    time.sleep(1)
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
        print("MOVEMENT : ", movement)
        pusher.send_string(movement)
        time.sleep(0.01)