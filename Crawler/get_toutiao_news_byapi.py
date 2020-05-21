# coding：utf-8
import time

import requests
import json
from Model.news import News
from fake_useragent import UserAgent
from Utils.Util import insert_data


def toutiao_news_api(url):
    # 代理服务器
    proxyHost = "http-dyn.abuyun.com"
    proxyPort = "9020"

    # 代理隧道验证信息
    proxyUser = "HD8W0C7I6B3416RD"
    proxyPass = "A8960BA3AD9F5B75"

    proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
        "host": proxyHost,
        "port": proxyPort,
        "user": proxyUser,
        "pass": proxyPass,
    }

    proxies = {
        "http": proxyMeta,
        "https": proxyMeta,
    }
    ua = UserAgent(verify_ssl=False)
    headers = {
        'cookie': 'tt_webid=6825236887406953998; s_v_web_id=verify_ka17kc91_J51hfIgB_1Ujy_4F87_AQ77_v44SCeaZdYbb; WEATHER_CITY=%E5%8C%97%E4%BA%AC; __tasessionId=ftj73c94a1589124278466; tt_webid=6825236887406953998; csrftoken=3bc73a541ff3c196706a5fa652baa10a; ttcid=93c87bb6d2c44204a824c060f2a0344b39; SLARDAR_WEB_ID=167cd898-158d-4682-84b7-515f808f9c49; tt_scid=nvrgh8BUDb5bfXypX.EbNgFcMiVjrSr7vdwnPAab2w2tEn2I8DLcdmqRb2aAGGvT6b9b',
        'user-agent': ua.random,
        'x-requested-with': 'XMLHttpRequest'
    }
    toutiao_data = requests.get(url,headers=headers,proxies=proxies).text
    global data
    data = json.loads(toutiao_data)
    global max_behot_time
    max_behot_time = data['next']['max_behot_time']
    items = data['data']

    news_list = []
    link_head = 'http://toutiao.com'

    for n in items:
        if 'title' in n and n['tag'] != 'ad' and n['tag'] != 'news_media':
            news = News()
            news.title = n['title']
            print(news.title)
            news.tag = n['tag']
            news.source = n['source']
            # 转换成localtime
            time_local = time.localtime(n['behot_time'])
            # 转换成新的时间格式(2016-05-05 20:28:54)
            dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
            news.news_date=dt
            print(news.news_date)
            news.source_url = link_head + n['source_url']

            news_list.append(news)
            #print(news.title, news.source_url, news.source, news.keyword, news.keywords)

    return news_list

global max_behot_time
max_behot_time = 0
while(1):
    time.sleep(1)
    print(max_behot_time)
    url = 'https://www.toutiao.com/api/pc/feed/?min_behot_time=0&category=__all__&utm_source=toutiao&widen=1&tadrequire=true&as=A1F55EA84F422DF&cp=5E8F8282EDAF0E1&_signature=FZq7pAAgEBAsZGkfmfjZfxWb-rAAEsatBE25MbFHNIgtOFj4L-l5kOR.NcuCLchOv57Otjzk.RCRnqs1BYEjqHXVj9bH.UOqT7I89ZXDC4HtEkFv69Bvm240kgG4n4DXBbn'
    news_list = toutiao_news_api(url)

    insert_data(news_list)
