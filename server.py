import socketserver
from time import ctime
import sqlite3
import struct
import pickle
from time import ctime
from queue import *
BUFFSIZE = 4
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
#为了让数据库查询的时候返回的是一个list，list里面装的是dict

clientlist = []
chatting = []
class MyServer(socketserver.BaseRequestHandler):
    def receiveSize(self):
        conn = self.request
        receive = conn.recv(4)
        return struct.unpack('i',receive)[0]
    def Command(self):
        conn = self.request
        receive = conn.recv(4)
        command = struct.unpack('i',receive)[0]
        self.business[str(command)]()
        return command
    def receiveDict(self,size):
        conn = self.request
        receive = conn.recv(size)
        dicts = pickle.loads(receive)
        return dicts;
    def getDict(self):
        return self.receiveDict(self.receiveSize())
    def sendPackages(self, command, dicts = None):
        conn = self.request
        command = struct.pack('i',command)
        if dicts != None:
            dicts = pickle.dumps(dicts)
            size = struct.pack('i',len(dicts))
            conn.sendall(command+size+dicts)
        else:
            conn.sendall(command)
    #上述都是为了封装好用
    def photomessage(self):
        conn = self.request
        info = self.getDict()
        f = open("chattingpicture/"+info['filename'],'wb')
        while True:
            byte = self.getDict()
            if byte['data'] == 123:
                f.close()
                break
            f.write(byte['data'])
        m = {}
        m["sender"] = info['username']
        m['time'] = ctime()
        m["message"] = "@image:"+info['filename']
        chatting.append(m)
    def userUpdate(self):
        conn = self.request
        update = self.getDict()
        dbconn = sqlite3.connect("user.db")
        cursor = dbconn.cursor()
        cursor.execute("UPDATE USERS SET NAME=\'"+update['name']+"\',PASSWORD=\'"+update['password']+"\',ADDRESS=\'"+update['address']+"\',AGE=\'"+update['age']+"\' WHERE ID="+update['id'])
        dbconn.commit()
        self.sendPackages(1)
    def dbRegister(self):
        conn = self.request
        info = self.getDict()
        dbconn = sqlite3.connect('user.db')
        cursor = dbconn.cursor()
        cursor.execute("select id from USERS where name = \'"+info['name']+"\'")
        result = cursor.fetchall()
        if result:
            self.sendPackages(2)
        else:
            cursor.execute("INSERT INTO USERS (NAME,AGE,ADDRESS,PASSWORD) VALUES (\'"+info['name']+"\',\'"+info['age']+"\',\'"+info['address']+"\',\'"+info['password']+"\')")
            dbconn.commit()
            dbconn.close()
            self.sendPackages(1)
    def logDetach(self):
        return 0
    def clientDetach(self):
        conn = self.request
        info = self.getDict()
        for i in range(len(clientlist)):
            if clientlist[i]["NAME"] == info['username']:
                bye = {"sender":"administor","message":info['username']+" has quited the chattingroom, bye!",'time':ctime()}
                chatting.append(bye)
                clientlist.remove(clientlist[i])
                break
    def fileInfo(self):
        conn = self.request
        dbconn = sqlite3.connect('user.db')
        dbconn.row_factory = dict_factory
        cursor = dbconn.cursor()
        cursor.execute("select* from FILES")
        files = cursor.fetchall()
        files = pickle.dumps(files)
        l = struct.pack('i',len(files))
        conn.sendall(l+files)
    def askImage(self):
        conn = self.request
        info = self.getDict()
        f = open("chattingpicture/"+info['filename'],"rb")
        while True:
            tmp = f.read(1024)
            if len(tmp)<1024:
                dicts = {'data':tmp,'num':-2}
            else:
                dicts = {'data':tmp,'num':1024}
            dicts = pickle.dumps(dicts)
            l = struct.pack('i',len(dicts))
            conn.send(l+dicts)
    def FilesDownload(self):
        conn = self.request
        info = self.getDict()
        f = open(info['filename'],'rb')
        while True:
            tmp = f.read(1024)
            if len(tmp)<1024:
                dicts = {'data':tmp,'num':-2}
            else:
                dicts = {'data':tmp,'num':1024}
            dicts = pickle.dumps(dicts)
            l = struct.pack('i',len(dicts))
            conn.send(l+dicts)
    def FilesUpload(self):
        info = self.getDict()
        dbconn = sqlite3.connect('user.db')
        dbconn.row_factory = dict_factory
        cursor = dbconn.cursor()
        cursor.execute("INSERT INTO FILES (FILENAME,SIZE,USERNAME) VALUES ("+"\'"+info['filename']+"\',\'"+info['size']+"\',\'"+info['username']+"\')")
        dbconn.commit()
        dbconn.close()
        f = open(info['filename'],'wb')
        while True:
            byte = self.getDict()
            if byte['data'] == 123:
                f.close()
                break
            f.write(byte['data'])
        m = {}
        m["sender"] = "administor"
        m['time'] = ctime()
        m["message"] = info['username']+" has uploaded "+info['filename']+" , "+info['size']
        chatting.append(m)
    def chat(self):
         package = self.getDict()#sender and message
         package['time'] = ctime()
         print (package)
         chatting.append(package)
    def handlePoll(self):
        package = self.getDict()
        if package['num'] == len(chatting) or package['num'] == -1:
            self.sendPackages(2)#2表示轮询没有新消息
        else:
            news = chatting[package['num']]
            self.sendPackages(3,news)#3表示轮询得到新消息
    def info(self):
        dicts = self.getDict()
        check = dicts['username']
        print(check)
        dbconn = sqlite3.connect('user.db')
        dbconn.row_factory = dict_factory
        cursor = dbconn.cursor()
        cursor.execute("SELECT * from users where name= "+"\'"+check+"\'")
        user = cursor.fetchall()[0]
        cursor.execute("SELECT name FROM users")
        users = cursor.fetchall()
        if len(chatting) == 0:
            user['NUM'] = len(chatting)#附带一条现在的聊到哪里了
        elif len(chatting) != 0:
            user['NUM'] = len(chatting)-1
        user['PERSONS'] = str(len(users))
        user['SPESIFIC'] = clientlist
        print(users)
        user['NOW'] = str(len(clientlist))
        self.sendPackages(1,user)

    def login(self):
        print("login")
        conn = self.request
        data = self.getDict()
        dbconn = sqlite3.connect('user.db')
        dbconn.row_factory = dict_factory
        cursor = dbconn.cursor()
        cursor.execute("SELECT * from users  where name = "+"\'"+data['username']+"\'")
        user = cursor.fetchall()[0]
        if user['PASSWORD'] == data['password']:
            returnCommand =struct.pack('i',1)
            conn.send(returnCommand)
            clientlist.append(user)###这个地方想想咋写
            hello = {"sender":"administor","message":data['username']+" has entered the chattingroom!",'time':ctime()}
            chatting.append(hello)
            return
        returnCommand = struct.pack('i',0)
        conn.send(returnCommand)
        return
    def handle(self):
        self.business= {'0':self.logDetach,'1':self.login,'2':self.info,'3':self.chat,'4':self.handlePoll,'5':self.FilesUpload,'6':self.FilesDownload,'7':self.fileInfo,"8":self.clientDetach,"9":self.dbRegister,"10":self.userUpdate,"11":self.photomessage,"12":self.askImage}
        print('...connected from:'+self.client_address[0])
        Flag = True
        conn = self.request
        while Flag:
            cmd = self.Command()
            if cmd == 8 or cmd == 0:
                break;



if __name__ == '__main__':
    server = socketserver.ThreadingTCPServer(('127.0.0.1', 23333), MyServer)
    server.serve_forever()
