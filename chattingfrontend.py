# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'chattingroom.ui'
#
# Created by: PyQt5 UI code generator 5.9.1
#
# WARNING! All changes made in this file will be lost!
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import tcpclisock as tcp
from PyQt5.QtWidgets import QMessageBox
from time import sleep
from chattingui import *
class chattingfrontend(QtCore.QObject):
    messagetoServer = QtCore.pyqtSignal(str)
    def __init__(self,window):
        super(chattingfrontend,self).__init__()
        self.window = window
        self.gui = Ui_Chat(window)
        self.gui.close.clicked.connect(self.window.close)
        self.gui.messages.textChanged.connect(self.movecursor)
        self.gui.send.clicked.connect(self.sendMessage)
    def Infodump(self,dicts):#初始化数据
        _translate =QtCore.QCoreApplication.translate
        if dicts['COMMAND']== 1:
            self.gui.address.setText(_translate("Dialog", dicts['ADDRESS']))
            self.gui.name.setText(_translate("Dialog", dicts['NAME']))
            self.gui.age.setText(_translate("Dialog", str(dicts['AGE'])))
            #信号定义全部在chatting中
        else:
            error = QMessageBox.warning(self.window, "Warning","你的网络出现问题，无法查询到你的信息！",QMessageBox.Yes)
    def sendMessage(self):
        s = self.gui.Edit.toPlainText()#test ok!
        self.gui.Edit.setPlainText("")
        self.messagetoServer.emit(s)
    def showMessage(self,dicts):
        line1 = dicts['sender']+" "+dicts['time']#sender message time
        line2 = dicts['message']
        self.gui.messages.append(line1)
        self.gui.messages.append(line2)
    def movecursor(self):
        self.gui.messages.moveCursor(QtGui.QTextCursor.End)

def main():
    app = QtWidgets.QApplication(sys.argv)
    w = QtWidgets.QDialog()
    form = Ui_Dialog()
    form.setupUi(w)
    w.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
