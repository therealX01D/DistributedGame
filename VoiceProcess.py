from vidstream import AudioSender
from vidstream import AudioReceiver
import urllib.request
import threading

external_ip = urllib.request.urlopen('https://ident.me').read().decode('utf8')
print(external_ip)

reviever = AudioReceiver(external_ip,9090)
reviever_thread = threading.Thread(target=reviever.start_server())
clients = ['0.0.0.0']
Voiceport = None
# async def vP():
#         for un in clients:

            # sender = AudioSender(client,5555)
            # sender_thread = threading.Thread(target=sender.start_stream)
            # sender_thread.start()
    # reviever_thread.start()

