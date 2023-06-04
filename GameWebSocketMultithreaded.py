#CLIENT
import multiprocessing as mp
from WSprocess import wsP
from guiProcess import guiP
from keyboardProcess import kbP
import zmq
from ReadFromDict import *
import portsChecker
if __name__ == "__main__" :
    portsChecker.PortsInit()
    wsP = mp.Process(target=wsP)
    pgP = mp.Process(target=guiP)
    kbP = mp.Process(target=kbP)
    wsP.start()
    kbP.start()
    pgP.start()
    context = zmq.Context()
    puller = context.socket(zmq.PULL)
    dictionary = read_dictionary_from_file()
    KillPort = dictionary["KillPort"]
    puller.connect("tcp://localhost:"+str(KillPort))
    puller.recv_string()
    print("GAME EXIT///")
    pgP.terminate()
    kbP.terminate()
    wsP.terminate()






