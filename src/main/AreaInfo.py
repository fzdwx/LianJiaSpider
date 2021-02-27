# - - - - - - - - - - - 
# @author like
# @since 2021-02-22 11:46
# @email 980650920@qq.com
#
class AreaInfo(object):
    # 房子所在区域的名字
    areaName: str
    # 房子的标题
    houseTitle: str
    # 房子所在的街道
    houseAddress: str
    # 小区名字
    community: str
    # 多少平方
    size: str
    # 朝向
    towards: str
    # 户型
    unitType: str
    # 租金
    rent: str
    # 租金单位
    rentUnit: str

    def getInfo(self):
        return \
            self.areaName + "," + self.houseTitle + "," + self.houseAddress + "," + self.community + "," + self.size + "," + self.towards + "," + self.unitType + "," + self.rent + "," + self.rentUnit
