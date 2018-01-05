import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from chattingfrontend import *
from chattingbackend import *
from change import *
import tcpclisock
class ChatDialog(QtWidgets.QDialog):
    needclose = QtCore.pyqtSignal()
    needsend = QtCore.pyqtSignal()
    def __init__(self):
        super(ChatDialog,self).__init__()
    def closeEvent(self,event):#主要是为了添加点击右上角×退出事件
        reply = QMessageBox.question(self, 'Message','Are you sure to quit?',QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.needclose.emit()
            event.accept()
        else:
            event.ignore()
    def keyPressEvent(self,e):
        if e.key() == QtCore.Qt.Key_Return:
            self.needsend.emit()
class Chatting(QtCore.QObject):
    def __init__(self,username):#同样是对chattingroom的前后端提供平台进行signal和slot的连接
        super(Chatting,self).__init__()
        self.window = ChatDialog()
        self.tmp =tcpclisock.tcpCliSock()
        self.client = Client(self.tmp,username)
        self.ui = Chattingfrontend(self.window)
        self.window.needclose.connect(self.ui.closeReady)
        self.client.hasnews.connect(self.ui.showMessage)
        self.client.info.connect(self.ui.infoDump)
        self.client.newinfo.connect(self.ui.newInfoDump)
        self.client.fileinfomation.connect(self.ui.setFile)
        self.ui.gui.tabWidget.currentChanged.connect(self.client.fileInfo)
        self.ui.gui.changeinfo.clicked.connect(self.enterChange)
        self.window.needsend.connect(self.ui.sendMessage)
        self.ui.messagetoserver.connect(self.client.sendMessage)
        self.ui.propare.connect(self.client.downloadFile)
        self.ui.detach.connect(self.client.detach)
        self.ui.newfile.connect(self.client.addFile)
        self.ui.newphoto.connect(self.client.addPhoto)
        self.ui.tr.show.connect(self.window.show)
        self.ui.tr.hide.connect(self.window.hide)
        self.ui.tr.invisiend.connect(self.client.onlineModel)
        self.ui.tr.invisistart.connect(self.client.invisibleModel)
        self.client.senddownloadsucess.connect(self.ui.downloadSucessInfo)
        self.client.senduploadsucess.connect(self.ui.uploadSucessInfo)
        self.client.filedatatofront.connect(self.ui.getDownloadProcess)
        self.client.getInfo()
        self.client.start()
        self.window.show()
    def enterChange(self):
        self.change = Change(self.client)
