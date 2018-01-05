
# Form implementation generated from reading ui file 'chattingroom.ui'
#
# Created by: PyQt5 UI code generator 5.9.1
#
# WARNING! All changes made in this file will be lost!
#在基础界面设计完成后，为了使得我们的QSS独立与文档，我们对改文件直接进行了修改，切记不要被覆盖
import sys
import os
from PyQt5 import QtCore, QtGui, QtWidgets,Qt
import tcpclisock as tcp
from PyQt5.QtWidgets import QMessageBox
from time import sleep
from chattingui import *
class Qtray(QtCore.QObject):#我没有直接把这个托盘化模块放在window下，我放在Chattingfrontend
    invisistart = QtCore.pyqtSignal()
    invisiend = QtCore.pyqtSignal()
    hide = QtCore.pyqtSignal()
    show = QtCore.pyqtSignal()
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
        self.cloaking = QtWidgets.QAction('隐身 ',self,triggered=self.invisible)
        self.hasonline = QtWidgets.QAction('在线 ',self,triggered=self.online)
        self.traymenu.addAction(self.reopen) #为菜单添加动作
        self.traymenu.addAction(self.cloaking)
        self.traymenu.addAction(self.hasonline)
        self.traymenu.addAction(self.minsize)
        self.tray.setContextMenu(self.traymenu) #设置系统托盘菜单
    def min(self):
        if self.mainshow:
            self.hide.emit()
            self.mainshow =False
    def iconClicked(self,signal):
        if self.mainshow and (signal == 2 ):
            self.hide.emit()
            self.mainshow = False
        else:
            self.reOpen()
    def reOpen(self):
        self.show.emit()
        self.mainshow = True
        self.tray.setIcon(self.icon)
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
    def hasMessage(self):
        self.tray.setIcon(self.hasmessage)


class Downloadbutton(QtWidgets.QPushButton):
    shotid = QtCore.pyqtSignal(int)
    def __init__(self,i):#主要是为了处理点击时确定是哪一个文件
        super(Downloadbutton,self).__init__()
        self.id = i
        self.clicked.connect(self.shot)
        self.setText("Download")#给关闭按钮加样式
    def shot(self):
        self.shotid.emit(self.id)
