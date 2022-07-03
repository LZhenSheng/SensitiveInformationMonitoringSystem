import json
import parser
from datetime import datetime
from gevent import pywsgi

import requests
from flask import Flask, request, jsonify
import pymysql
from flask_cors import CORS
import redis

from tools.weibo_spider import fetch_pages
from tools.zhh_spider import getzh

app = Flask(__name__)
CORS(app, supports_credentials=True)


@app.route('/insertUser', methods=['POST'])
def insertUser():
    yonghu = request.form.get('userName')
    mima = request.form.get('passWord')
    leibie = request.form.get('userType')
    nicheng = request.form.get('nicheng')
    qq = request.form.get('qq')
    print(yonghu)
    print(mima)
    connection = pymysql.connect(host="49.234.129.248", port=3306, user="root", password="lxy123456",
                                 db="dxnbr", charset='utf8')
    cursor = connection.cursor()
    cursor.execute("INSERT INTO goodsUser(goodsUser,goodsPass,leibie,nicheng,qq,is_valid) VALUES (%s,%s,%s,%s,%s,0)",
                   (yonghu, mima, leibie, nicheng, qq))
    connection.commit()

    return jsonify({'message': '注册成功'})


@app.route('/getUser', methods=['POST'])
def getUser():
    yonghu = request.form.get('yonghu')
    mima = request.form.get('mima')
    print(yonghu)
    print(mima)

    connection = pymysql.connect(host="49.234.129.248", port=3306, user="root", password="lxy123456",
                                 db="dxnbr", charset='utf8')
    cursor = connection.cursor()
    cursor.execute("select * from goodsUser where goodsUser='%s' and goodsPass='%s' and is_valid=1" % (yonghu, mima))
    r = cursor.fetchall()
    print("038894#######", r)
    result = []
    result.append(r[0][0])
    result.append(r[0][2])
    print(result)
    if r:
        return jsonify(result)


heihei = []


@app.route('/duofilter', methods=['POST'])
def duofilter():
    if request.method == "POST":
        conte = request.form.get('content')
        print(str(heihei) + '-----' + conte)
        try:
            heihei.index(conte)
            heihei.remove(conte)
        except:
            heihei.append(conte)

        print('123454', conte, str(heihei))

        r = redis.StrictRedis("127.0.0.1", 6379, db=4, decode_responses=True, charset='UTF-8', encoding='UTF-8')
        content = {}
        for i in r.keys():
            if r.get(i) is not None:
                for j in heihei:
                    if str(r.get(i)).find(j) == -1:
                        break
                    if j == heihei[len(heihei) - 1]:
                        v = {i: r.get(i)}
                        content.update(v)
        print(content)

        return jsonify(content)


@app.route('/shibie', methods=['POST'])
def shibie():
    if request.method == "POST":
        conte = request.form.get('content')
        sourse = request.form.get('sourse', None)
        userid = request.form.get('userid', None)
        print('123454', conte)
        content = {}
        if sourse == 'weibo':
            fetch_pages(conte, 3)
            r = redis.StrictRedis("127.0.0.1", 6379, db=4, decode_responses=True, charset='UTF-8', encoding='UTF-8')
            for i in r.keys():
                if str(r.get(i)).find(conte) != -1:
                    v = {i: r.get(i)}
                    content.update(v)
            print(content)
        elif sourse == 'zhihu':
            getzh(conte)
            r = redis.StrictRedis("127.0.0.1", 6379, db=5, decode_responses=True, charset='UTF-8', encoding='UTF-8')
            for i in r.keys():
                if str(r.get(i)).find(conte) != -1:
                    content.update({i: r.get(i)})
            print(content)
        return jsonify(content)


