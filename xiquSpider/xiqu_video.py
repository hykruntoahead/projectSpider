# encoding=utf-8
import pymysql
import urllib2
from  bs4 import BeautifulSoup
import re


class XiquVideo:
    def __init__(self):
        self.base_url = 'http://www.xiqu5.com'
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        self.headers = {'User-Agent': self.user_agent}

    def use_database(self):
        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', charset='UTF8')
        cursor = conn.cursor()
        cursor.execute("USE opera")
        return conn, cursor;

    def insert_into_video_table(self, conn, cursor, link_id, jishu, title, video_link):
        sql = '''
        insert into opera_video values(null,%d,%s,%s,%s)
        ''' % (link_id, "'" + jishu + "'", "'" + title + "'", "'" + video_link + "'")

        cursor.execute(sql)
        conn.commit()

    def query_all_list(self, conn, cursor):

        sql = '''
        select * from opera_list
        '''

        cursor.execute(sql)
        rows = cursor.fetchall()

        list_id = []
        list_link = []
        for row in rows:
            list_id.append(row[0])
            list_link.append(row[4])

        return list_id, list_link

    def parser_html(self, conn, cursor, id, link):
        print link
        req = urllib2.Request(link, headers=self.headers)
        cont = urllib2.urlopen(req)
        soup = BeautifulSoup(cont.read().decode('gb2312', 'ignore').encode('utf-8'), 'html.parser',
                             from_encoding='utf-8')
        try:
            bda = soup.find('div', class_='bord demand mtop').find(class_='demand')
            play_as = bda.find_all('a')
            js_index = 1
            for a in play_as:
                if ((id == 89956 and js_index >171) or id >89956):
                    v_link = link + a.attrs['href']
                    jishu = a.get_text().strip().encode('utf-8')
                    if jishu.find('缺') == -1:
                        # request = urllib2.Request(v_link, headers=self.headers)
                        ct = urllib2.urlopen(v_link)
                        sp = BeautifulSoup(ct.read().decode('gb2312', 'ignore').encode('utf-8'), 'html.parser',
                                           from_encoding='utf-8')
                        title = sp.find('div', class_='bord mtop cen').find('h1').get_text().strip()[:-6].encode(
                            'utf-8')
                        try:
                            swfs = sp.find('div', id='xiqu5flash')
                            scrip_text = swfs.get_text().strip()
                            sobj = re.search(r'var xiqu5 = new SWFObject(.*?),(.*)', scrip_text)
                            vd_link = sobj.group(1)[2:-1]
                        except:
                            try:
                                swfs = sp.find('div', class_='view500400').find('embed')
                                vd_link = swfs.attrs['src'].strip()
                                # print swfs
                                print vd_link
                            except:
                                print 'swf error'
                                vd_link = 'http://error'

                        if vd_link[:4] == 'http':
                            video_link = vd_link.encode('utf-8')
                        else:
                            video_link = self.base_url + vd_link.encode('utf-8')
                    else:
                        title = soup.find('div', class_='left').find(class_='g2').find('h4').get_text().strip().encode(
                            'utf-8') + ' %s' % jishu
                        video_link = "http：//error"

                    # print 'craw title:%s ' % title
                    # print 'craw video_link:%s' % video_link
                    print 'js_index:%d' % js_index

                    self.insert_into_video_table(conn, cursor, id, jishu, title, video_link)
                js_index += 1

        except:
          try:
            adg = soup.find('div',class_='left').find('div',class_='adgg').find('img')
            title = adg.attrs['alt'].strip().encode('utf-8')
            jishu='第1集'
            video_link = 'http://error'
            self.insert_into_video_table(conn, cursor, id, jishu, title, video_link)
          except:
            title ='404错误'
            jishu = '第1集'
            video_link = 'http://error'
            self.insert_into_video_table(conn, cursor, id, jishu, title, video_link)



    def start(self):
        conn, cursor = self.use_database()
        list_id, list_link = self.query_all_list(conn, cursor)
        index = 0;
        for id in list_id:
            if id > 89955:
                self.parser_html(conn, cursor, id, list_link[index])
                print 'id:' + str(id)
            index += 1


spider = XiquVideo()
spider.start()
