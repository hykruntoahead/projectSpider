# encoding=utf-8
import urllib2
from bs4 import BeautifulSoup
import pymysql
import random


class Health:
    def __init__(self):
        self.base_path = 'E:\health_pic'

    def use_database(self):
        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', charset='UTF8')
        cursor = conn.cursor()
        cursor.execute("USE health")
        return conn, cursor;

    def insert_into_table(self, conn, cursor, title, source,
                          description, type_id, body, pic):
        sql = '''
        insert into health_yangseng values(null,%s,%s,%s,%d,%s,%s)
        ''' % ("'" + title + "'", "'" + source + "'", "'" + description + "'",
               type_id, "'" + body + "'", "'" + pic + "'")

        cursor.execute(sql)
        conn.commit()

    def query_all_type(self, cursor):
        sql = '''
        SELECT * FROM health_article
        '''

        cursor.execute(sql)
        rows = cursor.fetchall()

        list_title = []
        list_source = []
        list_desc = []
        list_type_id = []
        list_body = []

        for row in rows:
            list_title.append(row[1])
            list_source.append(row[2])
            list_desc.append(row[3])
            list_type_id.append(row[4])
            list_body.append(row[6])

        return list_title, list_source, list_desc, list_type_id, list_body



    def start(self):
        conn, cursor = self.use_database()
        list_title, list_source, list_desc, list_type_id, list_body = self.query_all_type(cursor)
        index = 0
        for body in list_body:
            if index > -1:
                if body.find('None') != -1:
                    print "find--None-%d"%index
                elif len(body) < 40:
                    print "find--Nil-%d" % index
                else:
                    rd = random.randint(0, 300)
                    pic = self.base_path + '\old_%d' % rd
                    print pic
                    if body.find('<body>') != -1:
                        body = body.replace('<body>','')
                        body = body.replace('</body>','')
                    self.insert_into_table(conn,cursor,list_title[index],list_source[index],list_desc[index],
                                               list_type_id[index],body,pic)
            print "find--%d" % index
            index += 1


spider = Health()
spider.start()
