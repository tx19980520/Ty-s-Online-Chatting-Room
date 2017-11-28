import sqlite3
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
dbconn = sqlite3.connect('user.db')
dbconn.row_factory = dict_factory
c = dbconn.cursor()
dbconn.commit()
c.execute("INSERT INTO USERS (NAME,AGE,ADDRESS,PASSWORD) VALUES ( 'lxy',19, 'Tianjing','12345' )");
dbconn.commit()

dbconn.close()
