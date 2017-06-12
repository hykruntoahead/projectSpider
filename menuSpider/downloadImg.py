# encoding=utf-8

import urllib2
import pymysql


class ImgDownLoad:
    def __init__(self):
        self.base_path = 'E:\menu_jpg'
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'
        self.headers = {'User-Agent': self.user_agent}

    def init_db(self):
        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', charset='UTF8');
        cursor = conn.cursor();

        cursor.execute("use spider")
        return conn, cursor;

    def query_menu_list(self, conn, cursor):

        list1 = []
        try:
            cursor.execute('select * from menu')
            rows = cursor.fetchall()
        except:
            conn.rollback()
            print "fetchall error"

        for row in rows:
            list1.append(row[0])

            # print 'list::'+str(len(list))
        return list1;

    def query_menu_link(self, conn, cursor, id):


        try:
            cursor.execute('select pic from menu WHERE ID = %d' % (id))
            rows = cursor.fetchall()
        except:
            conn.rollback()
            print "fetchall error"

        li=rows[0];

        print 'li::'+str(li)

        return li[0];

    def query_img_list(self, conn, cursor):

        list = []
        try:
            cursor.execute('select * from menu_img')
            rows = cursor.fetchall()
        except:
            conn.rollback()
            print "fetchall error"

        for row in rows:
            list.append(row[0])

            # print 'list::'+str(len(list))
        return list;

    def create_img_table(self, conn, cursor):
        sql = '''
         create table MENU_IMG(
         ID INT(200) NOT NULL ,
         OLD_LINK TEXT,
         NEW_LINK TEXT ,
         PRIMARY KEY (ID)
         )
         '''

        try:
            cursor.execute(sql)
            conn.commit()
        except:
            conn.rollback()
            print 'create table failed'

        return conn, cursor;

    def insert_to_new_table(self, id, link, path, conn, cursor):
        sql = '''
        INSERT INTO MENU_IMG VALUES (
        %d,%s,%s)''' % (id, "'" + link + "'", "'" + path + "'")
        # try:
        cursor.execute(sql)
        conn.commit()
        # except:
        #     conn.rollback()
        #     print 'insert failed'

    def downloadImg(self, mylist, list1, conn, cursor):
        index=1;
        for id in mylist:
            if id not in list1:
                print "条数%d::%s" %(index,str(id))
                index+=1
                # try:
                #     li = self.query_menu_link(conn, cursor, id)
                #     request = urllib2.Request(li.encode('utf-8'), headers=self.headers)
                #     response = urllib2.urlopen(request)
                #     path = self.base_path + "\menu_" + str(id) + ".jpg"
                #     f = open(path, 'wb')
                #     print str(id) + "---", path
                #     f.write(response.read())
                #     f.flush()
                #     f.close()
                #     self.insert_to_new_table(id, li, path, conn, cursor)
                # except urllib2.URLError, e:
                #     if hasattr(e, "code"):
                #         print e.code
                #     if hasattr(e, "reason"):
                #         print e.reason

    def start(self):
        conn, cursor = self.init_db();
        list = self.query_menu_list(conn, cursor)
        list1 = self.query_img_list(conn, cursor)
        # conn, cursor = self.create_img_table(conn, cursor)
        self.downloadImg(list, list1, conn, cursor)


img_down = ImgDownLoad()
img_down.start()
