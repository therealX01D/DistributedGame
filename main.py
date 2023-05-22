import client
def init_game():
    res = client.send({"type":"initgameroom"})

