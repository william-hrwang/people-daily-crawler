import requests
import os
import datetime
import time
from lxml import etree
import random

def gen_dates(b_date, days):
    day = datetime.timedelta(days = 1)
    for i in range(days):
        yield b_date + day * i


def get_date_list(beginDate, endDate):

    start = datetime.datetime.strptime(beginDate, "%Y%m%d")
    end = datetime.datetime.strptime(endDate, "%Y%m%d")

    data = []
    for d in gen_dates(start, (end-start).days):
        data.append(d)

    return data

def header():      # 随机选择header防止被禁
    headers_list = [
        'Mozilla/5.0(Macintosh;U;IntelMacOSX10_6_8;en-us)AppleWebKit/534.50(KHTML,likeGecko)Version/5.1Safari/534.50',
        'Opera/9.80(WindowsNT6.1;U;en)Presto/2.8.131Version/11.11',
        'Mozilla/5.0(Windows;U;WindowsNT6.1;en-us)AppleWebKit/534.50(KHTML,likeGecko)Version/5.1Safari/534.50',
        'Mozilla/5.0(Macintosh;IntelMacOSX10_7_0)AppleWebKit/535.11(KHTML,likeGecko)Chrome/17.0.963.56Safari/535.11',
        'Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;Trident/4.0;SE2.XMetaSr1.0;SE2.XMetaSr1.0;.NETCLR2.0.50727;SE2.XMetaSr1.0)',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36',
        'Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;360SE)',
        'Mozilla/4.0(compatible;MSIE7.0;WindowsNT5.1;Maxthon2.0)',
        'Opera/9.80(Macintosh;IntelMacOSX10.6.8;U;en)Presto/2.8.131Version/11.11',
    ]
    header1 = random.choice(headers_list)
    headers = {"User-Agent": header1}
    return  headers

# 保存文章内容
def saveFile(content, path, filename):
    # 如果没有该文件夹，则自动生成
    if not os.path.exists(path):
        os.makedirs(path)
    # 保存文件
    with open(path + filename, 'w', encoding='utf-8') as f:
        f.write(content)

def fetchUrl(dataurl):

    headers = header()
    r = requests.get(dataurl,headers=headers)
    text = r.text
    html = etree.HTML(text)
    ul = html.xpath('//ul')[0]
    lis = ul.xpath("//li[1]/a/@href")
    lis.remove('/')
    return lis


def gethtml(link1):
    headers = header()
    r = requests.get(link1, headers=headers)
    text = r.text
    html = etree.HTML(text)
    plist1 = html.xpath("//*[@class='article']/descendant-or-self::text()")
    content1 = ''
    for plist in plist1:
        content1 += plist
    return content1


if __name__ == '__main__':
    # 输入起止日期，爬取之间的新闻
    beginDate = input('请输入开始日期:')
    endDate = input('请输入结束日期:')
    destdir = input("请输入数据保存的地址：")
    data = get_date_list(beginDate, endDate)

    for d in data:
        year = str(d.year)
        month = str(d.month) if d.month >= 10 else '0' + str(d.month)
        day = str(d.day) if d.day >= 10 else '0' + str(d.day)
        destdir = destdir                                                     # 爬下来的文件的存储地方

        dataurl = 'https://www.laoziliao.net/rmrb/' + year + '-' + month + '-' + day
        for link1 in fetchUrl(dataurl):           #每一个版面的链接
            content = gethtml(link1)
            path = destdir + '/' + year + '年' + '/' + year + '年' + month + '月' + '/' + year + month + day + '/'
            n = link1.split('-')[3].split('#')[0]
            filename = year + month + day + '-' + n + '.txt'
            saveFile(content, path, filename)
#            time.sleep(2)
        print('爬取完成' + year + month + day)
        time.sleep(3)    
    print('全部爬取完成')
