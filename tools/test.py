#!/home/zkfr/.local/share/virtualenvs/xf-5EfV3Nly/bin/python
# -*- coding:utf-8 -*-
# @author : MaLei
# @datetime : 2018-10-29 14:52
# @file : zhihu_app.py
# @software : PyCharm

import requests, time

headers = {
    'x-api-version': '3.0.89',
    'x-app-version': '5.26.2',
    'x-app-za': 'OS=Android&Release=8.0.0&Model=SM-G9500&VersionName=5.26.2&VersionCode=913&Product=com.zhihu.android&Width=1080&Height=2076&Installer=%E5%BA%94%E7%94%A8%E5%AE%9D&DeviceType=AndroidPhone&Brand=samsung',
    'x-app-flavor': 'myapp',
    'x-app-build': 'release',
    'x-network-type': 'WiFi',
    'Host': 'api.zhihu.com',
    'User-Agent': 'com.zhihu.android/Futureve/5.26.2 Mozilla/5.0 (Linux; Android 8.0.0; SM-G9500 Build/R16NW; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/67.0.3396.87 Mobile Safari/537.36',
    'Connection': 'keep-alive'
}

# 从热榜爬取热门问题
start_url = 'https://api.zhihu.com/topstory/hot-list?limit=10'
res = requests.get(start_url, headers=headers).json()['data']
a = []

for each in res:
    title = each['target']['title_area']['text']
    hot = each['target']['metrics_area']['text'][:-2]
    answer_count = each['feed_specific']['answer_count']
    card_id = list(str(each['target']['link']['url']).split('/'))[-1]

    q_url = 'https://api.zhihu.com/v4/questions/' + card_id + '/answers?order_by=&show_detail=1'

    # 有些热点是文章，不存在回答
    try:
        for i in range(0, 20, 5):
            params = {'offset': i}
            res = requests.get(q_url, headers=headers, params=params).json()['data']
            for item in res:
                update_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(item['updated_time']))
                print(q_url,res)
                # print(q_url,title,
                #       hot,
                #       answer_count,
                #       item['excerpt'],
                #       item['author']['name'],
                #       int(item['voteup_count']),
                #       int(item['comment_count']),
                #       str(update_time))
    except:
        pass
