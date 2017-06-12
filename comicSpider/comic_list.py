# encoding=utf-8
# .decode('gb2312','ignore').encode('utf-8')
import pymysql
import urllib2
import time
from bs4 import BeautifulSoup


class ComicList:
    def __init__(self):
        self.base_path = 'E:\comic\jpg'

    def use_database(self):
        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', charset='UTF8')
        cursor = conn.cursor()
        cursor.execute("USE comic")
        return conn, cursor;

    def query_all_comp(self, cursor):
        sql = '''
        select * from comic_comp
        '''
        list = []
        cursor.execute(sql);
        rows = cursor.fetchall()

        for row in rows:
            list.append(row[2])

        return list;

    def insert_into_table(self, conn, cursor, title, time, img_path, video_path, origin):
        sql = '''
        insert into comic_list_details values (null,%s,%s,%s,%s,%s)
        ''' % ("'" + title + "'", "'" + time + "'", "'" + img_path + "'", "'" + video_path + "'", "'" + origin + "'")

        cursor.execute(sql)
        conn.commit()

    def parser_net_html(self, conn, cursor, list):
        debug = False
        li_count=1;
        for li in list:
            print 'li_count = %d' % li_count
            if li_count >301:
                try:
                    cont = urllib2.urlopen(li)
                    soup = BeautifulSoup(cont.read().decode('GBK', 'ignore').encode('utf-8'), 'html.parser',
                                         from_encoding='utf-8')
                except:
                    li_count += 1;
                    continue
                try:
                    pages = soup.find('div', class_='pages').find_all('a')
                    end = (pages[-1].attrs['href'])
                except:
                    debug = True

                if (end[-7] != '_' or debug):
                    int_end = 2;
                    debug = False
                else:
                    int_end = int(end[-6]) + 1
                print 'int_end = %d' % (int_end)
                for page in range(1, int_end):
                    index = 1
                    l = li[:-5] + "_%d.html" % (page)
                    print  l
                    try:
                        cont = urllib2.urlopen(l)
                        soup = BeautifulSoup(cont.read().decode('GBK', 'ignore').encode('utf-8'), 'html.parser',
                                             from_encoding='utf-8')
                        dls = soup.find('div', class_='innerViewLeft').find_all('dl')
                        for dl in dls:
                            time_len = dl.find('span', class_='time').get_text().encode('utf-8')
                            a = dl.find('a', class_='pic')
                            title = a.attrs['title'].strip().encode('utf-8')
                            video_link = a.attrs['href'].strip().encode('utf-8')
                            img = a.find('img').attrs['src'].strip()
                            origin = '酷六网'
                            resp = urllib2.urlopen(img)
                            path = self.base_path + "\comic_" + str(time.time()).replace('.', '_') + ".jpg"
                            f = open(path, 'wb')
                            f.write(resp.read())
                            f.flush()
                            f.close()
                            print 'craw :page=%d,index=%d,title=%s' % (page, index, title)
                            self.insert_into_table(conn, cursor, title, time_len, path, video_link, origin)
                            index += 1
                    except:
                        print  'failed'
            li_count+=1;



    def start(self):
        conn, cursor = self.use_database()
        list = self.query_all_comp(cursor)
        self.parser_net_html(conn, cursor, list)


spider = ComicList()
spider.start()
