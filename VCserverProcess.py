import socket
import threading

clients = []

def vcsP():
    print("Hello voice Server")
    port = 17601
    host = "0.0.0.0"

    server = socket.socket()

    server.bind((host, port))

    server.listen(10) #MAX OF 10 PLAYERS

    while(True):
        conn, addr = server.accept()
        print("RECIEVED CONNECTION FROM : ",addr)
        clients.append(conn)
        t = threading.Thread(target = send, args = (conn, ))
        t.start()

def send(fromConnection):
        while(True):
                data = fromConnection.recv(4096)
                print("RECIEVED AUDIOP FROM ",fromConnection)
                print("CLIENT LIST", clients)
                for cl in clients:
                    try:
                        if cl != fromConnection:
                            cl.send(data)
                    except:
                        print("Client Disconnected",cl)
                        clients.remove(cl)

