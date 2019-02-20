# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 15:55:47 2019

@author: Administrator
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas.io.json import json_normalize
from pymongo import MongoClient
from pyecharts import Bar,Line,Overlap,Page,WordCloud,Pie,Funnel
import jieba
from collections import Counter


page=Page()   #实例化Page
conn = MongoClient(host='127.0.0.1', port=27017)  # 实例化MongoClient
db = conn.get_database('maoyan')  # 连接到maoyan数据库

maoyan = db.get_collection('maoyan') # 连接到集合maoyan
mon_data = maoyan.find()  # 查询这个集合下的所有记录

data=json_normalize([comment for comment in mon_data])

data = data.drop(columns='_id')
data = data.drop_duplicates(subset='userId')
data['time'] = pd.to_datetime(data['time']/1000, unit='s')
#读入的时间数据是字符串格式，转换成datetime格式,单位化为秒
data = data[data['time']>=pd.to_datetime('2019-02-05 00:00:00')]
data.set_index(data['time'], inplace=True)

data.info()
print(data.head())

# 数据清洗


'''
df信息

Data columns (total 10 columns):
content       84114 non-null object
gender        84114 non-null int64
id            84114 non-null int64
nick          84114 non-null object
replyCount    84114 non-null int64
score         84114 non-null int64
time          84114 non-null datetime64[ns]
upCount       84114 non-null int64
userId        84114 non-null int64
userLevel     84114 non-null int64
dtypes: datetime64[ns](1), int64(7), object(2)
memory usage: 7.1+ MB

输出头部信息

                              content  gender          id           nick  \
time                                                                       
2019-02-13 08:49:00      不好看 没意思 特效还行       2  1057160823          纯洁小萌萌   
2019-02-13 08:49:00          地有点粘，哈哈哈       1  1057162283          L1u三废   
2019-02-13 08:49:00  特效爆炸！  永远支持国产电影！       0  1057159336       八百逗比奔北坡😶   
2019-02-13 08:49:00       很泪目啊。 堪比好莱坞       2  1057160811  Kimi864293104   
2019-02-13 08:49:00            好看！！！！       2  1057156983             随便   

                     replyCount  score                time  upCount  \
time                                                                  
2019-02-13 08:49:00           0      5 2019-02-13 08:49:00        0   
2019-02-13 08:49:00           0     10 2019-02-13 08:49:00        0   
2019-02-13 08:49:00           0     10 2019-02-13 08:49:00        0   
2019-02-13 08:49:00           0     10 2019-02-13 08:49:00        0   
2019-02-13 08:49:00           0     10 2019-02-13 08:49:00        0   

                         userId  userLevel  
time                                        
2019-02-13 08:49:00    29444203          2  
2019-02-13 08:49:00   560675146          3  
2019-02-13 08:49:00  1022833680          2  
2019-02-13 08:49:00   170658854          1  
2019-02-13 08:49:00  1056871017          2  


'''


'''
总体评价
'''
print(data['score'].mean())
score_total = data['score'].value_counts().sort_index()
#sort_index(ascending=True) 方法可以对索引进行排序操作
print(score_total)
bar = Bar("《流浪地球》各评分数量", width=700)
line = Line("", width=700)
bar.add("", score_total.index, score_total.values, is_stack=True, is_label_show=True,
       bar_category_gap='40%', label_color = ['#196845'],
       legend_text_size=18,xaxis_label_textsize=18,yaxis_label_textsize=18)
line.add("", score_total.index, score_total.values+1000, is_smooth=True)

overlap = Overlap(width=700)
overlap.add(bar)
overlap.add(line)
#overlap.render()
page.add(overlap)

# 低分百分比
low_score=score_total[:4].sum()/score_total.sum()*100
# 高分百分比
high_score=score_total[8:].sum()/score_total.sum()*100
# 满分百分比
full_score=score_total[10:].sum()/score_total.sum()*100

print(u'低分占百分比为:{:.3f}%'.format(low_score))
print(u'高分占百分比为:{:.3f}%'.format(high_score))
print(u'满分占百分比为:{:.3f}%'.format(full_score))
'''
低分占百分比为:3.419%
高分占百分比为:90.625%
满分占百分比为:70.530%

'''


