# Search ZhihuUser Activity

import time
from urllib.parse import urlencode

import requests
import dataParser
from pymongo import MongoClient
from pyquery import PyQuery as pq

class ZhihuUser:
  def __init__(self):
    self.user_name = "ovilia"
    self.max_search_counts = 5
    self.params = {
      "limit": 7,
      "desktop": "True"
    }
    self.base_url = "https://www.zhihu.com/api/v4/members/"
    self.url = self.base_url + '/' + self.user_name + '/activities?' + urlencode(self.params)
    self.headers = {
      "User-Agent": "Mozilla/5.0 (X11; Linux x86_64)\
                    AppleWebKit/537.36 (KHTML, like Gecko)\
                    Chrome/70.0.3538.77 Safari/537.36",
      "Referer": "https://www.zhihu.com/",
      "x-requested-with": "fetch"
    }
    self.client = MongoClient('127.0.0.1',username='admin',
                        password='920804',
                        authSource='admin',
                        authMechanism='SCRAM-SHA-1')
    self.db = self.client["zhihu"]
    self.collection = self.db["zhihuDynamic"]
    self.data_Parser = dataParser.DataParser()

  def startSearch(self):
    for search_times in range(0, self.max_search_counts):
      json = self.get_Page(self.url)
      try:
        self.url = json.get("paging").get("next")
        print(self.url)
      except Exception as e:
        print("获取下一次请求的链接失败，失败原因：", e)
      results = self.get_Parse(json)
      print("=======================================")
      for result in results:
        self.save_to_mongodb(result)

  # 获取json数据
  def get_Page(self, url):
    try:
      response = requests.get(url, headers=self.headers)
      if response.status_code == 200:
        return response.json()
    except requests.ConnectionError as e:
      print("Error: ", e.args)

  # 解析json数据
  def get_Parse(self, json):
    if json:
      items = json.get('data')
      for item in items:
        zhihu = {}
        action_text = item.get("action_text")
        created_time = item.get("created_time")
        zhihu["操作行为"] = action_text
        zhihu["时间"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(created_time))
        if item.get('verb') == "MEMBER_VOTEUP_ARTICLE":
          item_detail = self.data_Parser.voteup_article(item.get("target"))
        elif item.get('verb') == "ANSWER_VOTE_UP":
          item_detail = self.data_Parser.answer_voteUp(item.get("target"))
        elif item.get('verb') == "MEMBER_CREATE_ARTICLE":
          item_detail = self.data_Parser.create_article(item.get("target"))
        elif item.get('verb') == "MEMBER_FOLLOW_COLUMN":
          item_detail = self.data_Parser.follow_column(item.get('target'))
        elif item.get('verb') == "ANSWER_CREATE":
          item_detail = self.data_Parser.answer_create(item.get('target'))
        elif item.get('verb') == "QUESTION_FOLLOW":
          item_detail = self.data_Parser.question_follow(item.get('target'))
        yield dict(zhihu, **item_detail)

  def save_to_mongodb(self, result):
    if self.collection.insert_one(result):
      print("Successful save to Mongodb")

if __name__ == "__main__":
  spider = ZhihuUser()
  spider.startSearch()