import socketserver
from time import ctime
import sqlite3
import struct
BUFFSIZE = 1024
def dict_factory(cursor, row):  
    d = {}  
    for idx, col in enumerate(cursor.description):  
        d[col[0]] = row[idx]  
    return d  
dbconn = sqlite3.connect('user.db')
dbconn.row_factory = dict_factory  
c = dbconn.cursor()
dbconn.commit()
c.execute('select * from users')
users = c.fetchall()
print(users)
