import socket
import pickle
def is_port_reserved(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('localhost', port)) == 0

def write_dictionary_to_file(dictionary, filename):
    with open(filename, "wb") as f:
        pickle.dump(dictionary, f)


def PortsInit() :
    keyboardPort = 60001
    GUIPort = 60002
    KillPort = 60003
    VoicePort = 60004
    KBaccPort = 60005
    while is_port_reserved(keyboardPort):
        keyboardPort+=1
    while is_port_reserved(GUIPort):
        GUIPort+=1
    while is_port_reserved(KillPort):
        KillPort+=1
    while is_port_reserved(VoicePort):
        VoicePort+=1
    while is_port_reserved(KBaccPort):
        KBaccPort+=1
    dictionary = {"keyboardPort": keyboardPort, "GUIPort": GUIPort, "KillPort": KillPort , "VoicePort":VoicePort,"KBaccPort":KBaccPort}
    filename = "ports.pkl"
    write_dictionary_to_file(dictionary, filename)
    print("PORTS GENERATED ✓")

