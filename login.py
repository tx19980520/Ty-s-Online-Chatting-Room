import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from loginbackend import *
from loginfrontend import *
from chatting import *
HOST = '106.15.225.249'
PORT = 21567
BUFSIZE = 1024
ADDR=(HOST,PORT)
class login(self):
    def __init__(self):
        self.window = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.window)
        self.client = loginbackend()
        self.ui.register.clicked.connect(self.ui.linkregister)
        self.ui.login.clicked.connect(self.ui.log);
        self.ui.logSucess.connect(self.enterChatting)
        self.ui.loginInfo.connect(self.client.login)
        self.client.loginResult.connect(self.ui.checklog)
    def enterChatting(self,username):
        self.window.close()
        self.chatting = Chatting(self.client,username)
