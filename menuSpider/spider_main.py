#encoding=utf-8

import urllib2
import  pymysql
from bs4 import BeautifulSoup

class SpriderMain:
    def __init__(self):
        self.base_url="http://home.meishichina.com/recipe/recai/page/"


    def get_url_code(self,url):
        if url is None:
            return None

        response = urllib2.urlopen(url)

        if (response.getcode() != 200):
            return None

        return response.read()


    def parser_code(self,html_code):
        if html_code is None:
            return None
        ls = []

        soup=BeautifulSoup(html_code,'html.parser',from_encoding='utf-8')
        lis=soup.find(class_="ui_newlist_1 get_num").find('ul').findAll('li')
        for li in lis:
            list = []
            list.append(li.find(class_='detail').find('h2').find('a').get_text().strip())
            list.append(li.find(class_='pic').find('img').attrs['data-src'].strip())
            list.append(li.find(class_='detail').find('h2').find('a').attrs['href'].strip())
            # list.append(li.find(class_='subline').find('a').get_text())
            list.append(li.find(class_='subcontent').get_text().strip())
            ls.append(list)
        return  ls

    def create_sql_table(self):
        conn=pymysql.connect(host='localhost', port=3306, user='root', passwd='123456',charset='UTF8')
        cursor = conn.cursor()
        cursor.execute("USE spider")

        sql = """CREATE TABLE MENU (
                 MENU_NAME  CHAR(200) NOT NULL,
                 MENU_PIC   TEXT ,
                 MENU_LINK  TEXT,
                 CONTENT TEXT )"""
        try:
            cursor.execute(sql)
            conn.commit()
        except:
            conn.rollback()


        return conn,cursor

    def output_to_sql(self,conn,cursor,list):
        sql = '''
        INSERT INTO MENU(MENU_NAME ,MENU_PIC , MENU_LINK , CONTENT) VALUES (%s , %s ,  %s , %s )''' % ("'"+list[0].encode('utf-8')+"'","'"+list[1].encode('utf-8')+"'","'"+list[2].encode('utf-8')+"'","'"+list[3].encode('utf-8')+"'")

        print sql;
            # 执行SQL语句
        try:
            cursor.execute(sql)
            conn.commit()
        except:
            conn.rollback()

    def start(self):
        pageIndex=1
        conn, cursor = self.create_sql_table()
        while pageIndex<=4265:
            full_url = self.base_url + str(pageIndex) + "/"
            code=self.get_url_code(full_url)
            la=self.parser_code(code)
            print la;
            for l in la:
                self.output_to_sql(conn,cursor,l)
            pageIndex+=1
            print "craw %d -- %s:"% (pageIndex,full_url)
        conn.close()


spider=SpriderMain()
spider.start()


