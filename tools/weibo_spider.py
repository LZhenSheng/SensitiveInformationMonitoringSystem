# coding: utf-8

import re
import json
from datetime import datetime

import pymysql
import redis
import requests

# 基于 m.weibo.cn 抓取少量数据，无需登陆验证
from tools.aimodel_kw import DefaultModelServer
from tools.savedata import  save

url_template = "https://m.weibo.cn/api/container/getIndex?type=wb&queryVal={}&containerid=100103type=2%26q%3D{}&page={}"

def clean_text(text):
    """清除文本中的标签等信息"""
    dr = re.compile(r'(<)[^>]+>', re.S)
    dd = dr.sub('', text)
    dr = re.compile(r'#[^#]+#', re.S)
    dd = dr.sub('', dd)
    dr = re.compile(r'@[^ ]+ ', re.S)
    dd = dr.sub('', dd)
    return dd.strip()


def fetch_data(query_val, page_id):
    """抓取关键词某一页的数据"""
    resp = requests.get(url_template.format(query_val, query_val, page_id))
    card_group = json.loads(resp.text)['data']['cards'][0]['card_group']
    # print('url：', resp.url, ' --- 条数:', len(card_group))

    mblogs = []  # 保存处理过的微博
    for card in card_group:
        # print(card)
        mblog = card['mblog']
        # print(card['scheme'])
        blog = {'mid': mblog['id'],  # 微博id
                'text': clean_text(mblog['text']),  # 文本
                'userid': str(mblog['user']['id']),  # 用户id
                'username': mblog['user']['screen_name'],  # 用户名
                'reposts_count': mblog['reposts_count'],  # 转发
                'comments_count': mblog['comments_count'],  # 评论
                'attitudes_count': mblog['attitudes_count'],  # 点赞
                'uri': card['scheme']
                }
        mblogs.append(blog)
    return mblogs


def remove_duplication(mblogs):
    """根据微博的id对微博进行去重"""
    mid_set = {mblogs[0]['mid']}
    new_blogs = []
    for blog in mblogs[1:]:
        if blog['mid'] not in mid_set:
            new_blogs.append(blog)
            mid_set.add(blog['mid'])
    return new_blogs


def fetch_pages(query_val, page_num):
    result={}
    """抓取关键词多页的数据"""
    mblogs = []
    for page_id in range(1 + page_num + 1):
        try:
            mblogs.extend(fetch_data(query_val, page_id))
        except Exception as e:
            print(e)

    print("去重前：", len(mblogs))
    if len(mblogs)>0:
        mblogs = remove_duplication(mblogs)
    print("去重后：", len(mblogs))
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
        "INSERT INTO request(`now`,`date`,`num`,`type`,`province`) VALUES (%s,%s,%s,%s,%s)",
        (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), datetime.now().strftime('%Y-%m-%d'), str(len(mblogs)), query_val,
         data["regionName"]))
    connection.commit()
    r = redis.StrictRedis("127.0.0.1", 6379, db=4, decode_responses=True, charset='UTF-8', encoding='UTF-8')
    a = DefaultModelServer("keyword")
    print("--------------------------------------------------")
    for page_id in range(len(mblogs)):
        res = a.predict(mblogs[page_id].get('text'), 'keyword')
        if res.get('code')==1:
            r.set(mblogs[page_id].get('uri'), mblogs[page_id].get('text'))
            result.update({mblogs[page_id].get('uri'):mblogs[page_id].get('text')})
            print(r.get(mblogs[page_id].get('uri')))
    print("--------------------------------------------------")
    return result

def getcidian_weibo():
    result={}
    connection = pymysql.connect(host="49.234.129.248", port=3306, user="root", password="lxy123456",
                                 db="dxnbr", charset='utf8')
    cursor = connection.cursor()
    sql = 'select * from cidian'
    cursor.execute(sql)  # TODO 用户
    results = cursor.fetchall()
    for i in range(len(results)):
        print("0000" + results[i][1])
        result.update(fetch_pages(results[i][1], 5))
    return result
if __name__ == '__main__':
    save(getcidian_weibo())
