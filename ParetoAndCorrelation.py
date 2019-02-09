#-*- coding: utf-8 -*-
#菜品盈利数据 绘制帕累托图

import pandas as pd
import matplotlib.pyplot as plt #导入图像库

#初始化参数
dish_profit = 'E:/Analysis/python/demo/data/catering_dish_profit.xls' #餐饮菜品盈利数据
data = pd.read_excel(dish_profit, index_col = u'菜品名')
data=data.sort_values(u'盈利',ascending=False)
#print(data)
data=data[u'盈利'].copy()
#data=data.drop(u'菜品ID',1)
print(data)
plt.rcParams['font.sans-serif'] = ['SimHei'] #用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False #用来正常显示负号

plt.figure()
data.plot(kind='bar')
plt.ylabel(u'盈利（元）')
p = 1.0*data.cumsum()/data.sum()
p.plot(color = 'r', secondary_y = True, style = '-o',linewidth = 2)
plt.annotate(format(p[6], '.4%'), xy = (6, p[6]), xytext=(6*0.9, p[6]*0.9), arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=.2")) #添加注释，即85%处的标记。这里包括了指定箭头样式。
plt.ylabel(u'盈利（比例）')
plt.show()
  
#相关性分析
catering_sale = '../data/catering_sale_all.xls' #餐饮数据，含有其他属性
data1 = pd.read_excel(catering_sale, index_col = u'日期') #读取数据，指定“日期”列为索引列

print(data1.corr()) #相关系数矩阵，即给出了任意两款菜式之间的相关系数
print(data1.corr()[u'百合酱蒸凤爪']) #只显示“百合酱蒸凤爪”与其他菜式的相关系数
print(data1[u'百合酱蒸凤爪'].corr(data1[u'翡翠蒸香茜饺'])) #计算“百合酱蒸凤爪”与“翡翠蒸香茜饺”的相关系数