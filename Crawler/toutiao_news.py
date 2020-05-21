import re

import requests
import urllib3

from Model.news import News
from Utils.Util import get_connect

urllib3.disable_warnings()


class Toutiao():
    def __init__(self):
        self.index_url = 'https://www.toutiao.com/'
        self.session = requests.Session()
        self.news_list = []
        self.nodejs_server = 'http://127.0.0.1:8000/toutiao'

    def get_news_info(self):
        for index, n in enumerate(self.news_list):
            headers = {
                'authority': 'www.toutiao.com',
                'pragma': 'no-cache',
                'cache-control': 'no-cache',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-dest': 'document',
                'accept-language': 'zh-CN,zh;q=0.9',
            }
            print(n.source_url)
            try:
                if index == 0:
                    # 第一次获取请求在 response 中获取 key为：__ac_nonce 的值，用来生成 __ac_signature
                    res = self.session.get(url=n.source_url, headers=headers, verify=False)
                    nonce = res.cookies['__ac_nonce']
                    userAgent = headers['user-agent']
                    params = {
                        'nonce': nonce,
                        'url': n.source_url,
                        'userAgent': userAgent
                    }
                    signature = requests.get(self.nodejs_server, params=params).text
                    self.session.cookies['__ac_signature'] = signature
                    #开始爬取
                    res = self.session.get(url=n.source_url, headers=headers, verify=False)
                    data=res.text
                    article_content = re.findall("content: '(.*?)'", data, re.S, )[0]
                    article_content = article_content.replace('&quot;', '').replace('u003C', '<').replace(
                        'u003E',
                        '>').replace(
                        '&#x3D;',
                        '=').replace(
                        'u002F', '/').replace('\\', '')
                    dr = re.compile(r'<[^>]+>', re.S)
                    article_content = dr.sub('', article_content)
                    print(article_content)
                    n.content=article_content
                    self.update_content(n)
                else:
                    res = self.session.get(url=n.source_url, headers=headers, verify=False)
                    data = res.text
                    article_content = re.findall("content: '(.*?)'", data, re.S, )[0]
                    article_content = article_content.replace('&quot;', '').replace('u003C', '<').replace(
                        'u003E',
                        '>').replace(
                        '&#x3D;',
                        '=').replace(
                        'u002F', '/').replace('\\', '')
                    dr = re.compile(r'<[^>]+>', re.S)
                    article_content = dr.sub('', article_content)
                    print(article_content)
                    n.content = article_content
                    self.update_content(n)
            except Exception as e:
                print(e)



    def update_content(self,news):
        try:
            connect = get_connect()
            cursor = connect.cursor()
            sql = "UPDATE toutiao_news SET content = %s WHERE id = %s "
            cursor.execute(sql, (news.content, news.id))
            connect.commit()
        except Exception as e:
            e
    def run(self):
        self.get_news_info()

    def select_url(self):
        try:
            connect = get_connect()
            cursor = connect.cursor()
            print("connection")
            sql = "SELECT id,source_url FROM toutiao_news where id >(select min(t.id) from (select id from toutiao_news where content is null order by id) t) order by id desc "
            cursor.execute(sql)
            result = cursor.fetchall()
            for row in result:
                # print(row[0])
                news = News()
                news.id = row[0]
                news.source_url = row[1]
                self.news_list.append(news)
        except Exception as e:
            print(e)


if __name__ == '__main__':
    tt = Toutiao()
    tt.select_url()
    tt.run()