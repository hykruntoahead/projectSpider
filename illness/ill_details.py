#encoding=utf-8
import urllib2

import pymysql
from  bs4 import BeautifulSoup
import time

class IllDetails:

    def __init__(self):
        self.user_agent = 'Baiduspider+(+http://www.baidu.com/search/spider.htm)'
        self.headers = {'User-Agent': self.user_agent}

    def use_db(self):
        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', charset='UTF8')
        cursor = conn.cursor()
        cursor.execute("USE illness")
        return conn, cursor;


    def query_all_link(self,conn,cursor):

        sql = '''
        select * from ill_list
        '''

        cursor.execute(sql)
        rows = cursor.fetchall()
        list_name = []
        list_link = []
        for row in rows:
            list_name.append(row[1])
            list_link.append(row[2])

        return list_name,list_link


    def insert_into_table(self,conn,cursor,name,text):

        sql = '''
        insert into ill_detail values(null,%s,%s)
        '''%("'"+name+"'","'"+text+"'")

        cursor.execute(sql)
        conn.commit()


    def parser_html(self,conn,cursor,name,url):

        try:
            time.sleep(5)
            cont = urllib2.urlopen(url,timeout = 20).read()
        except:
            try:
                request = urllib2.Request(url, headers=self.headers)
                cont = urllib2.urlopen(request, timeout = 20).read()
            except:
                cont = urllib2.urlopen(url, timeout = 20).read()

        soup = BeautifulSoup(cont,'html.parser',from_encoding='utf-8')

        body = soup.find('body')

        ps = body.find_all('p')

        text = ''
        for p in ps:
             text +=p.get_text()

        while text.find("'") != -1:
            text = text[:text.index("'")] + '`' + text[text.index("'") + 1:]
        text.encode(encoding='utf-8')
        self.insert_into_table(conn,cursor,name,text)
        print  'craw name:%s'% (name)

    def start(self):
        conn,cursor = self.use_db()
        list_name,list_link = self.query_all_link(conn,cursor)
        item = 0
        for link in list_link:
          if item > 14811:
            self.parser_html(conn,cursor,list_name[item],link)
          print 'craw item:%d'% (item)
          item +=1

spider = IllDetails()
spider.start()

