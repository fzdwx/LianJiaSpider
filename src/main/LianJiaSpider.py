# - - - - - - - - - - - 
# @author like
# @since 2021-02-21 12:22
# @email 980650920@qq.com
#
import requests
from fake_useragent import UserAgent
from lxml import etree
from queue import Queue
from threading import Thread
from src.main.AreaInfo import *
import csv
import codecs


class LianJiaSpider(object):
    def __init__(self):
        self.theme = 'zufang'
        # 主路径
        self.mainUrl = 'https://wh.lianjia.com{}'
        # 请求房子信息列表url
        self.getListUrl = 'https://wh.lianjia.com/zufang/pg{}/#contentList'
        # 保存各个地区的名称
        self.areaNameList = []
        # 保存各个地区的url地址
        self.areaUrlList = []
        # 保存url : name
        self.areaInfoMap = {}
        self.queue = Queue()

        self.areaFullDataList = []
        # 1、统计每个区域的房源总数量 areaName : count
        self.areaMapHouseCount = {}

    # 随机获取user-agent
    def genUserAgent(self):
        return {"User-Agent": UserAgent().random}

    # 发送请求返回页面
    def getPage(self, url):
        req = requests.get(url=url, headers=self.genUserAgent())
        return req.text

    # 解析页面
    # page : 页面
    # reg : xpath 表达式
    def parse(self, page, reg):
        p = etree.HTML(page)
        return p.xpath(reg)

    def urlEnQue(self, url):
        self.queue.put(url)

    # 获取每个区域的房子数量
    def parsePageGetAreaCount(self):
        while not self.queue.empty():
            if self.queue.empty():
                break
            reqUrl = self.queue.get()
            page = self.getPage(reqUrl)
            areaCount = self.parse(page, '//span[@class="content__title--hl"]/text()')
            areaName = self.areaInfoMap.get(reqUrl)

            self.areaMapHouseCount[areaName] = areaCount

    # 获取单个房源的具体信息并保存到list中
    def parsePageGetHouseInfo(self):
        while not self.queue.empty():
            if self.queue.empty():
                break
            url = self.queue.get()
            page = self.getPage(url)

            # 进行数据解析
            infoMainXpath = self.parse(page, '//div[@class="content__list--item--main"]')
            for info in infoMainXpath:
                desInfo = info.xpath('./p[@class="content__list--item--des"]')
                houseTitle = info.xpath('./p[@class="content__list--item--title"]/a/text()')[0]
                areaName = None
                houseAddress = None
                community = None
                size = None
                towards = None
                unitType = None
                for title in desInfo:
                    x1 = title.xpath('./a/text()')
                    areaName = x1[0]
                    houseAddress = x1[1]
                    community = x1[2]
                    x2 = title.xpath('./text()')
                    size = x2[5]
                    towards = x2[6]
                    unitType = x2[7]

                rentUnit = info.xpath('./span[@class="content__list--item-price"]/text()')
                rent = info.xpath('./span[@class="content__list--item-price"]/em/text()')

                # 封装成对象
                area_info = AreaInfo()
                area_info.areaName = areaName
                area_info.houseTitle = houseTitle.replace('\n', '').strip()
                area_info.houseAddress = houseAddress
                area_info.community = community
                area_info.size = size.strip()
                area_info.towards = towards.replace('\n', '').strip()
                area_info.unitType = unitType.replace('\n', '').strip()
                area_info.rent = rent[0]
                area_info.rentUnit = rentUnit[0]
                # 保存到list中
                self.areaFullDataList.append(area_info.getInfo())
                # print(area_info.getInfo())
