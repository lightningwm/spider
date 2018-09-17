import requests
from bs4 import BeautifulSoup
import csv
import re
from apscheduler.schedulers.blocking import BlockingScheduler
import datetime


def getHTMLText(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        r.encoding = 'gb2312'
        return r.text
    except:
        return ""


def parsePage(html, plst):
    try:
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find(name='table')
        goldList = table.find_all(name='tr')
        # 获取表格数据
        for gold in goldList:
            try:
                price = gold.find_all(name='td')
                if len(price) == 0:
                    continue
                temp = []
                for p in price:
                    temp.append(p.text)
                plst.append(temp)
            except:
                continue
    except:
        print("Error!")


def parsePageGold(html, plst):
    try:
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find(name='table')
        goldList = table.find_all(name='tr')[1]
        # 获取表格数据
        for gold in goldList:
            try:
                price = gold.find_all(name='td')
                if len(price) == 0:
                    continue
                temp = []
                for p in price:
                    temp.append(p.text)
                plst.append(temp)
            except:
                continue
    except:
        print("Error!")


def parsePageSilver(html, plst):
    try:
        soup = BeautifulSoup(html, 'html.parser')
        table = soup.find(name='table')
        goldList = table.find_all(name='tr')
        # 获取表格数据
        for gold in goldList:
            try:
                price = gold.find_all(name='td')
                temp = []
                for i, p in enumerate(price):
                    temp.append(p.text)
                plst.append(temp)
            except:
                continue
    except:
        print("Error!")


def printPriceListCSV(plst, header, file_name):
    with open(file_name, 'a', errors='ignore', newline='') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(header)
        f_csv.writerows(plst)


def item_sh(url, file_name):
    # 上海黄金
    priceList = []
    html = getHTMLText(url)
    html = re.sub(r'</font>', '', html)
    parsePage(html, priceList)
    header = '上海黄金交易所行情'
    printPriceListCSV(priceList, header, file_name)


def item_gold(url, header, file_name):
    # 黄金现货
    priceList = []
    html = getHTMLText(url)
    parsePageGold(html, priceList)
    printPriceListCSV(priceList, header, file_name)


def item_silver(url, header, file_name):
    # 银和贵金属
    priceList = []
    html = getHTMLText(url)
    parsePageSilver(html, priceList)
    printPriceListCSV(priceList, header, file_name)


def main():
    # 初始化文件
    file_name = 'data.csv'
    open(file_name, 'w').close()
    urlBase = 'http://www.kitco.cn/KitcoDynamicSite/RequestHandler?requestName=getFileContent&AttributeId='

    url_sh = urlBase + 'ShangHaiPrices'
    item_sh(url_sh, file_name)

    url_GoldSpotPrice = urlBase + 'GoldSpotPrice'
    header = '黄金现货'
    item_gold(url_GoldSpotPrice, header, file_name)

    url_siliverPrice = urlBase + 'SilverPGMPricesCNY'
    header = '银及铂族金属'
    item_silver(url_siliverPrice, header, file_name)
    print(datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3])


if __name__ == '__main__':
    main()
    # 定时更新
    scheduler = BlockingScheduler()
    scheduler.add_job(main, 'interval', minutes=3)
    scheduler.start()
