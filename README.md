编写关于知乎站点的各类爬虫

# 知乎用户动态
利用`requests`库请求用户的动态数据，包括赞同文章、赞同回答、发表文章、关注问题、关注专栏、回答问题等数据。之后序列化处理这些数据，以`json`的形式存储到MongoDB中。

### 代码地址：[知乎用户动态](https://github.com/Cloving/zhihu-Spider/tree/master/%E7%9F%A5%E4%B9%8E%E7%94%A8%E6%88%B7%E5%8A%A8%E6%80%81)

### 使用方式
在各类模块成功安装以及MongoDB配置完成的情况下，指定文件`zhihuUserSpider.py`中的`self.user_name`的值，即用户的个性化域名，运行该文件，即可完成。本例中的MongoDB配置了密码，如果MongoDB中没有使用密码可根据实际情况自行配置。

### 详细介绍：[抓取知乎用户动态数据](http://yaodongsheng.com/2018/11/20/%E6%8A%93%E5%8F%96%E7%9F%A5%E4%B9%8E%E7%94%A8%E6%88%B7%E5%8A%A8%E6%80%81%E6%95%B0%E6%8D%AE/)


# 知乎用户粉丝
抓取并分析了知乎用户的粉丝数据，包括粉丝名、粉丝标题、粉丝男女比例、粉丝回答问题比例、粉丝被关注数等数据。之后利用`pyecharts`库对这些数据进行可视化的显示。

### 代码地址：[知乎用户粉丝](https://github.com/Cloving/zhihu-Spider/tree/master/%E7%9F%A5%E4%B9%8E%E7%94%A8%E6%88%B7%E7%B2%89%E4%B8%9D)

### 使用方式
在文件`Zhihu_spider.py`中配置用户的个性化域名后直接运行即可将抓取到的文件存储，之后运行`analysis_followers_data.py`可以得到部分数据的可视化图表，框架已经完成，具体提取哪些数据以及用哪些图表展示可以自行配置。可以参考[pyecharts - A Python Echarts Plotting Library](http://pyecharts.org/#/zh-cn/charts_base)

### 详细介绍：[抓取知乎用户粉丝数据](http://yaodongsheng.com/2018/12/13/%E6%8A%93%E5%8F%96%E7%9F%A5%E4%B9%8E%E7%94%A8%E6%88%B7%E7%B2%89%E4%B8%9D%E6%95%B0%E6%8D%AE/)

### 示例图
![标题词云图](https://github.com/Cloving/zhihu-Spider/blob/master/%E7%9F%A5%E4%B9%8E%E7%94%A8%E6%88%B7%E7%B2%89%E4%B8%9D/result/%E6%A0%87%E9%A2%98%E8%AF%8D%E4%BA%91%E5%9B%BE.png?raw=true)

![用户名词云图](https://github.com/Cloving/zhihu-Spider/blob/master/%E7%9F%A5%E4%B9%8E%E7%94%A8%E6%88%B7%E7%B2%89%E4%B8%9D/result/%E7%94%A8%E6%88%B7%E5%90%8D%E8%AF%8D%E4%BA%91%E5%9B%BE.png?raw=true)

![粉丝回答数量直方图](https://github.com/Cloving/zhihu-Spider/blob/master/%E7%9F%A5%E4%B9%8E%E7%94%A8%E6%88%B7%E7%B2%89%E4%B8%9D/result/%E7%B2%89%E4%B8%9D%E5%9B%9E%E7%AD%94%E6%95%B0%E9%87%8F%E7%9B%B4%E6%96%B9%E5%9B%BE.png?raw=true)

![粉丝男女比例饼图](https://github.com/Cloving/zhihu-Spider/blob/master/%E7%9F%A5%E4%B9%8E%E7%94%A8%E6%88%B7%E7%B2%89%E4%B8%9D/result/%E7%B2%89%E4%B8%9D%E7%94%B7%E5%A5%B3%E6%AF%94%E4%BE%8B%E9%A5%BC%E5%9B%BE.png?raw=true)

![粉丝被关注数量直方图](https://github.com/Cloving/zhihu-Spider/blob/master/%E7%9F%A5%E4%B9%8E%E7%94%A8%E6%88%B7%E7%B2%89%E4%B8%9D/result/%E7%B2%89%E4%B8%9D%E8%A2%AB%E5%85%B3%E6%B3%A8%E6%95%B0%E9%87%8F%E7%9B%B4%E6%96%B9%E5%9B%BE.png?raw=true)