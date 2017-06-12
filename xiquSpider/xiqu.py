#encoding=utf-8
import re
import urllib2
import  pymysql
from bs4 import BeautifulSoup

class XQ_Spider:
    def  __init__(self):
        self.base_url='http://www.1ting.com'
        self.url='http://www.1ting.com/xiqu/'
        self.list1=[]
        self.list2 = []

    def use_database(self):
        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', charset='UTF8')
        cursor = conn.cursor()
        cursor.execute("USE opera")
        return conn,cursor;

    def insert_to_table(self,conn,cursor,index,name,link):
        sql = ''' INSERT INTO opera_categories VALUES (%d , %s ,  %s )''' % (index,
                "'" + name.encode('utf-8') + "'", "'" + link.encode('utf-8') + "'" )

        cursor.execute(sql)
        conn.commit()



    def parser_html(self):
        cont=urllib2.urlopen(self.url)
        # .decode('gb2312','ignore').encode('utf-8'),
        soup= BeautifulSoup(cont.read(),'html.parser',from_encoding='utf-8')
        nav=soup.find(class_='catebox clearfix')
        lis=nav.find_all('a')
        for li in lis:
               self.list1.append(li.attrs['href'].strip())
               self.list2.append(li.find('span').get_text())


    def start(self):
        conn,cursor=self.use_database()
        index=0
        self.parser_html()
        for d in self.list2:
            print 'craw %d:name %s' %(index,d)
            self.insert_to_table(conn,cursor,index+1,d,self.base_url+self.list1[index])
            index+=1

spider=XQ_Spider()
spider.start()
