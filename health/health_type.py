#encoding=utf-8
import pymysql
import urllib2
from bs4 import BeautifulSoup

class healthType:
    def __init__(self):
        self.base_url=''
        self.tuple = ('http://laoren.jiankangzu.com/laorenbaojian/','http://laoren.jiankangzu.com/laorenshenghuo/'
                      ,'http://laoren.jiankangzu.com/laorengushi_1/')

    def use_databse(self):
        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', charset='UTF8')
        cursor = conn.cursor()
        cursor.execute("USE health")
        return conn, cursor;

    def insert_into_table(self,conn,cursor,type,link):
        sql ='''
        insert into health_new_type values (null,%s,%s)
        '''%("'"+type+"'","'"+link+"'")

        cursor.execute(sql)
        conn.commit()

    def parser_html(self,conn,cursor,lk):
        req = urllib2.urlopen(lk)
        soup = BeautifulSoup(req.read(), 'html.parser',
                             from_encoding='utf-8')
        divs = soup.find_all('div',class_='box5 omanbg1')
        for div in divs:
            type = div.find('div',class_='box_title').get_text()
            link = div.find('div',class_='box_more').find('a').attrs['href']
            self.insert_into_table(conn,cursor,type,link)
            print 'craw type=%s'% type


    def start(self):
        conn,cursor = self.use_databse()
        for tp in self.tuple:
            self.parser_html(conn,cursor,tp)


spider = healthType()
spider.start()

