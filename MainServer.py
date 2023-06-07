import multiprocessing as mp
import time

import Server
import zmq
context = zmq.Context()
puller = context.socket(zmq.PULL)
vis = False
if __name__ == "__main__":
    print("MAIN SERVER ")
    maxP = int(input("Enter Number of Max players"))
    while True:
        ServerProcess = mp.Process(target=Server.RUN, args=(maxP,))
        print("Starting Process")
        ServerProcess.start()
        if(vis == False):
            vis = True
            puller.connect("tcp://localhost:" + str(20222))
        puller.recv_string()
        print("I'm Dying xxxx....")

        print("Sleeping 4 seconds")
        time.sleep(4)
        ServerProcess.join()

        ServerProcess.terminate()
