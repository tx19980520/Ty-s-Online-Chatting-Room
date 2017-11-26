import socketserver
from time import ctime
import sqlite3
import struct
import pickle
from time import ctime
BUFFSIZE = 4
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
#为了让数据库查询的时候返回的是一个list，list里面装的是dict
class MyServer(socketserver.BaseRequestHandler):
    chatting = []
    clientlist = []
    def receiveSize(self):
        conn = self.request
        receive = conn.recv(4)
        return struct.unpack('i',receive)[0]
    def Command(self):
        conn = self.request
        receive = conn.recv(4)
        command = struct.unpack('i',receive)[0]
        self.business[str(command)]()
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
    def chat(self):
         package = getDict()#sender and message
         package['time'] = ctime()
         chatting.append(package)
    def handlePoll(self):
        package = self.getDict()
        if package['num'] == len(MyServer.chatting):
            self.sendPackages(2)#2表示轮询没有新消息
        else:
            news = MyServer.chatting[package['num']]
            self.sendPackages(3，news)#3表示轮询得到新消息


    def info(self):
        dicts = self.getDict()
        check = dicts['username']
        dbconn = sqlite3.connect('user.db')
        dbconn.row_factory = dict_factory
        cursor = dbconn.cursor()
        cursor.execute("SELECT * from users where name= "+"\'"+check+"\'")
        user = cursor.fetchall()[0]
        self.sendPackages(1,user)
    def login(self):
        conn = self.request
        data = self.getDict()
        dbconn = sqlite3.connect('user.db')
        dbconn.row_factory = dict_factory
        cursor = dbconn.cursor()
        cursor.execute("SELECT password from users  where name = "+"\'"+data['username']+"\'")
        user = cursor.fetchall()[0]
        if user['PASSWORD'] == data['password']:
            returnCommand =struct.pack('i',1)
            conn.send(returnCommand)
            Myserver.clientlist.append()###这个地方想想咋写
            return
        returnCommand = struct.pack('i',0)
        conn.send(returnCommand)
        return
    def handle(self):
        self.business= {'1':self.login,'2':self.info,'3':self.chat,'4':self.handlePoll}
        print('...connected from:'+self.client_address[0])
        Flag = True
        conn = self.request
        while Flag:
            print("Waiting for connection...")
            self.Command()



if __name__ == '__main__':
    server = socketserver.ThreadingTCPServer(('127.0.0.1', 21567), MyServer)
    server.serve_forever()