'''
总体评价的时间走向
'''
score_by_time = data['score'].resample('H').mean()
#print(score_by_time)
line1 = Line("《流浪地球》平均评分时间走向", width=700)
line1.add("", score_by_time.index.date, score_by_time.values, is_smooth=True,
         legend_text_size=18,xaxis_label_textsize=18,yaxis_label_textsize=18,
         xaxis_rotate=20, yaxis_min=8)
#line.render()
page.add(line1)



#输出最高和最低平均评分的时间段
print(score_by_time.nsmallest(6))
print(score_by_time.nlargest(6))

'''
高分的评价理由
'''


jieba.add_word('屈楚萧')
jieba.add_word('刘启')
jieba.add_word('吴京')
jieba.add_word('刘培强')
jieba.add_word('李光洁')
jieba.add_word('王磊')
jieba.add_word('吴孟达')
jieba.add_word('达叔')
jieba.add_word('韩子昂')
jieba.add_word('赵今麦')
jieba.add_word('韩朵朵')

swords = [x.strip() for x in open ('stopwords.txt')]

def plot_word_cloud1(data, swords):
    text = ''.join(data['content'])
    words = list(jieba.cut(text))
    ex_sw_words = []
    for word in words:
        if len(word)>1 and (word not in swords):
            ex_sw_words.append(word)
    c = Counter()
    c = Counter(ex_sw_words)
    wc_data = pd.DataFrame({'word':list(c.keys()), 'counts':list(c.values())}).sort_values(by='counts', ascending=False).head(100)
    wordcloud = WordCloud(width=1300, height=620)
    wordcloud.add("", wc_data['word'], wc_data['counts'], word_size_range=[20, 100])
    page.add(wordcloud)

# 高分的评价词云

plot_word_cloud1(data=data[data['score']>7], swords=swords)
#高分评价点赞数目最多的评价

up_top_ten=data[data['score']>7].nlargest(10, 'upCount')
print("高分评价点赞数目最多的评价如下：")
for i in up_top_ten['content']:
    print(i+'\n')
reply_top_ten=data[data['score']>7].nlargest(10, 'replyCount')    
print("高分评价回复数目最多的评价如下：")
for i in reply_top_ten['content']:
    print(i+'\n')
    
'''
低分的理由
'''

def plot_word_cloud2(data, swords):
    text = ''.join(data['content'])
    words = list(jieba.cut(text))
    ex_sw_words = []
    for word in words:
        if len(word)>1 and (word not in swords):
            ex_sw_words.append(word)
    c = Counter()
    c = Counter(ex_sw_words)
    wc_data = pd.DataFrame({'word':list(c.keys()), 'counts':list(c.values())}).sort_values(by='counts', ascending=False).head(100)
    wordcloud = WordCloud(width=1300, height=620)
    wordcloud.add("", wc_data['word'], wc_data['counts'], word_size_range=[20, 100])
    page.add(wordcloud)
# 低分的评价
plot_word_cloud2(data=data[data['score']<4], swords=swords)
up_bottom_ten=data[data['score']<4].nlargest(10, 'upCount')
#低分评价点赞数目最多的评价
print("低分评价点赞数目最多的评价如下：")
for i in up_bottom_ten['content']:
    print(i+'\n')
    
reply_bottom_ten=data[data['score']>7].nlargest(10, 'replyCount')    
print("低分评价回复数目最多的评价如下：")
for i in reply_bottom_ten['content']:
    print(i+'\n')   
    
'''    
低分的人群有哪些特征
'''

# 总体的性别比例
#0,1,2分别指性别未知、男、女
gender_total = data['gender'].value_counts()
pie1 = Pie("《流浪地球》观众性别比例", width=700)
pie1.add("", ['未知', '男', '女'], gender_total.values, is_stack=True, is_label_show=True,
       bar_category_gap='60%', label_color = ['#278f9d'])
#pie1.render()
page.add(pie1)

total_gender_percent=gender_total/gender_total.sum()*100

print('总体各性别占百分比为:')
print(total_gender_percent)

# 低分的性别比例
gender_low = data.loc[data['score']<5, 'gender'].value_counts()
bar2 = Bar("《流浪地球》低分评论观众性别", width=700)
bar2.add("", ['未知', '男', '女'], gender_low.values, is_stack=True, is_label_show=True,
       bar_category_gap='60%', label_color = ['#278f9d'],
       legend_text_size=18,xaxis_label_textsize=18,yaxis_label_textsize=18)
