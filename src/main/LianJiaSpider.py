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
from threading import activeCount


class LianJiaSpider(object):
    def __init__(self):
        self.theme = 'zufang'
        # 主路径
        self.mainUrl = 'https://wh.lianjia.com{}'
        # 保存各个地区的名称
        self.areaNameList = []
        # 保存各个地区的url地址
        self.areaUrlList = []
        # 保存url : name
        self.areaInfoMap = {}
        self.queue = Queue()

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

    def parsePageGetAreaCount(self):
        if self.queue.empty():
            return
        reqUrl = self.queue.get()
        page = self.getPage(reqUrl)
        areaCount = self.parse(page, '//span[@class="content__title--hl"]/text()')
        areaName = self.areaInfoMap.get(reqUrl)

        self.areaMapHouseCount[areaName] = areaCount

    def main(self):
        # 1.获取租房主页面中的各区域的名字以及跳转url
        startUrl = self.mainUrl.format('/' + self.theme)
        page = self.getPage(startUrl)
        areaInfoListXpath = self.parse(page, '//ul/li[@data-type="district"]')
        for areaInfo in areaInfoListXpath:
            areaName = areaInfo.xpath('./a/text()')[0]
            areaUrl = self.mainUrl.format(areaInfo.xpath('./a/@href')[0])

            self.areaInfoMap[areaUrl] = areaName
            self.areaNameList.append(areaName)
            self.areaUrlList.append(areaUrl)

            # 2.将获取到的url
            self.urlEnQue(areaUrl)


        tList = []
        while not self.queue.empty():  # 启动n个线程
            t = Thread(target=self.parsePageGetAreaCount)
            t.start()
            tList.append(t)

        for t in tList:
            t.join()

        print(self.areaMapHouseCount)


if __name__ == '__main__':
    s = LianJiaSpider()
    s.main()