@app.route('/chaci', methods=['POST'])
def chaci():
    userid = request.form.get('userid', None)
    sourse = request.form.get('sourse', None)

    if request.method == "POST":
        connection = pymysql.connect(host="49.234.129.248", port=3306, user="root", password="lxy123456",
                                     db="dxnbr", charset='utf8')
        cursor = connection.cursor()
        sql = 'select * from cidian where sourse=%s'
        cursor.execute(sql, sourse)  # TODO 用户
        results = cursor.fetchall()
        return jsonify(results)

@app.route('/chareport', methods=['POST'])
def chareport():
    if request.method == "POST":
        connection = pymysql.connect(host="49.234.129.248", port=3306, user="root", password="lxy123456",
                                     db="dxnbr", charset='utf8')
        cursor = connection.cursor()
        sql = 'select * from report'
        cursor.execute(sql)  # TODO 用户
        results = cursor.fetchall()
        return jsonify(results)

@app.route('/chacis', methods=['POST'])
def chacis():
    print("dfjk")
    userid = request.form.get('userid', None)
    sourse = request.form.get('sourse')
    print(sourse)
    if request.method == "POST":
        connection = pymysql.connect(host="49.234.129.248", port=3306, user="root", password="lxy123456",
                                     db="dxnbr", charset='utf8')
        cursor = connection.cursor()
        sql = 'select * from cidian where sourse=%s '
        cursor.execute(sql, sourse)
        results = cursor.fetchall()
        print(results)
        content = ''
        for resu in results:
            cihui = resu[1]
            print(cihui)
            # if sourse == 'zhihu':
            #     print('--------zhh_cou---------')
            # hei=es.count(index='zhh_spider', q=cihui)
            # if sourse == 'weibo':
            #     print('--------wei_cou---------')
            # hei=es.count(index='wb_spider', q=cihui)   # TODO match用户
            content += cihui + ','
        content = content[:-1]
        print(content)
        return jsonify(content)


@app.route('/shanchu', methods=['POST'])
def shanchu():
    if request.method == "POST":
        id = request.form.get('id')
        userid = request.form.get('userid', None)

        connection = pymysql.connect(host="49.234.129.248", port=3306, user="root", password="lxy123456",
                                     db="dxnbr", charset='utf8')
        cursor = connection.cursor()
        # SQL 删除语句
        sql = "DELETE FROM cidian WHERE id = '%d'" % (int(id))
        try:
            hei = cursor.execute(sql)
            print(hei)
            connection.commit()
        except:
            connection.rollback()
        return jsonify({"message": 'ok'})


@app.route('/charu', methods=['POST'])
def charu():
    print("-----------------------------------")
    if request.method == "POST":
        mustContain = request.form.get('mustContain')
        ids = request.form.get("id")
        sourse = request.form.get('sourse', None)
        userid = request.form.get('userid', None)
        print(mustContain)
        connection = pymysql.connect(host="49.234.129.248", port=3306, user="root", password="lxy123456",
                                     db="dxnbr", charset='utf8')
        cursor = connection.cursor()
        # SQL 插入语句
        sql = "INSERT INTO cidian(id,keywords,sourse)VALUES ('%s','%s','%s')" % (ids, mustContain, sourse)
        try:
            # 提交到数据库执行
            cursor.execute(sql)
            connection.commit()
        except:
            connection.rollback()
        fetch_pages(mustContain, 2)
        print("-----------------------------------")
        return jsonify({"message": 'ok'})


@app.route('/getstatisticsdata', methods=['POST'])
def getstatisticsdata():
    if request.method == "POST":
        connection = pymysql.connect(host="49.234.129.248", port=3306, user="root", password="lxy123456",
                                     db="dxnbr", charset='utf8')
        cursor = connection.cursor()
        # SQL 插入语句
        sql = "select date,num,now from request"
        try:
            # 提交到数据库执行
            cursor.execute(sql)
            results = cursor.fetchall()
        except:
            connection.rollback()
        for i in range(10):
            print(results[i])
        results=list(reversed(results))
        for i in range(10):
            print(results[i])
        return jsonify(results)


