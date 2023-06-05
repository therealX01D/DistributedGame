import socket
import pickle
def find_port(port=8000):
    """Find a port not in ues starting at given port"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        if s.connect_ex(("localhost", port)) == 0:
            return find_port(port=port + 1)
        else:
            return port

def write_dictionary_to_file(dictionary, filename):
    with open(filename, "wb") as f:
        pickle.dump(dictionary, f)


def PortsInit() :
    keyboardPort = find_port()
    GUIPort = find_port(keyboardPort+1)
    KillPort = find_port(GUIPort+1)
    VoicePort = find_port(KillPort+1)
    KBaccPort = find_port(VoicePort+1)
    dictionary = {"keyboardPort": keyboardPort, "GUIPort": GUIPort, "KillPort": KillPort , "VoicePort":VoicePort,"KBaccPort":KBaccPort}
    filename = "ports.pkl"
    write_dictionary_to_file(dictionary, filename)
    print("PORTS GENERATED ✓")

