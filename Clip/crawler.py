# -*- coding: utf-8 -*-
"""
Created on Sat Feb 29 09:39:14 2020

@author: 老肥
@WeChat Official Accounts:老肥码码码
@Wechat: jennnny1216

Happy Python，Happy Life!
"""

import requests
from pymongo import MongoClient


db=MongoClient().clip
url='https://api.bilibili.com/x/space/arc/search'
headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'}


for i in range(1,6):
    params={
        'mid': '258150656',
        'ps': '30',
        'tid': '0',
        'pn': i,
        'order': 'pubdate',
        'jsonp': 'jsonp'
    }
    r=requests.get(url,headers=headers,params=params)

    data=r.json()['data']['list']['vlist']
    for vedio in data:
        comment=vedio['comment']
        play=vedio['play']
        description=vedio['description']
        title=vedio['title']
        created=vedio['created']
        length=vedio['length']
        pic=vedio['pic']
        item={
          'comment':comment, 
          'play':play, 
          'description':description, 
          'title':title, 
          'created_time':created, 
          'length':length, 
          'pic':pic
            }
    
        db['bilibili'].insert_one(item)