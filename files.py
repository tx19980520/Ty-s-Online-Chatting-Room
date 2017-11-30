from PyQt5 import QtCore
import struct
import pickle
from tcpclisock import tcpCliSock
import os
from time import sleep
import re
HOST = '127.0.0.1'
PORT = 23333
BUFSIZE = 1024
ADDR=(HOST,PORT)
class FilePip(QtCore.QThread,tcpCliSock):
    hasNewFile = QtCore.pyqtSignal()
    def __init__(self,filepath,username):
        super(Filepip,self).__init__()
        self.path = filepath
        path,self.filename = os.path.split(filepath)
        self.username = username
        self.size = str(os.path.getsize(filepath)/float(1024*1024))
        self.size = re.match("[0-9]*\.[0-9][0-9]",self.size).group()
    def run(self):
        self.link()
        f = open(self.path,'rb')
        command = 5
        command = struct.pack('i',command)
        self.send(command)
        simpleInfo = {'username':self.username,'filename':self.filename,'size':self.size}
        simpleInfo = self.packagesHandle(simpleInfo)
        self.send(simpleInfo)
        while True:
            tmp = f.read(BUFSIZE)
            if not tmp:
                d = {'data':123}
                d =self.packagesHandle(d)
                self.send(d)
                break;
            d = {'data':tmp}
            d = self.packagesHandle(d)
            self.send(d)
        self.quit()
class FileDownload(QtCore.QThread,tcpCliSock):
    def __init__(self,filename):
        super(FileDownload,self).__init__()
        self.filename = filename
    def run(self):
        self.link()
        command = 6
        command = self.commandHandle(command)
        info = {'filename':self.filename}
        info = self.packagesHandle(info)
        f = open('s'+self.filename,'wb')
        self.send(command+info)
        while True:
            packages = self.receive_packages()#package include data and num
            if packages['num'] == -2:
                f.close()
                break
            f.write(packages['data'])
        self.quit()
def main():
    test = FileDownload('tx.mp3')
    test.start()
    while True:
        sleep(5)
if __name__ == '__main__':
    main()
