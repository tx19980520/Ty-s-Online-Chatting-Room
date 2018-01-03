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
class Qtray(QtCore.QObject):#我没有直接把这个托盘化模块放在window下，我放在Chattingfrontend
    invisistart = QtCore.pyqtSignal()
    invisiend = QtCore.pyqtSignal()
    hide = QtCore.pyqtSignal()
    show = QtCore.pyqtSignal()
    quitall = QtCore.pyqtSignal()
    def __init__(self):
        super(Qtray,self).__init__()
        self.mainshow =True
        self.isInvisible = False;
        self.tray = QtWidgets.QSystemTrayIcon()
        self.icon = QtGui.QIcon("systempic/ico.ico")
        self.hasmessage = QtGui.QIcon("systempic/hasmessage.ico")
        self.invisibleicon = QtGui.QIcon("systempic/invisible.ico")
        self.tray.setIcon(self.icon)  #设置系统托盘图标
        self.tray.activated.connect(self.iconClicked) #设置托盘点击事件处理函数
        self.traymenu = QtWidgets.QMenu(QtWidgets.QApplication.desktop()) #创建菜单
        self.minsize = QtWidgets.QAction('最小化 ',self,triggered=self.min)
        self.reopen = QtWidgets.QAction('还原 ', self, triggered=self.reOpen)
        self.quitaction = QtWidgets.QAction('退出 ', self, triggered=self.quit)
        self.cloaking = QtWidgets.QAction('隐身 ',self,triggered=self.invisible)
        self.hasonline = QtWidgets.QAction('在线 ',self,triggered=self.online)
        self.traymenu.addAction(self.reopen) #为菜单添加动作
        self.traymenu.addAction(self.quitaction)
        self.traymenu.addAction(self.cloaking)
        self.traymenu.addAction(self.hasonline)
        self.traymenu.addAction(self.minsize)
        self.tray.setContextMenu(self.traymenu) #设置系统托盘菜单
    def min(self):
        if self.mainshow:
            self.hide.emit()
            self.mainshow =False
    def iconClicked(self,signal):
        if self.mainshow and (signal == 2 or signal == 3):
            self.hide.emit()
            self.mainshow = False
        else:
            self.show.emit()#父类的显示
            self.mainshow = True
    def reOpen(self):
        pw = self.parent()
        if pw.isVisible():
            pw.hide()#父类的隐藏，这东西是放在window里面的
    def invisible(self):
        if self.isInvisible == False:
            self.isInvisible = True
            self.tray.setIcon(self.invisibleicon)
            self.invisistart.emit()
    def online(self):
        if self.isInvisible == True:
            self.isInvisible = False
            self.tray.setIcon(self.icon)
            self.invisiend.emit()
    def quit(self):
        self.quitall.emit()


class Downloadbutton(QtWidgets.QPushButton):
    shotid = QtCore.pyqtSignal(int)
    def __init__(self,i):#主要是为了处理点击时确定是哪一个文件
        super(Downloadbutton,self).__init__()
        self.id = i
        self.clicked.connect(self.shot)
        self.setText("Download")#给关闭按钮加样式
        self.setStyleSheet(''' text-align : center;                                       background-color : NavajoWhite;
                                            height : 30px;
                                            border-style: outset;
                                           font : 20px  ''')
    def shot(self):
        self.shotid.emit(self.id)
