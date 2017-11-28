from PyQt5 import QtCore, QtGui, QtWidgets

class Client(QtCore.QThread):
    hasNews = QtCore.pyqtSignal(dict)
    Info = QtCore.pyqtSignal(dict)
    def __init__(self,link,username='',age=0,address=''):
        super(Client,self).__init__()
        self.link = link
        self.username = username
        self.age = age
        self.address = address
        self.num = -1
    def sendmessage(self,message):
        command = self.link.commandHandle(3)
        dicts = {'sender':self.username,'message':message}
        packages =self.link.packagesHandle(dicts)
        self.link.send(command+packages)
    def run(self):
        while True:
            sleep(1)
            command = self.link.poll(self.num)
            print(self.num)
            print(command)
            if command == 3:
                packages = self.link.receive_packages()
                self.num += 1
                self.hasNews.emit(packages)
            elif command == 0:
                break
    def getInfo(self):
        command = 2
        command = self.link.commandHandle(command)
        packages = {'username':self.client.username}
        packages = pickle.dumps(packages)
        lpackages = len(packages)
        lpackages = struct.pack('i',lpackages)
        self.client.link.send(command+lpackages+packages)
        receive = self.client.link.receive_command()#返回值只可能是0或1，0表示错误，1表示正确并继续读取后续信息
        if receive == 1:
            info = self.link.receive_packages()
            self.address = info['ADDRESS']
            self.age = info['AGE']
            info['COMMAND'] = 1
        else:
            info = {}
            info['COMMAND'] = 0
        self.Info.emit(info)