#bar.render()
page.add(bar2)
    
low_gender_percent=gender_low/gender_low.sum()*100
print('低分观众各性别占百分比为:')
print(low_gender_percent)


# 总体的等级比例
level_total = data['userLevel'].value_counts().sort_index()
bar3 = Bar("《流浪地球》观众等级", width=700)
bar3.add("", level_total.index, level_total.values, is_stack=True, is_label_show=True,
       bar_category_gap='40%', label_color = ['#130f40'],
       legend_text_size=18,xaxis_label_textsize=18,yaxis_label_textsize=18)

#bar.render()
page.add(bar3)
 # 低分评论的观众等级比例
level_low = data.loc[data['score']<5, 'userLevel'].value_counts().sort_index()
bar4 = Bar("《流浪地球》低分评论的观众等级", width=700)
bar4.add("", level_low.index, level_low.values, is_stack=True, is_label_show=True,
       bar_category_gap='40%', label_color = ['#130f40'],
       legend_text_size=18,xaxis_label_textsize=18,yaxis_label_textsize=18)   
    
    
#bar.render()
page.add(bar4)   

'''
高低分和哪位演员有关

'''

mapping = {'liucixin':'刘慈欣|大刘', 'guofan':'郭帆|郭导', 'quchuxiao':'屈楚萧|刘启|户口', 'wujing':'吴京|刘培强', 
           'liguangjie':'李光洁|王磊', 'wumengda':'吴孟达|达叔|韩子昂', 'zhaojinmai':'赵今麦|韩朵朵'}
for key, value in mapping.items():
    data[key] = data['content'].str.contains(value)

# 总体提及次数
    
staff_count = pd.Series({key: data.loc[data[key], 'score'].count() for key in mapping.keys()}).sort_values()
print(staff_count)
funnel = Funnel("《流浪地球》演职员总体提及次数", width=700)
funnel.add("", ['李光洁','郭帆','赵今麦','吴孟达','屈楚萧','刘慈欣','吴京'], staff_count.values, is_stack=True, is_label_show=True,
      legend_pos="50%",label_color = ['#677fge'],legend_text_size=8)
funnel.render()
    
page.add(funnel)



average_score = pd.Series({key: data.loc[data[key], 'score'].mean() for key in mapping.keys()}).sort_values()
print(average_score)

bar6 = Bar("《流浪地球》演职员平均分", width=700)
bar6.add("", ['赵今麦','吴孟达','屈楚萧','吴京','李光洁','刘慈欣','郭帆'], np.round(average_score.values,2), is_stack=True, is_label_show=True,
       bar_category_gap='60%', label_color = ['#677fge'],
       legend_text_size=18,xaxis_label_textsize=18,yaxis_label_textsize=18)

#bar.render()
    
page.add(bar6)



staff_count_low = pd.Series({key: data.loc[data[key]&(data['score']<5), 'score'].count() for key in mapping.keys()}).sort_values()
print(staff_count_low)
staff_count_pct = np.round(staff_count_low/staff_count*100, 2).sort_values()
print(staff_count_pct)

bar7 = Bar("《流浪地球》演职员低分评论提及百分比", width=700)
bar7.add("", ['郭帆','刘慈欣','李光洁','屈楚萧','赵今麦','吴京','吴孟达'], staff_count_pct.values, is_stack=True, is_label_show=True,
       bar_category_gap='60%', label_color = ['#8gfdaf'],
       legend_text_size=18,xaxis_label_textsize=18,yaxis_label_textsize=18)

#bar.render()
    
page.add(bar7)
data[data['wumengda']&(data['score']<5)].nlargest(5, 'upCount')
for i in data[data['wumengda']&(data['score']<5)].nlargest(5, 'upCount')['content']:
    print(i+'\n')
    
data[data['wujing']&(data['score']<5)].nlargest(5, 'upCount')
for i in data[data['wujing']&(data['score']<5)].nlargest(5, 'upCount')['content']:
    print(i+'\n')
data[data['zhaojinmai']&(data['score']<5)].nlargest(5, 'upCount')
for i in data[data['zhaojinmai']&(data['score']<5)].nlargest(5, 'upCount')['content']:
    print(i+'\n')



'''
被评论最多replycount，点赞最多的upcount
'''


page.render("./commentAnalysis.html")









