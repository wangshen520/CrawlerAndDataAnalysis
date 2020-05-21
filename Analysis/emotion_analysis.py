# -*- coding: utf-8 -*-
import re
from snownlp import SnowNLP
import matplotlib.pyplot as plt
import numpy as np
from Utils.Util import get_connect


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
            s = SnowNLP(article_content)
            print(s.sentiments)
            arrList.append(s.sentiments)
    except Exception as e:
        print(e)
    finally:
        return arrList


sentimentslist = get_news_content()
plt.hist(sentimentslist, bins = np.arange(0, 1, 0.01), facecolor = 'g')
plt.xlabel('Sentiments Probability')
plt.ylabel('Quantity')
plt.title('Analysis of Sentiments')
plt.savefig('emotion.jpg')
plt.show()
