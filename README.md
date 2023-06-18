# Distributed Multiplayer racing game (a.k.a) DMRG
![Static Badge](https://img.shields.io/badge/License-MIT-orange)
![GitHub contributors](https://img.shields.io/github/contributors/therealX01D/DistributedGame)
## Main Contributers
| Name | Github |
|Omar Ayman Ayoub |![](https://github.com/oaayoub)|
|Omer Ashraf| ![](https://github.com/omer-awwad)|
|Mahmoud Mohamed Omar |![](https://github.com/therealX01D)|
## Description
This is a multiplayer racing game with extra features as voice chat, text chat
### Used Technologies and reasons for using them
- Python

The game is built using python for its ease of use and its mature gui libraries,
- PyGame

 Built on top of pygame library that is for easy building of GUI of the game and do more effort in building the game processes to work efficiently with each other and respond in real time, 

- Websockets

we also decided to use the websocket protocol as it's both bidirectional and non-blocking features that makes any interactive feature run seamlessly and it also can be run on a coroutine architecture,
- Coroutine Architecture

we also decided to make our game run asynchronously by using multiple processes in each of those processes we employed the asyncio async await features that made our IO-bound process not block the flow of the application.
- Redis PubSub

We used the redis pubsub model in the chat app to allow for a multiserver architecture 

### Some of the challenges you faced:
- GIL:
In python there is no pure multithreading support as it implements a global interrupter lock to count for the references of variables and upon which deletes the unreferenced variables(garbage collection) this leads to the prevention of having more then one thread running at a single time this could cause a problem on running multiple cpu-bound processes but doesn't lead to a problem this problem is mitigated by allowing for multiple process for intensive processes
## Installation
download zip file at release section and run run.exe
### using source code
a. You've to run client
1. install dependencies
```bash
 pip install pygame,pyaudio,websocket-client,threading,json,zmq,socket,websocket,pygame-gui,eel 
```
2. run client
```bash
python ClientGame.py
```

b. you've to run on server
1. install dependencies 
```bash
 pip install pygame,math,json,zmq,asyncio,websockets,redis,secrets,logging
```
2. run chat server
```bash
 python  CHATserver.py
```
3. run game server
```bash
 python Server.py
```

## Contributing
Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License

MIT License

Copyright (c) 2023 Mahmoud Mohamed Omar

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
