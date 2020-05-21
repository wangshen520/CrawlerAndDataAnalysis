from matplotlib import font_manager as fm
from  matplotlib import cm
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from Utils.Util import get_connect


def get_news_content():
    tags = []
    value=[]

    try:
        connect = get_connect()
        cursor = connect.cursor()
        print("connection")
        sql = "select * from (SELECT tag,count(1) count FROM toutiao_news group by tag) c where c.count>42 and tag!='news'"
        cursor.execute(sql)
        result = cursor.fetchall()
        for row in result:
            tags.append(row[0])
            value.append(row[1])
    except Exception as e:
        print(e)
    finally:
        return tags,value
shapes,values=get_news_content()
s = pd.Series(values, index=shapes)
labels = s.index
sizes = s.values
# explode = (0.1,0,0,0,0,0,0,0,0,0,0,0,0,0.2,0)  # "explode" ， show the selected slice
#在ax1.pie（explode=explode
fig, axes = plt.subplots(figsize=(19,10),ncols=2) # 设置绘图区域大小
ax1, ax2 = axes.ravel()

colors = cm.rainbow(np.arange(len(sizes))/len(sizes)) # colormaps: Paired, autumn, rainbow, gray,spring,Darks
patches, texts, autotexts = ax1.pie(sizes, labels=labels, autopct='%1.0f%%',
        shadow=False, startangle=170, colors=colors, labeldistance=1.2,pctdistance=1.03, radius=0.4)
# labeldistance: 控制labels显示的位置
# pctdistance: 控制百分比显示的位置
# radius: 控制切片突出的距离

ax1.axis('equal')
# 重新设置字体大小
proptease = fm.FontProperties()
proptease.set_size('xx-small')
# font size include: ‘xx-small’,x-small’,'small’,'medium’,‘large’,‘x-large’,‘xx-large’ or number, e.g. '12'
plt.setp(autotexts, fontproperties=proptease)
plt.setp(texts, fontproperties=proptease)

ax1.set_title('Shapes', loc='center')

# ax2 只显示图例（legend）
ax2.axis('off')
ax2.legend(patches, labels, loc='center left')

plt.tight_layout()
# plt.savefig("pie_shape_ufo.png", bbox_inches='tight')
plt.savefig('classification.jpg')
plt.show()