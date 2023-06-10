import socket
import threading
import pyaudio
#TODO : put them back inside
def vcP():
    #here imports
    print("Hello Voice world")
    client = socket.socket()
    host = '35.158.245.102' #later initiate another server for chatting
    port = 17601
    p = pyaudio.PyAudio()

    Format = pyaudio.paInt16
    Chunks = 4096
    Channels = 2
    Rate = 44100

    input_stream = p.open(format=Format,
                          channels=Channels,
                          rate=Rate,
                          input=True,
                          frames_per_buffer=Chunks)

    output_stream = p.open(format=Format,
                           channels=Channels,
                           rate=Rate,
                           output=True,
                           frames_per_buffer=Chunks)
    client.connect((host, port))

    def send():
        while (True):
            try:
                data = input_stream.read(Chunks)
                client.send(data)
            except:
                print("ERROR in sending")

    def receive():
        while (True):
            try:
                data = client.recv(Chunks)
                output_stream.write(data)
            except:
                print("ERROR IN RECIEVING AUDIO")

    t1 = threading.Thread(target=send)
    t2 = threading.Thread(target=receive)

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    input_stream.stop()
    input_stream.close()
    output_stream.stop()
    output_stream.close()
    p.terminate()
