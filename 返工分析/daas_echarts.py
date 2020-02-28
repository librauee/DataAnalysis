# -*- coding: utf-8 -*-
"""
Created on Fri Feb 28 17:05:23 2020

@author: Administrator
"""

from pyecharts import options as opts
from pyecharts.charts import Geo,Line,Bar
from pymongo import MongoClient
import pandas as pd


db=MongoClient().work
data=pd.DataFrame(list(db['city'].find()))
data['values']=data['values'].apply(lambda x: x*100)


city=list(data['name'])
value=list(data['values'])


c = (
        Geo()
        .add_schema(maptype="china")
        .add("", [list(z) for z in zip(city, value)])
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(
            visualmap_opts=opts.VisualMapOpts(),
            title_opts=opts.TitleOpts(title="主要城市商办区人口活跃度"),
        )
    )
c.render('geo.html')


country_data=[0.215,0.2256,0.256,0.2679,0.2686,0.2821,0.2966,0.3079,0.3132,0.3665,0.3743,0.3783,0.3909,0.388,0.4024,0.4144,0.4946,0.4974,0.5027,0.5135,0.5242]
date_range=["2月8日","2月9日","2月10日","2月11日","2月12日","2月13日","2月14日","2月15日","2月16日","2月17日","2月18日","2月19日","2月20日","2月21日","2月22日","2月23日","2月24日","2月25日","2月26日","2月27日","2月28日"]
line=(
        Line()
        .add_xaxis(date_range)
        .add_yaxis("", country_data)
        .set_global_opts(title_opts=opts.TitleOpts(title="全国复工趋势之商办区人口活跃度"))
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    )
line.render('country.html')

bar=(
        Bar()
        .add_xaxis(city[:10])
        .add_yaxis("", value[:10])
        .set_global_opts(title_opts=opts.TitleOpts(title="商办区人口活跃度排名"))
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    )

bar.render('top.html')

country_data=[0.397,0.4387,0.481,0.5159,0.5514,0.583,0.6629,0.6708,0.6835,0.6944]
date_range=["2月19日","2月20日","2月21日","2月22日","2月23日","2月24日","2月25日","2月26日","2月27日","2月28日"]

line=(
        Line()
        .add_xaxis(date_range)
        .add_yaxis("", country_data)
        .set_global_opts(title_opts=opts.TitleOpts(title="全国复工趋势之务工人员返工率"))
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    )
line.render('country.html')