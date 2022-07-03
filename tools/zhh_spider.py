import json

import pymysql
import redis
import requests
from lxml import html

from tools.aimodel_kw import DefaultModelServer
from tools.filter import DFAFilter
from tools.savedata import save

etree = html.etree
import datetime


def get_zhihu(word, page):
    aa = datetime.datetime.now()
    bb = str(datetime.datetime.strftime(aa, '%Y-%m-%d %H:%M:%S'))
    mb_spi_time = datetime.datetime.strptime(bb, '%Y-%m-%d %H:%M:%S')

    param = {"query": word, "page": page}
    # UA伪装
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
    }
    url = 'http://zhihu.sogou.com/zhihu?p=40351207&ie=utf8'
    # get方法
    response = requests.get(url, params=param, headers=headers).content.decode('utf-8')  #
    html = etree.HTML(response)
    pp = html.xpath('//*[@class="vrwrap"]')
    # tt = html.xpath('//*[@class="cite-date"]/text()')
    # print(tt)
    qq = []
    try:
        for i in pp:
            r = etree.tostring(i, encoding="utf-8", pretty_print=True).decode("utf-8")
            co = r.split('class="star-wiki "')[1].split('..<')[0].split('">')[-1].replace('<em><!--red_beg-->',
                                                                                          '').replace(
                '<!--red_end--></em>', '') + '..'
            if '&#13;' in co:
                zz = co.split('&#13;')[1]
            else:
                zz = co
            # print('#####', zz)
            a = r.split('<a class=" " target="_blank" href="')[1].split('" id="&quot;sogou_vr_')[0]
            print(a)
            url = "https://www.sogou.com/" + a
            print(url)
            pt = r.split('<span class="cite-date">- ')[1].split('</span>')[0]
            title = r.split('&quot;">')[1].split('&#13;')[0].replace('<em><!--red_beg-->', '').replace(
                '<!--red_end--></em>', '')
            qq.append(
                {'url': url, 'title': title, 'content': zz, 'nickname': '知乎网友', 'nickurl': url, 'publish_time': pt,
                 'spider_time': mb_spi_time})
        print(qq+"-------")
    except Exception as e:
        pass
    return qq

def getzh(kw):
    result={}
    for i in range(2, 3):
        ten = get_zhihu(kw, i)
        print(len(ten))
        url = "http://httpbin.org/ip"  # 也可以直接在浏览器访问这个地址
        r = requests.get(url)  # 获取返回的值
        ip = json.loads(r.text)["origin"]  # 取其中某个字段的值
        # 发送get请求
        url = f'http://ip-api.com/json/{ip}?fields=status,message,country,countryCode,region,regionName,city,zip,lat,lon,timezone,isp,org,as,query&lang=zh-CN'
        res = requests.get(url)
        data = json.loads(res.text)
        print(data["regionName"])
        connection = pymysql.connect(host="49.234.129.248", port=3306, user="root", password="lxy123456",
                                     db="dxnbr", charset='utf8')
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO request(now,date,num,type,province) VALUES (%s,%s,%s,%s,%s)",
            (datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), datetime.datetime.now().strftime('%Y-%m-%d'), len(ten), kw,
             data["regionName"]))
        connection.commit()
        a = DefaultModelServer('keyword')
        print("--------------------------------------------------")
        r = redis.StrictRedis("127.0.0.1", 6379, db=5, decode_responses=True, charset='UTF-8', encoding='UTF-8')
        for j in ten:
            res = a.predict(j.get('title')+j.get('content'), 'keyword')
            if j.get('url') != None and res.get("code") == 1:
                r.set(j.get('url'), j.get('title') + j.get('content'))
                result.update({j.get('uri'): j.get('title')+j.get('content')})
                print(r.get(j.get('url')))
        print("--------------------------------------------------")
    return result

def getcidian():
    result={}
    connection = pymysql.connect(host="49.234.129.248", port=3306, user="root", password="lxy123456",
                                 db="dxnbr", charset='utf8')
    cursor = connection.cursor()
    sql = 'select * from cidian'
    cursor.execute(sql)  # TODO 用户
    results = cursor.fetchall()
    for i in range(len(results)):
        print("0000" + results[i][1])
        temp=getzh(results[i][1])
        # print(temp)
        result.update(temp)
    return result

if __name__ == '__main__':
    save(getcidian())
    # getcidian()
    # r = redis.StrictRedis("127.0.0.1", 6379, db=1, decode_responses=True, charset='UTF-8', encoding='UTF-8')
    # content=[]
    # for i in r.keys():
    #     content.append(r.get(i))
    # print(content)