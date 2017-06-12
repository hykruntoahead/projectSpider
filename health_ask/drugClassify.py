#encoding = utf-8
import json
import urllib2

import pymysql


class drugClassify:
    def __init__(self):
        self.base_url = "http://www.tngou.net/api/drug/classify"

    def useDb(self):
        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', charset='UTF8')
        cursor = conn.cursor()
        cursor.execute("USE health_illness")
        return conn, cursor;

    def insert_into_table(self, conn, cursor, name, description,classify):
        sql = 'insert into drug_classify values(null,%s,%s,%d)' % ("'" + name + "'","'" + description + "'",  classify)

        cursor.execute(sql)
        conn.commit()

    def parser_json(self, conn, cursor, url):
        cont = urllib2.urlopen(url, timeout=20).read()
        results = json.loads(cont)['tngou']

        for result in results:
            name = result['name']
            classify = result['id']
            des = result['description']
            self.insert_into_table(conn, cursor, name, des,classify)
            print 'craw name:%s,id:%d' % (name, classify)

    def start(self):
        conn, cursor = self.useDb();
        self.parser_json(conn, cursor, self.base_url)

classify = drugClassify()
classify.start()