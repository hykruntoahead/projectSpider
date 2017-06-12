#encoding=utf-8
import pymysql
import urllib2
from bs4 import BeautifulSoup


class healthSpider:
    def __init__(self):
        self.base_path="http://laoren.ewsos.com"
        self.tuple = ('http://laoren.ewsos.com/lrbj/','http://laoren.ewsos.com/jkys/','http://laoren.ewsos.com/lrsh/')


    def use_databse(self):
        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', charset='UTF8')
        cursor = conn.cursor()
        cursor.execute("USE health")
        return conn, cursor;

    def insert_into_table(self,conn,cursor,type,link):
        sql = '''
        insert into health_type  VALUES (null ,%s,%s)
        '''%("'"+type+"'","'"+link+"'")

        cursor.execute(sql)
        conn.commit()


    def parser_html(self,conn,cursor,url):
        cont=urllib2.urlopen(url)
        soup = BeautifulSoup(cont.read().decode('gb2312', 'ignore').encode('utf-8'), 'html.parser',
                             from_encoding='utf-8')

        types = soup.find_all('div',class_='leftBox5')
        for ty in types:
            type = ty.find(class_='a_04').find('a').get_text()
            link = ty.find(class_='a_05').find('a').attrs['href']
            self.insert_into_table(conn,cursor,type,self.base_path+link)
            print 'craw :type= %s'%type


    def start(self):
        conn,cursor = self.use_databse();
        for li in self.tuple:
            self.parser_html(conn,cursor,li)


spider = healthSpider()
spider.start()