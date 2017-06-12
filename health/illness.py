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
         insert into illness values(null,%s,%s)
         '''%("'"+illness+"'","'"+link+"'")

         cursor.execute(sql)
         conn.commit()


     def parser_html(self,conn,cursor,url):
         cont = urllib2.urlopen(url,timeout=20).read()

         soup = BeautifulSoup(cont.decode('gb2312', 'ignore').encode('utf-8'), 'html.parser',
                                 from_encoding='utf-8')

         lis = soup.find('div',class_='leftPinBoxUL a_02').find('ul','a_02').find_all('li')

         for li in lis:
             link = li.find('a').attrs['href'].strip().encode('utf-8')
             illness = li.find('a').get_text().strip().encode('utf-8')
             self.insert_into_table(conn,cursor,illness,link)
             print 'craw illness:%s'% illness

     def start(self):
         url = 'http://jibing.ewsos.com/jibing/keshi-LaoNianKe771'
         conn,cursor = self.use_database()
         self.parser_html(conn,cursor,url)




spider = Illness()
spider.start()





