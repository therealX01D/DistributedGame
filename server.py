import websockets
import asyncio
import pygame

IPADDRESS = "localhost"
PORT = 1761


# handler processes the message and sends "Success" back to the client
async def handler(websocket, path):
    async for message in websocket:
        await processMsg(message)
        await websocket.send("Success")

async def processMsg(message):
    print(f"[Received From Client]: {message}")
    pygame.fastevent.post(pygame.event.Event(EVENTTYPE, message=message))

async def main(future):
    async with websockets.serve(handler, IPADDRESS, PORT):
        await future  # run forever

if __name__ == "__main__":
    asyncio.run(main())