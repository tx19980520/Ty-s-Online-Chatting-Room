import socketserver
from time import ctime
import json
import sqlite3
import struct
import pickle
from time import ctime,sleep
BUFFSIZE = 4
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
#为了让数据库查询的时候返回的是一个list，list里面装的是dict

clientlist = []
invisiblelist = []
chatting = []
class MyServer(socketserver.BaseRequestHandler):
    def receiveSize(self):
        conn = self.request
        receive = conn.recv(4)
        return struct.unpack('i',receive)[0]
    def command(self):
        conn = self.request
        receive = conn.recv(4)
        try:
            command = struct.unpack('i',receive)[0]
            self.business[str(command)]()
        except:#可能有人只是打开了登陆页面但是后来直接关掉这个时候就会出现struct.error我们对其进行处理，直接断开链接
            return 0
        else:
            return command
    def receiveDict(self,size):
        conn = self.request
        receive = conn.recv(size)
        dicts = pickle.loads(receive)
        return dicts;
    def getDict(self):#收到指令后接受信息的最顶层封装
        try:
            return self.receiveDict(self.receiveSize())
        except:
            return None
    def sendPackages(self, command, dicts = None):
        conn = self.request
        command = struct.pack('i',command)
        if dicts != None:
            dicts = pickle.dumps(dicts)
            size = struct.pack('i',len(dicts))
            conn.sendall(command+size+dicts)
        else:
            conn.sendall(command)
    #############上述都是为了封装好用###############
    def photomessage(self):
        conn = self.request
        info = self.getDict()
        f = open("chattingpicture/"+info['filename'],'wb')
        while True:
            byte = self.getDict()
            if byte == None:
                sleep(0.1)
                continue
            if byte['data'] == -1:
                f.close()
                break
            f.write(byte['data'])
        m = {}
        m["sender"] = info['username']
        m['time'] = ctime()
        m["message"] = "@image:"+info['filename']
        chatting.append(m)
    def userUpdate(self):#用户修改个人信息
        conn = self.request
        update = self.getDict()
        dbconn = sqlite3.connect("user.db")
        cursor = dbconn.cursor()
        cursor.execute("UPDATE USERS SET NAME=\'"+update['name']+"\',PASSWORD=\'"+update['password']+"\',ADDRESS=\'"+update['address']+"\',AGE=\'"+update['age']+"\' WHERE ID="+str(update['id']))
        dbconn.commit()
        self.sendPackages(1)
    def dbRegister(self):#新user的服务器注册
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
    def checkAnyonehere(self):#服务器上提供收集history的服务，在每次聊天室没人的时候进行history的保存
    #对这个部分的开发比较少，暂时是把history以json的格式保存在文件中，这样以后对这个部分的开发也比较方便
        if len(clientlist) == 0:
            global chatting
            times = ctime().split(":")
            m = "-"#这个地方修改了格式，
            times = m.join(times)
            with open("history/"+times+'.txt',"w") as f:
                for message in chatting:
                    json.dump(message,f)
            chatting = []
    def clientDetach(self):
        conn = self.request
        info = self.getDict()
        for i in range(len(clientlist)):
            if clientlist[i] == info['username']:
                bye = {"sender":"administor","message":info['username']+" has quited the chattingroom, bye!",'time':ctime()}
                chatting.append(bye)
                del clientlist[i]
                break
        self.checkAnyonehere()
        #下述是两个状态的改变
    def invisiState(self):
        conn = self.request
        info =self.getDict()
        invisiblelist.append(info['username'])
        clientlist.remove(info['username'])
        bye = {"sender":"administor","message":info['username']+" has quited the chattingroom, bye!",'time':ctime()}
        chatting.append(bye)
    def onlineState(self):
        conn = self.request
        info =self.getDict()
        clientlist.append(info['username'])
        invisiblelist.remove(info['username'])
        hello = {"sender":"administor","message":info['username']+" has entered the chattingroom!",'time':ctime()}
        chatting.append(hello)
        #更新当前的文件消息
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
            tmp = f.read(2048)
            if len(tmp)<2048:
                dicts = {'data':tmp,'num':-2}
            else:
                dicts = {'data':tmp,'num':2048}
            dicts = pickle.dumps(dicts)
            l = struct.pack('i',len(dicts))
            conn.sendall(l+dicts)
    def filesDownload(self):
        conn = self.request
        info = self.getDict()
        f = open("files/"+info['filename'],'rb')
        while True:
            tmp = f.read(2048)
            if len(tmp)<2048:
                dicts = {'data':tmp,'num':-2}
            else:
                dicts = {'data':tmp,'num':2048}
            dicts = pickle.dumps(dicts)
            l = struct.pack('i',len(dicts))
            conn.sendall(l+dicts)
        f.close()
    def filesUpload(self):
        info = self.getDict()
        f = open("files/"+info['filename'],'wb')
        t= True
        while t:
            byte = self.getDict()
            if byte == None:
                break
            elif byte['num'] == -2:
                t = False
            f.write(byte['data'])
        f.close()
        dbconn = sqlite3.connect('user.db')
        dbconn.row_factory = dict_factory
        cursor = dbconn.cursor()
        cursor.execute("INSERT INTO FILES (FILENAME,SIZE,USERNAME) VALUES ("+"\'"+info['filename']+"\',\'"+info['size']+"\',\'"+info['username']+"\')")
        dbconn.commit()
        dbconn.close()
        m = {}
        m["sender"] = "administor"
        m['time'] = ctime()
        m["message"] = info['username']+" has uploaded "+info['filename']+" , "+info['size']
        chatting.append(m)
    def chat(self):
         package = self.getDict()#sender and message
         package['time'] = ctime()
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
        user['NOW'] = str(len(clientlist))
        self.sendPackages(1,user)
    def login(self):
        conn = self.request
        data = self.getDict()
        dbconn = sqlite3.connect('user.db')
        dbconn.row_factory = dict_factory
        cursor = dbconn.cursor()
        cursor.execute("SELECT * from users  where name = "+"\'"+data['username']+"\'")
        try:#如果数据库根本就没有人，则我们下述语句会出现IndexError，对此进行异常处理
            user = cursor.fetchall()[0]
        except IndexError:
            returnCommand = struct.pack('i',0)
            conn.sendall(returnCommand)
            return
        if user['PASSWORD'] == data['password']:
            returnCommand =struct.pack('i',1)
            conn.sendall(returnCommand)
            clientlist.append(data['username'])
            hello = {"sender":"administor","message":data['username']+" has entered the chattingroom!",'time':ctime()}
            chatting.append(hello)
            return
    def handle(self):
        self.business= {'0':self.logDetach,'1':self.login,'2':self.info,'3':self.chat,\
        '4':self.handlePoll,'5':self.filesUpload,'6':self.filesDownload,'7':self.fileInfo,"8":self.clientDetach,\
        "9":self.dbRegister,"10":self.userUpdate,"11":self.photomessage,"12":self.askImage,'13':self.invisiState,"14":self.onlineState}
        print('...connected from:'+self.client_address[0]+"...")
        Flag = True
        conn = self.request
        while Flag:
            cmd = self.command()
            if cmd == 8 or cmd == 0:
                break;


if __name__ == '__main__':
    server = socketserver.ThreadingTCPServer(('0.0.0.0', 14333), MyServer)
    server.serve_forever()
