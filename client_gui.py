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
import configparser
from appJar import gui

parser = argparse.ArgumentParser()
parser.add_argument("--verbosity", help="increase output verbosity")
parser.add_argument("--ip", help="listening ip")
parser.add_argument("--port", help="listening port", type=int)
args = parser.parse_args()
if args.verbosity:
    print("verbosity turned on")

if args.ip:
    ip = args.ip
else:
    ip = '127.0.0.1'
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
            print(bcolors.HEADER + "\n<<< " + data + bcolors.ENDC)
            app.infoBox("Reply: ", str(data))
            if not data:
                print("disconnect")
                sys.exit()

class send(threading.Thread):
    def __init__(self, socket):
        threading.Thread.__init__(self)
        self.wrappedSocket = socket

    def run(self):
        print("recieved message!")
        test = "lol"
        self.wrappedSocket.send(test.encode())

def press(btn):
    if btn=="Cancel":
        sys.exit()
    else:
        test = app.getEntry("msg")
        wrappedSocket.send(test.encode())
        app.clearEntry("msg")

threads = []

try:

    buffer_size = 2048
    mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    wrappedSocket = ssl.wrap_socket(mySocket,ssl_version=ssl.PROTOCOL_TLSv1_2,\
    certfile='client.crt',keyfile='client.key', ciphers='ECDH')
    wrappedSocket.connect((ip, port))
    thread1 = rec(wrappedSocket)
    thread1.start()
    app = gui()
    app.addLabel("title", "Welcome to the Chatroom", 0, 0, 2)
    app.setLabelBg("title", "red")
    app.addLabel("msg", "Message:", 2, 0)
    app.addEntry("msg", 2, 1, 10)
    app.addButtons(["Send", "Cancel"], press, 3, 0, 2) # Row 3,Column 0,Span 2
    app.setEntryFocus("msg")
    thread2 = app.go()
    thread2.start()
except KeyboardInterrupt:
    print("Can't connect")
    sys.exit()
for t in threads:
    t.join()
