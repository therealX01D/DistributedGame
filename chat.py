import secrets
import json
class Encoder(json.JSONEncoder):
        def default(self, o):
            return o.__dict__

class decodeclass():
    def __init__(self):
        pass
    def getmsg(self):
        return json.dumps(self,indent=4, cls=Encoder)
class chatmsg(decodeclass) :
    def __init__(self,text,date,userid):
        super().__init__()
        self.text=text
        self.date=date
        self.userid=userid


class chatroom(decodeclass):
    def __init__(self):
        super().__init__()
        self.chatkey=secrets.token_urlsafe(12)
        self.chatmsg=[]
        self.users=[]
    def addchat(self,msg):
        self.chatmsg.append(msg)
    def addusers(self,usr):
        self.users.append(usr) 
class user(decodeclass):
    def __init__(self):
        super().__init__()
        self.userkey=secrets.token_urlsafe(12)
        self.chatsessions=[]
    def addchatsession(self,chatsession):
        self.chatsessions.append(chatsession)
class Payload(object):
   def __init__(self, j):
         self.__dict__ = json.loads(j)

if __name__=="__main__":
    u = user()
    c = chatmsg("hello","it40u3",u.getmsg()[5:9])
    cs = chatroom()
    cs.addusers(u)
    cs.addchat(c)
    print(u.getmsg())
    print(c.getmsg())
    print(cs.getmsg())

