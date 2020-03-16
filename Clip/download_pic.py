# -*- coding: utf-8 -*-
"""
Created on Sat Feb 29 10:28:23 2020

@author: 老肥
@WeChat Official Accounts:老肥码码码
@Wechat: jennnny1216

Happy Python，Happy Life!
"""

import requests
from pymongo import MongoClient
import pandas as pd
import os
from PIL import Image
import math

def download(img_dir):
    
    db=MongoClient().clip
    data=pd.DataFrame(list(db['bilibili'].find()))
    urls=['http:'+i for i in data['pic']]
    for i in range(len(urls)):
        r=requests.get(urls[i])
        with open('{}/{}.jpg'.format(img_dir,i+1),'wb') as f:
            f.write(r.content)


def compose(img_dir):
    
    img_list=[img_dir+img_name for img_name in os.listdir(img_dir)]
    size=3000
    rows=int(math.sqrt(len(img_list)))
    each_size=int(size/rows)
    img=Image.new('RGB',(each_size*rows,each_size*rows))
    x=y=0
    for pic in img_list:
        pic=Image.open(pic)
        pic=pic.resize((each_size,each_size))
        img.paste(pic,(x*each_size,y*each_size))
        x+=1
        if x==rows:
            x=0
            y+=1
    img.save("new.jpg")

if __name__=='__main__':
    img_dir='pic/'
    download(img_dir)
    compose(img_dir)
    