class Chattingfrontend(QtCore.QObject):
    messagetoserver = QtCore.pyqtSignal(str)
    propare = QtCore.pyqtSignal(str)
    detach = QtCore.pyqtSignal()
    newfile = QtCore.pyqtSignal(str)
    newphoto = QtCore.pyqtSignal(str,int)
    messageimage = QtCore.pyqtSignal(str)
    def __init__(self,window):
        super(Chattingfrontend,self).__init__()
        self.buttons = []
        self.nowpeople = []
        self.now = 0
        self.allPersons = 0
        self.window = window
        self.username = ''
        self.tr = Qtray()
        self.tr.tray.show()
        #gui信号连接
        self.gui = Ui_Chat(window)
        self.gui.messages.textChanged.connect(self.moveCursor)
        self.gui.send.clicked.connect(self.sendMessage)
        self.gui.upload.clicked.connect(self.chooseFile)
        self.gui.photo.clicked.connect(self.choosePhoto)
        self.tr.quitall.connect(self.trayClose)
    def choosePhoto(self):#选择图片
        filepath,filetype = QtWidgets.QFileDialog.getOpenFileNames(self.window,"选择发送图片（可多选）","D:/","Image Files(*.png *.jpg *.bmp *.gif)")
        self.newphoto.emit(filepath[0],1)
    def chooseFile(self):#选择文件
        filepath,filetype = QtWidgets.QFileDialog.getOpenFileNames(self.window,"选择上传文件（可多选）","C:/","All Files (*)")
        self.newfile.emit(filepath[0])
    def downloadSucessInfo(self,s):
        sucess =QMessageBox.about(self.window,"Sucess!","您已成功下载%s！"%(s))
    def uploadSucessInfo(self,s):
        sucess =QMessageBox.about(self.window,"Sucess!","您已成功上传%s！"%(s))
    def trayClose(self):
        self.closeReady()
        self.window.hide()
    def closeReady(self):
        self.detach.emit()
    def clientNow(self,text,l=None):#右下角显示现有的人数
        _translate =QtCore.QCoreApplication.translate
        self.gui.show_people.setText(_translate("Dialog",text))
        if l != None:
            self.nowpeople =l
            for user in l:
                row_count = self.gui.users.rowCount()
                self.gui.users.insertRow(row_count)
                self.gui.users.setItem(row_count,0,QtWidgets.QTableWidgetItem(user))
    def infoDump(self,dicts):#初始化数据
        _translate =QtCore.QCoreApplication.translate
        if dicts['COMMAND']== 1:
            self.username = dicts['NAME']
            self.allPersons = int(dicts['PERSONS'])
            self.now = int(dicts['NOW'])
            self.gui.address.setText(_translate("Dialog", dicts['ADDRESS']))
            self.gui.name.setText(_translate("Dialog", dicts['NAME']))
            self.gui.age.setText(_translate("Dialog", str(dicts['AGE'])))
            self.clientNow(dicts["NOW"]+'/'+dicts['PERSONS'],dicts['SPESIFIC'])
        else:
            error = QMessageBox.warning(self.window, "Warning","你的网络出现问题，无法查询到你的信息！",QMessageBox.Yes)
    def newInfoDump(self,dicts):
        _translate =QtCore.QCoreApplication.translate
        if dicts['COMMAND']== 1:
            self.username = dicts['NAME']
            self.allPersons = int(dicts['PERSONS'])
            self.gui.address.setText(_translate("Dialog", dicts['ADDRESS']))
            self.gui.name.setText(_translate("Dialog", dicts['NAME']))
            self.gui.age.setText(_translate("Dialog", str(dicts['AGE'])))
        else:
            error = QMessageBox.warning(self.window, "Warning","你的网络出现问题，无法查询到你的信息！",QMessageBox.Yes)
    def sendMessage(self):
        s = self.gui.Edit.toPlainText()#test ok!
        if s == "":
            error = QMessageBox.warning(self.window, "Warning","你不能发送空白消息！",QMessageBox.Yes)
            return
        self.gui.Edit.setPlainText("")
        self.messagetoserver.emit(s)
    def showMessage(self,dicts):
        line1 = dicts['sender']+" "+dicts['time']#sender message time
        line2 = dicts['message']
        #info['username']+" has quited the chattingroom,bye!"
        if dicts['sender'] == "administor":#一下是管理员消息的处理
            tmp = dicts['message'].split(" ")
            print(tmp)
            if "entered" in tmp and (self.username not in tmp ) and (tmp[0] not in self.nowpeople):
                self.nowpeople.append(tmp[0])
                print(self.nowpeople)
                row_count = self.gui.users.rowCount()
                self.now += 1
                s = str(self.now)+'/'+str(self.allPersons)
                self.clientNow(s)
                self.gui.users.insertRow(row_count)
                self.gui.users.setItem(row_count,0,QtWidgets.QTableWidgetItem(tmp[0]))
            elif "quited" in tmp and (self.username not in tmp )and (tmp[0] in self.nowpeople):#用户退出，去掉其在用户列表中的那一行
                row_count = self.gui.users.rowCount()
                for i in range(row_count+1):
                    if self.gui.users.item(i,0).text() == tmp[0]:
                        self.gui.users.removeRow(i)
                        self.nowpeople.remove(tmp[0])
                        break
                self.now -= 1
                s = str(self.now)+'/'+str(self.allPersons)
                self.clientNow(s)
            elif "uploaded" in tmp:
                row_count = self.gui.tableWidget.rowCount()
                self.gui.tableWidget.insertRow(row_count)
                button = Downloadbutton(row_count)
                self.buttons.append(button)
                button.shotid.connect(self.prepareFile)
                self.gui.tableWidget.setItem(row_count,0,QtWidgets.QTableWidgetItem(tmp[3]))
                self.gui.tableWidget.setItem(row_count,1,QtWidgets.QTableWidgetItem(tmp[-1]))
                self.gui.tableWidget.setItem(row_count,2,QtWidgets.QTableWidgetItem(tmp[0]))
                self.gui.tableWidget.setCellWidget(row_count,3,button)
                line2 += 'mb'
            line1 = self.adminMessage(line1)
            line2 = self.adminMessage(line2)
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
            line1 = self.normalMessage(line1)
            line2 = self.normalMessage(line2)
            self.gui.messages.append(line1)
            self.gui.messages.append(line2)
    def normalMessage(self,s):
        l = "<font size='4'>%s</font>"%(s)
        return l
    def adminMessage(self,s):#由于我们的展示的是使用的QTextBrowser,他是支持HTML格式的，下同
        l = "<br><font size='4' color='red'>%s</font>" % (s)
        return l
    def changeHtml(self,filename):
        s = "<br><img src=\"%s\">" % (filename)
        return s
    def moveCursor(self):
        self.gui.messages.moveCursor(QtGui.QTextCursor.End)
    def setFile(self,files):#对于每一次载入我们的文件页面，我们都会实时更新一下我们的文件相关数据
        row_count = self.gui.tableWidget.rowCount()
        if self.gui.tabWidget.currentIndex() == 0 or row_count >= len(files):
            return
        m = 0
        for f in files:
            p = m
            button = Downloadbutton(p)
            self.buttons.append(button)
            button.shotid.connect(self.prepareFile)
            row_count = self.gui.tableWidget.rowCount()
            self.gui.tableWidget.insertRow(row_count)
            self.gui.tableWidget.setItem(row_count,0,QtWidgets.QTableWidgetItem(f['FILENAME']))
            self.gui.tableWidget.setItem(row_count,1,QtWidgets.QTableWidgetItem(f['SIZE']))
            self.gui.tableWidget.setItem(row_count,2,QtWidgets.QTableWidgetItem(f['USERNAME']))
            self.gui.tableWidget.setCellWidget(row_count,3,button)
            m += 1
    def prepareFile(self,num):
        filename = self.gui.tableWidget.item(num,0).text()
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
