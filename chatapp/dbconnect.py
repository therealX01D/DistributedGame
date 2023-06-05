import asyncio
import redis.asyncio as redis
import json
import secrets
STOPWORD = "STOP"
r = redis.from_url("redis://default:COs2t56kFoF9DmpG66qFIFoeJVupv3F1@redis-10943.c244.us-east-1-2.ec2.cloud.redislabs.com:10943")

ws = None
users = {}
#multiserver consistency issues
userkeytoname = {}
cachedChat={}
###############################
# todo : implement a specific channel for each and update on publishing
async def sender(chatroom:list,stringe:str):
    jsonrec=json.loads(stringe)
    if jsonrec["type"]=="chat":
        for chat in chatroom:
            jsonrec["usrname"]=userkeytoname[jsonrec["userid"]]
            processed=json.dumps(jsonrec)
            await r.publish(chat, processed)
            # prob will change
            # if(chat not in users.keys()):
            #     users[chat]=set()
            # users[chat].add(ws)
            # should transfer to recieving 
            if(chat not in cachedChat.keys()):
                cachedChat[chat]=list()
            cachedChat[chat].append(processed)
            print("chatroom",chat," has ",processed)
    elif jsonrec["type"]=="adduser":
        tmp = secrets.token_urlsafe(12)
        userkeytoname[tmp] = jsonrec["usrname"]
        event={
            "type":"acceptinit",
            "userid":tmp
               }
        print("initialized user",event)
        await ws.send(json.dumps(event))

async def reader(channel: redis.client.PubSub):
    while True:

        message = await channel.get_message(ignore_subscribe_messages=True)
        if message is not None:    
            print(f"(Reader) Message Received: {message}")
            chat = message["channel"].decode()
            print(users[chat])
            li = users[chat]
           
            await asyncio.gather(*[wsi.send(message["data"].decode()) for wsi in li])
            if message["data"].decode() == STOPWORD:
                print("(Reader) STOP")
                break
       
            

async def start(chatrooms):
    
    async with r.pubsub() as pubsub:
        
        await pubsub.subscribe(*chatrooms)
        print("subscribed to ",chatrooms)
        future = asyncio.create_task(reader(pubsub))

        # await r.publish("channel:1", "Hello")
        # await r.publish("channel:2", "World")
        # await r.publish("channel:1", STOPWORD)

        await future

