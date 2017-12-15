from PyQt5 import QtCore
import gzip
import struct
import pickle
from tcpclisock import tcpCliSock
import os
from time import sleep
import re
from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
HOST = '127.0.0.1'
PORT = 23333
BUFSIZE = 1024
ADDR=(HOST,PORT)
class FilePip(QtCore.QThread,tcpCliSock):
    hasNewFile = QtCore.pyqtSignal()
    uploadComplete = QtCore.pyqtSignal(str)
    def __init__(self,filepath,username,special=0):
        super(FilePip,self).__init__()
        self.path = filepath
        self.special = special
        print (special)
        path,self.filename = os.path.split(filepath)
        self.username = username
        self.size = str(os.path.getsize(filepath)/float(1024*1024))
        self.size = re.match("[0-9]*\.[0-9][0-9]",self.size).group()
    def run(self):
        self.link()
        if self.special == 0:
            command = 5
            command = struct.pack('i',command)
            self.send(command)
            simpleInfo = {'username':self.username,'filename':self.filename,'size':self.size}
            simpleInfo = self.packagesHandle(simpleInfo)
            self.send(simpleInfo)
            f = open(self.path,'rb')
            t=True
            while t:
                tmp = f.read(BUFSIZE)
                if len(tmp)<BUFSIZE:
                    dicts = {'data':tmp,'num':-2}
                    t = False
                else:
                    dicts = {'data':tmp,'num':BUFSIZE}
                dicts = pickle.dumps(dicts)
                l = struct.pack('i',len(dicts))
                self.send(l+dicts)
                sleep(0.1)
            f.close()
            self.uploadComplete.emit(self.filename)
            self.quit()
        elif self.special == 1:
            f = open(self.path,'rb')
            command = 11
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
    downloadSucess = QtCore.pyqtSignal(str)
    def __init__(self,filename='',special=0,files=None):
        super(FileDownload,self).__init__()
        self.filename = filename
        self.special = special
        self.files =files
        self.signal = False;
    def run(self):
        self.link()
        if self.special == 1:
            command =12
        else:
            command = 6
        command = self.commandHandle(command)
        if self.filename !='' and self.files == None:
            info = {'filename':self.filename}
            info = self.packagesHandle(info)
            self.send(command+info)
            if self.special == 1:
                f = open("message/image/"+self.filename,"wb")
            else:
                f = open('download_'+self.filename,'wb')
            t = True
            while t:
                packages = self.receive_packages()#package include data and num
                if packages == None:
                    break
                elif packages['num'] == -2:
                    t = False
                f.write(packages['data'])
                sleep(0.1)
            f.close()
            if self.special == 1:
                self.imageAdjust("message/image/"+self.filename)
                self.signal = True
            else:
                self.downloadSucess.emit(self.filename)
        elif self.files != None:
            for filename in files:
                info = {'filename':filename}
                info = self.packagesHandle(info)
                self.send(command+info)
                f = open('history/'+filename,'wb')
                t = True
                while t:
                    packages = self.receive_packages()#package include data and num
                    if packages == None:
                        break
                    elif packages['num'] == -2:
                        t = False
                    f.write(packages['data'])
                    sleep(0.1)
                f.close()
            self.downloadSucess.emit("History")
        self.quit()
    def imageAdjust(self,s):
        im = Image.open(s)
        (x,y) = im.size
        x_ = x
        y_ = y
        while x_ > 350:
            x_ /= 1.1
            y_ /= 1.1
        x_ = int(x_)
        y_ = int(y_)
        out = im.resize((x_, y_), Image.ANTIALIAS)
        out.save(s)
def main():
    test = FileDownload('tx.mp3')
    test.start()
    while True:
        sleep(5)
if __name__ == '__main__':
    main()
