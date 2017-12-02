# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'hello.ui'
#
# Created by: PyQt5 UI code generator 5.9.1
#
# WARNING! All changes made in this file will be lost!
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import struct
import pickle
from time import ctime
from chatting import *
from loginui import *
from register import *
import tcpclisock as tcp
HOST = '106.15.225.249'
PORT = 21567
BUFSIZE = 1024
ADDR=(HOST,PORT)


class loginfrontend(QtCore.QObject):
    loginInfo = QtCore.pyqtSignal(str,str)#向后台传输
    logSucess = QtCore.pyqtSignal(str)#向上级传输
    loginFailed = QtCore.pyqtSignal()
    def __init__(self,window):
        super(loginfrontend,self).__init__()
        self.window = window
        self.window.enter.connect(self.log)
        self.gui = Ui_Login(window)
        self.gui.login.clicked.connect(self.log)
        self.gui.follow.clicked.connect(self.linkfollow)
        #self.gui.register.clicked.connect(self.linkregister)#在这里把部分不涉及与顶层直接有关的信号在这里做connect
    def linkfollow(self):
        QtGui.QDesktopServices.openUrl(QtCore.QUrl('http://www.cqdulux.cn'))
    def log(self):
        if self.gui.username.text() == "":
            reply = QMessageBox.warning(self.window, 'Warning', '请输入昵称!', QMessageBox.Yes)
        elif self.gui.password.text() == "":
            reply = QMessageBox.warning(self.window, "Wanring", "请输入密码！", QMessageBox.Yes)
        else:
            username = self.gui.username.text()
            password = self.gui.password.text()
            self.loginInfo.emit(username,password)
    def checklog(self,receive):
        if receive != 1:
            error = QMessageBox.warning(self.window, "Warning", "用户不存在或用户名、密码不正确!",QMessageBox.Yes)
            self.loginFailed.emit()
        else:
            self.logSucess.emit(self.gui.username.text())

def main():
    app = QtWidgets.QApplication(sys.argv)
    w =MainWindow()
    w.show()
    sys.exit(app.exec_())


if __name__=="__main__":
    main()
