import pymysql.cursors

from Model.news import News

#获取数据库连接
def get_connect():
    connect = pymysql.Connect(
        host='49.4.14.211',
        port=10005,
        user='root',
        passwd='a1b2c3',
        db='toutiao',
        charset='utf8'
    )
    return connect


#插入toutiao_news
def insert_data(news_list):
    try:
        connect = get_connect()
        cursor = connect.cursor()

        for news in news_list:
            sql = "INSERT INTO toutiao_news(title, tag, source, source_url,news_date) VALUES ( %s,%s,%s,%s,%s)"
            # data = {news.title, news.tag, news.source, news.source_url, news.keyword, news.keywords}
            cursor.execute(sql, (news.title, news.tag, news.source, news.source_url,news.news_date))
        connect.commit()

    except Exception as e:
        print(e)
    finally:
        cursor.close()
        connect.close()
# #查询key_words
# def find_key_words():
#     try:
#         connect = get_connect()
#         cursor = connect.cursor()
#         sql = "select distinct key_word from douyin"
#         cursor.execute(sql)
#         result = cursor.fetchall()
#         return result
#     except Exception as e:
#         print(e)
#     finally:
#         cursor.close()
#         connect.close()

# #插入douyin
# def insert_douyin_data(news_list):
#     try:
#         connect = get_connect()
#         cursor = connect.cursor()
#
#         for news in news_list:
#             sql = "INSERT INTO douyin(follower_count, nickname, signature, sec_uid,uid,short_id,unique_id,key_word) VALUES ( %s,%s,%s,%s,%s,%s,%s,%s)"
#             cursor.execute(sql, (news.follower_count, news.nickname,news.signature, news.sec_uid,news.uid,news.short_id,news.unique_id,news.key_word))
#         connect.commit()
#
#     except Exception as e:
#         print(e)
#     finally:
#         cursor.close()
#         connect.close()

# def insert_data_apinews(news_list):
#     try:
#         connect = get_connect()
#         cursor = connect.cursor()
#
#         for news in news_list:
#             sql = "INSERT INTO news_api(title, tag, source, source_url) VALUES ( %s,%s,%s,%s)"
#             # data = {news.title, news.tag, news.source, news.source_url, news.keyword, news.keywords}
#             cursor.execute(sql, (news.title, news.tag, news.source, news.source_url))
#         connect.commit()
#         print('successful')
#
#     except Exception as e:
#         print(e)
#     finally:
#         cursor.close()
#         connect.close()

#
def select_url():
    arrList = []
    try:
        connect = get_connect()
        cursor = connect.cursor()
        print("connection")
        sql = "SELECT id,source_url FROM toutiao_news WHERE id > 15855"
        cursor.execute(sql)
        result = cursor.fetchall()
        for row in result:
            # print(row[0])
            news = News()
            news.id = row[0]
            news.source_url = row[1]
            arrList.append(news)
    except Exception as e:
        print(e)
    finally:
        return arrList


def update_content(news):
    try:
        connect = get_connect()
        cursor = connect.cursor()
        sql = "UPDATE toutiao_news SET content = %s WHERE id = %s"
        cursor.execute(sql, (news.content, news.id))
        connect.commit()
    except Exception as e:
        print(e)

#查询头条新闻，id,title,keywords，返回arraylist
# def select_toutiao_news(keyword):
#     arrList = []
#     try:
#         connect = get_connect()
#         cursor = connect.cursor()
#         sql = "SELECT id,title,keywords FROM toutiao_news where keyword = %s"
#         cursor.execute(sql, keyword)
#         result = cursor.fetchall()
#         for row in result:
#             # print(row[0])
#             news = News()
#             news.id = row[0]
#             news.title = row[1]
#             arrList.append(news)
#     except Exception as e:
#         print(e)
#     finally:
#         return arrList

 #更新距离算法
# def update_distance(distance):
#     try:
#         connect = get_connect()
#         cursor = connect.cursor()
#
#         for item in distance:
#             sql = "UPDATE toutiao_news SET distance = distance + %s WHERE id = %s"
#             cursor.execute(sql, (distance[item], item))
#         connect.commit()
#
#     except Exception as e:
#         print(e)

#查询头条新闻链接，返回set
def select_source_url_returnset():
    arrList = set()
    try:
        connect = get_connect()
        cursor = connect.cursor()
        print("connection mysql successful")
        sql = "SELECT source_url FROM toutiao_news"
        cursor.execute(sql)
        result = cursor.fetchall()
        for row in result:
            # print(row[0])
            arrList.add(row[0])
    except Exception as e:
        print(e)
    finally:
        return arrList