import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from loginbackend import *
from loginfrontend import *
from chatting import *
HOST = '127.0.0.1'
PORT = 14333
BUFSIZE = 1024
ADDR=(HOST,PORT)
class Qmain(QtWidgets.QMainWindow):#主要是为了添加一个回车登陆功能
    enter = QtCore.pyqtSignal()
    closes = QtCore.pyqtSignal()
    def __init__(self):
        super(Qmain,self).__init__()
    def keyPressEvent(self,e):
        if e.key() == QtCore.Qt.Key_Return:
            self.enter.emit()
class Login(QtCore.QObject):#为前后端的signal和slot提供连接的平台
    def __init__(self):
        super(Login,self).__init__()
        self.window = Qmain()
        self.ui = Loginfrontend(self.window)
        self.client = Loginbackend()
        self.window.closes.connect(self.client.close)
        self.ui.logsucess.connect(self.enterChatting)
        self.ui.logininfo.connect(self.client.login)
        self.client.loginresult.connect(self.ui.checkLog)
        self.ui.gui.register.clicked.connect(self.enterRegister)
        self.window.show()
    def enterAnother(self):
        username = self.ui.gui.username.text()
        self.enterChatting(username)
    def enterChatting(self,username):
        self.window.close()#关闭当前窗口
        self.client.changeLink()#把link交给chatting
        self.chatting = Chatting(username)
    def enterRegister(self):#开启注册窗口
        self.register = Register(self.client)

def main():
    app = QtWidgets.QApplication(sys.argv)
    program = Login()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
