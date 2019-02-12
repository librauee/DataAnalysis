# -*- coding: utf-8 -*-
"""
Created on Sun Jan 27 22:25:04 2019

@author: Administrator
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
from pyecharts import Bar, Line, Overlap,WordCloud,Page
from pylab import mpl


mpl.rcParams['font.sans-serif'] = ['SimHei']  #解决seaborn中文字体显示问题
plt.rc('figure', figsize=(10, 10))            #把plt默认的图片size调大一点
page=Page()                                   #实例化Page类
data=pd.read_csv('F:/DataAnalysis/interestingprogram/NationalNames.csv')
                                              #读取csv文件，得到DataFrame

"""

1.从2010年到2017年之间最受欢迎的男女生英文名，画出男女生各前10名的年份-数量图

"""


#男生
top10_boy=data.loc[(data['Year'].isin(list(range(2010,2018))))&(data['Gender']=='M'),:].groupby('Name').Count.sum().nlargest(10)
boy_total=data.loc[(data['Year'].isin(list(range(2010,2018))))&(data['Gender']=='M'),:].groupby('Name').Count.sum().sum()
#print(boy_total)
bname=list(top10_boy.index)
bvalue=list(top10_boy.values)
wordcloud1=WordCloud("2010年以来最受欢迎的男生名Top10",width=1000,height=500,background_color='#f2eada')
wordcloud1.add("",bname,bvalue,word_size_range=[20,100],shape='dimand')      
page.add(wordcloud1)
#wordcloud.render()
data_top10_boy=data.loc[(data['Year'].isin(list(range(2010,2018))))&(data['Gender']=='M')&(data['Name']).isin(list(top10_boy.index)),:]
#print(data_top15_boy)
#sns绘图

sns.set(font_scale=2)   #标题大小
g1 = sns.FacetGrid(data_top10_boy, col="Name", col_wrap=4)   #列名为Name，一行四个
t1=g1.map(plt.plot, "Year", "Count",color="b",marker="o")       #绘图，横轴为Year,纵轴为Count
plt.show(t1)


#女生
top10_girl = data.loc[(data['Year'].isin(list(range(2010,2018)))) & (data['Gender'] == 'F'), :].groupby('Name').Count.sum().nlargest(10)
list(data.loc[(data['Year'].isin(list(range(2010,2018)))) & (data['Gender'] == 'F'), :].groupby('Name').Count.sum().nlargest(30).index)
gname = list(top10_girl.index)
gvalue = list(top10_girl.values)
wordcloud2 = WordCloud("2010年以来最受欢迎的女生名Top10",width=1000, height=500,background_color='#feeeed')  # feeeed
wordcloud2.add("", gname, gvalue, word_size_range=[20, 100],shape='diamond')
#wordcloud.show_config()
#wordcloud.render()
page.add(wordcloud2)
data_top10_girl = data.loc[(data['Year'].isin(list(range(2010,2018)))) & (data['Gender'] == 'F') &  (data['Name']).isin(list(top10_girl.index)), :]
data_top10_girl.sort_values(by = ['Year', 'Count'], ascending=False, inplace=True)
#sns绘图

sns.set(font_scale=2)
g2 = sns.FacetGrid(data_top10_girl, col="Name", col_wrap=4)
g2.set(axis_bgcolor='#feeeed')
t2=g2.map(plt.plot, "Year", "Count",color="#FF1CAE",marker="o")
plt.show(t2)
     
"""

2.1920年以来每个年代最流行的英文名

