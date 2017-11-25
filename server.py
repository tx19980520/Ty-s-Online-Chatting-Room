import socketserver
from time import ctime
import sqlite3
import struct
import pickle
BUFFSIZE = 4

class MyServer(socketserver.BaseRequestHandler):
    clientlist = []
    def login(self):
        conn = self.request
        data = conn.recv(4)
        data = struct.unpack('i',data)
        data = conn.recv(data[0])
        data = pickle.loads(data)
        dbconn = sqlite3.connect('user.db')
        cursor = dbconn.cursor()
        users = cursor.execute('SELECT name from users')
        for user in users:
            for thi in user:
                print(thi)
                if thi == data['username']:
                    print("success!")
    def handle(self):
        business= {'1':self.login}
        print('...connected from:'+self.client_address[0])
        Flag = True
        conn = self.request
        while Flag:
            print("Waiting for connection...")
            data = conn.recv(4)
            data = struct.unpack('i',data)
            print(data[0])
            business[str(data[0])]()
            


if __name__ == '__main__':
    server = socketserver.ThreadingTCPServer(('127.0.0.1', 21567), MyServer)
    server.serve_forever()
