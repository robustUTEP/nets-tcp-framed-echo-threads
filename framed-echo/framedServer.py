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

from encapFramedSock import EncapFramedSock


if paramMap['usage']:
    params.usage()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # listener socket
bindAddr = ("127.0.0.1", listenPort)
lsock.bind(bindAddr)
lsock.listen(5)
print("listening on:", bindAddr)


while True:
    sockAddr = lsock.accept()
    sock, name = sockAddr
    fsock = EncapFramedSock((sock, name))
    while True:
        payload = fsock.receive(debug)
        if debug: print("rec'd: ", payload)
        if not payload:     # done
            if debug: print(f"client at {name} done")
            fsock.close()
            break
        payload += b"!"             # make emphatic!
        fsock.send(payload, debug)






