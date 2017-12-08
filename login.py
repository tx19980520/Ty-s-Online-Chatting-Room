import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from loginbackend import *
from loginfrontend import *
from chatting import *
HOST = '106.15.225.249'
PORT = 14333
BUFSIZE = 1024
ADDR=(HOST,PORT)
class Qmain(QtWidgets.QMainWindow):
    enter = QtCore.pyqtSignal()
    closes = QtCore.pyqtSignal()
    def __init__(self):
        super(Qmain,self).__init__()
    def keyPressEvent(self,e):
        if e.key() == QtCore.Qt.Key_Return:
            self.enter.emit()
class login(QtCore.QObject):
    def __init__(self):
        super(login,self).__init__()
        self.window = Qmain()
        self.ui = loginfrontend(self.window)
        self.client = loginbackend()
        self.window.closes.connect(self.client.Close)
        self.ui.logSucess.connect(self.enterChatting)
        self.ui.loginInfo.connect(self.client.login)
        self.ui.loginFailed.connect(self.client.link.client.close)
        self.client.loginResult.connect(self.ui.checklog)
        self.ui.gui.register.clicked.connect(self.enterRegister)
        self.window.show()
    def enterAnother(self):
        username = self.ui.gui.username.text()
        self.enterChatting(username)
    def enterChatting(self,username):
        self.window.close()
        self.client.changelink()
        self.chatting = Chatting(username)
    def enterRegister(self):
        self.register = Register(self.client)
        #self.register.registerRequest.connect(self.client.RegistertoServer)
        #self.client.feedback.connect(self.register.ui.registerFeedback)

def main():
    app = QtWidgets.QApplication(sys.argv)
    program = login()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
