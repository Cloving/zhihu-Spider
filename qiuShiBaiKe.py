# -*- coding: utf-8 -*-
import urllib.request
import urllib.error
import re


class QSBK:
  def __init__(self):
    self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' \
             'AppleWebKit/537.36 (KHTML, like Gecko) ' \
             'Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134'
    self.headers = {'User_Agent': self.user_agent}
    self.pageIndex = 1
    self.stories = []
    self.enable = False

  def getPage(self, pageIndex):
    try:
      url = 'https://www.qiushibaike.com/hot/page/' + str(pageIndex)
      user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) ' \
             'AppleWebKit/537.36 (KHTML, like Gecko) ' \
             'Chrome/64.0.3282.140 Safari/537.36 Edge/17.17134'
      headers = {'User-Agent': user_agent}
      request = urllib.request.Request(url, headers)
      response = urllib.request.urlopen(request)
      pageCode = response.read().decode('utf8')
      return pageCode
    except(urllib.error.URLError, urllib.error.HTTPError) as e:
      if hasattr(e, "reason"):
        print(u"连接错误，错误原因", e.reason)
        return None

  def getPageItems(self, pageIndex):
    pageCode = self.getPage(pageIndex)
    if not pageCode:
      print(u"页面加载失败")
      return None
    pattern = re.compile('<div.*?class="author.*?>.*?<a.*?>.*?</a>.*?<a.*?>.*?<h2>(.*?)</h2>.*?'
                         '<div.*?class="articleGender.*?>(.*?)</div>.*?'
                         '<div.*?class="content.*?>.*?<span>(.*?)</span>.*?'
                         '<span.*?class="stats-vote.*?>.*?<i.*?>(.*?)</i>', re.S)
    items = re.findall(pattern, pageCode)
    pageStories = []
    for item in items:
      pageStories.append(item[0].strip(), item[1].strip(), item[2].strip().replace('<br/>', '\n'), item[3].strip())
    return pageStories

  def loadPage(self):
    if self.enable:
      if len(self.stories) < 2:
        pageStories = self.getPageItems(self.pageIndex)
        if pageStories:
          self.stories.append(pageStories)
          self.pageIndex += 1

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

