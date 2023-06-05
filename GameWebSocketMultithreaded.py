#CLIENT
import multiprocessing as mp
import time

from WSprocess import wsP
from guiProcess import guiP
from keyboardProcess import kbP
import zmq
from ReadFromDict import *
import portsChecker
import pygame
import pygame_gui
username = "oaayoub"
def take_username(txt):
    txt = str(txt)
    with open("username", "wb") as f:
        f.write(txt.encode())


def get_user_name():
    pygame.init()

    WIDTH, HEIGHT = 400, 50
    SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Text Input in PyGame")

    manager = pygame_gui.UIManager((WIDTH, HEIGHT))

    text_input = pygame_gui.elements.UITextEntryLine(relative_rect=pygame.Rect((0, 0), (300, 50)), manager=manager,
                                                     object_id='#main_text_entry')

    clock = pygame.time.Clock()
    done = False
    while True:
        UI_REFRESH_RATE = clock.tick(60) / 1000
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                break
            if (event.type == pygame_gui.UI_TEXT_ENTRY_FINISHED and
                    event.ui_object_id == '#main_text_entry'):
                txt = event.text
                global username
                username = txt
                print(username)
                take_username(txt)
                done = True
                break

            manager.process_events(event)

        manager.update(UI_REFRESH_RATE)

        SCREEN.fill("white")

        manager.draw_ui(SCREEN)

        pygame.display.update()
        if done:
            pygame.display.quit()
            break




if __name__ == "__main__" :
    portsChecker.PortsInit()
    wsP = mp.Process(target=wsP)
    pgP = mp.Process(target=guiP)
    kbP = mp.Process(target=kbP)
    get_user_name()
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






