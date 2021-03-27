# - - - - - - - - - - - 
# @author like
# @since 2021-02-26 9:39
# @email 980650920@qq.com
#
from threading import Thread
from src.resource.application import *
from src.main.LianJiaSpider import LianJiaSpider
import time
import pandas as pd
from matplotlib import pyplot as plt


# 数据爬取
def spiderData():
    print("开始爬取数据")
    print("*" * 100)
    start = time.time()
    spider = LianJiaSpider()
    tList = []
    # 爬取所有房子具体信息
    for j in range(SPIDER_PAGE_NUM):  # 生成url
        spider.urlEnQue(spider.pageUrl.format(j))
    for i in range(THREAD_COUNT):  # 启动n个线程 开始爬取数据
        t = Thread(target=spider.parsePageGetHouseInfo)
        t.start()
        tList.append(t)
    for t in tList:
        t.join()

    # 读取数据并写入csv文件
    with open(FILE_PATH, 'w', encoding=FILE_ENCODING) as f:
        f.writelines(["区域,", "标题,", "二级区域,", "小区名字,", "大小,", "朝向,", "户型,", "租金" "\r\n"])

        for i in spider.areaFullDataList:
            f.writelines(i + "\r\n")

    end = time.time() - start
    # 日志打印
    print("*" * 100)
    print("数据爬取完成:")
    print("爬取页面数：{}".format(SPIDER_PAGE_NUM))
    print("启动线程数：{}".format(THREAD_COUNT))
    print("共耗时(ms):{}".format(end))
    print("=" * 100)


# 解析数据 画图
def dataAnalysis():
    # 读取数据
    csvData = pd.read_csv(FILE_PATH, encoding=FILE_ENCODING)
    # 转换成dataFrame 并去重
    df = pd.DataFrame(csvData).drop_duplicates()

    # 1.使用条形图分析哪种户型的数量最多、最受欢迎
    doAnalysis_houseType(df)
    # 2.统计每个区域的平均租金，并结合柱状图和折线图分析各区域的房源数量和租金情况
    doAnalysis_areaAvgRent_And_HouseCount(df)
    # 3.统计面积区间的市场占有率，并使用饼图绘制各区间所占比例
    doAnalysis_area_Interval_Ratio_Pie_Chart(df)


# 统计面积区间的市场占有率的饼状图
def doAnalysis_area_Interval_Ratio_Pie_Chart(df):
    # 面积区间数量 Map
    AreaInterval = {
        "0-20㎡": 0,
        "20-40㎡": 0,
        "40-60㎡": 0,
        "60-80㎡": 0,
        "80-100㎡": 0,
        "100-120㎡": 0,
        "120-140㎡": 0,
        "140-160㎡": 0,
        "160-180㎡": 0,
        "180-~㎡": 0,
    }
    grb = df.groupby(by="大小")

    # 获取每个区间的数量并计算占有比例
    for i, j in grb:
        if int(i[:-1]) < 20:
            AreaInterval["0-20㎡"] = AreaInterval["0-20㎡"] + j.shape[0]
        elif 20 <= int(i[:-1]) < 40:
            AreaInterval["20-40㎡"] = AreaInterval["20-40㎡"] + j.shape[0]
        elif 40 <= int(i[:-1]) < 60:
            AreaInterval["40-60㎡"] = AreaInterval["40-60㎡"] + j.shape[0]
        elif 60 <= int(i[:-1]) < 80:
            AreaInterval["60-80㎡"] = AreaInterval["60-80㎡"] + j.shape[0]
        elif 80 <= int(i[:-1]) < 100:
            AreaInterval["80-100㎡"] = AreaInterval["80-100㎡"] + j.shape[0]
        elif 100 <= int(i[:-1]) < 120:
            AreaInterval["100-120㎡"] = AreaInterval["100-120㎡"] + j.shape[0]
        elif 120 <= int(i[:-1]) < 140:
            AreaInterval["120-140㎡"] = AreaInterval["120-140㎡"] + j.shape[0]
        elif 140 <= int(i[:-1]) < 160:
            AreaInterval["140-160㎡"] = AreaInterval["140-160㎡"] + j.shape[0]
        elif 160 <= int(i[:-1]) < 180:
            AreaInterval["160-180㎡"] = AreaInterval["160-180㎡"] + j.shape[0]
        else:
            AreaInterval["180-~㎡"] = AreaInterval["180-~㎡"] + j.shape[0]
    totalSize = df.shape[0]
    for k in AreaInterval:
        AreaInterval[k] = AreaInterval[k] / totalSize

    # 画图
    Pie_Chart = pd.Series(AreaInterval)
    Pie_Chart.name = ''
    # 控制饼图为正圆
    plt.axes(aspect='equal')
    # plot方法对序列进行绘图
    Pie_Chart.plot(kind='pie',  # 选择图形类型
                   autopct='%.1f%%',  # 饼图中添加数值标签
                   radius=1,  # 设置饼图的半径
                   startangle=180,  # 设置饼图的初始角度
                   counterclock=False,  # 将饼图的顺序设置为顺时针方向
                   title='出租房各面积区间的占有率',  # 为饼图添加标题
                   wedgeprops={'linewidth': 1.5, 'edgecolor': 'green'},  # 设置饼图内外边界的属性值
                   textprops={'fontsize': 10, 'color': 'black'}  # 设置文本标签的属性值
                   )
    # 显示图形
    plt.show()


