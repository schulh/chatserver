#!/usr/bin/env python3.5

import threading
import socket
import ssl
import argparse
from colors import bcolors


class SSLServer(threading.Thread):
    def __init__(self, ip, port):
        threading.Thread.__init__(self)
        self.ip = ip
        self.port = port
        print(bcolors.OKGREEN + "[+] New server socket thread started for " + ip + ":" + str(port) + bcolors.ENDC)

    def run(self):
        welcome = "Welcome!"
        SSLServer.broadcast(self, welcome)
        while True:
            data = conn.recv(buffer_size).decode()
            print(bcolors.OKBLUE + "RECIEVED FROM SOCKET: \n" + str(conn) + bcolors.ENDC)
            SSLServer.broadcast(self, data)

    def broadcast(self, data):
        print(bcolors.OKGREEN + "SOCKET LIST: \n"  + bcolors.ENDC)
        for socket in socketList:
            if socket != mySocket and sock:
                try:
                    print(bcolors.OKGREEN + str(socket) + bcolors.ENDC)
                    socket.send(data.encode())
                except:
                    socket.close()
                    if socket in socketList:
                        socketList.remove(socket)



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
socketList = []


while True:
    mySocket.listen(4)
    conn, addr = mySocket.accept()
    newThread = SSLServer(ip,port)
    newThread.start()
    threads.append(newThread)
    socketList.append(conn)
    #print(socketList)
for t in threads:
    t.join()
