#!/usr/bin/env python

import asyncio
import websockets
import dbconnect
import chat
import threading
import signal
JOIN={}

mainchat = None
async def handler(websocket):
    connected={websocket}
    #user=chat.user()
    #user.addchatsession(mainchat)
    #mainchat.addusers(user)
    try:    
        
        for chat in mainchat:
            if chat not in dbconnect.cachedChat.keys():
                continue
            if(len(dbconnect.cachedChat[chat])>=1):
                for message in dbconnect.cachedChat[chat]:
                    await websocket.send(message)
        dbconnect.ws=websocket
        for chat in mainchat:
            # prob will change
            if(chat not in dbconnect.users.keys()):
                dbconnect.users[chat]=set()
            dbconnect.users[chat].add(websocket)
        async for message in websocket:            
            await dbconnect.sender(mainchat,message)
    except websockets.ConnectionClosedOK:
        print("connection is closed !!!")
    finally:
        for chat in mainchat:
            dbconnect.users[chat].remove(websocket)


def wrap_async_func(args):
    asyncio.run(dbconnect.start(args))
async def main():
    mainchatroom=chat.chatroom()
    firstchat=chat.chatmsg("hello","0","1") 
    mainchatroom.addchat(firstchat)
    user=chat.user()
    Userkey=user.userkey
    mainchatroom.addusers(user)
    global mainchat
    mainchat=[mainchatroom.chatkey]
    print(len(mainchat))

    _thread = threading.Thread(target=wrap_async_func, args=[mainchat])
    _thread.start()
    loop = asyncio.get_running_loop()
    stop = loop.create_future()
    print("dbstarted") 
    async with websockets.serve(handler, "", 8001):
        await stop # run forever


if __name__ == "__main__":

    asyncio.run(main())
