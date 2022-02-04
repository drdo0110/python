import pymysql
import re
import requests
from bs4 import BeautifulSoup

conn = pymysql.connect(
        host='localhost', 
        user='root', 
        password='', 
        db='lotto', 
        charset='utf8',
    )
curs = conn.cursor()

#db last round select start
#db에 마지막 로또 회차 번호 가져옴
def roundSelect():
    source = requests.get("https://www.dhlottery.co.kr/gameResult.do?method=byWin&drwNo=1").text
    soup = BeautifulSoup(source, "html.parser")
    dhLastRound = soup.select('#dwrNoList > option')[0].text

    sql = 'SELECT `round` FROM crawl_data ORDER BY `round` DESC LIMIT 1'
    curs.execute(sql)
    result = curs.fetchone()

    dic = {}
    if not result:
        dic['first'] = 0
        dic['last'] = dhLastRound
    else:
        for val in result:
            dic['first'] = val
            dic['last'] = dhLastRound
            
    if dic['first'] != dic['last']:
        return dic
    else:
        exit()
#db last round select end

#crawl start
def crawlLogic(num):
    source = requests.get("https://www.dhlottery.co.kr/gameResult.do?method=byWin&drwNo=" + str(num)).text
    soup = BeautifulSoup(source, "html.parser")
    winResult = soup.select('.win_result')
    winResult = winResult[0]
    winMoney = soup.select('.content_wrap table tbody')
    winMoney = winMoney[0]

    roundNum = re.findall("\d+", winResult.h4.strong.string)
    selectDate = winResult.select('.desc')[0].text
    numberDate = re.findall("\d+", selectDate)
    resultDate = ''.join(numberDate)

    winningNumberTag = winResult.select('.nums p span')

    resultNumber = []
    for numberTag in winningNumberTag:
        resultNumber.append(numberTag.text)

    resultNumber = ', '.join(resultNumber)

    winningMoneyTag = winMoney.select('tr')
    resultMoney = []
    for moneyTag in winningMoneyTag:
        selectMoney = re.findall("\d+", moneyTag.select('.tar')[1].text)
        resultMoney.append(''.join(selectMoney))

    resultMoney = ', '.join(resultMoney)


    insertData = roundNum[0] + ', ' + resultDate + ', ' + resultNumber + ', ' + resultMoney
    insertQuery = "INSERT IGNORE INTO crawl_data (`round`, `date`, `number1`, `number2`, `number3`, `number4`, `number5`, `number6`, `number7`, `money1`, `money2`, `money3`, `money4`, `money5`) VALUES (%s)" % (insertData)

    curs.execute(insertQuery)
    conn.commit()
#crawl end

first_last_number = roundSelect()

for num in first_last_number:
    first = int(first_last_number['first'])
    last = int(first_last_number['last'])

for num in range(first + 1, last + 1):
    crawlLogic(num)    
 
conn.close()
