# Search ZhihuUser Activity

import time
from urllib.parse import urlencode

import requests
from pymongo import MongoClient
from pyquery import PyQuery as pq

user_name = "******"
limit = 7
max_search_counts = 5
params = {
  "limit": limit,
  "desktop": "True"
}
base_url = "https://www.zhihu.com/api/v4/members/"
url = base_url + '/' + user_name + '/activities?' + urlencode(params)

headers = {
  "User-Agent": "Mozilla/5.0 (X11; Linux x86_64)\
                AppleWebKit/537.36 (KHTML, like Gecko)\
                Chrome/70.0.3538.77 Safari/537.36",
  "Referer": "https://www.zhihu.com/",
  "x-requested-with": "fetch"
}

client = MongoClient('127.0.0.1',username='admin',
                        password='******',
                        authSource='admin',
                        authMechanism='SCRAM-SHA-1')
db = client["zhihu"]
collection = db["zhihuDynamic"]


# 获取json数据
def get_Page(url):
  try:
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
      return response.json()
  except requests.ConnectionError as e:
    print("Error: ", e.args)

# 解析json数据
def get_Parse(json):
  if json:
    items = json.get('data')
    for item in items:
      zhihu = {}
      action_text = item.get("action_text")
      created_time = item.get("created_time")
      zhihu["操作行为"] = action_text
      zhihu["时间"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(created_time))
      if item.get('verb') == "MEMBER_VOTEUP_ARTICLE":
        item_detail =  voteup_article(item.get("target"))
      elif item.get('verb') == "ANSWER_VOTE_UP":
        item_detail = answer_voteUp(item.get("target"))
      elif item.get('verb') == "MEMBER_CREATE_ARTICLE":
        item_detail =  create_article(item.get("target"))
      elif item.get('verb') == "MEMBER_FOLLOW_COLUMN":
        item_detail =  follow_column(item.get('target'))
      elif item.get('verb') == "ANSWER_CREATE":
        item_detail = answer_create(item.get('target'))
      elif item.get('verb') == "QUESTION_FOLLOW":
        item_detail = question_follow(item.get('target'))
      yield dict(zhihu, **item_detail)

# 处理赞同文章数据
def voteup_article(target):
  temp_item = {}
  temp_item["文章作者"] = target.get('author').get('name')
  temp_item["文章标题"] = target.get('title')
  temp_item["文章内容"] = pq(target.get('content')).text()
  temp_item["赞同数"] = target.get('voteup_count')
  temp_item["评论数"] = target.get('comment_count')
  return temp_item

# 处理赞同回答数据
def answer_voteUp(target):
  temp_item = {}
  temp_item["问题标题"] = target.get('question').get('title')
  temp_item["回答人"] = target.get('author').get('name')
  temp_item["回答内容"] = pq(target.get('content')).text()
  temp_item["评论数"] = target.get("comment_count")
  temp_item["赞同数"] = target.get("voteup_count")
  temp_item["感谢数"] = target.get("thanks_count")
  return temp_item

# 处理发表文章数据
def create_article(target):
  temp_item = {}
  temp_item["文章标题"] = target.get("title")
  temp_item["文章内容"] = target.get("content")
  temp_item["评论数"] = target.get("comment_count")
  temp_item["赞同数"] = target.get("voteup_count")
  return temp_item

# 处理关注问题数据
def question_follow(target):
  temp_item = {}
  temp_item["问题名称"] = target.get("title")
  temp_item["提问者"] = target.get("author").get('name')
  temp_item["问题创建时间"] = target.get("created")
  temp_item["回答数"] = target.get("answer_count")
  temp_item["关注数"] = target.get("follower_count")
  temp_item["评论数"] = target.get("comment_count")
  return temp_item

# 处理关注专栏数据
def follow_column(target):
  temp_item = {}
  temp_item["专栏标题"] = target.get("title")
  temp_item["专栏描述"] = target.get("description")
  temp_item["专栏关注人数"] = target.get("followers")
  temp_item["专栏发表文章数"] = target.get("articles_count")
  return temp_item

# 处理回答问题数据
def answer_create(target):
  temp_item = {}
  temp_item["提问人"] = target.get("question").get("author").get("name")
  temp_item["问题名称"] = target.get("question").get("title")
  created_time = target.get("question").get("created")
  temp_item["提问时间"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(created_time))
  temp_item["回答内容"] = target.get("content")
  updated_time = target.get("updated_time")
  temp_item["最后一次更新回答时间"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(updated_time))
  temp_item["点赞数"] = target.get("voteup_count")
  temp_item["评论数"] = target.get("comment_count")
  temp_item["感谢数"] = target.get("thanks_count")
  return temp_item

def save_to_mongodb(result):
  if collection.insert_one(result):
    print("Successful save to Mongodb")

if __name__ == "__main__":
    for search_times in range(0, max_search_counts):
      json = get_Page(url)
      try:
        url = json.get("paging").get("next")
        print(url)
      except Exception as e:
        print("获取下一次请求的链接失败，失败原因：", e)
      results = get_Parse(json)
      print("=======================================")
      for result in results:
        save_to_mongodb(result)

