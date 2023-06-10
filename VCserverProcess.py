import socket
import threading

client = []

def vcsP():
    port = 17601
    host = "0.0.0.0"

    server = socket.socket()

    server.bind((host, port))

    server.listen(10) #MAX OF 10 PLAYERS

    while(True):
        conn, addr = server.accept()
        client.append(conn)
        t = threading.Thread(target = send, args = (conn, ))
        t.start()

def send(fromConnection):
        while(True):
                data = fromConnection.recv(4096)
                for cl in client:
                    try:
                        if cl != fromConnection:
                            cl.send(data)
                    except:
                        print("Client Disconnected",cl)
                        client.remove(cl)

