# -*- coding: utf-8 -*-
"""
Created on Tue Jan 14 19:14:18 2020

@author: Lee
"""


from pyecharts import options as opts
from pyecharts.charts import Geo,Line,WordCloud,Pie,Parallel,PictorialBar,Bar,Polar,Grid,Map
from pyecharts.globals import ChartType, SymbolType


x_data = ['2012年','2013年','2014年','2015年','2016年','2017年','2018年','2019年(预测)']
bar = (
        Bar()
        .add_xaxis(x_data)
        .add_yaxis(
            "金额(亿元)",
            [0.3, 4.6, 12.9, 21.2, 29.1, 79.0,399.4, 250.0],
            yaxis_index=0,
            color="#6853BE",
            
        )
        .extend_axis(
            yaxis=opts.AxisOpts(
                type_="value",
                name="数量",
                min_=0,
                max_=800,
                position="right",
                axisline_opts=opts.AxisLineOpts(
                    linestyle_opts=opts.LineStyleOpts(color="#675bba")
                ),
                axislabel_opts=opts.LabelOpts(formatter="{value}"),
                splitline_opts=opts.SplitLineOpts(
                    is_show=False, linestyle_opts=opts.LineStyleOpts(opacity=0)
                ),
            )
        )
        .set_global_opts(
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-15)),   
            title_opts=opts.TitleOpts(title="全球区块链项目融资数量和金额"),
            tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
        )
    )

line = (
        Line()
        .add_xaxis(x_data)
        .add_yaxis(
            "数量（笔数）",
            [0.1*2, 2.8*2, 20*2, 16.5*2, 42*2, 81.8*2,301*2,547],
            yaxis_index=1,
            color="#5793f3",
            label_opts=opts.LabelOpts(is_show=False),
        )
    )

bar.overlap(line)
bar.render()
bar = (
        Bar()
        .add_xaxis(['中国','美国','新加坡','英国','日本','加拿大','印度','韩国','瑞士','德国'])
        .add_yaxis("融资数量", [647,339,92,75,27,20,20,19,16,13])
        .add_yaxis("公开融资总额（亿元）", [255.0,297.2,17.5,38.8,11.7,10.7,3.6,9.5,27.5,2.2])
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        .set_global_opts(title_opts=opts.TitleOpts(title="各国区块链项目融资排行榜Top10"))
    )




bar = (
      Bar()
      .add_xaxis(['2009年','2010年','2011年','2012年','2013年','2014年','2015年','2016年','2017年','2018年','2019年'])
      .add_yaxis("", [175, 127, 178, 156, 169, 339,741, 2250,5126,11256,4765],
            yaxis_index=0,
            color="#D6AF66"
            )
      .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
      .set_global_opts(title_opts=opts.TitleOpts(title="2009-2019年10月全球区块链专利申请情况（单位：条）"))
)

bar.render()


pie = (
       Pie()
       .add("", [list(z) for z in zip(['中国','美国','其他'], [3256,1077,432])])
       .set_global_opts(title_opts=opts.TitleOpts(title="2019年前10个月各国区块链专利申请情况"))
       .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
       
       
       )
pie.render()

bar = (
      Bar()
      .add_xaxis(['金融','零售及电子商务','农业','房地产及基建工程','物流'][::-1])
      .add_yaxis("", [3433, 1562, 468, 435, 79][::-1],
            yaxis_index=0,
            color="#295099"
            )
      .reversal_axis()
      .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
      .set_global_opts(title_opts=opts.TitleOpts(title="区块链专利行业分布情况（单位：条）"))
)

bar.render()
Provinces=['新疆','西藏','青海','内蒙古','宁夏','甘肃','四川','云南','陕西','重庆','贵州','广西','山西','河南','湖北','湖南','广东','海南','北京','天津','河北','山东','江苏','安徽','浙江','江西','福建','黑龙江','吉林','辽宁']
Values=['89','11','20','120','30','61','375','150','716','502','368','322','78','302','372','885','18922','988','366','361','375','1196','647','977','1826','157','339','83','157','290']


map1 = (
        Map()
        .add("", [list(z) for z in zip(Provinces,Values)], "china")

        .set_global_opts(
            legend_opts=opts.LegendOpts(is_show=False),
            title_opts=opts.TitleOpts(title="全国区块链企业的地域分布情况"),
            visualmap_opts=opts.VisualMapOpts(max_=1000,is_show=False),
        )
    )

map1.render()

bar = (
      Bar()
      .add_xaxis(['广东省','北京市','浙江省','上海市','江苏省','四川省','福建省','山东省','湖北省','安徽省'])
      .add_yaxis("", [3732, 3069, 1023, 838, 515, 406,282, 273,225,192],
            yaxis_index=0,
            color="#295099"
            )
      .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
      .set_global_opts(title_opts=opts.TitleOpts(title="全国区块链专利申请量前十省市（单位：条）"))
)

bar.render()
