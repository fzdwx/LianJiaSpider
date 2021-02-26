# - - - - - - - - - - - 
# @author like
# @since 2021-02-26 9:39
# @email 980650920@qq.com
#
from threading import Thread
from src.resource.application import *

from src.main.LianJiaSpider import LianJiaSpider


def main():
    spiderData()

    # todo 进行数据分析 pandas


def spiderData():
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
    n = 0
    with open(FILE_PATH, 'w', encoding='gbk') as f:
        f.writelines(["区域,", "标题,", "二级区域,", "小区名字,", "朝向,", "户型,", "租金,", "租金单位", "\r\n"])

        for i in spider.areaFullDataList:
            f.writelines(i + "\r\n")
            n = n + 1
    print("各区域总租房数：{}".format(spider.areaMapHouseCount))
    print("爬取页面数：{}".format(SPIDER_PAGE_NUM))
    print("启动线程数：{}".format(THREAD_COUNT))
    print("总数据条数:{}".format(n))


main()
