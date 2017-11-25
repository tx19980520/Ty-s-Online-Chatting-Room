import socketserver
from time import ctime
import sqlite3
import struct
BUFFSIZE = 1024
dbconn = sqlite3.connect('user.db')
c = dbconn.cursor()
c.execute('''CREATE TABLE USERS
       (ID INTEGER PRIMARY KEY AUTOINCREMENT    NOT NULL,
       NAME           TEXT    NOT NULL,
       ADDRESS TEXT NOT NULL,
       AGE INT NOT NULL,
       PASSWORD TEXT NOT NULL);''')

c.execute("INSERT INTO USERS (NAME,ADDRESS,AGE,PASSWORD) \
      VALUES ('Ty','ChongQing',19,'1234512345qwe')")
dbconn.commit()
users = c.execute('select * from users')
for user in users:
    print (user[0]);
