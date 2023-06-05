import multiprocessing as mp
import time

from Server import main
import zmq
context = zmq.Context()
if __name__ == "__main__" :
    print("MAIN SERVER ")
    ServerProcess = mp.Process(target=main,args=(2,))
    puller = context.socket(zmq.PULL)
    puller.connect("tcp://localhost:"+str(20211))
    while True:
        print("Starting Process")
        ServerProcess.start()
        puller.recv_string()
        print("terminating ....")
        ServerProcess.terminate()
        time.sleep(9)
