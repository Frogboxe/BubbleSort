"""
Created by GitHub user "mdebbar"
https://github.com/mdebbar/jsonsocket/
Modified by Frogboxe for Python 3.4

"""

import json, socket
from functools import partial

ENCODING = "utf-8"
SERVER_IP = ("127.0.0.1", 80)

Encode = partial(bytes, encoding=ENCODING)
Decode = partial(str, encoding=ENCODING)

class Server(object):
    client = None
    def __init__(self, addr, maxClients=5):
        self.socket = socket.socket()
        self.socket.bind(addr)
        self.socket.listen(maxClients)
        
    def __del__(self):
        self.Close()

    def Accept(self):
        if self.client:
            self.client.Close()
        self.client, self.addr = self.socket.accept()
        return self

    def Send(self, data):
        _Send(self.client, data)

    def Get(self):
        return _Get(self.client)

    def Close(self):
        if self.client:
            self.client.close()
            self.client = None
        if self.socket:
            self.socket.close()
            self.socket = None


class Client(object):
    socket = None
    def __del__(self):
        self.Close()

    def Connect(self, addr):
        self.socket = socket.socket()
        self.socket.connect(addr)

    def Send(self, data):
        _Send(self.socket, data)

    def Get(self):
        return _Get(self.socket)

    def Close(self):
        if self.socket:
            self.socket.close()
            self.socket = None


## helper functions ##

def _Send(socket, data):
    try:
        serialised = json.dumps(data)
    except (TypeError, ValueError):
        raise Exception('You can only send JSON-serializable data')
    socket.send(Encode(str(len(serialised))+"\n"))
    socket.sendall(Encode(serialised))

def _Get(socket):
    strLen = ""
    char = Decode(socket.recv(1))
    while char != '\n':
        strLen += char
        char = Decode(socket.recv(1))
    total = int(strLen)
    view = memoryview(bytearray(total))
    nextOffset = 0
    while total - nextOffset > 0:
        recvSize = socket.recv_into(view[nextOffset:], total - nextOffset)
        nextOffset += recvSize
    try:
        deserialised = json.loads(Decode(view.tobytes()))
    except (TypeError, ValueError):
        raise Exception('Data received was not in JSON format')
    return deserialised

# TEST
def RECV():
    server = Server(SERVER_IP)
    recv = server.Accept().Get()
    server.Send({'status': 'ok'})
    return recv


def SEND(data):
    client = Client()
    client.Connect(SERVER_IP)
    client.Send(data)
    recv = client.Get()
    return recv






