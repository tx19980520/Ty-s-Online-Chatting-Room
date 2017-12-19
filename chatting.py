import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from chattingfrontend import *
from chattingbackend import *
from change import *
import tcpclisock
class ChatDialog(QtWidgets.QDialog):
    needClose = QtCore.pyqtSignal()
    needSend = QtCore.pyqtSignal()
    def __init__(self):
        super(ChatDialog,self).__init__()
    def closeEvent(self,event):
        reply = QMessageBox.question(self, 'Message','Are you sure to quit?',QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.needClose.emit()
            event.accept()
        else:
            event.ignore()
    def keyPressEvent(self,e):
        if e.key() == QtCore.Qt.Key_Return:
            self.needSend.emit()
class Chatting(QtCore.QObject):
    def __init__(self,username):
        super(Chatting,self).__init__()
        self.window = ChatDialog()
        self.tmp =tcpclisock.tcpCliSock()
        self.client = Client(self.tmp,username)
        self.ui = chattingfrontend(self.window)
        self.window.needClose.connect(self.ui.closeReady)
        self.client.hasNews.connect(self.ui.showMessage)
        self.client.Info.connect(self.ui.infoDump)
        self.client.newInfo.connect(self.ui.newInfoDump)
        self.client.fileinfomation.connect(self.ui.setFile)
        self.ui.gui.tabWidget.currentChanged.connect(self.client.fileInfo)
        self.ui.gui.change_info.clicked.connect(self.enterChange)
        self.window.needSend.connect(self.ui.sendMessage)
        self.ui.messagetoServer.connect(self.client.sendmessage)
        self.ui.propare.connect(self.client.downloadFile)
        self.ui.detach.connect(self.client.detach)
        self.ui.newFile.connect(self.client.addFile)
        self.ui.newPhoto.connect(self.client.addPhoto)
        self.client.senddonwloadsucess.connect(self.ui.downloadSucessInfo)
        self.client.senduploadsucess.connect(self.ui.uploadSucessInfo)
        self.client.detachlink.connect(self.detachLink)
        self.client.getInfo()
        self.client.start()
        self.window.show()
    def detachLink(self):
        self.client.link.client.close()
    def enterChange(self):
        self.change = Change(self.client)
