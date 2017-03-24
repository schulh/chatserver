#!/usr/bin/env python3.6
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

class rec(threading.Thread):
    def __init__(self, socket):
        threading.Thread.__init__(self)
        self.wrappedSocket = socket

    def run(self):
        print(bcolors.OKBLUE + repr(self.wrappedSocket.getpeername()))
        print(self.wrappedSocket.cipher())
        print("connected... ")
        print(self.wrappedSocket)
        print(bcolors.ENDC)
        while True:
            data = self.wrappedSocket.recv(buffer_size).decode()
            print(bcolors.HEADER + "<<< " + data + bcolors.ENDC)
            if not data:
                print("disconnect")
                sys.exit()

class send(threading.Thread):
    def __init__(self, socket):
        threading.Thread.__init__(self)
        self.wrappedSocket = socket

    def run(self):
        while True:
            message = input(">>> ")
            self.wrappedSocket.send(message.encode())
        
threads = []

try:
    buffer_size = 2048
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    wrappedSocket = ssl.wrap_socket(mySocket,ssl_version=ssl.PROTOCOL_TLSv1_2,\
    certfile='client.crt',keyfile='client.key', ciphers='ECDH')
   # wrappedSocket.settimeout(20)
    wrappedSocket.connect((host, port))
    thread1 = rec(wrappedSocket)
    thread1.start()
    thread2 = send(wrappedSocket)
    thread2.start()
except KeyboardInterrupt:
    print("Can't connect")
    sys.exit()
for t in threads:
    t.join()