"""
matplotlib.rcParams['font.family']='SimHei'   #解决matplotlib中文字体显示问题  

data_decades = data[data['Year']>=1920]    #筛选1920年以后的数据形成新的df
data_decades['decade'] = pd.cut(data_decades['Year'], [1920,1930,1940,1950,1960,1970,1980,1990,2000,2010,2018], 
                                labels = ['20后','30后','40后', '50后','60后','70后','80后','90后','00后','10后'],right=False)
#print(data_decades)
#新增'decade'列名,将其划分为20后，30后等等
#right=False指定哪端是开区间或闭区间（指定右端为开区间）
decade = data_decades.groupby(['decade', 'Gender', 'Name']).Count.sum().groupby(['decade', 'Gender']).nlargest(1)  
#print(decade)


#boy
decade_boy_count = decade.iloc[decade.index.get_level_values(3)=='M'].reset_index(level=[0,1,3], drop=True)
#drop=True  删除原有行索引
#print(decade_boy_count)
decade_boy_total = data_decades[data_decades['Gender']=='M'].groupby('decade').Count.sum()
decade_boy_pct = (decade_boy_count/decade_boy_total*100).round(2)
#plt.subplot(311)
ax1=decade_boy_pct.plot.barh(stacked=True,title='各年代最流行的男性名字')
ax1.set_ylabel('')
ax1.set_xlabel('百分比')
plt.show(ax1)
        

#girl       
decade_girl_count = decade.iloc[decade.index.get_level_values(3)=='F'].reset_index(level=[0,1,3], drop=True)
#print(decade_girl_count)
decade_girl_total = data_decades[data_decades['Gender']=='F'].groupby('decade').Count.sum()
decade_girl_pct = (decade_girl_count/decade_girl_total*100).round(2)
#plt.subplot(313)
ax2 = decade_girl_pct.plot.barh(title='各年代最流行的女性名字')
ax2.set_ylabel('')
ax2.set_xlabel('百分比')
ax2.set(axis_bgcolor='#feeeed')
plt.show(ax2)

        
"""

3.以前很流行，现在不流行的英文名,用pyecharts画出折线图，反映出英文名走势

"""
a=range(1920,2018)
#boy       
data_popular_former = data[(data['Year'] < 1950) & (data['Count'] > 10500) & (data['Gender'] == 'M')]
data_not_popular_now = data[(data['Year'] > 2000) & (data['Count'] < 1000) & (data['Gender'] == 'M')]
boys_names_popular_former = list(set(list(data_popular_former.Name.unique())) & set(list(data_not_popular_now.Name.unique())))
#以前流行现在也流行的男生名， set也是一组数，无序，内容又不能重复，通过调用set()方法创建
boys_names_popular_former_data = data[(data['Name'].isin(boys_names_popular_former)) & (data['Year']>=1920) & (data['Gender']=='M')]

attr1=list(map(str,a))
#把元素map成str类型，因为该折线图下标必须是字符串
line1 = Line("男生姓名走势图",width=1000, height=600)
for name in boys_names_popular_former:
    v = list(boys_names_popular_former_data[boys_names_popular_former_data['Name']==name].Count.values)
    line1.add(name, attr1, v, legend_text_size=15,xaxis_label_textsize=18,yaxis_label_textsize=18,legend_pos="20%")
page.add(line1)

#girl
girldata_popular_former = data[(data['Year'] < 1950) & (data['Count'] > 22500) & (data['Gender'] == 'F')]
girldata_not_popular_now = data[(data['Year'] > 2000) & (data['Count'] < 1000) & (data['Gender'] == 'F')]
girl_names_popular_former = list(set(list(girldata_popular_former.Name.unique())) & set(list(girldata_not_popular_now.Name.unique())))
girl_names_popular_former_data = data[(data['Name'].isin(girl_names_popular_former)) & (data['Year']>=1920) & (data['Gender']=='F')]

#a=range(1920,2018)
attr2=list(map(str,a))
#把元素map成str类型，因为该折线图下标必须是字符串

line2 = Line("女生姓名走势图",width=1000, height=600)
for name in girl_names_popular_former:
    v = list(girl_names_popular_former_data[girl_names_popular_former_data['Name']==name].Count.values)
    line2.add(name, attr2, v,legend_text_size=15,xaxis_label_textsize=18,yaxis_label_textsize=18,legend_pos="20%")
page.add(line2)



"""

4.二十一世纪以来越来越流行的英文名字,绘制出折线图，体现变化趋势

