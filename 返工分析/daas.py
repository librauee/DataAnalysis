# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 11:55:53 2020

@author: Administrator
"""

import requests
import re
import json
from pymongo import MongoClient



# 数据爬取
db=MongoClient().work
url='https://sp.uidashi.com/app.32615eee.js'
headers={
        'Referer': 'https://rw.uidashi.com/?from=singlemessage',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
}
r=requests.get(url,headers=headers)
r.encoding=r.apparent_encoding

data=re.findall("JSON.parse\('(.*?)'\)",r.text)
city1=json.loads(data[0])['city']
city2=json.loads(data[1])['city']




# 存入MongoDB,方式一
# 用于pyecharts绘图
for city in city1:
    name=city['name']
    values=city['values']
    item={
            'name':name,
            'values':values[-1]
            }
    db['town'].insert_one(item)
for city in city2:
    name=city['name']
    values=city['values']
    item={
            'name':name,
            'values':values[-1]
            }
    db['city'].insert_one(item) 


# 存入MongoDB,方式二
# 存入多行数据用于绘制js动态图
    
for city in city1:
    name=city['name']
    values=city['values']
    periods=city['periods']
    for i in range(len(values)):
        item={
            'type':name[:2],
            'name':name,
            'value':values[i],
            'date':periods[i],
            
            }
        db['town2'].insert_one(item)
for city in city2:
    name=city['name']
    values=city['values']
    periods=city['periods']
    for i in range(len(values)):
        item={
            'type':'中国',
            'name':name,
            'value':values[i],
            'date':periods[i],

            }
        db['city2'].insert_one(item)
  
    
