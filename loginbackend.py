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

class Loginbackend(QtCore.QObject):
    loginresult = QtCore.pyqtSignal(int)
    feedback = QtCore.pyqtSignal(int)#1 is sucess ,0 is has already register
    def __init__(self):
        super(Loginbackend,self).__init__()
        self.link = tcp.tcpCliSock()
        self.link.link()
    def login(self,username,password):
        command = self.link.commandHandle(1)
        data = {'username':username,'password':password}
        packages = self.link.packagesHandle(data)
        self.link.send(command+packages)
        receive = self.link.receiveCommand()
        self.loginresult.emit(receive)
    def changeLink(self):
        command = self.link.commandHandle(0)
        self.link.send(command)
        self.link.close()
    def RegistertoServer(self,dicts):#发送注册的信息到服务器
        command = 9
        command =self.link.commandHandle(command)
        packages =self.link.packagesHandle(dicts)
        self.link.send(command+packages)
        feedback = self.link.receiveCommand()#接收注册是否成功的消息并发回给前端
        self.feedback.emit(feedback)
    def close(self):
        self.link.close()
