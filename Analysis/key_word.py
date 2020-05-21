# -*- coding: utf-8 -*-
import os
import re
from imp import reload

from snownlp import SnowNLP
import matplotlib.pyplot as plt
import numpy as np
from wordcloud import wordcloud

from Utils.Util import get_connect
import codecs
from textrank4zh import TextRank4Keyword, TextRank4Sentence

import sys
try:
    reload(sys)
    sys.setdefaultencoding('utf-8')
except:
    pass


def get_news_content():
    arrList = []
    try:
        connect = get_connect()
        cursor = connect.cursor()
        print("connection")
        sql = "SELECT content FROM toutiao_news"
        cursor.execute(sql)
        result = cursor.fetchall()
        for row in result:
            news = str(row[0])
            dr = re.compile(r'<[^>]+>', re.S)
            article_content = dr.sub('', news)
            print(article_content)
            tr4s = TextRank4Sentence()
            tr4s.analyze(text=article_content, lower=True, source = 'all_filters')
            print( '摘要：' )
            for item in tr4s.get_key_sentences(num=1):
                print(item.index, item.weight, item.sentence)
            print('*'*10)
            tr4w = TextRank4Keyword()
            tr4w.analyze(text=article_content, lower=True, window=2)
            print('关键字：')
            key_word=[]
            for item in tr4w.get_keywords(10, word_min_len=1):
                print(item.word, item.weight)
                key_word.append(item.word)
            arrList.append(" ".join(key_word))
    except Exception as e:
        print(e)
    finally:
        return arrList

def generate_ciyun():
    try:
        # 调用jieba的lcut()方法对原始文本进行中文分词，得到string
        string = " ".join(get_news_content())
        print(string)
        #string = " ".join(txtlist)
        # 构建并配置词云对象w
        w = wordcloud.WordCloud(width=1000,
                                height=700,
                                background_color='black',
                                font_path='/Library/Fonts/华文行楷.ttf')


        # 将string变量传入w的generate()方法，给词云输入文字
        w.generate(string)
        #检测词云文件是否存在，如果存在就删除
        my_file = 'key_word_ciyun.png'
        if os.path.exists(my_file):
            # 删除文件，可使用以下两种方法。
            os.remove(my_file)
            # os.unlink(my_file)
        else:
            print
            'no such file:%s' % my_file
        # 将词云图片导出到当前文件夹
        w.to_file('key_word_ciyun.png')
    except Exception as e:
        print(e)

generate_ciyun()

