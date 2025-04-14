#! /usr/bin/env python3

import sys
sys.path.append("../lib")       # for params
import re, socket, params, os

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

debug, listenPort = paramMap['debug'], paramMap['listenPort']

from threading import Thread;
from encapFramedSock import EncapFramedSock

class Server(Thread):
    def __init__(self, sockName):
        Thread.__init__(self)
        self.sock, self.name = sockName
        self.fsock = EncapFramedSock((self.sock, self.name))
    def run(self):
        print("new thread handling connection from", self.name)
        while True:
            payload = self.fsock.receive(debug)
            if debug: print("rec'd: ", payload)
            if not payload:     # done
                if debug: print(f"thread connected to {self.name} done")
                self.fsock.close()
                return          # exit
            payload += b"!"             # make emphatic!
            self.fsock.send(payload, debug)



if paramMap['usage']:
    params.usage()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # listener socket
bindAddr = ("127.0.0.1", listenPort)
lsock.bind(bindAddr)
lsock.listen(5)
print("listening on:", bindAddr)


        

while True:
    sockAddr = lsock.accept()
    server = Server(sockAddr)
    server.start()


