# - - - - - - - - - - - 
# @author like
# @since 2021-02-21 12:22
# @email 980650920@qq.com
#
import requests
from fake_useragent import UserAgent
from lxml import etree
from queue import Queue
from src.resource.application import mainUrl, pageUrl


class LianJiaSpider(object):
    def __init__(self):
        self.theme = 'zufang'
        # 主路径
        self.mainUrl = mainUrl
        # 请求房子信息列表url
        self.pageUrl = pageUrl
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
        print("开始爬取页面:{}".format(url))
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
            for main in infoMainXpath:
                desInfo = main.xpath('./p[@class="content__list--item--des"]')
                for des in desInfo:
                    title = main.xpath('./p[@class="content__list--item--title"]/a/text()')[0].replace('\n', '').strip()

                    area_name_and_address_community = des.xpath("./a/text()")
                    areaName = area_name_and_address_community[0]
                    address = area_name_and_address_community[1]
                    community = area_name_and_address_community[2]

                    house_size_and_toward_and_house_type = des.xpath('./text()')
                    size = house_size_and_toward_and_house_type[4].replace('\n', '').strip()
                    toward = house_size_and_toward_and_house_type[5].replace('\n', '').strip()
                    house_type = house_size_and_toward_and_house_type[6].replace('\n', '').strip()
                    rent = main.xpath('./span[@class="content__list--item-price"]/em/text()')[0]
                    info = areaName + "," + title + "," + address + "," + community + "," + size + "," + toward + "," + house_type + "," + rent

                    self.areaFullDataList.append(info)
