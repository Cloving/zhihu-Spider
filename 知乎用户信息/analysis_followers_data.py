import pickle
import os
import jieba
import re
from pyecharts import Bar
from pyecharts import Pie
from pyecharts import Scatter
from pyecharts import WordCloud


class ZhihuUserAnalysis():
  def process_nickname_data(self):
    nicknames_dict = {}
    nicknames = [followers_data[0] for followers_data in followers_data.items()]
    for nickname in nicknames:
      if nickname in nicknames_dict.keys():
        nicknames_dict[nickname] += 1
      else:
        nicknames_dict[nickname] = 1
    nickname_data = list(nicknames_dict.items())
    print(len(nickname_data))
    self.DrawWordCloud('用户名词云图', nickname_data, width=2500, height=1200, word_size_range=[20,40], savepath='./result')

  def process_headline_data(self):
    headline_data = [follower_data[1][0] for follower_data in followers_data.items()]
    stopwords = open('./stopwords.txt', 'r', encoding="utf-8").read().split('\n')
    headline = self.statistic_word_frequency(headline_data, stopwords)
    self.DrawWordCloud('标题词云图', headline, width=2500, height=1200, word_size_range=[20,40], savepath='./result')

  def process_gender_data(self):
    # 性别分析
    gender_data = [follower_data[1][1] for follower_data in followers_data.items()]
    male = gender_data.count(1)
    female = gender_data.count(0)
    unknow = gender_data.count(-1)
    gender_data = [['男性', male], ['女性', female], ['保密', unknow]]
    # self.Darbar("粉丝男女比例直方图", gender_data, savepath='./result')
    self.DarPie("粉丝男女比例饼图", gender_data, savepath='./result')

  def process_followers_data(self):
    # 粉丝的关注数({关注数：对应的人数})
    followers_count_dict = {}
    for follower_data in followers_data.items():
      follower_count = follower_data[1][2]
      if follower_count not in followers_count_dict:
        followers_count_dict.setdefault(follower_count, 0)
      followers_count_dict[follower_count] += 1
    followers_count_list = list(followers_count_dict.items())
    self.DraScatter("粉丝被关注数的散点图", followers_count_list, savepath='./result')
    # 处于各个区间段的数量
    follower_count_lt100 = 0
    follower_count_ge100_lt1000 = 0
    follower_count_ge1000 = 0
    for follower_count_value in followers_count_list:
      if follower_count_value[0] < 100:
        follower_count_lt100 += follower_count_value[1]
      elif 100 <= follower_count_value[0] < 1000:
        follower_count_ge100_lt1000 += follower_count_value[1]
      elif follower_count_value[0] >= 1000:
        follower_count_ge1000 += follower_count_value[1]
    follower_count_data = [
      ('count < 100', follower_count_lt100),
      ('100 <= count < 1000', follower_count_ge100_lt1000),
      ('count >= 1000', follower_count_ge1000)
    ]
    self.Darbar('粉丝被关注数量直方图', follower_count_data, savepath='./result')

  def process_answers_data(self):
    # 粉丝的回答数量
    answer_count_dict = {'0-10': 0, '10-20': 0, '20-30': 0, 
                        '30-40': 0, '40-50': 0, '50-60': 0, 
                        '60-70': 0, '70-80': 0, '80-90': 0, 
                        '90-100': 0, '大于等于100': 0, }
    for answer_data in followers_data.items():
      answer_count = answer_data[1][3]
      if 0 <= answer_count < 10:
        answer_count_dict['0-10'] += 1
      elif 10 <= answer_count < 20:
        answer_count_dict['10-20'] += 1
      elif 20 <= answer_count < 30:
        answer_count_dict['20-30'] += 1
      elif 30 <= answer_count < 40:
        answer_count_dict['30-40'] += 1
      elif 40 <= answer_count < 50:
        answer_count_dict['40-50'] += 1
      elif 50 <= answer_count < 60:
        answer_count_dict['50-60'] += 1
      elif 60 <= answer_count < 70:
        answer_count_dict['60-70'] += 1
      elif 70 <= answer_count < 80:
        answer_count_dict['70-80'] += 1
      elif 80 <= answer_count < 90:
        answer_count_dict['80-90'] += 1
      elif 90 <= answer_count < 100:
        answer_count_dict['90-100'] += 1    
      elif answer_count >= 100:
        answer_count_dict['大于等于100'] += 1
    answer_count_data = list(answer_count_dict.items())
    self.DarPie('粉丝回答数量饼图', answer_count_data, savepath='./result')
    self.Darbar('粉丝回答数量直方图', answer_count_data, savepath='./result')


  def Darbar(self, title, data, savepath='./result'):
    if (os.path.exists(savepath) is None):
      os.mkdir(savepath)
    bar = Bar(title)
    attrs = [data[i][0] for i in range(len(data))]
    vals = [data[i][1] for i in range(len(data))]
    bar.add('', attrs, vals, mark_point=['min', 'max'])
    bar.render(os.path.join(savepath, '%s.html' % title))

  def DarPie(self, title, data, savepath='./result'):
    if (os.path.exists(savepath) is None):
      os.mkdir(savepath)
    pie = Pie(title)
    attrs = [data[i][0] for i in range(len(data))]
    vals = [data[i][1] for i in range(len(data))]
    pie.add('', attrs, vals, is_label_show=True)
    pie.render(os.path.join(savepath, '%s.html' % title))

  def DraScatter(self, title, data, savepath='./result'):
    if (os.path.exists(savepath) is None):
      os.mkdir(savepath)
    scatter = Scatter(title)
    attrs = [data[i][0] for i in range(len(data))]
    vals = [data[i][1] for i in range(len(data))]
    scatter.add('', attrs, vals, is_visualmap=True)
    scatter.render(os.path.join(savepath, '%s.html' % title))
  
  def DrawWordCloud(self, title, data, width, height, word_size_range, savepath='./result'):
    if (os.path.exists(savepath) is None):
      os.mkdir(savepath)
    wordcloud = WordCloud(title, width=width, height=height)
    attrs = [data[i][0] for i in range(len(data))]
    vals = [data[i][1] for i in range(len(data))]
    wordcloud.add('', attrs, vals, word_size_range=word_size_range, shape='diamond')
    wordcloud.render(os.path.join(savepath, '%s.html' % title))

  def statistic_word_frequency(self, texts, stopwords):
    statistic_dict = {}
    for text in texts:
      temp = jieba.cut(text, cut_all=False)
      for t in temp:
        if t in stopwords or t == 'Empty':
          continue;
        if t in statistic_dict.keys():
          statistic_dict[t] += 1
        else:
          statistic_dict[t] = 1
    return list(statistic_dict.items())

if __name__ == "__main__":
  for root, dirs, files in os.walk(os.path.join(os.path.dirname(__file__),'result')):
    # print(root)  # 当前目录路径
    # print(dirs)  # 当前路径下所有子目录
    # print(files)  # 当前路径下所有非目录子文件
    for file in files:
      try:
        file_name = re.search('(.*?).pkl', file).group()
        break
      except Exception as e:
        continue
  with open('./result/'+file_name, 'rb') as f:
    followers_data = pickle.load(f)
  analysis = ZhihuUserAnalysis()
  analysis.process_nickname_data()
  analysis.process_headline_data()
  analysis.process_gender_data()
  analysis.process_followers_data()
  analysis.process_answers_data()
