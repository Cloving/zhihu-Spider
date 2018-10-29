# -*- coding: utf-8 -*-
import urllib.request
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
spider.startIndex()

