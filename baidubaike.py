# -*- coding:utf-8 -*-
# 爬取百度百科中电视剧词条的分集剧情简介
# 默认唐顿庄园
import requests
from bs4 import BeautifulSoup

url = 'https://baike.baidu.com/item/%E5%94%90%E9%A1%BF%E5%BA%84%E5%9B%AD/4562295'
# 构造post数据
data = {}
headers = {'User-Agent': 'Mozilla/5.0 '
                         '(Windows NT 10.0; Win64; x64) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/55.0.2883.87 Safari/537.36'}
r = requests.post(url, data, headers=headers)
page = r.text

r = requests.post(url, data=data, headers=headers)
r.encoding = 'utf-8'
page = r.text
# print(page)

soup = BeautifulSoup(page, "html.parser")
result = soup.find('ul', attrs={'class': 'dramaSerialList'}).find_all('dl')
# print(len(result))
# print(result)

for item in result:
    totalLength = len(item.find_all('dt'))
    for i in range(0, totalLength):
        # .string 属性来提取标签里的内容时，该标签应该是只有单个节点的
        print(item.find_all('dt')[i].string)
        # .get_text()会得到该节点的所有文本，包括子节点的
        print(item.find_all('dd')[i].get_text())