"""


#boy

data_popular_now = data[(data['Year']>=2000)&(data['Gender'] =='M')&(data['Count']>7000)]
data_popular_now = data_popular_now.pivot(index='Name', columns='Year',values='Count')
#pivot行列转置，把Name变为索引项
#print(data_popular_now)
year = pd.DataFrame({'Year':list(range(2000, 2018))}, index=list(range(2000, 2018)))
data_popular_now_corr = data_popular_now.corrwith(year['Year'], axis=1)
boys_names_popular_now = list(data_popular_now_corr[data_popular_now_corr > 0.8].index)
boys_names_popular_now_data = data[(data['Name'].isin(boys_names_popular_now)) & (data['Year']>=1920) & (data['Gender']=='M')]
boys_names_popular_now_data = boys_names_popular_now_data.pivot(index='Name', columns='Year',values='Count').reset_index().melt('Name', value_name='Count')
#df.melt() 是 df.pivot() 逆转操作函数,将列名转换为列数据(columns name → column values)，重构DataFrame

#a=range(1920,2018)
attr3=list(map(str,a))
line3 = Line("二十一世纪以来越来越流行的男生名",width=1000, height=600)
for name in boys_names_popular_now:
    v = list(boys_names_popular_now_data[boys_names_popular_now_data['Name']==name].Count.values)
    line3.add(name, attr3, v, legend_text_size=15,xaxis_label_textsize=18,yaxis_label_textsize=18,legend_pos="30%")
page.add(line3)


#girl

data_popular_now = data[(data['Year']>=2000)&(data['Gender'] =='F')&(data['Count']>6000)]
data_popular_now = data_popular_now.pivot(index='Name', columns='Year',values='Count')
data_popular_now_corr = data_popular_now.corrwith(year['Year'], axis=1)
girls_names_popular_now = list(data_popular_now_corr[data_popular_now_corr > 0.7].index)
girls_names_popular_now_data = data[(data['Name'].isin(girls_names_popular_now)) & (data['Year']>=1920) & (data['Gender']=='F')]
girls_names_popular_now_data = girls_names_popular_now_data.pivot(index='Name', columns='Year',values='Count').reset_index().melt('Name', value_name='Count')

#a=range(1920,2018)
attr4=list(map(str,a))
line4 = Line("二十一世纪以来越来越流行的女生名",width=1000, height=600)
for name in girls_names_popular_now:
    v = list(girls_names_popular_now_data[girls_names_popular_now_data['Name']==name].Count.values)
    line4.add(name, attr4, v, legend_text_size=15,xaxis_label_textsize=18,yaxis_label_textsize=18,legend_pos="30%")
page.add(line4)




"""

5.影响美国人取名的因素：体育明星、电视明星，选取了一系列名人，绘制折线与柱状图

"""


def name_trend(name, data, gender=['M','F'], year=1920, dodge = 500):
    if isinstance(gender, str):
        name_data = data[(data['Name'] == name)&(data['Gender']==gender)&(data['Year']>=year)]
        attr = list(name_data['Year'].values)
        attr1=list(map(str,attr))
        bar = Bar("名人名字的影响",width=1000, height=600)
        bar.add(name, attr, list(name_data['Count'].values), mark_line=["average"], mark_point=["max", "min"],
               legend_text_size=18,xaxis_label_textsize=18,yaxis_label_textsize=18)
        line = Line()
        line.add(name, attr1, list(name_data['Count'].values + dodge))
        
    else:
        name_data = data[(data['Name'] == name)&(data['Year']>=year)]
        attr = list(range(year, 2018))
        attr1=list(map(str,attr))
        v1 = name_data[name_data['Gender']==gender[0]].Count.values
        v2 = name_data[name_data['Gender']==gender[1]].Count.values
        bar = Bar("名人名字的影响",width=1000, height=600)
        bar.add(name+"男", attr, list(v1), legend_text_size=18,xaxis_label_textsize=18,yaxis_label_textsize=18)
        bar.add(name+"女", attr, list(v2), legend_text_size=18,xaxis_label_textsize=18,yaxis_label_textsize=18)
        line = Line()
        line.add(name+"男", attr1, list(v1 + dodge))
        line.add(name+"女", attr1, list(v2 + dodge))
    
    overlap = Overlap()
    overlap.add(bar)
    overlap.add(line)
    page.add(overlap)

name_trend('Jordan',data,gender='M',year=1960)
name_trend('Irving',data,gender='M',year=2000)
name_trend('Wade',data,gender='M',year=1990)
name_trend('Kobe',data,gender='M',year=1920, dodge=100)
name_trend('Jordan',data,year=1976, dodge=100)
name_trend('Chandler',data,year=1976, dodge=100)
name_trend('Taylor',data,year=1976, dodge=100)
name_trend('Riley', data,year=1976, dodge=100)
name_trend('Kobe',data,gender='M',year=1920, dodge=100)
name_trend('Emma',data,gender='F',year=1980)
name_trend('Scarlett',data,gender='F',year=1980, dodge=200)

#page.render("./starsinfuence.html")

"""

