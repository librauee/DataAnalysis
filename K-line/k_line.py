# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 10:16:57 2020

@author: 老肥
@WeChat Official Accounts:老肥码码码
@Wechat: jennnny1216

Happy Python，Happy Life!
"""

from matplotlib import pyplot as plt
from mpl_finance import candlestick_ohlc
from matplotlib.pylab import date2num
import datetime
import random

"""
matplotlib绘制
"""

start="2020-1-1"
data=[]

# 开，最高，最低，收

for i in range(31):    
    random_data=[random.randint(2000,2500) for _ in range(4)]
    sorted_data=sorted(random_data)
    day=date2num(datetime.datetime.strptime(start,'%Y-%m-%d'))
    print(day)
    if i==0:
        one=(day,sorted_data[1],sorted_data[3],sorted_data[0],sorted_data[2]) if random.random()>0.5 else (day,sorted_data[2],sorted_data[3],sorted_data[0],sorted_data[1])
        
    else:
        one=(day+i,sorted_data[1],sorted_data[3],sorted_data[0],sorted_data[2]) if random.random()>0.5 else (day+i,sorted_data[2],sorted_data[3],sorted_data[0],sorted_data[1])
    data.append(one)

print(data)

fig,ax=plt.subplots(facecolor="white",figsize=(12,8))
fig.subplots_adjust(bottom=0.1)
ax.xaxis_date()
plt.xticks(rotation=30)
plt.title('K-line')
plt.xlabel('time')
plt.ylabel('price')
candlestick_ohlc(ax,data,width=0.5,colorup='r',colordown='green') # 上涨为红色K线，下跌为绿色，K线宽度为0.7
plt.grid(True)
