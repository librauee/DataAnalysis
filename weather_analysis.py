# -*- coding: utf-8 -*-
"""
Created on Tue Sep 17 22:09:59 2019

@author: Administrator
"""

from pymongo import MongoClient
from pandas.io.json import json_normalize
import pandas as pd
import re

from pyecharts import options as opts
from pyecharts.charts import Geo,Line,WordCloud,Pie,Parallel,PictorialBar
from pyecharts.globals import ChartType, SymbolType


"""
从MongoDB读取数据
"""

conn=MongoClient('127.0.0.1', 27017)
db=conn.weather                   
mongo_weather=db.info1

data=mongo_weather.find()
data=json_normalize([ip for ip in data])

"""
数据预处理
"""
data.drop('_id',axis=1, inplace=True)

# str转换成数值，可用max()取出最大值 
data[['最高气温','最低气温']]=data[['最高气温','最低气温']].apply(pd.to_numeric)

def date2string(date):
    date_string=date[:4]+date[5:7]+date[8:10]
    return int(date_string)

data['日期']=data['日期'].apply(date2string)

data=data[data['日期']>20190000]
# print(data)

data.drop_duplicates(subset=['城市','日期'],keep='first',inplace=True)

def get_power(rank):
    
    power_rank=re.findall(r'\d{1,}级',rank)
    if power_rank:
        return int(power_rank[0][:-1])
    else:
        return 0
    
# 全国风最大最小的城市    
data['风力']=data['风力'].apply(get_power)
#wind_power_rank=data.sort_values(by='风力',ascending=False)
#print(wind_power_rank[:10])
#
#city=data.groupby('城市').mean()
#power_top10=city.nlargest(10,'风力')
#weak_top10=city.sort_values(by='风力',ascending=True)[:10]
#print(power_top10)
#print(weak_top10)
#
#words=zip(list(power_top10.index),list(power_top10['风力']))
#words2=zip(list(weak_top10.index),list(weak_top10['风力']))
#
#cloud=(
#       WordCloud()
#       .add("",words,word_size_range=[20,100],shape="diamond")
#       .set_global_opts(title_opts=opts.TitleOpts(title="全国风最大的十个市县",pos_left='center'))
#
#       )
#
#cloud.render('1.html')
#
#
#cloud=(
#       WordCloud()
#       .add("11",words2,word_size_range=[20,100],shape="diamond")
#       .set_global_opts(title_opts=opts.TitleOpts(title="全国最‘风平浪静’的十个市县",pos_left='center'))
#
#       )
#
#cloud.render('2.html')





#print(data[data['最高气温']==max(data['最高气温'])])
##print(data.loc[data['城市']=='北京','最高气温'].max())         
#
#print(data[data['最低气温']==min(data['最低气温'])])
#print(data.sort_values("最高气温",ascending=True))
#print(data.sort_values("最低气温",ascending=True))
#
#

## 风向频率
#direct=data['风向'].value_counts()
#print(direct)
## print(len(set(data['城市'])))
#
## wind_freq=[list(z) for z in zip(list(direct.index),list(direct.values))]
#wind_freq=[['东南风', 201969], ['东北风', 194769], ['西南风', 162898], ['西北风', 143694], ['北风', 15666], ['南风', 12172], ['东风', 4081], ['西风', 3321], ['无持续风向', 1750], ['西南偏南风', 316], ['西南偏西风', 315], ['西北偏西风', 292], ['东南偏东风', 284], ['东北偏东风', 282], ['西北偏北风', 246], ['东北偏北风', 241], ['东南偏南风', 235], ['微风', 133]]
#pie=(
#    Pie()
#    .add("", wind_freq)
#    .set_global_opts(title_opts=opts.TitleOpts(title="风向频数图"),
#                     legend_opts=opts.LegendOpts(is_show=False)
#                     )
#    .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}:{c}"))
#     )
#
#pie.render('wind.html')   

# 全国最热、最冷
#data_nlargest=data.nlargest(10,'最高气温')
#data_nsmallest=data.sort_values(by='最低气温',ascending=True)
#print(data_nsmallest[:10])
#
## 最热城市top10
#hot_top10=city.nlargest(10,'最高气温')
#print(hot_top10)
#cold_top10=city.sort_values(by='最低气温',ascending=True)[:10]
#print(cold_top10)
## 最冷城市top10
#cold_top10_list1=['西藏双湖','称多','聂荣','根河','仲巴','漠河','噶尔','革吉','玛多','多县']
#
## cold_top10_list1=list(cold_top10['城市'])
#cold_top10_list2=list(cold_top10['最低气温'])
#
#
#geo1=(
#        Geo()
#        .add_schema(maptype="china")
#        .add("城市", [list(z) for z in zip(cold_top10_list1,cold_top10_list2)],color="blue")
#        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
#        .set_global_opts(
#            visualmap_opts=opts.VisualMapOpts(is_show=False),
#            title_opts=opts.TitleOpts(title="全国最冷的十座城市"),
#        )
#    )
#
#geo1.render('cold.html')
#
#hot_top10_list1=list(hot_top10.index)
#hot_top10_list1=['云南元江','元阳','景洪','三亚','勐腊','元谋','海口','琼山','秀英','美兰']
#hot_top10_list2=list(hot_top10['最高气温'])
#
#geo2=(
#        Geo()
#        .add_schema(maptype="china")
#        .add("城市", [list(z) for z in zip(hot_top10_list1,hot_top10_list2)],color="red")
#        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
#        .set_global_opts(
#            visualmap_opts=opts.VisualMapOpts(is_show=False),
#            title_opts=opts.TitleOpts(title="全国最热的十座城市"),
#        )
#    )
#        
#geo2.render('hot.html')
beijing=data[data['城市']=='北京']
#shanghai=data[data['城市']=='上海']
shanghai=data[data['城市']=='阿城']
#guangzhou=data[data['城市']=='广州']
#shenzhen=data[data['城市']=='深圳']
#hangzhou=data[data['城市']=='杭州']
#chengdu=data[data['城市']=='成都']

