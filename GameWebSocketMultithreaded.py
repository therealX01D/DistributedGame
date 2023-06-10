#CLIENT
import multiprocessing as mp

from WSprocess import wsP
from guiProcess import guiP
from keyboardProcess import kbP
from Voice_Client_Process import vcP
import zmq
from ReadFromDict import *
import portsChecker
from Screen1 import get_user_name


if __name__ == "__main__" :
    portsChecker.PortsInit()
    get_user_name()
    wsP = mp.Process(target=wsP)
    pgP = mp.Process(target=guiP)
    kbP = mp.Process(target=kbP)
    vcP = mp.Process(target=vcP)
    wsP.start()
    kbP.start()
    pgP.start()
    vcP.start()
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
    vcP.terminate()






