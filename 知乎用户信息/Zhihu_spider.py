import json
import os
import pickle

import requests
from fake_useragent import UserAgent

class ZhihuUser(object):
  def __init__(self):
    self.data = {}
    self.base_url = "https://www.zhihu.com/api/v4/members/{user}/followers?{include}"
    self.include = 'include=data%5B*%5D.answer_count%2Carticles_count%2C\
      gender%2Cfollower_count%2Cis_followed%2Cis_following%2C\
      badge%5B%3F(type%3Dbest_answerer)%5D.topics&offset={offset}&limit=20'
    self.agent = UserAgent()
    self.header = {
      'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) \
                    AppleWebKit/537.36 (KHTML, like Gecko) \
                    Chrome/70.0.3538.77 Safari/537.36'
    }
  
  def start(self, username, savepath, savename):
    index = 0
    flag = True
    while flag:
      offset=index*20
      include = self.include.format(offset=offset)
      url = self.base_url.format(user=username, include=include)
      # 请求json数据
      print("正在进行第{}次请求".format(index+1))
      jsonData = self.requests_source(url)
      # 提取需要的数据
      self.process_data(jsonData)
      # 如果仍然存在数据，处理下一次请求
      if jsonData.get('paging').get('is_end') is False:
        index = index + 1
        self.header['user-agent'] = self.agent.random
      else:
        flag = False
        print("完成请求")
    # 保存数据
    self.save_data(self.data, savepath, savename)

  def requests_source(self, url):
    try:
      response = requests.get(url, headers=self.header, timeout=(5,30))
      if response.status_code == 200:
        return response.json()
    except requests.ConnectionError as e:
      print("获取请求失败，失败原因：", e)

  def process_data(self, jsonData):
    followers = jsonData.get('data')
    for follow in followers:
      name = self.read_data_from_jsonData(follow, 'name')
      headline = self.read_data_from_jsonData(follow, 'headline')
      gender = self.read_data_from_jsonData(follow, 'gender')
      follower_count = self.read_data_from_jsonData(follow, 'follower_count')
      answer_count = self.read_data_from_jsonData(follow, 'answer_count')
      self.data[name] = [headline, gender, follower_count, answer_count]
      print(name, self.data[name])
    print('\n')

  def read_data_from_jsonData(self, json, key):
    value = json.get(key)
    return value if value is not '' else 'Empty'

  def save_data(self, follower_data, savepath, savename):
    if not os.path.exists(savepath):
      os.mkdir(savepath)
    with open(os.path.join(savepath, savename), 'wb') as f:
      pickle.dump(follower_data, f)
    f.close()
    print("完成存储")

if __name__ == "__main__":
  username = 'ou-ran-xing-17'
  savepath = './result'
  savename = username + '.pkl'
  zhihu = ZhihuUser()
  zhihu.start(username = username, savepath = savepath, savename=savename)
  