from socket import *
import struct
import pickle
HOST = '127.0.0.1'
PORT = 14333
BUFSIZE = 1024
ADDR=(HOST,PORT)
class tcpCliSock(object):
    def __init__(self):
        self.client = socket(AF_INET, SOCK_STREAM)
    def link(self):
        self.client.connect(ADDR)
    def send(self,package):
        self.client.sendall(package)
    def receive_command(self):
        receive = self.client.recv(4)
        return struct.unpack('i',receive)[0]
    def receive_packages(self):
        receive = self.client.recv(4)
        size = struct.unpack('i',receive)[0]
        packages = self.client.recv(size)
        try:
            packages = pickle.loads(packages)
        except EOFError:
            return None
        return packages
    def commandHandle(self,command):
        return struct.pack('i',command)
    def packagesHandle(self,dicts):
        dicts = pickle.dumps(dicts)
        size = len(dicts)
        size = struct.pack('i',size)
        return size+dicts
    def poll(self,num):
        packages = {'num':num}
        command = self.commandHandle(4)
        packages = self.packagesHandle(packages)
        packages = command + packages
        self.send(packages)
        return self.receive_command()
    def Close(self):
        command = self.commandHandle(0)
        self.send(command)
        self.client.close()
    def sendPackages(self, command, dicts = None):
        command = self.commandHandle(command)
        if dicts != None:
            dicts = self.packagesHandle(dicts)
            self.send(command+dicts)
        else:
            self.send(command)
