# -*- coding=utf-8 -*-
import time

from pyquery import PyQuery as pq


class DataParser:
  # 处理赞同文章数据
  def voteup_article(self, target):
    temp_item = {}
    temp_item["文章作者"] = target.get('author').get('name')
    temp_item["文章标题"] = target.get('title')
    temp_item["文章内容"] = pq(target.get('content')).text().strip().replace('\n', '')
    temp_item["赞同数"] = target.get('voteup_count')
    temp_item["评论数"] = target.get('comment_count')
    return temp_item

  # 处理赞同回答数据
  def answer_voteUp(self, target):
    temp_item = {}
    temp_item["问题标题"] = target.get('question').get('title')
    temp_item["回答人"] = target.get('author').get('name')
    temp_item["回答内容"] = pq(target.get('content')).text().strip().replace('\n', '')
    temp_item["评论数"] = target.get("comment_count")
    temp_item["赞同数"] = target.get("voteup_count")
    temp_item["感谢数"] = target.get("thanks_count")
    return temp_item

  # 处理发表文章数据
  def create_article(self, target):
    temp_item = {}
    temp_item["文章标题"] = target.get("title")
    temp_item["文章内容"] = target.get("content").strip().replace('\n', '')
    temp_item["评论数"] = target.get("comment_count")
    temp_item["赞同数"] = target.get("voteup_count")
    return temp_item

  # 处理关注问题数据
  def question_follow(self, target):
    temp_item = {}
    temp_item["问题名称"] = target.get("title")
    temp_item["提问者"] = target.get("author").get('name')
    created = target.get("created")
    temp_item["问题创建时间"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(created))
    temp_item["回答数"] = target.get("answer_count")
    temp_item["关注数"] = target.get("follower_count")
    temp_item["评论数"] = target.get("comment_count")
    return temp_item

  # 处理关注专栏数据
  def follow_column(self, target):
    temp_item = {}
    temp_item["专栏标题"] = target.get("title")
    temp_item["专栏描述"] = target.get("description")
    temp_item["专栏关注人数"] = target.get("followers")
    temp_item["专栏发表文章数"] = target.get("articles_count")
    return temp_item

  # 处理回答问题数据
  def answer_create(self, target):
    temp_item = {}
    temp_item["提问人"] = target.get("question").get("author").get("name")
    temp_item["问题名称"] = target.get("question").get("title")
    created_time = target.get("question").get("created")
    temp_item["提问时间"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(created_time))
    temp_item["回答内容"] = pq(target.get("content")).text().replace('\n', '')
    updated_time = target.get("updated_time")
    temp_item["最后一次更新回答时间"] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(updated_time))
    temp_item["点赞数"] = target.get("voteup_count")
    temp_item["评论数"] = target.get("comment_count")
    temp_item["感谢数"] = target.get("thanks_count")
    return temp_item
