# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 13:08:59 2019

@author: Lee
"""

from pymongo import MongoClient
import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Geo,Line,WordCloud,Pie,Parallel,PictorialBar,Bar,Polar
from pyecharts.globals import ChartType, SymbolType

pd.set_option('display.max_rows', None)
db=MongoClient().ranking
data=pd.DataFrame(list(db['subject'].find()))

"""
上榜学科最多的十所高校
"""
#all_subject=data['school'].value_counts()[:10]
#
#school_top10=list(all_subject.index)
#number=[int(j) for j in all_subject.values]
#
#bar1=(
#        Bar()
#        .add_xaxis(school_top10[::-1])
#        .add_yaxis("", number[::-1], category_gap="50%")
#        .reversal_axis()
#        .set_global_opts(title_opts=opts.TitleOpts(title="上榜学科最多的十所高校"))
#    )
#bar1.render('上榜学科最多的学校.html')


"""
排名前10%学科最多的十所高校
"""

#def correct(percent):
#    percent=percent[1:-1]
#    return int(percent)
#
#data['percent']=data['percent'].apply(correct)
#
#percent_top=data[data['percent']<=10]
#percent_top_count=percent_top.groupby('school').count()['ranking']
#percent_top_count=percent_top_count.sort_values(ascending=False)
#number2=list(percent_top_count.values)[:10]
#
#pie1=(
#      Pie()
#        .add(
#            "",
#            [list(z) for z in zip(list(percent_top_count.index)[:10], [int(i) for i in number2])],
#            radius=["20%", "75%"],
#
#            label_opts=opts.LabelOpts(formatter="{b}: {c}"),
#        )
#
#        .set_global_opts(title_opts=opts.TitleOpts(title="排名前10%学科最多的十所高校"),
#                         legend_opts=opts.LegendOpts(is_show=False))
#      )
#
#pie1.render('排名前10%学科最多的高校.html')


"""
全国排名第一的学科最多的十所高校
"""
ranking_top=data[data['ranking']=='1']
ranking_top_count=ranking_top.groupby('school').count()['ranking']
ranking_top_count=ranking_top_count.sort_values(ascending=False)
print(ranking_top_count)
#
#words=zip(list(ranking_top_count.index)[:21],[int(i) for i in ranking_top_count.values][:21])
#wc=(
#        WordCloud()
#        .add("", words, word_size_range=[20, 100])
#        .set_global_opts(title_opts=opts.TitleOpts(title="全国排名第一的学科最多的高校"))
#    )
#wc.render('全国排名第一的学科最多的高校.html')


"""
重点关注计算机与软件的学科排名
"""

def replace(school):
    if school=='国防科技大学':
        return '国防科学技术大学'
    else:
        return school


data2018=pd.DataFrame(list(db['subject2018'].find()))
data2017=pd.DataFrame(list(db['subject2017'].find()))
cs2019=data[data['subject']=='计算机科学与技术']
cs2019['year']=2019
cs2018=data2018[data2018['subject']=='计算机科学与技术']
cs2018['year']=2018
cs2017=data2017[data2017['subject']=='计算机科学与技术']
cs2017['year']=2017

cs_total=pd.concat([cs2019,cs2018,cs2017])

cs_total[['ranking','score']]=cs_total[['ranking','score']].apply(pd.to_numeric)
cs_total['school']=cs_total['school'].apply(replace)
#print(cs_total)
mean_ranking=cs_total.groupby('school').mean()
mean_ranking=mean_ranking.sort_values(by='ranking')
top_school=list(mean_ranking.index)[:10]
score_2017=[]
score_2018=[]
score_2019=[]
rank_2017=[]
rank_2018=[]
rank_2019=[]
ranking=[]
for school in top_school:
    school_data=cs_total[cs_total['school']==school]
    ranking.append(list(school_data['ranking']))
    score_2019.append(int(school_data[school_data['year']==2019]['score']))
    score_2018.append(int(school_data[school_data['year']==2018]['score']))
    score_2017.append(int(school_data[school_data['year']==2017]['score']))
    rank_2019.append(int(school_data[school_data['year']==2019]['ranking']))
    rank_2018.append(int(school_data[school_data['year']==2018]['ranking']))
    rank_2017.append(int(school_data[school_data['year']==2017]['ranking']))
print(ranking)
bar2=(
        Bar()
        .add_xaxis(top_school)
        .add_yaxis("2017年", score_2017, category_gap="20%")
        .add_yaxis("2018年", score_2018, category_gap="20%")
        .add_yaxis("2019年", score_2019, category_gap="20%")
        .set_global_opts(title_opts=opts.TitleOpts(title="计算机强校的三年分数变化情况"),
                         xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-30,font_weight='bold')))
    )
bar2.render('计算机强校的三年分数变化情况.html')



polar=(
       Polar()
       .add_schema(
            radiusaxis_opts=opts.RadiusAxisOpts(data=[2019,2018,2017], type_="category")
        )
       .add("清华大学",ranking[0], type_="bar", stack="stack0")
       .add("浙江大学", ranking[1], type_="bar", stack="stack0")
       .add("北京大学", ranking[2], type_="bar", stack="stack0")
       .add("华中科技大学", ranking[3], type_="bar", stack="stack0")
       .add("国防科技大学", ranking[4], type_="bar", stack="stack0")
       .add("上海交通大学", ranking[5], type_="bar", stack="stack0")
       .add("哈尔滨工业大学", ranking[6], type_="bar", stack="stack0")
       .add("北京航空航天大学", ranking[7], type_="bar", stack="stack0")
       .add("西安电子科技大学", ranking[8], type_="bar", stack="stack0")
       .add("电子科技大学", ranking[9], type_="bar", stack="stack0")
       .set_global_opts(title_opts=opts.TitleOpts(title="最近三年计算机科学与技术高校排名变化情况",subtitle="从外圈到内圈依次为2017，2018，2019"),
                        legend_opts=opts.LegendOpts(
                        pos_left="80%", orient="vertical"
            ))
        )
       
       
polar.render('最近三年计算机科学与技术高校排名.html')  



 
year=cs_total.groupby('school').count()['year']
year3=year[year>2]
percent=len(year3)/len(year)
print(percent)
# 0.7409638554216867
print(year[year==1])

# 河北工业大学,常州大学,河南科技大学,烟台大学 第一次进入计算机学科的榜单