@app.route('/getdata', methods=['POST'])
def getdata():
    if request.method == "POST":
        connection = pymysql.connect(host="49.234.129.248", port=3306, user="root", password="lxy123456",
                                     db="dxnbr", charset='utf8')
        cursor = connection.cursor()
        # SQL 插入语句
        sql = "select date,num,now from request"
        try:
            # 提交到数据库执行
            cursor.execute(sql)
            results = cursor.fetchall()
        except:
            connection.rollback()
        now = datetime.now().strftime('%Y-%m-%d')
        date1 = datetime.strptime(now, "%Y-%m-%d").date()
        num = [0, 0, 0, 0, 0, 0, 0]
        for i in range(len(results)):
            date2 = datetime.strptime(results[i][0], "%Y-%m-%d").date()
            day = (date1 - date2).days
            if day <= 6:
                num[day] += int(results[i][1])
            print(results[i])
        print(num)
        return jsonify(num)


@app.route('/getmap', methods=['POST'])
def getmap():
    if request.method == "POST":
        connection = pymysql.connect(host="49.234.129.248", port=3306, user="root", password="lxy123456",
                                     db="dxnbr", charset='utf8')
        cursor = connection.cursor()
        # SQL 插入语句
        turn = []
        sql = "select distinct province from request"
        try:
            # 提交到数据库执行
            cursor.execute(sql)
            results = cursor.fetchall()
        except:
            connection.rollback()
        for i in range(len(results)):
            sql = "select num from request where province=%s"
            try:
                cursor.execute(sql, results[i][0])
                result = cursor.fetchall()
            except:
                connection.rollback()
            num = 0
            for j in range(len(result)):
                num += int(result[j][0])
            print(results[i][0], num)
            if results[i][0] is not None:
                turn.append({"value": num, "name": results[i][0]})
        print(turn)
        return jsonify(turn)


@app.route('/usermanage', methods=['POST'])
def usermanage():
    if request.method == "POST":
        print("-----------------------")
        userid = request.form.get('userid', None)
        status = request.form.get('status', None)
        user = request.form.get('username', None)
        leibiw = request.form.get('leibie', None)
        nicheng = request.form.get('nicheng', None)
        qq = request.form.get('qq', None)
        valid = request.form.get('valid', None)
        print(userid)
        print(status)
        print(user)
        print(leibiw)
        print(nicheng)
        print(valid)
        connection = pymysql.connect(host="49.234.129.248", port=3306, user="root", password="lxy123456",
                                     db="dxnbr", charset='utf8')
        cursor = connection.cursor()  # cursor=pymysql.cursors.DictCursor
        # SQL 插入语句
        # data =
        sql = "SELECT * FROM goodsUser"
        sqls = "SELECT * FROM goodsUser WHERE goodsUser=%s"
        sqlss = "SELECT * FROM goodsUser WHERE goodsUser=%s"
        sqlu = "UPDATE goodsUser set goodsUser=%s,leibie=%s,nicheng=%s,qq=%s,goodsPass=%s Where goodsUser=%s"

        if status == '0' and user == 'admin':  # 管理员可查看全部用户
            cursor.execute(sql)
            users = cursor.fetchall()
            return jsonify({"users": users})
        elif status == '0' and user != 'admin':
            cursor.execute(sqls, user)
            users = cursor.fetchall()
            return jsonify({"users": users})
        elif status == '1':
            cursor.execute(sqlss, user)
            users = cursor.fetchall()
            return jsonify({"users": users})
        elif status == '2':
            cursor.execute(sqlu, (userid, leibiw, nicheng, qq, user, userid))
            connection.commit()

        return jsonify({"users": 'users'})\

