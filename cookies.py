import urllib.request
import http.cookiejar

# 1. cookie保存在变量中
# 声明一个CookiesJar对象实例来保存cookies
cookie = http.cookiejar.CookieJar()
# 创建cookie处理器
handler = urllib.request.HTTPCookieProcessor(cookie)
# 通过handler来构建opener
opener = urllib.request.build_opener(handler)
# 获取cookie
response = opener.open('https://www.baidu.com')
for item in cookie:
  print('Name = ' + item.name)
  print('Value = ' + item.value)


# 2. cookie保存在文件中
# 创建一个同级目录下的文件用来保存cookies
fileName = 'cookie.txt'
# 声明一个MozillaCookieJar对象实例保存cookies, 之后保存到文件中
# MozillaCookieJar同时也可以从磁盘中读取已保存的cookie文件
cookie2 = http.cookiejar.MozillaCookieJar(fileName)
# 创建cookie处理器
handler2 = urllib.request.HTTPCookieProcessor(cookie2)
# 通过handler2来构建opener2
opener2 = urllib.request.build_opener(handler2)
# 获取cookie
response2 = opener2.open('https://www.baidu.com')
cookie2.save(ignore_discard=True, ignore_expires=True)


# 3. 读取cookie并访问
# 创建MozillaCookiesJar实例对象
cookie3 = http.cookiejar.MozillaCookieJar()
# 从文件中读取内容到变量
cookie3.load('cookie.txt', ignore_expires=True, ignore_discard=True)
# 创建请求的request
request = urllib.request.Request('https://www.baidu.com')
# 创建一个opener
opener3 = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookie3))
response3 = opener3.open(request)
print(str(response3.read(), 'utf-8'))


