#!/usr/bin/env python3.5
import socket
import sys
import argparse
import ssl
import time
from colors import bcolors
import threading
from multiprocessing import Process
import select

parser = argparse.ArgumentParser()
parser.add_argument("--verbosity", help="increase output verbosity")
parser.add_argument("--ip", help="listening ip")
parser.add_argument("--port", help="listening port", type=int)
args = parser.parse_args()
if args.verbosity:
    print("verbosity turned on")

if args.ip:
    host = args.ip
else:
    host = '127.0.0.1'
if args.port:
    port = args.port
else:
    port = 50000

class ChatClient():
    def __init__(self, socket):
        self.socket = wrappedSocket

    def run(self):
        print(bcolors.OKBLUE + repr(wrappedSocket.getpeername()))
        print(wrappedSocket.cipher())
        print("connected... ")
        print(wrappedSocket)
        print(bcolors.ENDC)
        while True:
            socket_list = [wrappedSocket]
            # Get the list sockets which are readable
            read_sockets, write_sockets, error_sockets = \
            select.select(socket_list , [], [])
            for socket in socket_list:
                if socket == wrappedSocket:
                    data = wrappedSocket.recv(buffer_size).decode()
                    if not data:
                        print("error")
                        sys.exit()
                    else:
                        print(bcolors.HEADER + "<<< " + data + bcolors.ENDC)
                else:
                    message = input(">>> ")
                    wrappedSocket.send(message.encode())


try:
    buffer_size = 2048
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    wrappedSocket = ssl.wrap_socket(mySocket,ssl_version=ssl.PROTOCOL_TLSv1_2,\
    certfile='client.crt',keyfile='client.key', ciphers='ECDH')
    wrappedSocket.settimeout(2)
    wrappedSocket.connect((host, port))
    client = ChatClient(wrappedSocket)
    client.run()
except KeyboardInterrupt:
    print("Can't connect")
    sys.exit()
#except KeyboardInterrupt:
#    print("fuck you")
#    sys.exit("exit")