6. 为什么同一发音的名字，有很多不同的拼写变体？

"""

Catherine = data['Name'][data['Name'].str.contains('^[C|K]ath(.*)')].unique()
Catherine_data = data[data['Name'].isin(Catherine)].groupby('Name').Count.sum()
name1 = list(Catherine_data.index)
value1 = list(Catherine_data.values)
wordcloud3 = WordCloud("凯斯",width=1000, height=600,background_color='#feeeed')  # feeeed
wordcloud3.add("", name1, value1, word_size_range=[20, 100],shape='diamond')
page.add(wordcloud3)
Emily = data['Name'][data['Name'].str.contains('Emil(.*)')].unique()
Emily_data = data[data['Name'].isin(Emily)].groupby('Name').Count.sum()
name2 = list(Emily_data.index)
value2 = list(Emily_data.values)
wordcloud4 = WordCloud("艾米",width=1000, height=600,background_color='#f2eada')  # f2eada
wordcloud4.add("", name2, value2, word_size_range=[20, 100],shape='diamond')
page.add(wordcloud4)



'''

7. 一些具有特殊含义的名字，有多少人取？

'''


def name_trend2(name, data, gender, dodge=100):
    name_data = data[(data['Name']==name)&(data['Gender']==gender)]
    attr = list(name_data['Year'].values)
    attr1=list(map(str,attr))
    v1 = name_data['Count'].values

    bar = Bar("Special Name",width=1000, height=600)
    bar.add("", attr, list(v1), legend_text_size=18,xaxis_label_textsize=18,yaxis_label_textsize=18)
    
    line = Line()
    line.add(name, attr1, list(v1 + dodge))
    
    overlap = Overlap()
    overlap.add(bar)
    overlap.add(line)
    page.add(overlap)

    

name_trend2('Dick',data,gender='M', dodge=50)
name_trend2('Dong', data, gender='M', dodge=1)
name_trend2('Cherry',data,gender='F', dodge=10)

#page.render("./specialname.html")


'''

#8. 一些特殊的名字    

'''
class Solution:
    #return a string
    def getlongestpalindrome(self, s, l, r):    #最长回文
        while l >= 0 and r < len(s) and s[l] == s[r]:
            l -= 1; r += 1
        return s[l+1 : r]
    #return bool
    def longestPalindrome(self, s):
        palindrome = ''
        for i in range(len(s)):
            len1 = len(self.getlongestpalindrome(s, i, i))
            if len1 > len(palindrome): palindrome = self.getlongestpalindrome(s, i, i)
            #回文字符串中间字符仅有一个
            len2 = len(self.getlongestpalindrome(s, i, i + 1))
            if len2 > len(palindrome): palindrome = self.getlongestpalindrome(s, i, i + 1)
        return True if len(palindrome) > 5 else False
        
a = Solution()
a.longestPalindrome('alfrederfl')
all_name = data['Name'].unique()
palindrome_name = []
for name in all_name:
    if a.longestPalindrome(name):
        palindrome_name.append(name)
palindrome_data = data[data['Name'].isin(palindrome_name)].groupby('Name').Count.sum()
name3 = list(palindrome_data.index)
value3 = list(palindrome_data.values)
wordcloud5 = WordCloud("带回文的名字",width=1000, height=600,background_color='#feeeed')  # feeeed
wordcloud5.add("", name3, value3, word_size_range=[20, 100],shape='diamond')
#wordcloud5.render()
page.add(wordcloud5)

page.render("./totalpicture.html")






