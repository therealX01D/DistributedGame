import socket
import threading
import pyaudio
import json
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
    #        audio_settings = {"mic_on":micOn , "sound_on":headsetOn}

    def send():
        while (True):
            with open('AUDIO_SETTINGS.json', 'r') as openfile:
                try:
                    audio_settings = json.loads(openfile)
                except:
                    print("couldn't read audio")
                    audio_settings = {"mic_on":True , "sound_on":True}
            try:
                data = input_stream.read(Chunks)
                if audio_settings["mic_on"]:
                    client.send(data)
            except:
                break

    def receive():
        while (True):
            with open('AUDIO_SETTINGS.json', 'r') as openfile:
                try:
                    audio_settings = json.loads(openfile)
                except:
                    print("couldn't read audio")
                    audio_settings = {"mic_on":True , "sound_on":True}
            try:
                data = client.recv(Chunks)
                if audio_settings["sound_on"]:
                    output_stream.write(data)
            except:
                break

    t1 = threading.Thread(target=send)
    t2 = threading.Thread(target=receive)

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    input_stream.stop_stream()
    input_stream.close()
    output_stream.stop_stream()
    output_stream.close()
    p.terminate()
