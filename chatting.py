import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
from chattingfrontend import *
from chattingbackend import *
from change import *
import tcpclisock
class Chatting(QtCore.QObject):
    def __init__(self,username):
        super(Chatting,self).__init__()
        self.window = QtWidgets.QDialog()
        self.tmp =tcpclisock.tcpCliSock()
        self.client = Client(self.tmp,username)
        self.ui = chattingfrontend(self.window)
        self.client.hasNews.connect(self.ui.showMessage)
        self.client.Info.connect(self.ui.infoDump)
        self.client.fileinfomation.connect(self.ui.setFile)
        self.ui.gui.tabWidget.currentChanged.connect(self.client.fileInfo)
        self.ui.gui.change_info.clicked.connect(self.enterChange)
        self.ui.messagetoServer.connect(self.client.sendmessage)
        self.ui.propare.connect(self.client.downloadFile)
        self.ui.detach.connect(self.client.detach)
        self.ui.newFile.connect(self.client.addFile)
        self.ui.newPhoto.connect(self.client.addPhoto)
        self.client.senduploadsucess.connect(self.ui.sucessinfo)
        self.client.detachlink.connect(self.detachLink)
        self.client.getInfo()
        self.client.start()
        self.window.show()
    def detachLink(self):
        self.client.link.client.close()
    def enterChange(self):
        self.change = Change(self.client)
