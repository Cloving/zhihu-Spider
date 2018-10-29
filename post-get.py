import urllib.request

values = {"Username": "iTest", "Password": "Qaz123"}
getdata = urllib.parse.urlencode(values)
postdata = urllib.parse.urlencode(values).encode('utf-8')
print(postdata)

# post方式
postUrl = 'http://120.92.21.18/main.html'
postRequest = urllib.request.Request(postUrl, postdata)
postResponse = urllib.request.urlopen(postRequest)
print(str(postResponse.read(), 'utf-8'))

# get方式
url = 'http://120.92.21.18/main.html'
getUrl = url + '?' + getdata
getRequest = urllib.request.Request(getUrl)
getResponse = urllib.request.urlopen(getRequest)
print(str(getResponse.read(), 'utf-8'))
print(getUrl)




































