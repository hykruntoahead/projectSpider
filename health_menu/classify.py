#encoding=utf-8
import json

import pymysql
import urllib2

class Classify:
    def __init__(self):
        self.base_url="http://api.avatardata.cn/Cook/CookClass?key=8b01fc974ed0445cbe7e987879d9d830&id=0";

    def use_db(self):
        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', charset='UTF8')
        cursor = conn.cursor()
        cursor.execute("USE health_menu")
        return conn, cursor;


    def insert_into_table(self,conn,cursor,classify,name,keyword):
        sql = '''
        insert into classify values (null, %d,%s,%s)

        '''%(classify,"'"+name+"'","'"+keyword+"'")

        cursor.execute(sql)
        conn.commit();

    def parser_json(self,conn,cursor,url):
        cont = urllib2.urlopen(url, timeout=20).read()

        js = json.loads(cont)

        results = js['result']

        for result in results:
            id = result['id']
            name = result['name']
            keywords = result['keywords']
            self.insert_into_table(conn, cursor,  id, name,keywords)
            print 'craw name:%s' % name


    def start(self):
        conn,cursor = self.use_db();
        self.parser_json(conn,cursor,self.base_url)

cls = Classify();
cls.start();