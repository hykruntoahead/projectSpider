#encoding=utf-8

import urllib2
import  pymysql
from bs4 import BeautifulSoup

class XQ_Spider:
    def  __init__(self):
        self.base_url='http://www.1ting.com/'
        self.base_path="E:\opera_jpg"

    def use_database(self):
        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', charset='UTF8')
        cursor = conn.cursor()
        cursor.execute("USE opera")
        return conn,cursor;

    def query_all_link(self,conn,cursor):
        sql = '''
         select * from opera_categories
         '''
        list = []
        try:
            cursor.execute(sql)
            rows = cursor.fetchall()
        except:
            conn.rollback()
            print "fetchall error"

        for row in rows:
            if(row[0]>33):
                list.append(row[2])

        return list;

    def insert_to_table(self,conn,cursor,index,page,title,img_link,type,video_link):
        sql = ''' INSERT INTO opera_detail VALUES (%d ,%d, %s ,  %s ,%s,%s)''' % (index,page,
                "'" + title.encode('utf-8') + "'", "'" + img_link.encode('utf-8') + "'",
                "'" + type.encode('utf-8') + "'",  "'" + video_link.encode('utf-8') + "'" )
        # try:
        cursor.execute(sql)
        conn.commit()
        # except:
        #     conn.rollback()
        #     print 'insert failed'



    def parser_html(self,conn,cursor,url,page):
        cont=urllib2.urlopen(url)
        soup= BeautifulSoup(cont.read(),'html.parser',from_encoding='utf-8')
        lis=soup.find('ul',class_='divlist').find_all('li')
        index = 1

        type=soup.find('h3',class_='subhead').get_text()
        for li in  lis:

                 link = self.base_url+li.find('a').attrs['href'].strip()
                 title=li.find('p').find('a').get_text()
                 img= self.base_url + li.find('a').find('img').attrs['src']
                 req = urllib2.urlopen(link)
                 sp=BeautifulSoup(req.read(),'html.parser',from_encoding='utf-8')
                 link=sp.find('embed').attrs['src'].strip()
                 response = urllib2.urlopen(img)
                 path = self.base_path + "\opera_"+type+'_'+ str(page)+'_'+str(index) + ".jpg"
                 f = open(path, 'wb')
                 print 'download:'+str(index) + "---", path
                 f.write(response.read())
                 f.flush()
                 f.close()
                 self.insert_to_table(conn,cursor,index,page,title,path,type,link)
                 index += 1



    def start(self):
        conn,cursor=self.use_database()
        list = self.query_all_link(conn,cursor)
        print len(list);
        # for li in list:
        #         d_url=li;
        #         page=1
        #         self.parser_html(conn,cursor,d_url,page)

spider=XQ_Spider()
spider.start()
