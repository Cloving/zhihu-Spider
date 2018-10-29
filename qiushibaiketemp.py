# -*- coding:utf-8 -*-
# 爬去糗事百科（Time: 2018-10-26 15:54）
import urllib.error
import urllib.request
import re

pageIndex = 1
url = 'https://www.qiushibaike.com/hot/page/' + str(pageIndex)
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' \
             'AppleWebKit/537.36 (KHTML, like Gecko) ' \
             'Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134'
headers = {'User-Agent': user_agent}

try:
  request = urllib.request.Request(url, headers=headers)
  response = urllib.request.urlopen(request)
  content = response.read().decode('utf8')
  # print(content)
  pattern = re.compile('<div.*?class="author.*?>.*?<a.*?>.*?</a>.*?<a.*?>.*?<h2>(.*?)</h2>.*?'
                       '<div.*?class="articleGender.*?>(.*?)</div>.*?'
                       '<div.*?class="content.*?>.*?<span>(.*?)</span>.*?'
                       '<span.*?class="stats-vote.*?>.*?<i.*?>(.*?)</i>', re.S)
  items = re.findall(pattern, content)
  for item in items:
    # 清除字符串两边的空格，并转换换行符<br/>为\n
    print("发布人: " + item[0].strip())
    print('年龄: ' + item[1].strip())
    print('内容: '+item[2].strip().replace('<br/>', '\n'))
    print('点赞数：' + item[3].strip())
    print('\n')
except(urllib.error.URLError, urllib.error.HTTPError) as e:
  if hasattr(e, 'code'):
    print(e.code)
  if hasattr(e, 'reason'):
    print(e.reason)

