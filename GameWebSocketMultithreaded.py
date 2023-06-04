#CLIENT
import multiprocessing as mp
from WSprocess import wsP
from guiProcess import guiP
from keyboardProcess import kbP
import eventScript


if __name__ == "__main__" :
    wsP = mp.Process(target=wsP)
    pgP = mp.Process(target=guiP)
    kbP = mp.Process(target=kbP)
    wsP.start()
    kbP.start()
    pgP.start()
    eventScript.myevent.wait()
    print("GAME EXIT///")
    pgP.terminate()
    kbP.terminate()
    wsP.terminate()






