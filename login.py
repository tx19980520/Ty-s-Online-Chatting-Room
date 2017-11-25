# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'hello.ui'
#
# Created by: PyQt5 UI code generator 5.9.1
#
# WARNING! All changes made in this file will be lost!
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from socket import *
import struct
from time import ctime

HOST = '127.0.0.1'
PORT = 8000
BUFSIZE = 1024
ADDR=(HOST,PORT)
class tcpCliSock(object):
    def __init__(self):
        self.client = socket(AF_INET, SOCK_STREAM)
    def link(self):
        print("s")
        self.client.connect(ADDR)
        print("I")

class Ui_MainWindow(object):
    def __init__(self,window):
        self.link = tcpCliSock()
        self.window = window
    def setupUi(self):
        self.window.setObjectName("MainWindow")
        self.window.resize(600, 450)
        self.centralwidget = QtWidgets.QWidget(self.window)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(135, 30, 330, 90))
        font = QtGui.QFont()
        font.setFamily("Helvetica-Condensed-Black-Se")
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setTextFormat(QtCore.Qt.RichText)
        self.label.setScaledContents(True)
        self.label.setObjectName("label")
        self.username = QtWidgets.QLineEdit(self.centralwidget)
        self.username.setGeometry(QtCore.QRect(190, 150, 200, 35))
        self.username.setObjectName("username")
        self.password = QtWidgets.QLineEdit(self.centralwidget)
        self.password.setGeometry(QtCore.QRect(190, 230, 200, 35))
        self.password.setObjectName("password")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(90, 150, 100, 30))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(90, 230, 100, 30))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setContextMenuPolicy(QtCore.Qt.NoContextMenu)
        self.label_3.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_3.setTextFormat(QtCore.Qt.RichText)
        self.label_3.setObjectName("label_3")
        self.register = QtWidgets.QPushButton(self.centralwidget)
        self.register.setGeometry(QtCore.QRect(420, 150, 112, 34))
        self.register.setObjectName("register_2")
        self.find = QtWidgets.QPushButton(self.centralwidget)
        self.find.setGeometry(QtCore.QRect(420, 230, 112, 34))
        self.find.setObjectName("find")
        self.login = QtWidgets.QPushButton(self.centralwidget)
        self.login.setGeometry(QtCore.QRect(240, 320, 112, 34))
        self.login.setObjectName("login")
        self.window.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(self.window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 600, 30))
        self.menubar.setObjectName("menubar")
        self.window.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(self.window)
        self.statusbar.setObjectName("statusbar")
        self.window.setStatusBar(self.statusbar)
        self.register.clicked.connect(self.linkregister)
        self.login.clicked.connect(self.log);
        self.retranslateUi()
        QtCore.QMetaObject.connectSlotsByName(self.window)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.window.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "Ty\'s Online Chatting Room"))
        self.label_2.setText(_translate("MainWindow", "昵称"))
        self.label_3.setText(_translate("MainWindow", "密码"))
        self.register.setText(_translate("MainWindow", "注册账号"))
        self.find.setText(_translate("MainWindow", "找回密码"))
        self.login.setText(_translate("MainWindow", "登陆"))
    def linkregister(self):
        QtGui.QDesktopServices.openUrl(QtCore.QUrl('http://www.cqdulux.cn/register'))
    def linkfind(self):
        QtGui.QDesktopServices.openUrl(QtCore.QUrl('http://www.cqdulux.cn/find'))
    def log(self):
        data = "login"
        if self.username.text() !="" and self.password.text() !="":
            username = self.username.text()
            password = self.passowrd.text()
        elif self.username.text() == "":
            reply = QMessageBox.warning(self.window, 'Warning', '请输入昵称!', QMessageBox.Yes)
            print("here!")
        elif self.password.text() == "":
            print("here!")
            reply = QMessageBox.warning(self.window, "Wanring", "请输入密码！", QMessageBox.Yes)
        print("here！！")
        self.link.link()
        self.link.client.send(bytes(data,encoding = "utf-8"))
        luser = len(username)
        lpassword = len(password)
        givelen =  struct.pack('2i',luser,lpassword)
        self.link.client.sendall(givelen)
        givestring = struct.pack(str(luser)+'s'+str(lpassword)+"s",username,password)
        receive = self.link.client.recv(BUFSIZE)
        if(receive != "sucess"):#登陆不成功
            error = QMessageBox.warning(self, "Warning", "用户名不存在或密码不正确!",QMessageBox.Yes)
            self.link.client.close()
        else:
            print("sucess!")

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow(self)
        self.ui.setupUi()

def main():
    app = QtWidgets.QApplication(sys.argv)
    w = QtWidgets.QMainWindow()
    form = Ui_MainWindow(w)
    form.setupUi()
    w.show()
    sys.exit(app.exec_())


if __name__=="__main__":
    main()
