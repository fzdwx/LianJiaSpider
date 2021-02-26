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


def main():
    # spiderData()
    dataAnalysis()


def dataAnalysis():
    # 读取数据
    csvData = pd.read_csv(FILE_PATH, encoding=FILE_ENCODING)
    # 转换成dataFrame 并去重
    df = pd.DataFrame(csvData).drop_duplicates()

    # 1.使用条形图分析哪种户型的数量最多、最受欢迎
    doAnalysis_houseType(df)
    # todo  统计每个区域的平均租金，并结合柱状图和折线图分析各区域的房源数量和租金情况


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
    plt.title("分析出租房中哪种户型的数量最多", fontproperties=chFont, fontsize=24)
    plt.grid()
    plt.show()

    print("         最多户型:{},共{}户".format(maxCount['户型'], maxCount['数量']))


def spiderData():
    print("开始爬取数据")
    print("*" * 100)
    start = time.time()
    spider = LianJiaSpider()
    # 1.获取租房主页面中的各区域的名字以及跳转url
    startUrl = spider.mainUrl.format('/' + spider.theme)
    page = spider.getPage(startUrl)
    areaInfoListXpath = spider.parse(page, '//ul/li[@data-type="district"]')
    for areaInfo in areaInfoListXpath:
        areaName = areaInfo.xpath('./a/text()')[0]
        areaUrl = spider.mainUrl.format(areaInfo.xpath('./a/@href')[0])

        spider.areaInfoMap[areaUrl] = areaName
        spider.areaNameList.append(areaName)
        spider.areaUrlList.append(areaUrl)

        # 将获取到的url
        spider.urlEnQue(areaUrl)

    # 2.获取各个区域的房源总数
    tList = []
    for i in range(THREAD_COUNT):  # 启动n个线程
        t = Thread(target=spider.parsePageGetAreaCount)
        t.start()
        tList.append(t)
    for t in tList:
        t.join()

    # 3.爬取所有房子具体信息
    for j in range(SPIDER_PAGE_NUM):  # 生成url
        spider.urlEnQue(spider.getListUrl.format(j))
    for i in range(THREAD_COUNT):  # 启动n个线程 开始爬取数据
        t = Thread(target=spider.parsePageGetHouseInfo)
        t.start()
        tList.append(t)
    for t in tList:
        t.join()

    # 读取数据并写入csv文件
    with open(FILE_PATH, 'w', encoding=FILE_ENCODING) as f:
        f.writelines(["区域,", "标题,", "二级区域,", "小区名字,", "朝向,", "户型,", "租金,", "租金单位", "\r\n"])

        for i in spider.areaFullDataList:
            f.writelines(i + "\r\n")

    end = time.time() - start
    # 日志打印
    print("*" * 100)
    print("数据爬取完成:")
    # print("各区域总租房数：{}".format(spider.areaMapHouseCount))
    print("爬取页面数：{}".format(SPIDER_PAGE_NUM))
    print("启动线程数：{}".format(THREAD_COUNT))
    print("共耗时(ms):{}".format(end))
    print("=" * 100)


main()
