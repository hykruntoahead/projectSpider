# encoding=utf-8
import urllib2

import pymysql
from bs4 import BeautifulSoup
import time


class Health_New:
    def __init__(self):
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'
        self.headers = {'User-Agent': self.user_agent}

    def use_database(self):
        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', charset='UTF8')
        cursor = conn.cursor()
        cursor.execute("USE health")
        return conn, cursor;

    def insert_into_table(self, conn, cursor, title, source,
                          description, url, type_id, pic, path):
        sql = '''
        insert into health_article_new values(null,%s,%s,%s,%s,%d,%s,%s)
        ''' % (
            "'" + title + "'", "'" + source + "'", "'" + description + "'", "'" + url + "'", + type_id, "'" + pic + "'",
            "'" + path + "'")

        cursor.execute(sql)
        conn.commit()

    def query_all_type(self, cursor):
        sql = '''
        SELECT * FROM health_articles2
        '''

        cursor.execute(sql)
        rows = cursor.fetchall()

        list_title = []
        list_source = []
        list_desc = []
        list_url = []
        list_type_id = []
        list_pic = []

        for row in rows:
            list_title.append(row[1])
            list_source.append(row[2])
            list_desc.append(row[3])
            list_url.append(row[4])
            list_type_id.append(row[5])
            list_pic.append(row[6])

        return list_title, list_source, list_desc, list_url, list_type_id, list_pic

    def parser_html(self, index, link):
        req = urllib2.Request(link, headers=self.headers)
        try:
            cont = urllib2.urlopen(req, timeout=25).read()
        except:
            try:
                cont = urllib2.urlopen(req, timeout=25).read()
            except:
                print "error:%s" + index;

        soup = BeautifulSoup(cont, 'html.parser', from_encoding='utf-8')
        body = soup.body

        print "Body:%s" % body

        if body == None:
            return None
        elif body == "":
            return None
        else:
            str_body = unicode(str(body), "utf-8")

            while str_body.find("'") != -1 :
                str_body = str_body[:str_body.index("'")] + '`' + str_body[str_body.index("'") + 1:]

        return str_body

    def start(self):
        conn, cursor = self.use_database()
        list_title, list_source, list_desc, list_url, list_type_id, list_pic = self.query_all_type(cursor)
        index = 0
        for url in list_url:
            if index > 14174:
                path = self.parser_html(index, "http://or5zfqk8v.bkt.clouddn.com" + url)
                if path != None:
                    self.insert_into_table(conn, cursor, list_title[index], list_source[index], list_desc[index],
                                           list_url[index], list_type_id[index], list_pic[index], path)
                print "craw:index:%s" % index
            index += 1


spider = Health_New()
spider.start()
