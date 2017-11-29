from socket import *
import struct
import pickle
HOST = '127.0.0.1'
PORT = 21567
BUFSIZE = 1024
ADDR=(HOST,PORT)
class tcpCliSock(object):
    def __init__(self):
        self.client = socket(AF_INET, SOCK_STREAM)
    def link(self):
        self.client.connect(ADDR)
    def test(self):
        self.link()
        packages = {'username':'Ty','password':'1234512345qwe'}
        packages = pickle.dumps(packages)
        command = struct.pack('i',1)
        packagelen = struct.pack("i",len(packages))
        send = command+packagelen+packages
        self.client.sendall(send)
        self.client.recv(4)
def main():

    C = tcpCliSock()
    C.test()

main()
