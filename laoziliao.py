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

def header():      # Randomly select header to prevent being banned
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

# Save article content
def saveFile(content, path, filename):
    if not os.path.exists(path):
        os.makedirs(path)
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
    # Enter the start and end dates to crawl news between them
    beginDate = input('Please input start date:')
    endDate = input('Please input end date:')
    destdir = input("Please input where you want to save result：")
    data = get_date_list(beginDate, endDate)

    for d in data:
        year = str(d.year)
        month = str(d.month) if d.month >= 10 else '0' + str(d.month)
        day = str(d.day) if d.day >= 10 else '0' + str(d.day)
        destdir = destdir

        dataurl = 'https://www.laoziliao.net/rmrb/' + year + '-' + month + '-' + day
        for link1 in fetchUrl(dataurl):
            content = gethtml(link1)
            path = destdir + '/' + year + 'year' + '/' + year + 'year' + month + 'month' + '/' + year + month + day + '/'
            n = link1.split('-')[3].split('#')[0]
            filename = year + month + day + '-' + n + '.txt'
            saveFile(content, path, filename)
#            time.sleep(2)
        print('Finish' + year + month + day)
        time.sleep(3)    
    print('All finished')
