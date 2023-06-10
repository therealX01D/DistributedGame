import multiprocessing as mp
import time

import Server
import VCserverProcess
import zmq
context = zmq.Context()
puller = context.socket(zmq.PULL)
vis = False
if __name__ == "__main__":
    print("MAIN SERVER ")
    maxP = int(input("Enter Number of Max players"))
    while True:
        ServerProcess = mp.Process(target=Server.RUN, args=(maxP,))
        time.sleep(5)
        VoiceProcess = mp.Process(target=VCserverProcess.vcsP())
        print("Starting Process")
        ServerProcess.start()
        VoiceProcess.start()
        print("Staerted Process....")
        if(vis == False):
            vis = True
            puller.connect("tcp://localhost:" + str(20222))
        puller.recv_string()
        print("I'm Dying xxxx....")

        print("Sleeping 4 seconds")
        time.sleep(4)
        ServerProcess.terminate()
        VoiceProcess.terminate()
        ServerProcess.join(timeout=3)
        VoiceProcess.join(timeout=1)
        if ServerProcess.is_alive():
            ServerProcess.kill()
            "SERVER PROCESS KILLED"
        else :
            print("SERVER PROCESS SURRENDERED")

        if VoiceProcess.is_alive():
            VoiceProcess.kill()
            "VOICE PRINT KILLED"
        else :
            print("VOICE PROCESS SURRENDERED")