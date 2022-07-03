from datetime import datetime

import pymysql

for i in range(100):
    connection = pymysql.connect(host="42.192.116.184", port=3306, user="root", password="lxy123456",
                                 db="dxnbr", charset='utf8')
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO request(now,date,num) VALUES (%s,%s,%s)",
        (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), datetime.now().strftime('%Y-%m-%d'), 100))
    connection.commit()