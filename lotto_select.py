import pymysql

conn = pymysql.connect(
        host='localhost', 
        user='root', 
        password='', 
        db='lotto', 
        charset='utf8',
    )
curs = conn.cursor()

# 주 단위 조회한 데이터 insert start
def weekSelect(week):
    deleteQuery = "DELETE FROM lotto_num_week"
    curs.execute(deleteQuery)
    conn.commit()

    sql = 'SELECT round FROM crawl_data ORDER BY seq DESC LIMIT 1'
    curs.execute(sql)
    result = curs.fetchone()
    lastRound = result[0]
    startRound = lastRound - week

    arr = []
    for num in range(1, 46):
        sql = 'SELECT COUNT(seq) as cnt FROM crawl_data where round <= %s AND round >= %s AND (number1 = %s OR number2 = %s OR number3 = %s OR number4 = %s OR number5 = %s OR number6 = %s OR number7 = %s)' % (lastRound, startRound, num, num, num, num, num, num, num)
        curs.execute(sql)
        result = curs.fetchone()

        arr.append(result[0])

    for idx, val in enumerate(arr):
        insertSql = 'INSERT INTO lotto_num_week (number, count) VALUES(%s, %s)' % (idx + 1, val)
        curs.execute(insertSql)
        conn.commit()
# 주 단위 조회한 데이터 insert end

def continueNum():
    lastRound = 934 #몇 회차부터
    startRound = 930 #몇 회차까지
    num = 36

    sql = 'SELECT round FROM crawl_data where round <= %s AND round >= %s AND (number1 = %s OR number2 = %s OR number3 = %s OR number4 = %s OR number5 = %s OR number6 = %s OR number7 = %s)' % (lastRound, startRound, num, num, num, num, num, num, num)
    curs.execute(sql)
    result = curs.fetchall()
    
    arr = []
    for val in result:
        arr.append(val[0])
        
    reversArr = list(reversed(arr))
    
    continueRound = []
    for num in reversArr:
        if (num != lastRound):
            break
        else: 
            continueRound.append(num)

        lastRound -= 1
        print(num)

    roundCount = len(continueRound)

week = 20
weekSelect(week)

#continueNum()

conn.close()