#encoding=utf-8
import json
import urllib2

import pymysql
from bs4 import BeautifulSoup


class LinkSpider:
    def __init__(self):
        self.base_url="http://www.a-hospital.com";
        self.base_str='''
        <p><a href="/w/%E7%96%BE%E7%97%85%E6%9D%A1%E7%9B%AE%E7%B4%A2%E5%BC%95-A" title="疾病条目索引-A">A</a> | <a href="/w/%E7%96%BE%E7%97%85%E6%9D%A1%E7%9B%AE%E7%B4%A2%E5%BC%95-B" title="疾病条目索引-B">B</a> | <a href="/w/%E7%96%BE%E7%97%85%E6%9D%A1%E7%9B%AE%E7%B4%A2%E5%BC%95-C" title="疾病条目索引-C">C</a> | <a href="/w/%E7%96%BE%E7%97%85%E6%9D%A1%E7%9B%AE%E7%B4%A2%E5%BC%95-D" title="疾病条目索引-D">D</a> | <a href="/w/%E7%96%BE%E7%97%85%E6%9D%A1%E7%9B%AE%E7%B4%A2%E5%BC%95-E" title="疾病条目索引-E">E</a> | <a href="/w/%E7%96%BE%E7%97%85%E6%9D%A1%E7%9B%AE%E7%B4%A2%E5%BC%95-F" title="疾病条目索引-F">F</a> | <a href="/w/%E7%96%BE%E7%97%85%E6%9D%A1%E7%9B%AE%E7%B4%A2%E5%BC%95-G" title="疾病条目索引-G">G</a> | <a href="/w/%E7%96%BE%E7%97%85%E6%9D%A1%E7%9B%AE%E7%B4%A2%E5%BC%95-H" title="疾病条目索引-H">H</a> | <a href="/w/%E7%96%BE%E7%97%85%E6%9D%A1%E7%9B%AE%E7%B4%A2%E5%BC%95-J" title="疾病条目索引-J">J</a> | <a href="/w/%E7%96%BE%E7%97%85%E6%9D%A1%E7%9B%AE%E7%B4%A2%E5%BC%95-K" title="疾病条目索引-K">K</a> | <a href="/w/%E7%96%BE%E7%97%85%E6%9D%A1%E7%9B%AE%E7%B4%A2%E5%BC%95-L" title="疾病条目索引-L">L</a> | <a href="/w/%E7%96%BE%E7%97%85%E6%9D%A1%E7%9B%AE%E7%B4%A2%E5%BC%95-M" title="疾病条目索引-M">M</a> | <a href="/w/%E7%96%BE%E7%97%85%E6%9D%A1%E7%9B%AE%E7%B4%A2%E5%BC%95-N" title="疾病条目索引-N">N</a> | <a href="/w/%E7%96%BE%E7%97%85%E6%9D%A1%E7%9B%AE%E7%B4%A2%E5%BC%95-P" title="疾病条目索引-P">P</a> | <a href="/w/%E7%96%BE%E7%97%85%E6%9D%A1%E7%9B%AE%E7%B4%A2%E5%BC%95-Q" title="疾病条目索引-Q">Q</a> | <a href="/w/%E7%96%BE%E7%97%85%E6%9D%A1%E7%9B%AE%E7%B4%A2%E5%BC%95-R" title="疾病条目索引-R">R</a> | <a href="/w/%E7%96%BE%E7%97%85%E6%9D%A1%E7%9B%AE%E7%B4%A2%E5%BC%95-S" title="疾病条目索引-S">S</a> | <a href="/w/%E7%96%BE%E7%97%85%E6%9D%A1%E7%9B%AE%E7%B4%A2%E5%BC%95-T" title="疾病条目索引-T">T</a> | <a href="/w/%E7%96%BE%E7%97%85%E6%9D%A1%E7%9B%AE%E7%B4%A2%E5%BC%95-W" title="疾病条目索引-W">W</a> | <a href="/w/%E7%96%BE%E7%97%85%E6%9D%A1%E7%9B%AE%E7%B4%A2%E5%BC%95-X" title="疾病条目索引-X">X</a> | <a href="/w/%E7%96%BE%E7%97%85%E6%9D%A1%E7%9B%AE%E7%B4%A2%E5%BC%95-Y" title="疾病条目索引-Y">Y</a> | <a href="/w/%E7%96%BE%E7%97%85%E6%9D%A1%E7%9B%AE%E7%B4%A2%E5%BC%95-Z" title="疾病条目索引-Z">Z</a></p>
        '''

    def use_db(self):
        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', charset='UTF8')
        cursor = conn.cursor()
        cursor.execute("USE illness")
        return conn, cursor;

    def  insert_into_table(self,conn,cursor,title,link):

        sql = '''
        insert into link_list values(null,%s,%s)
        '''%("'"+title+"'","'"+link+"'")

        cursor.execute(sql)
        conn.commit();

    def parser_html(self,conn,cursor):
        soup = BeautifulSoup(self.base_str, 'html.parser',
                             from_encoding='utf-8')
        lis = soup.find('p').find_all('a')

        for li in lis:
            link = self.base_url + li.attrs['href']
            title = li.attrs['title']
            self.insert_into_table(conn,cursor,title,link)


    def start(self):
        conn,cursor =  self.use_db()
        self.parser_html(conn,cursor)

spider = LinkSpider()
spider.start()

