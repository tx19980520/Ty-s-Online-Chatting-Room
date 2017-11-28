import sys
import struct
import pickle
from time import ctime
from chattingroom import *
import tcpclisock as tcp
HOST = '106.15.225.249'
PORT = 21567
BUFSIZE = 1024
ADDR=(HOST,PORT)

class loginbackend(object):
    loginResult = QtCore.pyqtSignal(int)
    def __init__(self):
        self.link = tcp.tcpCliSock()
    def login(self,username,password):
        command = self.link.commandHandle(1)
        data = {'username':username,'password':password}
        packages = self.link.packagesHandle(data)
        self.link.send(command+data)
        receive = self.link.receive_command()
        self.loginResult.emit(receive)
