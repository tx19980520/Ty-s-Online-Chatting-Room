import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from chattingfrontend import *
from chattingbackend import *
class Chatting(QtCore.QObject):
    def __init__(self,client,username):
        super(Chatting,self).__init__()
        self.window = QtWidgets.QDialog()
        self.client = Client(client,username)
        self.ui = chattingfrontend(self.window)
        self.client.hasNews.connect(self.ui.showMessage)
        self.client.Info.connect(self.ui.Infodump)
        self.client.fileinfomation.connect(self.ui.setFile)
        self.ui.gui.tabWidget.currentChanged.connect(self.client.fileInfo)
        self.ui.messagetoServer.connect(self.client.sendmessage)
        self.ui.propare.connect(self.client.downloadFile)
        self.client.getInfo()
        self.client.start()
        self.window.show()
