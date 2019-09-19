# Data Analysis

* Language:Python3
* 一些数据分析的学习实例和自己的数据分析实战汇总
* 我的微信公众号如下，欢迎学习交流

![Wechat](https://github.com/librauee/Reptile/blob/master/image/vx_code.jpg)

## No.1 英文名分析

* 数据来源：美国1880年到2017年的新生婴儿取名记录

### Q1:
从2010年到2017年之间最受欢迎的男女生英文名，画出男女生各前10名的年份-数量图，并生成词云

![pic](https://github.com/librauee/DataAnalysis/blob/master/%E8%8B%B1%E6%96%87%E5%90%8D%E5%88%86%E6%9E%90/2010%E5%B9%B4%E4%BB%A5%E6%9D%A5%E6%9C%80%E5%8F%97%E6%AC%A2%E8%BF%8E%E7%9A%84%E5%A5%B3%E7%94%9F%E5%90%8DTop10.png)
### Q2：
1920年以来每个年代最流行的英文名

### Q3:
以前很流行，现在不流行的英文名,用pyecharts画出折线图，反映出英文名走势
![pic](https://github.com/librauee/DataAnalysis/blob/master/%E8%8B%B1%E6%96%87%E5%90%8D%E5%88%86%E6%9E%90/%E5%A5%B3%E7%94%9F%E5%A7%93%E5%90%8D%E8%B5%B0%E5%8A%BF%E5%9B%BE.png)
### Q4:
二十一世纪以来越来越流行的英文名字,绘制出折线图，体现变化趋势

### Q5:
影响美国人取名的因素：体育明星、电视明星，选取了一系列名人，绘制折线与柱状图
![pic](https://github.com/librauee/DataAnalysis/blob/master/%E8%8B%B1%E6%96%87%E5%90%8D%E5%88%86%E6%9E%90/%E5%90%8D%E4%BA%BA%E5%90%8D%E5%AD%97%E7%9A%84%E5%BD%B1%E5%93%8D.png)
### Q6:
同一发音的名字，有很多不同的拼写变体,生成词云
![pic](https://github.com/librauee/DataAnalysis/blob/master/%E8%8B%B1%E6%96%87%E5%90%8D%E5%88%86%E6%9E%90/%E5%87%AF%E6%96%AF.png)
### Q7：
一些有特殊含义的名字是否有人取

### Q8：
名字里面带有部分回文的名字有哪些，生成词云

### Tips

* 以pyecharts库中的page自定义渲染多张数量的图片，以html的形式展示
* 目前pyecharts库已更新至新的大版本 V1 
* 本代码只能在pyecharts V0.5版本下运行 

