#encoding=utf-8
# .decode('gb2312','ignore').encode('utf-8')
import pymysql
import urllib2
from bs4 import BeautifulSoup


class ComicCompSpider:
    def __init__(self):
        self.base_url='http://www.ku6.com/jinghua/xsxp/'


    def use_database(self):
        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', charset='UTF8')
        cursor = conn.cursor()
        cursor.execute("USE comic")
        return conn, cursor;

    def insert_into_table(self,conn,cursor,id,c_name,link):
        sql='''
        insert into comic_comp values(%d,%s,%s)
        ''' %(id,"'"+c_name+"'","'"+link+"'")

        cursor.execute(sql)
        conn.commit()

    def parser_net(self):
        cont=urllib2.urlopen(self.base_url)
        soup=BeautifulSoup(cont.read().decode('gb2312','ignore').encode('utf-8'),'html.parser',from_encoding='utf-8')
        lis = soup.find(class_='soul_list cfix').find_all('li')
        name_list=[]
        link_list=[]
        for li in lis:
            a=li.find('a')
            name = a.get_text()
            link = a.attrs['href'].strip()
            name_list.append(name)
            link_list.append(link)
        return name_list,link_list

    def start(self):
        conn,cursor=self.use_database()
        name_list ,link_list=self.parser_net()
        index=0
        for li in name_list:
            self.insert_into_table(conn,cursor,index+1,li,link_list[index])
            print 'craw %d : name=%s' %(index,li)
            index += 1

spider = ComicCompSpider();
spider.start()


