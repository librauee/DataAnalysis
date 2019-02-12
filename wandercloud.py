# -*- coding: utf-8 -*-
"""
Created on Tue Feb 12 11:38:40 2019

@author: Administrator
"""

import matplotlib.pyplot as plt
from wordcloud import WordCloud
from scipy.misc import imread
import jieba

f=open("流浪地球豆瓣评论.txt","rb")
text = f.read()
#结巴分词
wordlist = jieba.cut(text,cut_all=True)
wl = " ".join(wordlist)
#print(wl)#输出分词之后的txt


#把分词后的txt写入文本文件
#fenciTxt  = open("fenciHou.txt","w+")
#fenciTxt.writelines(wl)
#fenciTxt.close()


#设置词云
wc = WordCloud(background_color = "white", #设置背景颜色
               mask = imread('ball.jpg'),  #设置背景图片
               max_words = 1000, #设置最大显示的字数
               stopwords = ["的", "这种", "这样", "还是", "就是", "这个"], #设置停用词
               font_path = "C:\Windows\Fonts\simkai.ttf",  # 设置为楷体 常规
               #设置中文字体，使得词云可以显示（词云默认字体是“DroidSansMono.ttf字体库”，不支持中文）
               max_font_size = 60,  #设置字体最大值
               random_state = 30, #设置有多少种随机生成状态，即有多少种配色方案
    )
myword = wc.generate(wl)#生成词云
wc.to_file('result.jpg')

#展示词云图
plt.imshow(myword)
plt.axis("off")
plt.show()

f.close()