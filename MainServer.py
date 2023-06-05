import multiprocessing as mp
import time

from Server import main
import zmq
context = zmq.Context()

print("MAIN SERVER ")
ServerProcess = mp.Process(target=main)
puller = context.socket(zmq.PULL)
puller.connect("tcp://localhost:"+str(20211))
while True:
    print("Starting Process")
    ServerProcess.start()
    puller.recv_string()
    print("terminating ....")
    ServerProcess.terminate()
    print("Sleeping 9 seconds")
    time.sleep(9)
