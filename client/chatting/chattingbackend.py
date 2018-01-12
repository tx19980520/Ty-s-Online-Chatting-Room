from PyQt5 import QtCore, QtGui, QtWidgets
import struct
import pickle
from time import sleep
from chatting.files import FilePip,FileDownload
class Client(QtCore.QThread):
    hasnews = QtCore.pyqtSignal(dict)
    info = QtCore.pyqtSignal(dict)#进入房间得到自己和之前房间的一些消息发送到前端
    newinfo = QtCore.pyqtSignal(dict)#轮询得到消息传递到前端
    fileinfomation = QtCore.pyqtSignal(list)#传进文件的消息
    senduploadsucess = QtCore.pyqtSignal(str)
    senddownloadsucess = QtCore.pyqtSignal(str)
    changeresult = QtCore.pyqtSignal(int)
    filedatatofront = QtCore.pyqtSignal(str,float)
    def __init__(self,link,username='',age=0,address=''):
        super(Client,self).__init__()#鉴于可能在本地就会调用到一些信息，会对发送下来的信息做保存
        self.id = 0
        self.connection = link
        self.username = username
        self.age = age
        self.address = address
        self.num = -1
        self.q = False
        self.connection.link()
    def sendMessage(self,message):
        command = self.connection.commandHandle(3)
        dicts = {'sender':self.username,'message':message}
        packages =self.connection.packagesHandle(dicts)
        self.connection.send(command+packages)
    def run(self):#这个部分是对QThread run的复写，主要是处理轮询
        while not self.q:
            sleep(1)#防止网络情况不太好的情况下数据不到位的情况
            command = self.connection.poll(self.num)
            if command == 3:
                packages = self.connection.receivePackages()
                self.num += 1
                if "@image:" in packages['message']:#通知有图片消息
                    self.downloadImageMessage(packages["message"][7:])#启发下载图片，另开线程
                    while not self.imageDownloadThread.signal:
                        sleep(1)
                self.hasnews.emit(packages)
            elif command == 0 or command == 8:
                break
        self.quit()
    def invisibleModel(self):#用于更新为隐身状态
        command = 13
        command = self.connection.commandHandle(command)
        packages = {'username':self.username}
        packages = pickle.dumps(packages)
        lpackages = len(packages)
        lpackages = struct.pack('i',lpackages)
        self.connection.send(command+lpackages+packages)
    def onlineModel(self):#用于更新为在线状态
        command = 14
        command = self.connection.commandHandle(command)
        packages = {'username':self.username}
        packages = pickle.dumps(packages)
        lpackages = len(packages)
        lpackages = struct.pack('i',lpackages)
        self.connection.send(command+lpackages+packages)
    def getInfo(self,model=1):#最开始初始化自身的数据，以及如果存在修改的情况也会启用
        command = 2
        command = self.connection.commandHandle(command)
        packages = {'username':self.username}
        packages = pickle.dumps(packages)
        lpackages = len(packages)
        lpackages = struct.pack('i',lpackages)
        self.connection.send(command+lpackages+packages)
        receive = self.connection.receiveCommand()#返回值只可能是0或1，0表示错误，1表示正确并继续读取后续信息
        if receive == 1:
            info = self.connection.receivePackages()
            self.password = info['PASSWORD']
            self.address = info['ADDRESS']
            self.id = info['ID']
            self.age = info['AGE']
            self.now = info['NOW']
            if model == 1:
                self.num = info['NUM']
            info['COMMAND'] = 1
        else:
            info = {}
            info['COMMAND'] = 0
        if model == 1:#这里是两个不同的地方出里
            self.info.emit(info)
        else:
            self.newinfo.emit(info)
    def fileInfo(self):#从服务器得到实时的文件数据
        command = 7
        command = self.connection.commandHandle(command)
        self.connection.send(command)
        receive = self.connection.receivePackages()#反给我的是一个list里面装的是dict
        try:
            self.fileinfomation.emit(receive)
        except TypeError:
            while receive == None:
                receive = self.connection.receivePackages()
            self.fileinfomation.emit(receive)
    def downloadFile(self,filename):#经过测试是可以多个文件下载的
        self.downloadThread = FileDownload(filename)
        self.downloadThread.downloadsucess.connect(self.sendDownloadSucess)
        self.downloadThread.downloadnum.connect(self.downloadnumtoFront)
        self.downloadThread.start()
    def downloadImageMessage(self,filename):
        self.imageDownloadThread = FileDownload(filename,1)
        self.imageDownloadThread.start()
    def addFile(self,filepath):
        self.uploadThread = FilePip(filepath,self.username)
        self.uploadThread.uploadcomplete.connect(self.sendUploadSucess)
        self.uploadThread.start()
    def addPhoto(self,filepath,special):
        self.photoThread = FilePip(filepath,self.username,special)
        self.photoThread.start()
    def sendUploadSucess(self,s):#一下两个信号主要是相当于再做一次封装，方便操作
        self.senduploadsucess.emit(s)
    def sendDownloadSucess(self,s):
        self.senddownloadsucess.emit(s)
        self.fileInfo()
    def downloadnumtoFront(self,str,num):
        self.filedatatofront.emit(str,num)
    def detach(self):#向服务器发送消息准备离开
        self.q= True
        sleep(1)
        command = 8
        command = self.connection.commandHandle(command)
        packages = {"username":self.username}
        packages = pickle.dumps(packages)
        lpackages = len(packages)
        lpackages = struct.pack('i',lpackages)
        self.connection.send(command+lpackages+packages)
        self.connection.client.close()
    def userInfoChange(self,dicts):
        command =10
        dicts['id'] = self.id
        self.connection.sendPackages(command,dicts)
        feedback = self.connection.receiveCommand()
        self.changeresult.emit(feedback)
        self.getInfo(model=2)
