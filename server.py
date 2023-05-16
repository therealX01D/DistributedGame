#!/usr/bin/env python

import asyncio
from websockets.server import serve
import json

async def error(websocket, message):
    event = {
        "type": "error",
        "message": message,
    }
    await websocket.send(json.dumps(event))

async def Handler(websocket):
    async for message in websocket:
        dic=json.loads(message)
        if dic["type"]=="init":
            #todo: create a join key and return it
            pass
        print(message)
        await websocket.send(message)

async def main():
    async with serve(Handler, "localhost", 8765):
        await asyncio.Future()  # run forever
        

asyncio.run(main())