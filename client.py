import asyncio
from websockets.sync.client import connect

def hello(msg):
    with connect("ws://localhost:8765") as websocket:
        websocket.send("Hello world!")
        message = websocket.recv()
        print(f"Received: {message}")

