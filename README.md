# LianJiaSpider
python爬虫-毕业设计

## 主要内容
1、统计每个区域的房源总数量

2、使用条形图分析哪种户型的数量最多、最受欢迎

3、统计每个区域的平均租金，并结合柱状图和折线图分析各区域的房源数量和租金情况

4、统计面积区间的时长占有率，并使用饼图绘制各区间所占比例


## 主要设计方法或技术路线
1、数据来源：选择一个合适的租房平台通过爬虫技术获取房源信息

2、数据读取：使用Pandas将数据读取保存在csv文件的数据，将其转换成DataFrame对象展示

3、数据预处理：在使用数据前对这些数据进行一系列的检测与处理，包括处理重复值和缺失值、统一数据类型等

4、图表分析：设计合适的图表完成要求的各项数据统计


# 使用方法：
1、 src/resource/application.py 配置爬取多少页面、启动线程数量、csv文件保存地址

2、 运行start.py