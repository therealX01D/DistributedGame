import asyncio
import redis.asyncio as redis
#import rediscluster 
#from redis.cluster import RedisCluster as Redis
import json
import secrets
import logging
STOPWORD = "STOP"
#r = redis.from_url("redis://elustercfg.gamerediscluster.nfqxhj.euw2.cache.amazonaws.com:6379")
logging.basicConfig(level=logging.INFO)
r = redis.from_url("redis://chatappsingleshard.nfqxhj.ng.0001.euw3.cache.amazonaws.com:6379")
#r = redis.cluster.RedisCluster(host="clustercfg.distgamechat.nfqxhj.euw3.cache.amazonaws.com",port="6379", decode_responses=True,require_full_coverage=False)
#r = r.ClusterPubSub

if r.ping():
    logging.info("Connected to Redis")
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
            jsonrec["usrname"] = userkeytoname[jsonrec["userid"]]
            processed=json.dumps(jsonrec)
            await r.publish(chat, processed)
            # prob will change
            # if(chat not in users.keys()):
            #     users[chat]=set()
            # users[chat].add(ws)
            # should transfer to recieving 
            if(chat not in cachedChat.keys()):
                cachedChat[chat]=list()
            jsonrec["cached"]="true"
            processed2=json.dumps(jsonrec)
            cachedChat[chat].append(processed2)
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

async def reader(channel:redis.client.PubSub):
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

                                      