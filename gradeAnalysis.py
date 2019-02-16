# -*- coding: utf-8 -*-
"""
Created on Fri Feb 15 22:01:23 2019

@author: Administrator
"""

import numpy as np
import pandas as pd
from pyecharts import Bar, Line, Overlap,Page
from pylab import mpl
import matplotlib.pyplot as plt

mpl.rcParams['font.sans-serif'] = ['SimHei']  #解决中文字体显示问题
plt.rc('figure', figsize=(10, 10))            #把plt默认的图片size调大一点
#读入数据
data=pd.DataFrame(pd.read_excel('软微2019成绩.xlsx'))
page=Page()

#print(data.shape)
#print(data.head)



'''
数据清洗，
1.去除无关列
2.去除每一页的头，只留一行列索引
3.去除缺考任何一门的考生
'''
data=data.drop(['政治','外语','报名号'],axis=1)
for i in range(73):
    x=3328-i*38
    data.drop([x],inplace=True)
#print(data.shape)
#print(data.head)
data=data[~data['政治分'].isin(['缺考'])]
data=data[~data['外语分'].isin(['缺考'])]
data=data[~data['科目1分'].isin(['缺考'])]
data=data[~data['科目2分'].isin(['缺考'])]

technology=data[(data['专业名称']=='计算机技术')]
computer=data[(data['专业名称']=='计算机技术')&(data['科目2']=='计算机基础综合')]
#print(technology.shape)
economic=data[(data['专业名称']=='计算机技术')&(data['科目2']=='经济学综合')]
embedded_system=data[(data['专业名称']=='计算机技术')&(data['科目2']=='嵌入式技术基础')]
apply=data[(data['专业名称']=='计算机技术')&(data['科目2']=='计算机应用基础')]

soft=data[(data['专业名称']=='软件工程')]

s1=soft.sort_values('总分',ascending=False)
s1=s1.reset_index(drop=True)

t1=technology.sort_values('总分',ascending=False)
t1=t1.reset_index(drop=True)


c1=computer.sort_values('总分',ascending=False)
c1=c1.reset_index(drop=True)

e1=economic.sort_values('总分',ascending=False)
e1=e1.reset_index(drop=True)

a1=apply.sort_values('总分',ascending=False)
a1=a1.reset_index(drop=True)

e2=embedded_system.sort_values('总分',ascending=False)
e2=e2.reset_index(drop=True)
#print(technology)
#top_ten=technology.loc[:9]
technology_top_ten=t1.iloc[:10,]
computer_top_ten=c1.iloc[:10,]
economic_top_ten=e1.iloc[:10,]
embedded_system_top_ten=e2.iloc[:10,]
apply_top_ten=a1.iloc[:10,]
soft_top_ten=s1.iloc[:10,]
#技术类总的前十名，金融的前十名，以及计算机的前十名等

#统计计算机考生成绩的相关数据
'''

statistics=computer1.describe()
statistics.loc['range']=statistics.loc['max']-statistics.loc['min']   #显示极差
statistics.loc['var']=statistics.loc['std']-statistics.loc['mean']    #显示变异系数
statistics.loc['dis']=statistics.loc['75%']-statistics.loc['25%']     #x显示四分位系数

print(statistics)
'''
#构造新的dataframe
computer1=pd.DataFrame(computer,columns=['政治分','外语分','科目1分','科目2分','总分'])
#print(computer1)
print(computer1.mean())
print(computer1.std())
print(computer1.describe())
print(computer1.max())
print(computer1.min())

soft1=pd.DataFrame(soft,columns=['政治分','外语分','科目1分','科目2分','总分'])
print(soft1.mean())
print(soft1.std())
print(soft1.describe())
print(soft1.max())
print(soft1.min())


'''
数学成绩与专业课成绩的相关性
'''
computer2=pd.DataFrame(computer,columns=['科目1分','科目2分'])
#computer2=computer2.drop_duplicates(subset=['科目2分'])

#print(computer2.shape)

x=computer2['科目1分']
y=computer2['科目2分'].values
#print(computer1)
'''

regr=linear_model.LinearRegression()
regr.fit(x,y)
print('Intercept:{}'.format(regr.intercept_))
print('Coeffecien:{}'.format(regr.coef_))
plt.plot(x,regr.predict(x),linewidth=10,color='blue')
'''
#散点图绘制
plt.scatter(x,y,color='black')
plt.xlabel('专业课成绩')
plt.ylabel('数学成绩')


#考生编号转换列为索引
computer_top_ten.set_index('考生编号')
#print(computer_top_ten)
line1=Line("计算机前十名")
i=computer_top_ten['考生编号']
j=computer_top_ten['总分']
attr1=list(map(str,i))
v=list(j)
line1.add("",attr1,v,is_smooth=True,mark_line=["max","average"])
page.add(line1)



'''
绘制成绩分布直方图
'''
computer.set_index('考生编号')


computer['成绩分段']=pd.cut(computer['总分'],[1,100,200,250,290,310,330,350,370,390,410,430,450],
        labels=['0-99分','100-199分','200-249分','250-289分','290-309分','310-329分','330-349分','350-369分','370-389分','390-409分','410-429分','430-449分'],right=False)


bar1=Bar('计算机总体成绩分布')
score_total = computer['成绩分段'].value_counts().sort_index()

line2 = Line("", width=700)
bar1.add("", score_total.index, score_total.values, bar_category_gap='40%', label_color = ['#130f40'],mark_line=["max","average"])
line2.add("", score_total.index, score_total.values+5, is_smooth=True)

overlap = Overlap(width=700)
overlap.add(bar1)
overlap.add(line2)
page.add(overlap)

'''
单科可能未过线
'''
computer_fail=computer.loc[(computer['政治分']<50)|(computer['外语分']<50)|(computer['科目1分']<90)|(computer['科目2分']<90)]
computer_fail1=computer_fail.loc[computer['总分']>350]
print(computer_fail1)

'''
计算机大概率进复试 差额比1：1.2，150*1.2=180
软工约为57
'''
computer_reexamin=c1.iloc[:180,]
print(computer_reexamin)

soft_reexamin=s1.iloc[:57],
print(soft_reexamin)


page.render("./total.html")





