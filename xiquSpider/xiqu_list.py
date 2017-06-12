# encoding=utf-8

import pymysql
import urllib2
import time
from bs4 import BeautifulSoup


class XiquList:
    def __init__(self):
        self.base_url = 'http://www.xiqu5.com'
        self.base_path = 'E:\opera_1\jpg'
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        self.headers = {'User-Agent': self.user_agent}

    def use_database(self):
        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', charset='UTF8')
        cursor = conn.cursor()
        cursor.execute("USE opera")
        return conn, cursor;

    def insert_to_table(self, conn, cursor, title, category, img_path, link):
        sql = '''
        insert into opera_list values(null,%s,%d,%s,%s)
        ''' % ("'" + title + "'", category, "'" + img_path + "'", "'" + link + "'")

        cursor.execute(sql)
        conn.commit()

    def query_all_cate_links(self, conn, cursor):
        sql = '''
        select * from opera_new1
        '''

        cursor.execute(sql)
        rows = cursor.fetchall()

        list_id = []
        list_link = []
        for row in rows:
            list_id.append(row[0])
            list_link.append(row[2])

        return list_id, list_link

    def parser_to_sql(self, conn, cursor, category_id, link):
        req = urllib2.Request(link, headers=self.headers)
        cont = urllib2.urlopen(req)
        soup = BeautifulSoup(cont.read().decode('gb2312', 'ignore').encode('utf-8'), 'html.parser',
                             from_encoding='utf-8')
        d = soup.find('div', id='page')
        s = d.get_text().encode('utf-8')
        page_count = int(s.strip()[s.index('共') - 2:s.index('部') - 5])
        print 'page_count :%d' % page_count
        # +1实际页数+1range 不包括end
        end = page_count / 12 + 1 + 1
        print 'end:' + str(end)
        for pg in range(1, end):
            if (pg == 1):
                if category_id > 94:
                    lis = soup.find('div', class_='left').find_all('li')
                    item = 1;
                    for li in lis:
                        try:
                            a_s = li.find_all('a')
                            img_link = a_s[0].find('img').attrs['src'].strip()
                            item_link = link[:-10] + a_s[1].attrs['href'].strip()
                            title = a_s[1].attrs['title'].strip()
                            if img_link[:5] == 'http:':
                                req = urllib2.Request(img_link, headers=self.headers)
                                resp = urllib2.urlopen(req)
                            else:
                                req = urllib2.Request(self.base_url + img_link, headers=self.headers)
                                resp = urllib2.urlopen(req)
                            path = self.base_path + "\opera_" + str(time.time()).replace('.', '_') + ".jpg"
                            f = open(path, 'wb')
                            f.write(resp.read())
                            f.flush()
                            f.close()
                            print 'craw category:%d,page:%d,item:%d' % (category_id, pg, item)
                            self.insert_to_table(conn, cursor, title, category_id, path, item_link)
                        except:
                            print 'item error'
                            item += 1
                            continue
                    item += 1

            else:
                if not (category_id == 94 and pg < 3):
                  try:
                    l = link[:-5] + '%d.html' % pg
                    req = urllib2.Request(l, headers=self.headers)
                    ct = urllib2.urlopen(req)
                    sp = BeautifulSoup(ct.read().decode('gb2312', 'ignore').encode('utf-8'), 'html.parser',
                                       from_encoding='utf-8')
                    lis = sp.find('div', class_='left').find_all('li')
                    item = 1;
                    for li in lis:
                        a_s = li.find_all('a')
                        img_link = a_s[0].find('img').attrs['src'].strip()
                        item_link = link[:-10] + a_s[1].attrs['href'].strip()
                        title = a_s[1].attrs['title'].strip()
                        canOpen = False
                        try:
                            if img_link[:5] == 'http:':
                                req = urllib2.Request(img_link, headers=self.headers)
                                resp = urllib2.urlopen(req)
                                canOpen = True
                            else:
                                req = urllib2.Request(self.base_url + img_link, headers=self.headers)
                                resp = urllib2.urlopen(req)
                                canOpen = True
                        except:
                              print "jpg open error"
                              print img_link

                        if  canOpen :
                            path = self.base_path + "\opera_" + str(time.time()).replace('.', '_') + ".jpg"
                            f = open(path, 'wb')
                            f.write(resp.read())
                            f.flush()
                            f.close()
                        else:
                            path = self.base_path+'\opera_default.jpg'
                        print 'craw category:%d,page:%d,item:%d' % (category_id, pg, item)
                        self.insert_to_table(conn, cursor, title, category_id, path, item_link)
                        item += 1
                  except:
                      print 'page error'
                      continue



    def start(self):
        conn, cursor = self.use_database()
        list_id, list_link = self.query_all_cate_links(conn, cursor)
        for li in list_id:
            if (li > 93):
                self.parser_to_sql(conn, cursor, li, list_link[li - 1])
            print 'category:' + str(li)


spider = XiquList()
spider.start()
