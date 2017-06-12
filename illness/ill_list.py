#encoding=utf-8
import urllib2

import pymysql
from  bs4 import BeautifulSoup


class IllSpider:

    def __init__(self):
        self.base_url="http://www.a-hospital.com"

    def use_db(self):
        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', charset='UTF8')
        cursor = conn.cursor()
        cursor.execute("USE illness")
        return conn, cursor;

    def query_list(self,conn,cursor):

        sql ='''
        select * from link_list
        '''

        cursor.execute(sql)
        rows = cursor.fetchall()
        list_link = []
        for row in rows:
            list_link.append(row[2])

        return  list_link


    def insert_into_table(self,conn,cursor,title,link):

        sql = '''
        insert into ill_list values(null,%s,%s)
        '''%("'"+title+"'","'"+link+"'")

        cursor.execute(sql)
        conn.commit()


    def parser_html(self,conn,cursor,url):
        try:
            cont = urllib2.urlopen(url,timeout=20).read()
        except:
            cont = urllib2.urlopen(url, timeout=20).read()

        soup = BeautifulSoup(cont, 'html.parser',
                             from_encoding='utf-8')
        lis = soup.find_all('ul')[0].find_all('li')

        for li in lis:
            a = li.find('a')
            try:
                title = a.attrs['title']
                link = self.base_url + a.attrs['href']
                print 'craw title;%s'%(title)
                self.insert_into_table(conn,cursor,title,link)
            except:
                continue


    def start(self):
        conn,cursor = self.use_db()
        list_link = self.query_list(conn,cursor)
        item = 1
        for li in list_link:
            self.parser_html(conn,cursor,li)
            print 'craw item;%d'%(item)
            item += 1
spider = IllSpider()
spider.start()



