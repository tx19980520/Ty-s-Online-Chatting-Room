import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from chattingfrontend import *
from chattingbackend import *
class Chatting(object):
    def __init__(self,client,username):
        self.client = Clinet(client)
        self.window = QtWidgets.QDialog()
        self.ui = Ui_Dialog(self.window)
        self.ui.close.clicked.connect(self.window.close)
        self.ui.messages.textChanged.connect(self.ui.movecursor)
        self.client.hasNews.connect(self.ui.showMessage)
        self.client.Info.connect(self.ui.Infodump)
        self.ui.send.clicked.connect(self.ui.sendMessage)
        self.ui.messagetoServer.connect(self.client.sendmessage)
        self.client.getInfo()
        self.client.start()
        self.window.show()
