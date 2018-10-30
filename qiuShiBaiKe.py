# -*- coding: utf-8 -*-
'''
  第一次执行输出会请求2次，以达到标准长度
  之后执行输出时都只会请求1次，就达到了标准长度
'''

import re
import urllib.error
import urllib.request
from builtins import input


class QSBK:
  def __init__(self):
    self.user_agent = 'Mozilla/5.0 (X11; Linux x86_64)' \
                      ' AppleWebKit/537.36 (KHTML, like Gecko)' \
                      ' Chrome/68.0.3440.84 Safari/537.36'
    self.headers = {'User-Agent': self.user_agent}
    self.pageIndex = 1
    self.stories = []
    self.enable = False

  def getPage(self, pageIndex):
    try:
      url = 'https://www.qiushibaike.com/hot/page/' + str(pageIndex)
      request = urllib.request.Request(url, headers=self.headers)
      response = urllib.request.urlopen(request)
      pageCode = response.read().decode('utf8')
      return pageCode
    except(urllib.error.URLError, urllib.error.HTTPError) as e:
      if hasattr(e, "reason"):
        print("连接错误，错误原因", e.reason)
        return None

  def getPageItems(self, pageIndex):
    pageCode = self.getPage(pageIndex)
    if not pageCode:
      print("页面加载失败")
      return None
    pattern = re.compile('<div.*?class="author.*?>.*?<a.*?>.*?</a>.*?<a.*?>.*?<h2>(.*?)</h2>.*?'
                         '<div.*?class="articleGender.*?>(.*?)</div>.*?'
                         '<div.*?class="content.*?>.*?<span>(.*?)</span>.*?'
                         '<span.*?class="stats-vote.*?>.*?<i.*?>(.*?)</i>', re.S)
    items = re.findall(pattern, pageCode)
    pageStories = []
    for item in items:
      pageStories.append([item[0].strip(), item[1].strip(), item[2].strip().replace('<br/>', '\n'), item[3].strip()])
    # print(pageStories)
    return pageStories

  def loadPage(self):
    if self.enable is True:
      if len(self.stories) < 2:
        pageStories = self.getPageItems(self.pageIndex)
        if pageStories:
          self.stories.append(pageStories)
          self.pageIndex += 1

  def getOneStory(self, pageStories, curPage):
    for story in pageStories:
      inp = input('Please Press Enter: ')
      if inp is '':
        self.loadPage()
      elif inp is 'q':
        self.enable = False
        return
      print("第"+str(curPage) + "页")
      print("发布人: " + story[0])
      print('年龄: ' + story[1])
      print('内容: ' + story[2])
      print('点赞数：' + story[3])
      print('\n')

  def startSearch(self):
    print('Reading... Press Q quit')
    self.enable = True
    self.loadPage()
    curPage = 0
    while self.enable:
      if len(self.stories) > 0:
        pageStories = self.stories[0]
        curPage += 1
        del self.stories[0]
        self.getOneStory(pageStories, curPage)


spider = QSBK()
spider.startSearch()