beijing_nlargest=beijing.nlargest(10,'最高气温')

print(beijing_nlargest)

beijing['日期']=beijing['日期'].apply(lambda x:str(x)[4:6])

# 月均温度 可绘折线图
beijing_mean=beijing.groupby('日期').mean()
beijing_high_mean=list(beijing_mean['最高气温'])
beijing_low_mean=list(beijing_mean['最低气温'])
line=(
      Line()
      .add_xaxis(['1月','2月','3月','4月','5月','6月','7月','8月'])
      .add_yaxis("月均最高温度",beijing_high_mean)
      .add_yaxis("月均最低温度",beijing_low_mean)
      .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
      .set_global_opts(title_opts=opts.TitleOpts(title="北京气温"))
)
line.render('beijing.html')

shanghai['日期']=shanghai['日期'].apply(lambda x:str(x)[4:6])
high=list(beijing.mean().values)
high.append('北京')

high_shanghai=list(shanghai.mean().values)
high_shanghai.append('上海')
print(high)
city_data=[]
city_data.append(high)
city_data.append(high_shanghai)
print(city_data)
parallel=(
        Parallel()
        .add_schema(
                [
                opts.ParallelAxisOpts(dim=0, name="平均最低气温"),
                opts.ParallelAxisOpts(dim=1, name="平均最高气温"),
                opts.ParallelAxisOpts(dim=2, name="平均风力"),
                 opts.ParallelAxisOpts(dim=3,
                    name="城市",
                    type_="category",
                    data=["北京", "上海"],
                    )
                ]
                )
        .add("parallel",city_data)
        .set_global_opts(title_opts=opts.TitleOpts(title="Parallel-Category"))
        )   
                
parallel.render('1.html')


location = ["山西", "四川", "西藏", "北京", "上海", "内蒙古", "云南", "黑龙江", "广东", "福建"]
values = [13, 42, 67, 81, 86, 94, 166, 220, 249, 262]




sunny= (
        PictorialBar()
        .add_xaxis(location)
        .add_yaxis(
            "",
            values,
            label_opts=opts.LabelOpts(is_show=False),
            symbol_size=18,
            symbol_repeat="fixed",
            symbol_offset=[0, 0],
            is_symbol_clip=True,
            symbol='image://https://mat1.gtimg.com/pingjs/ext2020/weather/pc/icon/weather/day/00.png'
        )
        .reversal_axis()
        .set_global_opts(
            title_opts=opts.TitleOpts(title="晴天最多的县市"),
            xaxis_opts=opts.AxisOpts(is_show=False),
            yaxis_opts=opts.AxisOpts(
                axistick_opts=opts.AxisTickOpts(is_show=False),
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(opacity=0)
                )
            )
        )
    )
sunny.render('sunny.html')

cloudy=(
        PictorialBar()
        .add_xaxis(location)
        .add_yaxis(
            "",
            values,
            label_opts=opts.LabelOpts(is_show=False),
            symbol_size=18,
            symbol_repeat="fixed",
            symbol_offset=[0, 0],
            is_symbol_clip=True,
            symbol='image:https://mat1.gtimg.com/pingjs/ext2020/weather/pc/icon/weather/day/01.png'
        )
        .reversal_axis()
        .set_global_opts(
            title_opts=opts.TitleOpts(title="多云最多的县市"),
            xaxis_opts=opts.AxisOpts(is_show=False),
            yaxis_opts=opts.AxisOpts(
                axistick_opts=opts.AxisTickOpts(is_show=False),
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(opacity=0)
                )
            )
        )
    )
                
cloudy.render('cloudy.html')                

                
                
overcast=(
        PictorialBar()
        .add_xaxis(location)
        .add_yaxis(
            "",
            values,
            label_opts=opts.LabelOpts(is_show=False),
            symbol_size=18,
            symbol_repeat="fixed",
            symbol_offset=[0, 0],
            is_symbol_clip=True,
            symbol='image:https://mat1.gtimg.com/pingjs/ext2020/weather/pc/icon/weather/day/02.png'
        )
        .reversal_axis()
        .set_global_opts(
            title_opts=opts.TitleOpts(title="阴天最多的县市"),
            xaxis_opts=opts.AxisOpts(is_show=False),
            yaxis_opts=opts.AxisOpts(
                axistick_opts=opts.AxisTickOpts(is_show=False),
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(opacity=0)
                )
            )
        )
    )
                
overcast.render('overcast.html')

rainy=(
        PictorialBar()
        .add_xaxis(location)
        .add_yaxis(
            "",
            values,
            label_opts=opts.LabelOpts(is_show=False),
            symbol_size=18,
            symbol_repeat="fixed",
            symbol_offset=[0, 0],
            is_symbol_clip=True,
            symbol='image://https://mat1.gtimg.com/pingjs/ext2020/weather/pc/icon/weather/day/07.png'
        )
        .reversal_axis()
        .set_global_opts(
            title_opts=opts.TitleOpts(title="小雨最多的县市"),
            xaxis_opts=opts.AxisOpts(is_show=False),
            yaxis_opts=opts.AxisOpts(
                axistick_opts=opts.AxisTickOpts(is_show=False),
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(opacity=0)
                )
            )
        )
    )
                
                
rainy.render()