@app.route('/reportdetail', methods=['POST'])
def reportdetail():
    if request.method == "POST":
        username = request.form.get('username', None)
        connection = pymysql.connect(host="49.234.129.248", port=3306, user="root", password="lxy123456",
                                     db="dxnbr", charset='utf8')
        cursor = connection.cursor()  # cursor=pymysql.cursors.DictCursor
        sqls = "SELECT * FROM report WHERE name=%s"

        cursor.execute(sqls, username)
        users = cursor.fetchall()
        return jsonify({"users": users})


@app.route('/report', methods=['POST'])
def report():
    if request.method == "POST":
        name = request.form.get('name', None)
        connection = pymysql.connect(host="49.234.129.248", port=3306, user="root", password="lxy123456",
                                     db="dxnbr", charset='utf8')
        cursor = connection.cursor()
        sqlss = "SELECT * FROM report WHERE name=%s"

        cursor.execute(sqlss, name)
        users = cursor.fetchall()
        print(users[0])
        return jsonify(users[0])

@app.route('/updatereportmessage', methods=['POST'])
def updatereportmessage():
    if request.method == "POST":
        name = request.form.get('name', None)
        key = request.form.get('key', None)
        refile = request.form.get('refile', None)
        content = request.form.get('content', None)

        connection = pymysql.connect(host="49.234.129.248", port=3306, user="root", password="lxy123456",
                                     db="dxnbr", charset='utf8')
        cursor = connection.cursor()
        sqlu = "UPDATE report set keyword=%s,refile=%s,content=%s Where name=%s"
        cursor.execute(sqlu, (key, refile, content, name))
        connection.commit()
        return jsonify("users[0]")

@app.route('/updatemessage', methods=['POST'])
def updatemessage():
    if request.method == "POST":
        username = request.form.get('username', None)
        password = request.form.get('password', None)
        type = request.form.get('type', None)
        newnicheng = request.form.get('newnicheng', None)
        nqq = request.form.get('nqq', None)
        status = request.form.get('status', None)
        connection = pymysql.connect(host="49.234.129.248", port=3306, user="root", password="lxy123456",
                                     db="dxnbr", charset='utf8')
        cursor = connection.cursor()  # cursor=pymysql.cursors.DictCursor
        sqlu = "UPDATE goodsUser set goodsPass=%s,leibie=%s,nicheng=%s,qq=%s,is_valid=%s Where goodsUser=%s"
        cursor.execute(sqlu, (password, type, newnicheng, nqq, status, username))
        connection.commit()
        return jsonify({"users": 'users'})

@app.route('/examinemessage', methods=['POST'])
def examinemessage():
    if request.method == "POST":
        name = request.form.get('name', None)
        key = request.form.get('key', None)
        refile = request.form.get('refile', None)
        content = request.form.get('content', None)
        date = request.form.get('date', None)
        status = request.form.get('status', None)
        connection = pymysql.connect(host="49.234.129.248", port=3306, user="root", password="lxy123456",
                                     db="dxnbr", charset='utf8')
        cursor = connection.cursor()  # cursor=pymysql.cursors.DictCursor
        sqlu = "UPDATE report set status=%s Where name=%s"
        cursor.execute(sqlu, (status,name))
        connection.commit()
        return jsonify({"users": 'users'})


@app.route('/userlist', methods=['POST'])
def userlist():
    if request.method == "POST":
        is_valid = request.form.get('is_valid', None)
        connection = pymysql.connect(host="49.234.129.248", port=3306, user="root", password="lxy123456",
                                     db="dxnbr", charset='utf8')
        cursor = connection.cursor()  # cursor=pymysql.cursors.DictCursor
        # SQL 插入语句
        # data =
        sql = "SELECT * FROM goodsUser Where is_valid=0"
        cursor.execute(sql)
        users = cursor.fetchall()
        return jsonify({"users": users})

