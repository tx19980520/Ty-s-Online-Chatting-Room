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

class Loginfrontend(QtCore.QObject):
    logininfo = QtCore.pyqtSignal(str,str)#向后台传输
    logsucess = QtCore.pyqtSignal(str)#向上级传输
    def __init__(self,window):
        super(Loginfrontend,self).__init__()
        self.window = window
        self.window.enter.connect(self.log)
        self.gui = Ui_Login(window)
        self.gui.login.clicked.connect(self.log)
        self.gui.follow.clicked.connect(self.linkFollow)
        #self.gui.register.clicked.connect(self.linkregister)#在这里把部分不涉及与顶层直接有关的信号在这里做connect
    def linkFollow(self):
        QtGui.QDesktopServices.openUrl(QtCore.QUrl('http://www.cqdulux.cn'))
    def log(self):#在发送信息之前的检查
        if self.gui.username.text() == "":
            reply = QMessageBox.warning(self.window, 'Warning', '请输入昵称!', QMessageBox.Yes)
        elif self.gui.password.text() == "":
            reply = QMessageBox.warning(self.window, "Wanring", "请输入密码！", QMessageBox.Yes)
        else:
            username = self.gui.username.text()
            password = self.gui.password.text()
            self.logininfo.emit(username,password)
    def checkLog(self,receive):#得到登陆结果
        if receive != 1:
            error = QMessageBox.warning(self.window, "Warning", "用户不存在或用户名、密码不正确!",QMessageBox.Yes)
        else:
            self.logsucess.emit(self.gui.username.text())

def main():
    app = QtWidgets.QApplication(sys.argv)
    w =MainWindow()
    w.show()
    sys.exit(app.exec_())


if __name__=="__main__":
    main()
