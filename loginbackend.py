import sys
import struct
import pickle
from time import ctime
import tcpclisock as tcp
from PyQt5 import QtCore
HOST = '106.15.225.249'
PORT = 21567
BUFSIZE = 1024
ADDR=(HOST,PORT)

class loginbackend(QtCore.QObject):
    loginResult = QtCore.pyqtSignal(int)
    feedback = QtCore.pyqtSignal(int)#1 is sucess ,0 is has already register
    def __init__(self):
        super(loginbackend,self).__init__()
        self.link = tcp.tcpCliSock()
        self.link.link()
    def login(self,username,password):
        command = self.link.commandHandle(1)
        data = {'username':username,'password':password}
        packages = self.link.packagesHandle(data)
        self.link.send(command+packages)
        receive = self.link.receive_command()
        self.loginResult.emit(receive)
    def changelink(self):
        command = self.link.commandHandle(0)
        self.link.send(command)
        self.link.client.close()
    def RegistertoServer(self,dicts):
        command = 9
        command =self.link.commandHandle(command)
        packages =self.link.packagesHandle(dicts)
        self.link.send(command+packages)
        feedback = self.link.receive_command()
        self.feedback.emit(feedback)
