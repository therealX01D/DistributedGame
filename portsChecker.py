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
    while is_port_reserved(keyboardPort):
        keyboardPort+=1
    while is_port_reserved(keyboardPort):
        GUIPort+=1
    while is_port_reserved(keyboardPort):
        KillPort+=1
    dictionary = {"keyboardPort": keyboardPort, "GUIPort": GUIPort, "KillPort": KillPort}
    filename = "ports.pkl"
    write_dictionary_to_file(dictionary, filename)
    print("PORTS GENERATED ✓")

