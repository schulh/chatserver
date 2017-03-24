#!/usr/bin/env python3.6

import threading
import socket
import ssl
import argparse
from colors import bcolors
import time

class SSLServer(threading.Thread):
    def __init__(self, conn, addr):
        threading.Thread.__init__(self)
        self.conn = conn
        self.addr = addr
        print(bcolors.OKGREEN + "[+] New connection from " + str(conn) + bcolors.ENDC)

    def run(self):
        data = "Client " + str(addr) + " connected"
        SSLServer.broadcast(self, data, self.conn, self.addr)
        #SSLServer.broadcast(self, welcome, conn)
        while True:
            data = self.conn.recv(buffer_size).decode()
            if data:
                SSLServer.broadcast(self, data, self.conn, self.addr)
            else:
                if conn in socketList:
                    socketList.remove(conn)
                    data = "Client " + str(addr) + "disconnected"
                    SSLServer.broadcast(self, data, self.conn, self.addr)
    def broadcast(self, data, conn, addr):
        print(bcolors.OKGREEN + "SOCKET LIST: \n"  + bcolors.ENDC)
        print(bcolors.OKGREEN + str(socketList) + bcolors.ENDC)
        for i in range(0, len(socketList)):
            if socketListPort[i] != addr[1]:
                data = str(addr) + data
                socketList[i].send(data.encode())
                print("Message sent to: " + str(socketListPort[i]))
                print(str(len(socketListPort)))
            else:
                print("failed to send to: " + str(socketListPort[i]))
                print(str(len(socketListPort)))
        print("\n")




ip = '0.0.0.0'
port = 50000
buffer_size = 2048

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
mySocket = ssl.wrap_socket(sock,keyfile='ca.key', certfile='ca.crt', \
cert_reqs=ssl.CERT_NONE, ssl_version=ssl.PROTOCOL_TLSv1_2, \
ciphers='ECDH', do_handshake_on_connect=True)
mySocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
mySocket.bind((ip,port))
threads = []
socketListPort = []
socketList = []


while True:
    mySocket.listen(4)
    conn, addr = mySocket.accept()
    socketListPort.append(addr[1])
    socketList.append(conn)
    newThread = SSLServer(conn, addr)
    newThread.start()
    threads.append(newThread)
for t in threads:
    t.join()
