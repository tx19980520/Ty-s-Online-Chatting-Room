# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'chattingroom.ui'
#
# Created by: PyQt5 UI code generator 5.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Chat(QtCore.QObject):
    def __init__(self,window):
        super(Ui_Chat,self).__init__()
        self.window = window
        self.setupUi()
    def setupUi(self):
        self.window.setObjectName("Dialog")
        self.window.resize(1310, 830)
        self.label = QtWidgets.QLabel(self.window)
        self.label.setGeometry(QtCore.QRect(20, 0, 321, 61))
        font = QtGui.QFont()
        font.setFamily("Helvetica-Condensed-Black-Se")
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.tabWidget = QtWidgets.QTabWidget(self.window)
        self.tabWidget.setGeometry(QtCore.QRect(0, 60, 1301, 751))
        self.tabWidget.setObjectName("tabWidget")
        self.Chatting = QtWidgets.QWidget()
        self.Chatting.setObjectName("Chatting")
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
        self.label_5 = QtWidgets.QLabel(self.Chatting)
        self.label_5.setGeometry(QtCore.QRect(1010, 140, 81, 30))
        font = QtGui.QFont()
        font.setFamily("Helvetica-Condensed-Black-Se")
        font.setPointSize(10)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.label_4 = QtWidgets.QLabel(self.Chatting)
        self.label_4.setGeometry(QtCore.QRect(1010, 210, 81, 30))
        font = QtGui.QFont()
        font.setFamily("Helvetica-Condensed-Black-Se")
        font.setPointSize(10)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
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
        self.address.setObjectName("address")
        self.verticalLayout.addWidget(self.address)
        self.change_info = QtWidgets.QPushButton(self.Chatting)
        self.change_info.setGeometry(QtCore.QRect(1080, 293, 112, 41))
        self.change_info.setObjectName("change_info")
        self.messages = QtWidgets.QTextBrowser(self.Chatting)
        self.messages.setGeometry(QtCore.QRect(20, 30, 931, 441))
        self.messages.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.messages.setObjectName("messages")
        self.users = QtWidgets.QTextBrowser(self.Chatting)
        self.users.setGeometry(QtCore.QRect(1010, 390, 256, 251))
        self.users.setObjectName("users")
        self.tabWidget.addTab(self.Chatting, "")
        self.Files = QtWidgets.QWidget()
        self.Files.setObjectName("Files")
        self.tableWidget = QtWidgets.QTableWidget(self.Files)
        self.tableWidget.setGeometry(QtCore.QRect(30, 20, 1241, 691))
        self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        #self.tableWidget.horizontalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(True)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(300)
        self.tableWidget.horizontalHeader().setHighlightSections(True)
        self.tabWidget.addTab(self.Files, "")

        self.retranslateUi()
        self.tabWidget.setCurrentIndex(0)
        self.close.clicked.connect(self.window.close)
        QtCore.QMetaObject.connectSlotsByName(self.window)

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.window.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Ty\'s Chatting Room"))
        self.label_2.setText(_translate("Dialog", "Your own Information"))
        self.label_3.setText(_translate("Dialog", "name:"))
        self.label_5.setText(_translate("Dialog", "age:"))
        self.label_4.setText(_translate("Dialog", "adrress:"))
        self.send.setText(_translate("Dialog", "send"))
        self.close.setText(_translate("Dialog", "close"))
        self.change_info.setText(_translate("Dialog", "Edit"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Chatting), _translate("Dialog", "Chatting"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "FileName"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "Size"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", "uploaders"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("Dialog", "operation"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.Files), _translate("Dialog", "Files"))
