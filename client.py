import asyncio
import json
from websockets.sync.client import connect
def parsedata(x,y):
    data= {"X":x,"y":y}
    return json.dumps(data)
def send(msg):
    with connect("ws://localhost:8765") as websocket:
        websocket.send(msg)
        message = websocket.recv()
        print(f"Received: {message}")

