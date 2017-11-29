import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from loginbackend import *
from loginfrontend import *
from chatting import *
HOST = '127.0.0.1'
PORT = 23333
BUFSIZE = 1024
ADDR=(HOST,PORT)
class login(QtCore.QObject):
    def __init__(self):
        super(login,self).__init__()
        self.window = QtWidgets.QMainWindow()
        self.ui = loginfrontend(self.window)
        self.client = loginbackend()
        self.ui.logSucess.connect(self.enterChatting)
        self.ui.loginInfo.connect(self.client.login)
        self.client.loginResult.connect(self.ui.checklog)
        self.window.show()
    def enterChatting(self,username):
        self.window.close()
        self.chatting = Chatting(self.client,username)


def main():
    app = QtWidgets.QApplication(sys.argv)
    program = login()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
