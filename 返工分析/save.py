# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 17:11:21 2020

@author: Administrator
"""

from pymongo import MongoClient
import pandas as pd


db=MongoClient().work
data=pd.DataFrame(list(db['town2'].find()))
data.drop(columns='_id',inplace=True)
data['date']=data['date'].apply(lambda x:'2020/'+x.replace("月","/").replace("日",""))
data['value']=data['value'].apply(lambda x: x*100)
print(data)
data.to_csv('c.csv',index=0)