@app.route('/reportlist', methods=['POST'])
def reportlist():
    if request.method == "POST":
        connection = pymysql.connect(host="49.234.129.248", port=3306, user="root", password="lxy123456",
                                     db="dxnbr", charset='utf8')
        cursor = connection.cursor()  # cursor=pymysql.cursors.DictCursor
        # SQL 插入语句
        # data =
        sql = "SELECT * FROM report Where status=0"
        cursor.execute(sql)
        users = cursor.fetchall()
        return jsonify({"users": users})
@app.route('/reportlistdetail', methods=['POST'])
def reportlistdetail():
    if request.method == "POST":
        connection = pymysql.connect(host="49.234.129.248", port=3306, user="root", password="lxy123456",
                                     db="dxnbr", charset='utf8')
        cursor = connection.cursor()  # cursor=pymysql.cursors.DictCursor
        # SQL 插入语句
        # data =
        sql = "SELECT * FROM report Where status=1"
        cursor.execute(sql)
        users = cursor.fetchall()
        return jsonify({"users": users})

@app.route('/gettotal', methods=['POST'])
def gettotal():
    if request.method == "POST":
        connection = pymysql.connect(host="49.234.129.248", port=3306, user="root", password="lxy123456",
                                     db="dxnbr", charset='utf8')
        cursor = connection.cursor()
        # SQL 插入语句
        sql = "select date,num,now from request"
        try:
            # 提交到数据库执行
            cursor.execute(sql)
            results = cursor.fetchall()
        except:
            connection.rollback()
        now = datetime.now().strftime('%Y-%m-%d')
        date1 = datetime.strptime(now, "%Y-%m-%d").date()
        num = [0, 0, 0, 0]
        for i in range(len(results)):
            date2 = datetime.strptime(results[i][0], "%Y-%m-%d").date()
            if ((date2 - date1).days == 0):
                num[0] += int(results[i][1])
            elif (date2 - date1).days == 1:
                num[1] += int(results[i][1])
            if (date2 - date1).days < 30:
                num[2] += int(results[i][1])
            num[3] += int(results[i][1])
            print(results[i])
        print(num)
        return jsonify(num)


@app.route('/getcircle', methods=['POST', 'GET'])
def getcircle():
    turn = []
    connection = pymysql.connect(host="49.234.129.248", port=3306, user="root", password="lxy123456",
                                 db="dxnbr", charset='utf8')
    cursor = connection.cursor()
    # SQL 插入语句
    sql = "select distinct type from request"
    try:
        # 提交到数据库执行
        cursor.execute(sql)
        results = cursor.fetchall()
    except:
        connection.rollback()
    for i in range(len(results)):
        sql = "select num from request where type=%s"
        try:
            cursor.execute(sql, results[i][0])
            result = cursor.fetchall()
        except:
            connection.rollback()
        num = 0
        for j in range(len(result)):
            num += int(result[j][0])
        print(results[i][0], num)
        turn.append({"value": num, "name": results[i][0]})
    print(turn)
    return jsonify(turn)


@app.route('/addreport', methods=['POST', 'GET'])
def addreport():
    name = request.form.get('name', None)
    key = request.form.get('key', None)
    refile = request.form.get('refile', None)
    content = request.form.get('content', None)
    dt = datetime.now()
    data = dt.strftime("%Y-%m-%d %H:%M:%S")
    print(type(data))
    connection = pymysql.connect(host="49.234.129.248", port=3306, user="root", password="lxy123456",
                                 db="dxnbr", charset='utf8')
    cursor = connection.cursor()
    sql="INSERT INTO report(`name`,`keyword`,`refile`,`content`,`date`,`status`) VALUES ('%s','%s','%s','%s','%s',0)"%(name,key, refile, content,str(datetime.now()))
    cursor.execute(sql)
    connection.commit()
    return jsonify("成功")


@app.route('/', methods=['POST', 'GET'])
def get():
    print('sdfj')
    return "dlfjks"


if __name__ == '__main__':
    server = pywsgi.WSGIServer(('0.0.0.0', 5000), app)
    server.serve_forever()