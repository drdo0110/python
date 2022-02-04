import pymysql

conn = pymysql.connect(
        host='localhost', 
        user='root', 
        password='', 
        db='lotto', 
        charset='utf8',
    )
curs = conn.cursor()

#로또번호 1 ~ 7 까지 insert start
def insertLottoNumber():
    for cnt in range(1, 8):
        arr = []
        for no in range(1, 45 + 1):
            sql = 'SELECT count(`seq`) AS cnt FROM crawl_data where `number%s` = %s' % (cnt, no)
            curs.execute(sql)
            result = curs.fetchone()
            
            arrNumber = []
            for value in result:
                arrNumber.append(value)
            
            for number in arrNumber:
                arr.append(number)

        deleteQuery = "DELETE FROM lotto_num_%s" % (cnt)
        curs.execute(deleteQuery)
        conn.commit()

        for idx, val in enumerate(arr):
            insertQuery = "INSERT INTO lotto_num_%s (`number`, `count`) VALUES(%s, %s)" % (cnt, idx + 1, val)

            curs.execute(insertQuery)
            conn.commit()
#end

#로또번호 1 ~ 7까지 total insert start
def totalInsert():
    deleteQuery = "DELETE FROM lotto_num_total"
    curs.execute(deleteQuery)
    conn.commit()

    sql = 'SELECT num1.number AS number, (num1.count + num2.count + num3.count + num4.count + num5.count + num6.count + num7.count) AS total FROM lotto_num_1 AS num1 JOIN lotto_num_2 AS num2 ON num2.number = num1.number JOIN lotto_num_3 AS num3 ON num3.number = num1.number JOIN lotto_num_4 AS num4 ON num4.number = num1.number JOIN lotto_num_5 AS num5 ON num5.number = num1.number JOIN lotto_num_6 AS num6 ON num6.number = num1.number JOIN lotto_num_7 AS num7 ON num7.number = num1.number;'
    curs.execute(sql)
    result = curs.fetchall()

    for val in result:
        insertSql = "INSERT INTO lotto_num_total (number, count) VALUES (%s, %s)" % (val[0], val[1])
        curs.execute(insertSql)
        conn.commit()
#end

insertLottoNumber()
totalInsert()

conn.close()