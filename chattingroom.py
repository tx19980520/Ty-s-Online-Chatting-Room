# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'chattingroom.ui'
#
# Created by: PyQt5 UI code generator 5.9.1
#
# WARNING! All changes made in this file will be lost!
import sys
from PyQt5 import QtCore, QtGui, QtWidgets
import struct
import pickle
import tcpclisock as tcp
from PyQt5.QtWidgets import QMessageBox
class Client(QtCore.QThread):
    def __init__(self,link,username='',age=0,address=''):
        self.hasNews = Qtcore.pyqtSignal(dict)
        super(Client,self).__init__()
        self.link = link
        self.username = name
        self.age = age
        self.address = address
        self.num = -1;
        self.hasNews.connect(Ui_Dialog)
    def sendmessage(self,message):
        command = self.link.commandHandle(3)
        dicts = {'sender':self.username,'message':message}
        packages =self.link.packagesHandle(dicts)
        self.link.send(command+packages)
    def run(self):
        command = self.link.poll(self.num)
        if command == 2:
            return
        elif command == 3:
            packages = self.link.receive_packages()
            self.num += 1
            self.hasNews.emit(packages)
class Ui_Dialog(object):
    def __init__(self,link,username):
        self.client =Client(link,username)
        self.client.hasNews.connect(self.messageshow)
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1319, 830)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 0, 321, 61))
        font = QtGui.QFont()
        font.setFamily("Helvetica-Condensed-Black-Se")
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.tabWidget = QtWidgets.QTabWidget(Dialog)
        self.tabWidget.setGeometry(QtCore.QRect(0, 60, 1301, 751))
        self.tabWidget.setObjectName("tabWidget")
        self.Chatting = QtWidgets.QWidget()
        self.Chatting.setObjectName("Chatting")
        self.mainarea = QtWidgets.QScrollArea(self.Chatting)
        self.mainarea.setGeometry(QtCore.QRect(10, 10, 941, 471))
        self.mainarea.setWidgetResizable(True)
        self.mainarea.setObjectName("mainarea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 939, 469))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.showmessage = QtWidgets.QWidget(self.scrollAreaWidgetContents)
        self.showmessage.setGeometry(QtCore.QRect(10, 10, 911, 451))
        self.showmessage.setObjectName("showmessage")
        self.mainarea.setWidget(self.scrollAreaWidgetContents)
        self.Edit = QtWidgets.QPlainTextEdit(self.Chatting)
        self.Edit.setGeometry(QtCore.QRect(20, 490, 931, 151))
        self.Edit.setObjectName("Edit")
        self.label_2 = QtWidgets.QLabel(self.Chatting)
        self.label_2.setGeometry(QtCore.QRect(980, 0, 321, 51))
        font = QtGui.QFont()
        font.setFamily("Helvetica-Condensed-Black-Se")
        font.setPointSize(16)
        self.label_2.setFont(font)
        self.label_2.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.label_2.setTextFormat(QtCore.Qt.RichText)
        self.label_2.setScaledContents(False)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.Chatting)
        self.label_3.setGeometry(QtCore.QRect(1010, 70, 81, 30))
        font = QtGui.QFont()
        font.setFamily("Helvetica-Condensed-Black-Se")
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_6 = QtWidgets.QLabel(self.Chatting)
        self.label_6.setGeometry(QtCore.QRect(1010, 140, 81, 30))
        font = QtGui.QFont()
        font.setFamily("Helvetica-Condensed-Black-Se")
        font.setPointSize(10)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.label_5 = QtWidgets.QLabel(self.Chatting)
        self.label_5.setGeometry(QtCore.QRect(570, 240, 81, 18))
        self.label_5.setText("")
        self.label_5.setObjectName("label_5")
        self.label_4 = QtWidgets.QLabel(self.Chatting)
        self.label_4.setGeometry(QtCore.QRect(1010, 210, 81, 30))
        font = QtGui.QFont()
        font.setFamily("Helvetica-Condensed-Black-Se")
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.scrollArea_2 = QtWidgets.QScrollArea(self.Chatting)
        self.scrollArea_2.setGeometry(QtCore.QRect(1000, 400, 251, 271))
        self.scrollArea_2.setWidgetResizable(True)
        self.scrollArea_2.setObjectName("scrollArea_2")
        self.scrollAreaWidgetContents_2 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_2.setGeometry(QtCore.QRect(0, 0, 249, 269))
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.widget = QtWidgets.QWidget(self.scrollAreaWidgetContents_2)
        self.widget.setGeometry(QtCore.QRect(10, 10, 211, 251))
        self.widget.setObjectName("widget")
        self.scrollArea_2.setWidget(self.scrollAreaWidgetContents_2)
        self.send = QtWidgets.QPushButton(self.Chatting)
        self.send.setGeometry(QtCore.QRect(700, 650, 112, 41))
        self.send.setObjectName("send")
        self.close = QtWidgets.QPushButton(self.Chatting)
        self.close.setGeometry(QtCore.QRect(840, 650, 112, 41))
        self.close.setObjectName("close")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.Chatting)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(1109, 50, 171, 201))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.name = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Helvetica-Condensed-Black-Se")
        font.setPointSize(10)
        self.name.setFont(font)
        self.name.setText("")
        self.name.setObjectName("name")
        self.verticalLayout.addWidget(self.name)
        self.age = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Helvetica-Condensed-Black-Se")
        font.setPointSize(10)
        self.age.setFont(font)
        self.age.setText("")
        self.age.setObjectName("age")
        self.verticalLayout.addWidget(self.age)
        self.address = QtWidgets.QLabel(self.verticalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Helvetica-Condensed-Black-Se")
        font.setPointSize(10)
        self.address.setFont(font)
        self.address.setText("")
        self.address.setObjectName("label_8")
        self.verticalLayout.addWidget(self.address)
        self.pushButton_3 = QtWidgets.QPushButton(self.Chatting)
        self.pushButton_3.setGeometry(QtCore.QRect(1080, 293, 112, 41))
        self.pushButton_3.setObjectName("pushButton_3")
        self.tabWidget.addTab(self.Chatting, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.scrollArea = QtWidgets.QScrollArea(self.tab_2)
        self.scrollArea.setGeometry(QtCore.QRect(10, 16, 741, 481))
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents_3 = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_3.setGeometry(QtCore.QRect(0, 0, 739, 479))
        self.scrollAreaWidgetContents_3.setObjectName("scrollAreaWidgetContents_3")
        self.tableWidget = QtWidgets.QTableWidget(self.scrollAreaWidgetContents_3)
        self.tableWidget.setGeometry(QtCore.QRect(0, 0, 721, 481))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents_3)
        self.tabWidget.addTab(self.tab_2, "")
        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)


    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Ty\'s Chatting Room"))
        self.label_2.setText(_translate("Dialog", "Your own Information"))
        self.label_3.setText(_translate("Dialog", "name:"))
        self.label_6.setText(_translate("Dialog", "age:"))
        self.label_4.setText(_translate("Dialog", "adrress:"))
        self.send.setText(_translate("Dialog", "send"))
        self.close.setText(_translate("Dialog", "close"))
        self.pushButton_3.setText(_translate("Dialog", "Edit"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Chatting), _translate("Dialog", "Chatting"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "FileName"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "Size"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("Dialog", "Tab 2"))


        #一下为初始化的一些需要处理的数据
        command = 2
        command = struct.pack('i',command)
        packages = {'username':self.client.username}
        packages = pickle.dumps(packages)
        lpackages = len(packages)
        lpackages = struct.pack('i',lpackages)
        self.client.link.send(command+lpackages+packages)
        receive = self.client.link.receive_command()#返回值只可能是0或1，0表示错误，1表示正确并继续读取后续信息
        if receive== 1:
            dicts = self.client.link.receive_packages()
            self.address.setText(_translate("Dialog", dicts['ADDRESS']))
            self.name.setText(_translate("Dialog", dicts['NAME']))
            self.age.setText(_translate("Dialog", str(dicts['AGE'])))
            self.client.name = dicts['NAME']
            self.client.address = dicts['ADDRESS']
            self.client.age = dicts['AGE']
            self.client.num = dicts['NUM']
        else:
            error = QMessageBox.warning(self, "Warning","你的网络出现问题，无法查询到你的信息！",QMessageBox.Yes)
    def showmessage(self):


def main():
    app = QtWidgets.QApplication(sys.argv)
    w = QtWidgets.QDialog()
    form = Ui_Dialog()
    form.setupUi(w)
    w.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()