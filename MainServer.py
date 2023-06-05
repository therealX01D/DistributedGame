import multiprocessing as mp
import time

from Server import main
import zmq
context = zmq.Context()
if __name__ == "__main__" :
    ServerProcess = mp.Process(target=main)
    puller = context.socket(zmq.PULL)
    puller.connect("tcp://localhost:"+str(20211))
    while True:
        ServerProcess.start()
        puller.recv_string()
        ServerProcess.terminate()
        time.sleep(9)