class Chattingfrontend(QtCore.QObject):
    messagetoserver = QtCore.pyqtSignal(str)
    propare = QtCore.pyqtSignal(str)
    detach = QtCore.pyqtSignal()
    newfile = QtCore.pyqtSignal(str)
    newphoto = QtCore.pyqtSignal(str,int)
    messageimage = QtCore.pyqtSignal(str)
    changeico = QtCore.pyqtSignal()
    def __init__(self,window):
        super(Chattingfrontend,self).__init__()
        self.buttons = []
        self.nowpeople = []
        self.nowdownload = []
        self.process = {}
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
        self.changeico.connect(self.tr.hasMessage)
    def choosePhoto(self):#选择图片
        filepath,filetype = QtWidgets.QFileDialog.getOpenFileNames(self.window,"选择发送图片（可多选）","D:/","Image Files(*.png *.jpg *.bmp *.gif)")
        try:
            self.newphoto.emit(filepath[0],1)
        except:
            return
    def chooseFile(self):#选择文件
        filepath,filetype = QtWidgets.QFileDialog.getOpenFileNames(self.window,"选择上传文件（可多选）","C:/","All Files (*)")
        try:
            self.newfile.emit(filepath[0])
        except:
            return
    def downloadSucessInfo(self,s):
        self.nowdownload.remove(self.process[s+'id'])
        sucess =QMessageBox.about(self.window,"Sucess!","您已成功下载%s！"%(s))
    def uploadSucessInfo(self,s):
        sucess =QMessageBox.about(self.window,"Sucess!","您已成功上传%s！"%(s))
    def trayClose(self):
        self.closeReady()
        self.window.hide()
        self.tr.tray.hide()
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
                tmp = QtWidgets.QTableWidgetItem(user)
                tmp.setTextAlignment(QtCore.Qt.AlignCenter)
                self.gui.users.setItem(row_count,0,tmp)
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
            if "entered" in tmp and (self.username not in tmp ) and (tmp[0] not in self.nowpeople):
                self.nowpeople.append(tmp[0])
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
                self.gui.tableWidget.setCellWidget(row_count,4,button)
                line2 += 'mb'
            line1 = self.adminMessage(line1)
            line2 = self.adminMessage(line2,2)
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
            if self.username !=dicts['sender']:
                self.changeico.emit()
            line1 = self.normalMessage(line1)
            line2 = self.normalMessage(line2,2)
            self.gui.messages.append(line1)
            self.gui.messages.append(line2)
    def normalMessage(self,s,num=1):
        if num == 1:
            l = "<span style='font-weight:bold;'><font size='4'>%s</font></span>"%(s)
        else:
            l = "<font size='4'>%s</font>"%(s)
        return l
    def adminMessage(self,s,num=1):#由于我们的展示的是使用的QTextBrowser,他是支持HTML格式的，上同
        if num == 1:
            l = "<br><span style='font-weight:bold;'><font size='4' color='red'>%s</font></span>" % (s)
        else:
            l = "<br><font size='4' color='red'>%s</font>" % (s)
        return l
    def changeHtml(self,filename):
        s = "<br><img src=\"%s\">" % (filename)
        return s
    def moveCursor(self):
        self.gui.messages.moveCursor(QtGui.QTextCursor.End)
    def setFile(self,files):#对于每一次载入我们的文件页面，我们都会实时更新一下我们的文件相关数据
        self.gui.tableWidget.clear()
        row_count = row_count = self.gui.tableWidget.rowCount()
        need = len(files)
        while need > row_count:
            self.gui.tableWidget.insertRow(row_count)
            row_count += 1
        m = 0
        for f in files:
            p = m
            button = Downloadbutton(p)
            self.buttons.append(button)
            button.shotid.connect(self.prepareFile)
            t1 = QtWidgets.QTableWidgetItem(f['FILENAME'])
            t1.setTextAlignment(QtCore.Qt.AlignCenter)
            t2 = QtWidgets.QTableWidgetItem(f['SIZE'])
            t2.setTextAlignment(QtCore.Qt.AlignCenter)
            t3 = QtWidgets.QTableWidgetItem(f['USERNAME'])
            t3.setTextAlignment(QtCore.Qt.AlignCenter)
            if (os.path.exists("download/"+f['FILENAME']) and p not in self.nowdownload):
                t4 = QtWidgets.QTableWidgetItem("已下载")
                self.gui.tableWidget.setItem(p,3,t4)
            elif p in self.nowdownload:
                tmp = QtWidgets.QProgressBar()
                self.process[f['FILENAME']] = tmp
                tmp.setValue(self.process[f['FILENAME']+'num'])
                self.gui.tableWidget.setCellWidget(p,3,tmp)
            else:
                t4 = QtWidgets.QTableWidgetItem("未下载")
                self.gui.tableWidget.setItem(p,3,t4)
            t4.setTextAlignment(QtCore.Qt.AlignCenter)
            self.gui.tableWidget.setItem(p,0,t1)
            self.gui.tableWidget.setItem(p,1,t2)
            self.gui.tableWidget.setItem(p,2,t3)
            self.gui.tableWidget.setCellWidget(p,4,button)
            m += 1
    def prepareFile(self,num):
        filename = self.gui.tableWidget.item(num,0).text()
        tmp = QtWidgets.QProgressBar()
        tmp.setValue(0)
        self.nowdownload.append(num)
        self.gui.tableWidget.setCellWidget(num,3,tmp)
        self.process[filename]=tmp
        self.process[filename+'id'] = num
        self.propare.emit(filename)
    def getDownloadProcess(self,filename,num):
        total = float(self.gui.tableWidget.item(self.process[filename+'id'],1).text())
        if self.gui.tabWidget.currentIndex() == 1:
            self.process[filename+'num']=(round(100*num/total))
            self.process[filename].setValue(self.process[filename+'num'])
        else:
            self.process[filename+'num'] = (round(100*num/total))
def main():
    app = QtWidgets.QApplication(sys.argv)
    w = QtWidgets.QDialog()
    form = Ui_Dialog()
    form.setupUi(w)
    w.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
