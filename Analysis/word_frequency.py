

# 导入词云制作库wordcloud和中文分词库jieba
import os
from PIL import Image
import jieba
import wordcloud
import re
import numpy as np
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
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
            arrList.append(article_content)
    except Exception as e:
        print(e)
    finally:
        return " ".join(arrList)
# 创建停用词list
def stopwordslist(filepath):
    stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]
    return stopwords

# 对句子进行分词
def seg_sentence(sentence):
    sentence_seged = jieba.cut(sentence.strip())
    stopwords = stopwordslist('stopwords.txt')  # 这里加载停用词的路径
    outstr = ''
    for word in sentence_seged:
        if word not in stopwords:
            if word != '\t':
                outstr += word
                outstr += " "
    return outstr

def generate_ciyun(news):
    try:
        # 调用jieba的lcut()方法对原始文本进行中文分词，得到string
        string = seg_sentence(news)
        print(string)
        #string = " ".join(txtlist)
        # 构建并配置词云对象
        mask = np.array(Image.open("util/mask.jpg"))  # 定义词云的形状
        w = wordcloud.WordCloud(width=1000,
                                height=700,
                                background_color='white',
                                font_path='/Library/Fonts/MSYH.TTC',
                                mask = mask,)


        # 将string变量传入w的generate()方法，给词云输入文字
        w.generate(string)
        #检测词云文件是否存在，如果存在就删除
        my_file = 'news_ciyun.png'
        if os.path.exists(my_file):
            # 删除文件，可使用以下两种方法。
            os.remove(my_file)
            # os.unlink(my_file)
        else:
            print
            'no such file:%s' % my_file
        # 将词云图片导出到当前文件夹
        w.to_file('word_frequency_ciyun.png')
    except Exception as e:
        print(e)

res = get_news_content()
print(res)
print(type(res))
generate_ciyun(res)






