import pymysql

conn = pymysql.connect(
        host='localhost', 
        user='root', 
        password='', 
        db='lotto', 
        charset='utf8',
    )
curs = conn.cursor()