# 1.获取各区域平均租金折线图
# 2.获取各区域房源数量柱状图
def doAnalysis_areaAvgRent_And_HouseCount(df):
    grb = df.groupby(by="区域")
    areaNameList_x = []
    areaAvgRentList_y1 = []
    areaHouseCountList_y2 = []
    for i, j in grb:
        # 当前区域
        areaName = i
        # 当前区域平均租金
        areaAvgRent = j["租金"].mean()
        # 当前区域房源数量
        areaHouseCount = j["租金"].count()

        areaNameList_x.append(areaName)
        areaAvgRentList_y1.append(areaAvgRent)
        areaHouseCountList_y2.append(areaHouseCount)

    # 画图 折线图 -> 区域 == 租金情况
    plt.figure(figsize=(20, 8), dpi=80)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.plot(areaNameList_x, areaAvgRentList_y1, color="cyan")
    plt.title("各区域平均租金折线图", fontsize=24)
    plt.ylabel("平均租金(元/套)", fontsize=16)
    plt.xlabel("区域名字", fontsize=16)
    plt.grid()
    plt.show()

    # 画图 柱状图-> 区域 == 房源数量
    plt.figure(figsize=(20, 8), dpi=80)
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.rcParams['axes.unicode_minus'] = False
    plt.bar(areaNameList_x, areaHouseCountList_y2, width=0.3, color="cyan")
    plt.title("各区域房源数量柱状图", fontsize=24)
    plt.ylabel("房源数量(套)", fontsize=16)
    plt.xlabel("区域名字", fontsize=16)
    plt.grid()
    plt.show()


# 分析出租房中哪种户型的数量最多的柱状图
def doAnalysis_houseType(df):
    gpb_hx = df.groupby(["户型"])
    houseTypeList_x = []
    houseTypeCountList_y = []
    maxCount = {}
    count = 0
    for houseType, df in gpb_hx:
        df__count = df["户型"].count()
        if df__count > count:
            maxCount = {"户型": houseType, "数量": df__count}
            count = df__count
        houseTypeList_x.append(houseType)
        houseTypeCountList_y.append(df__count)

    plt.figure(figsize=(20, 8), dpi=80)
    plt.bar(houseTypeList_x, houseTypeCountList_y, width=0.5, color="cyan")
    plt.xticks(houseTypeList_x, fontproperties=chFont, rotation=45)
    plt.title("分析出租房中哪种户型的数量最多的柱状图", fontproperties=chFont, fontsize=24)
    plt.ylabel("房源个数(套)", fontproperties=chFont, fontsize=16)
    plt.xlabel("户型", fontproperties=chFont, fontsize=16)
    plt.grid()
    plt.show()
