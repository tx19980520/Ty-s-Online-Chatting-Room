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
dbconn = sqlite3.connect('server/user.db')
dbconn.row_factory = dict_factory
c = dbconn.cursor()
dbconn.commit()
c.execute("delete from files where ID ="+str(12))
dbconn.commit()
c.execute("SELECT * from files")
s = c.fetchall()
print(s)