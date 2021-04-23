# - - - - - - - - - - - 
# @author like
# @since 2021-03-27 14:42
# @email 980650920@qq.com
#
from src.main.Start import spiderData, dataAnalysis

if __name__ == '__main__':
    while True:
        read = input("请输入要爬取的城市例如[武汉]->[wh]")
        if (read == "exit"):
            break
        spiderData(read)
        dataAnalysis()
