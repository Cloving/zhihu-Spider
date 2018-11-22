# encoding=utf8

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep
import pymysql

url = "https://music.163.com/"
chrome_option = Options()
chrome_option.add_argument('--headless')
DRIVER = webdriver.Chrome(chrome_options=chrome_option)

# 其中 driver.get 方法会打开请求的URL，
# WebDriver 会等待页面完全加载完成之后才会返回，
# 即程序会等待页面的所有内容加载完成，JS渲染完毕之后才继续往下执行。
DRIVER.get(url)

DRIVER.find_element_by_xpath("/html/body/div[@id='g-topbar']"
                             "/div[@id='g_nav2']/div[@class='wrap f-pr']"
                             "/ul[@class='nav']/li[2]/a/em").click()

try:
   firstChild_iframe = DRIVER.find_element_by_id("g_iframe")
except Exception as e:
  print("get mask-layer failed: ", e)

sleep(2)
DRIVER.switch_to.frame(firstChild_iframe)
table = DRIVER.find_element_by_tag_name('table')

div = DRIVER.find_element_by_xpath('//div[@id="song-list-pre-cache"]')
songList = table.find_elements_by_xpath('tbody/tr')

print(len(songList))
totalList = []
songChildList = []
for song in songList:
  songChildList.append(song.find_element_by_xpath('td[2]//b').get_attribute('title'))
  songChildList.append(song.find_element_by_xpath('td[3]//span[@class="u-dur "]').text)
  songChildList.append(song.find_element_by_xpath('td[last()]//span').get_attribute('title'))
  totalList.append(songChildList)
  songChildList = []

print(totalList)
print('\n')

db = pymysql.connect(host="127.0.0.1", user="root", passwd="******", db="spider")
print("成功连接MySQL数据库")
cursor = db.cursor()
cursor.execute("DROP TABLE IF EXISTS NetEaseCloudMusic")
# 如果使用单引号，需要在每行末尾添加 \
sql = '''CREATE TABLE NetEaseCloudMusic(
        ID INT NOT NULL,
        musicName LONGTEXT,
        time LONGTEXT,
        singer LONGTEXT
        )CHARSET=utf8'''
cursor.execute(sql)

# The format string is not really a normal Python format string.
# Must always use %s for all fields.
count = 0
importSQL = """INSERT INTO NetEaseCloudMusic(ID, musicName, time, singer)
              VALUES (%s, %s, %s, %s)"""
for (index, child_SongList) in zip(range(1, len(totalList)+1), totalList):
  try:
    cursor.execute(importSQL, (index, child_SongList[0], child_SongList[1], child_SongList[2]))
    db.commit()
    count += 1
  except Exception as e:
    print('导入数据失败： ', e)
    db.rollback()

print("成功导入" + str(count) + "条数据")

