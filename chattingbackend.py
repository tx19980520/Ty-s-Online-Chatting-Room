from PyQt5 import QtCore, QtGui, QtWidgets
import struct
import pickle
from time import sleep
from files import FilePip,FileDownload
class Client(QtCore.QThread):
    hasNews = QtCore.pyqtSignal(dict)
    Info = QtCore.pyqtSignal(dict)
    fileinfomation = QtCore.pyqtSignal(list)
    detachlink = QtCore.pyqtSignal()
    senduploadsucess = QtCore.pyqtSignal(str)
    changeresult = QtCore.pyqtSignal(int)
    def __init__(self,link,username='',age=0,address=''):
        super(Client,self).__init__()
        self.id = 0
        self.link = link
        self.username = username
        self.age = age
        self.address = address
        self.num = -1
        self.q = False
        self.link.link()
    def sendmessage(self,message):
        command = self.link.commandHandle(3)
        dicts = {'sender':self.username,'message':message}
        packages =self.link.packagesHandle(dicts)
        self.link.send(command+packages)
    def run(self):
        while not self.q:
            sleep(1)
            command = self.link.poll(self.num)
            if command == 3:
                packages = self.link.receive_packages()
                self.num += 1
                if "@image:" in packages['message']:
                    self.downloadImageMessage(packages["message"][7:])
                    while not self.imageDownloadThread.singal:
                        sleep(0.2)
                self.hasNews.emit(packages)
            elif command == 0 or command == 8:
                break
        self.quit()
    def getInfo(self):
        command = 2
        command = self.link.commandHandle(command)
        packages = {'username':self.username}
        packages = pickle.dumps(packages,protocol=1)
        lpackages = len(packages)
        lpackages = struct.pack('i',lpackages)
        self.link.send(command+lpackages+packages)
        receive = self.link.receive_command()#返回值只可能是0或1，0表示错误，1表示正确并继续读取后续信息
        if receive == 1:
            info = self.link.receive_packages()
            self.password = info['PASSWORD']
            self.address = info['ADDRESS']
            self.id = info['ID']
            self.age = info['AGE']
            self.num = info['NUM']
            info['COMMAND'] = 1
        else:
            info = {}
            info['COMMAND'] = 0
        self.Info.emit(info)
    def fileInfo(self):
        command = 7
        command = self.link.commandHandle(command)
        self.link.send(command)
        receive = self.link.receive_packages()#反给我的是一个list里面装的是dict
        self.fileinfomation.emit(receive)
    def downloadFile(self,filename):
        self.downloadThread = FileDownload(filename)
        self.downloadThread.start()
    def downloadImageMessage(self,filename):
        self.imageDownloadThread = FileDownload(filename,1)
        self.imageDownloadThread.start()
    def addFile(self,filepath):
        self.uploadThread = FilePip(filepath,self.username)
        self.uploadThread.uploadComplete.connect(self.sendUploadSucess)
        self.uploadThread.start()
    def addPhoto(self,filepath,special):
        self.photoThread = FilePip(filepath,self.username,special)
        self.photoThread.start()
    def sendUploadSucess(self,s):
        self.senduploadsucess.emit(s)
    def detach(self):
        self.q= True
        sleep(1)
        command = 8
        command = self.link.commandHandle(command)
        packages = {"username":self.username}
        packages = pickle.dumps(packages,protocol=1)
        lpackages = len(packages)
        lpackages = struct.pack('i',lpackages)
        self.link.send(command+lpackages+packages)
        self.detachlink.emit()
    def userInfoChange(self,dicts):
        command = self.link.commandHandle(10)
        dicts['id'] = self.id
        packages = self.link.packagesHandle(dicts)
        self.link.send(command+packages)
        feedback = self.link.receive_command()
        self.changresult.emit(feedback)
