# -*- coding: utf-8 -*-
"""
Created on Sat Feb 22 17:16:06 2020

@author: 老肥
@WeChat Official Accounts:老肥码码码
@Wechat: jennnny1216

Happy Python，Happy Life!
"""


from pymongo import MongoClient
import pandas as pd
import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from pyecharts import options as opts
from pyecharts.charts import Geo,Line,WordCloud,Pie,Parallel,PictorialBar,Bar
from pyecharts.globals import ChartType, SymbolType

pd.options.display.max_columns=None
db=MongoClient().clip
data=pd.DataFrame(list(db['bilibili'].find()))

print(data)


def cut(title):
    return title[14:]
    
data['title']=data['title'].apply(cut)
title=list(data['title'])
count=0
for i in title:
    print(i)
    if '？' in i:
        count+=1

print(count/len(title))
# 0.7923076923076923



description=list(data['description'])
count1=0
count2=0
count3=0
for i in description:
    print(i)
    if i.count('？')==1:
        count+=1
    if i.count('？')==2:
        count2+=1
    if i.count('？')>2:
        count3+=1
print(count1/len(description))
print(count2/len(description))
print(count3/len(description))

data['length']=data['length'].apply(lambda x:int(x[:2])*60+int(x[3:]))
print(data['length'].sum()/len(data))



text="".join(title)
wordlist=jieba.cut(text,cut_all=False)
wl=" ".join(wordlist)
#设置词云
wc=WordCloud(
               background_color = "white", #设置背景颜色
               mask = plt.imread('clip.jpg'),  #设置背景图片
               stopwords = ["的", "这种", "这样", "还是", "就是", "这个"], #设置停用词
               font_path = "C:\Windows\Fonts\simkai.ttf",  # 设置为楷体 常规
               max_words=300,
               max_font_size=100,
               min_font_size=8,
               random_state=50,
    )
myword=wc.generate(wl)#生成词云
wc.to_file('result.jpg')

#展示词云图
plt.imshow(myword)
plt.axis("off")
plt.show()



print(data)
play_top=data.sort_values(by='play',ascending=False)
play_top_title=list(play_top[:10]['title'])
play_top_count=list(play_top[:10]['play'])

c=(
   Bar()
   .add_xaxis(play_top_title)
   .add_yaxis("",play_top_count)
   .set_global_opts(
            title_opts=opts.TitleOpts(title="回形针B站视频播放量前十榜单"),
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-13,font_weight='bold'))
        )
    )
   
c.render()


play_top=data.sort_values(by='comment',ascending=False)
play_top_title=list(play_top[:10]['title'])
play_top_count=list(play_top[:10]['comment'])

c=(
   Bar()
   .add_xaxis(play_top_title)
   .add_yaxis("",play_top_count)
   .set_global_opts(
            title_opts=opts.TitleOpts(title="回形针B站视频评论数目前十榜单"),            
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-13,font_weight='bold')
            )
        )
    )
   
c.render()