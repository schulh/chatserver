#!/usr/bin/env python3.6
import socket
import sys
import argparse
import ssl
import time
from colors import bcolors
import threading
from multiprocessing import Process

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
        #self.ip =  ip
        #self.port = port
        self.socket = wrappedSocket

    def run(self):
        print(bcolors.OKBLUE + repr(wrappedSocket.getpeername()))
        print(wrappedSocket.cipher())
        print("connected... ")
        print(bcolors.ENDC)

    def send(self):
        while True:
            message = input(">>> ")
            wrappedSocket.send(message.encode())
        wrappedSocket.close()

    def rec(self):
        print("test")
        while True:
            data = wrappedSocket.recv(buffer_size).decode()
            #sys.stdout(data)
            print(bcolors.HEADER + "<<< " + data + bcolors.ENDC)
            time.sleep(1)
       

try:
    buffer_size = 2048
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    wrappedSocket = ssl.wrap_socket(mySocket,ssl_version=ssl.PROTOCOL_TLSv1_2, \
    certfile='client.crt',keyfile='client.key', ciphers='ECDH')
    wrappedSocket.connect((host, port))
    client = ChatClient(wrappedSocket)
#    p2 = Process(target=client.rec())
    p1 = Process(target=client.send())
 #   p2.start()
    p1.start()
    #client.run()
except KeyboardInterrupt:
    print("fuck you")
    sys.exit("exit")
