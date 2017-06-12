# encoding=utf-8

"1.确定URL并抓取页面代码"

import urllib2

from bs4 import BeautifulSoup


class QSBK:
    def __init__(self):
        self.pageIndex = 1
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        self.headers = {'User-Agent': self.user_agent}
        # 存放每一页的段子
        self.stories = []
        # 存放程序是否继续进行的变量
        self.enable = False

    # 传入某一页的索引获得页面代码
    def getPage(self, pageIndex):
        try:
            url = 'http://www.qiushibaike.com/hot/page/' + str(pageIndex)
            # 构建请求的request
            request = urllib2.Request(url, headers=self.headers)
            # 利用urlopen获取页面代码
            response = urllib2.urlopen(request)
            # 将页面转化为UTF-8编码
            pageCode = response.read()
            return pageCode
        except urllib2.URLError, e:
            if (hasattr(e, "reason")):
                print u"连接糗事百科失败,错误原因：", e.reason
                return None

    # 传入某一页代码，返回本页不带图片的段子列表
    def getPageItems(self, pageIndex):
        pageCode = self.getPage(pageIndex)
        if not pageCode:
            print "页面加载失败"
            return None
        soup = BeautifulSoup(pageCode, "html.parser", from_encoding='utf-8')
        links = soup.find_all(class_='article block untagged mb15')
        dict = {}
        for link in links:
            dict['name'] = link.find('h2').get_text()
            dict['content'] = link.find(class_='content').get_text()
            dict['stats'] = link.find(class_='stats-vote').find(class_='number').get_text()
            dict['comments'] = link.find(class_='qiushi_comments').find(class_='number').get_text()
        return dict;

    # 加载并提取网页内容，加入到列表

    def loadPage(self):
        # 如果当前未看的页面少于2页，则加载新一页
        if self.enable == True:
            # 获取新一页
            if len(self.stories) < 2:
                # get a new page
                pageStories = self.getPageItems(self.pageIndex)
                print pageStories
                # 将该页的段子存放到全局list中
                if (pageStories):
                    self.stories.append(pageStories)
                    # 获取完之后页码索引加一，表示下次读取下一页
                    self.pageIndex += 1


    # 调用该方法，每次敲回车打印输出一个段子
    def getOneStory(self, pageStories, page):
        # 遍历一页的段子
        for story in pageStories:
            # 等待用户输入
            input = raw_input()
            # 每当输入回车一次，判断一下是否要加载新页面
            self.loadPage()

            if input == 'Q':
                self.enable = False
                return
            print u"第%d页\t 发布人：%s\t 内容:%s \n 星数:%s\t 评论数:%s" %(page, story['name']
                                                               , story['content'],
                                                                story['stats'],
                                                                story['comments'])

    # 开始方法
    def start(self):
        print u"正在读取糗事百科,按回车查看新段子，Q退出"

        self.enable = True

        self.loadPage()

        newPage = 0;

        while self.enable:
            if len(self.stories)> 0:
                pageStories = self.stories[0]
                # 当前读到的页数加一
                newPage += 1
                # 将全局list中第一个元素删除，因为已经取出
                del self.stories[0]
                # 输出该页的段子
                self.getOneStory(pageStories, newPage)


spider = QSBK()
spider.start()
