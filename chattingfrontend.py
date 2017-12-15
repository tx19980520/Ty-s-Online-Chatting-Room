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
class downloadButton(QtWidgets.QPushButton):
    shot_id = QtCore.pyqtSignal(int)
    def __init__(self,i):
        super(downloadButton,self).__init__()
        self.id = i
        self.clicked.connect(self.shot)
        self.setText("Download")
        self.setStyleSheet(''' text-align : center;                                       background-color : NavajoWhite;
                                            height : 30px;
                                            border-style: outset;
                                           font : 17px  ''')
    def shot(self):
        self.shot_id.emit(self.id)
class chattingfrontend(QtCore.QObject):
    messagetoServer = QtCore.pyqtSignal(str)
    propare = QtCore.pyqtSignal(str)
    detach = QtCore.pyqtSignal()
    newFile = QtCore.pyqtSignal(str)
    newPhoto = QtCore.pyqtSignal(str,int)
    messageImage = QtCore.pyqtSignal(str)
    def __init__(self,window):
        super(chattingfrontend,self).__init__()
        self.buttons = []
        self.now = 0
        self.allPersons = 0
        self.window = window
        self.username = ''
        self.gui = Ui_Chat(window)
        self.gui.messages.textChanged.connect(self.movecursor)
        self.gui.send.clicked.connect(self.sendMessage)
        self.gui.upload.clicked.connect(self.chooseFile)
        self.gui.photo.clicked.connect(self.choosePhoto)
    def choosePhoto(self):
        filepath,filetype = QtWidgets.QFileDialog.getOpenFileNames(self.window,"选择发送图片（可多选）","D:/","Image Files(*.png *.jpg *.bmp *.gif)")
        self.newPhoto.emit(filepath[0],1)
    def chooseFile(self):
        filepath,filetype = QtWidgets.QFileDialog.getOpenFileNames(self.window,"选择上传文件（可多选）","C:/","All Files (*)")
        self.newFile.emit(filepath[0])
    def downloadSucessInfo(self,s):
        sucess =QMessageBox.about(self.window,"Sucess!","您已成功下载%s！"%(s))
    def uploadSucessInfo(self,s):
        sucess =QMessageBox.about(self.window,"Sucess!","您已成功上传%s！"%(s))
    def closeReady(self):
        self.detach.emit()
    def clientNow(self,text,l=None):
        _translate =QtCore.QCoreApplication.translate
        self.gui.show_people.setText(_translate("Dialog",text))
        if l != None:
            for user in l:
                row_count = self.gui.users.rowCount()
                self.gui.users.insertRow(row_count)
                self.gui.users.setItem(row_count,0,QtWidgets.QTableWidgetItem(user['NAME']))
    def infoDump(self,dicts):#初始化数据
        _translate =QtCore.QCoreApplication.translate
        if dicts['COMMAND']== 1:
            self.gui.address.setText(_translate("Dialog", dicts['ADDRESS']))
            self.username = dicts['NAME']
            self.allPersons = int(dicts['PERSONS'])
            self.now = int(dicts['NOW'])
            self.gui.name.setText(_translate("Dialog", dicts['NAME']))
            self.gui.age.setText(_translate("Dialog", str(dicts['AGE'])))
            self.clientNow(dicts["NOW"]+'/'+dicts['PERSONS'],dicts['SPESIFIC'])
        else:
            error = QMessageBox.warning(self.window, "Warning","你的网络出现问题，无法查询到你的信息！",QMessageBox.Yes)
    def sendMessage(self):
        s = self.gui.Edit.toPlainText()#test ok!
        if s == "":
            error = QMessageBox.warning(self.window, "Warning","你不能发送空白消息！",QMessageBox.Yes)
            return
        self.gui.Edit.setPlainText("")
        self.messagetoServer.emit(s)
    def showMessage(self,dicts):
        line1 = dicts['sender']+" "+dicts['time']#sender message time
        line2 = dicts['message']
        #info['username']+" has quited the chattingroom,bye!"
        if dicts['sender'] == "administor":
            tmp = dicts['message'].split(" ")
            if "entered" in tmp and self.username not in tmp:
                row_count = self.gui.users.rowCount()
                self.now += 1
                s = str(self.now)+'/'+str(self.allPersons)
                self.clientNow(s)
                self.gui.users.insertRow(row_count)
                self.gui.users.setItem(row_count,0,QtWidgets.QTableWidgetItem(tmp[0]))
            elif "quited" in tmp:
                row_count = self.gui.users.rowCount()
                for i in range(row_count+1):
                    if self.gui.users.item(i,0).text() == tmp[0]:
                        self.gui.users.removeRow(i)
                        break
                self.now -= 1
                s = str(self.now)+'/'+str(self.allPersons)
                self.clientNow(s)
            elif "uploaded" in tmp:
                row_count = self.gui.tableWidget.rowCount()
                self.gui.tableWidget.insertRow(row_count)
                button = downloadButton(row_count)
                self.buttons.append(button)
                button.shot_id.connect(self.preparefile)
                self.gui.tableWidget.setItem(row_count,0,QtWidgets.QTableWidgetItem(tmp[3]))
                self.gui.tableWidget.setItem(row_count,1,QtWidgets.QTableWidgetItem(tmp[-1]))
                self.gui.tableWidget.setItem(row_count,2,QtWidgets.QTableWidgetItem(tmp[0]))
                self.gui.tableWidget.setCellWidget(row_count,3,button)
                line1 = self.adminmessage(line1)
                line2 = self.adminmessage(line2)
                self.gui.messages.insertHtml(line1)
                self.gui.messages.insertHtml(line2)
                return
        elif "@image:" in dicts['message']:
            filename = "message/image/"+dicts['message'][7:]
            filename = self.changeHtml(filename)
            self.gui.messages.append(line1)
            self.gui.messages.insertHtml(filename)
            return
        else:
            line1 = self.normalmessage(line1)
            line2 = self.normalmessage(line2)
            self.gui.messages.append(line1)
            self.gui.messages.append(line2)
    def normalmessage(self,s):
        l = "<br><font size='4'>%s</font>"%(s)
        return l
    def adminmessage(self,s):
        l = "<br><font size='4' color='red'>%s</font>"%(s)
        return l
    def changeHtml(self,filename):
        s = "<br><img src=\"%s\">"%(filename)
        return s
    def movecursor(self):
        self.gui.messages.moveCursor(QtGui.QTextCursor.End)
    def setFile(self,files):
        row_count = self.gui.tableWidget.rowCount()
        if self.gui.tabWidget.currentIndex() == 0 or row_count >= len(files):
            return
        num = range(len(files))
        m = 0
        for f in files:
            p = m
            button = downloadButton(p)
            self.buttons.append(button)
            button.shot_id.connect(self.preparefile)
            row_count = self.gui.tableWidget.rowCount()
            self.gui.tableWidget.insertRow(row_count)
            self.gui.tableWidget.setItem(row_count,0,QtWidgets.QTableWidgetItem(f['FILENAME']))
            self.gui.tableWidget.setItem(row_count,1,QtWidgets.QTableWidgetItem(f['SIZE']))
            self.gui.tableWidget.setItem(row_count,2,QtWidgets.QTableWidgetItem(f['USERNAME']))
            self.gui.tableWidget.setCellWidget(row_count,3,button)
            m += 1
    def preparefile(self,num):
        print (num)
        filename = self.gui.tableWidget.item(num,0).text()
        print (filename)
        self.propare.emit(filename)
def main():
    app = QtWidgets.QApplication(sys.argv)
    w = QtWidgets.QDialog()
    form = Ui_Dialog()
    form.setupUi(w)
    w.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
