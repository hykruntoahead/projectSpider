#encoding=utf-8
import pymysql
import urllib2
from bs4 import BeautifulSoup

class Illness:

     def use_database(self):
         conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', charset='UTF8')
         cursor = conn.cursor()
         cursor.execute("USE health")
         return conn, cursor;

     def insert_into_table(self,conn,cursor,illness,link):

         sql = '''
         insert into illness_new values(null,%s,%s)
         '''%("'"+illness+"'","'"+link+"'")

         cursor.execute(sql)
         conn.commit()


     def parser_html(self,conn,cursor,url,page):
         cont = urllib2.urlopen(url,timeout=20).read()

         soup = BeautifulSoup(cont.decode('gb2312', 'ignore').encode('utf-8'), 'html.parser',
                                 from_encoding='utf-8')

         dls = soup.find('div',class_='part-cont3').find_all('dl')

         for dl in dls:
             dd = dl.find('dd')
             illness = dd.find('h3').get_text().strip()
             link = dd.find('h3').find('a').attrs['href'].strip()

             self.insert_into_table(conn,cursor,illness,link)
             print 'craw page :%d,illness:%s'% (page,illness)

     def start(self):

         conn,cursor = self.use_database()
         for page in range(1,12):
             if page>5:
                 url = 'http://jbk.99.com.cn/keshi/laonianke-%d.html'%page
                 self.parser_html(conn,cursor,url,page)




spider = Illness()
spider.start()





