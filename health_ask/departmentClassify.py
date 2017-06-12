#encoding=utf-8
import json
import urllib2

import pymysql


class Classify:
    def __init__(self):
        self.baseUrl='http://www.tngou.net/api/department/classify';

    def useDb(self):
        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', charset='UTF8')
        cursor = conn.cursor()
        cursor.execute("USE health_illness")
        return conn, cursor;


    def insert_into_table(self,conn,cursor,name,classify):
        sql = 'insert into department values(null,%s,%d)'%("'"+name+"'",classify)

        cursor.execute(sql)
        conn.commit()


    def parser_json(self,conn,cursor,url):
        cont = urllib2.urlopen(url,timeout=20).read()
        results = json.loads(cont)['tngou']

        for result in results:
            name = result['name']
            classify = result['id']
            self.insert_into_table(conn,cursor,name,classify)
            print 'craw name:%s,id:%d'%(name ,classify)

    def start(self):
        conn,cursor= self.useDb();
        self.parser_json(conn,cursor,self.baseUrl)

classify = Classify()
classify.start()