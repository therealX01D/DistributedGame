#CLIENT
import asyncio
import keyboard
import websocket
import time

server = 'ws://localhost:1761'
def on_open(ws):
    print("Connection opened")
    send_message(ws)

def on_message(ws, message):
    print("Received message:", message)
    send_message(ws)

def on_error(ws, error):
    print("Error:", error)

def on_close(ws):
    print("Connection closed")

def send_message(ws):
    # message = input("Enter a message to send: ")#
    print("HERE")
    message = ""
    if keyboard.is_pressed('a'):
        message = "left"
    if keyboard.is_pressed('d'):
        if(len(message)):
           message += "," + "right"
        else:
            message = "right"
    if keyboard.is_pressed('s'):
        if (len(message)):
            message += "," + "down"
        else:
            message = "down"
    if keyboard.is_pressed('w'):
        if (len(message)):
            message += "," + "up"
        else:
            message = "up"
    print("THERE")
    time.sleep(0.01)
    if(message == ""):
        message = "NULL"
    print(message)
    ws.send(message)

# Create a WebSocket instance and connect to the server
ws = websocket.WebSocketApp(server,
                            on_open=on_open,
                            on_message=on_message,
                            on_error=on_error,
                            on_close=on_close)

# Start the WebSocket connection
while 1:
    ws.run_forever()
    print("RECONNECTING")