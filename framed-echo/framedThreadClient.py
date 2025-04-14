#! /usr/bin/env python3

# Echo client program
import socket, sys, re
from threading import Thread;

sys.path.append("../lib")       # for params
import params

from encapFramedSock import EncapFramedSock


switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )


progname = "framedClient"
paramMap = params.parseParams(switchesVarDefaults)

server, usage, debug  = paramMap["server"], paramMap["usage"], paramMap["debug"]

if usage:
    params.usage()


try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)

addrFamily = socket.AF_INET
socktype = socket.SOCK_STREAM
addrPort = (serverHost, serverPort)

class Client(Thread):
    def __init__(self):
        Thread.__init__(self)
    def run(self):
        print("client started")
        sock = socket.socket(addrFamily, socktype)

        if sock is None:
            print('could not open socket')
            sys.exit(1)
        sock.connect(addrPort)
        name = sock.getsockname()
        print(f"client {name} connected")
        fsock = EncapFramedSock((sock, name))
        fsock.send( b"hello world", debug)
        print(f"client {name} received:", fsock.receive(debug))

        fsock.send( b"hello world", debug)
        fsock.shutdown()
        print(f"client {name} received:", fsock.receive(debug))

        fsock.close()
        print(f"client {name} done")

clients = [ Client() for _ in range(10) ]
for c in clients:
    c.start()

for c in clients:
    c.join()
