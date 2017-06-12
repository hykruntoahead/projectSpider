#encoding=utf-8
import urllib2

import pymysql
from bs4 import BeautifulSoup


class HealthHtml :
    def __init__(self):
        self.base_path='E:\health_html_2'
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'
        self.headers = {'User-Agent': self.user_agent}

    def use_database(self):
        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', charset='UTF8')
        cursor = conn.cursor()
        cursor.execute("USE health")
        return conn, cursor;

    def query_all_links(self,conn,cursor):
        sql = '''
        select * from health_detail_2n
        '''

        cursor.execute(sql)
        rows = cursor.fetchall()
        list_id,list_title,list_desc,list_type_id,list_link=[],[],[],[],[]
        for row in rows:
            list_id.append(row[0])
            list_title.append(row[1])
            list_desc.append(row[2])
            list_type_id.append(row[3])
            list_link.append(row[4])

        return list_id,list_title,list_desc,list_type_id,list_link


    def insert_into_table(self,conn,cursor,title,source,desc,path,type_id):

         sql = '''
         insert into health_html_2 values(null,%s,%s,%s,%s,%d)
         '''%("'"+title+"'","'"+source+"'","'"+desc+"'","'"+path+"'",type_id)

         cursor.execute(sql)
         conn.commit()


    def parser_html(self,conn,cursor,id,title,desc,type_id,link):
        newlink = 'http://'+link[6:]
        print newlink
        req = urllib2.Request(newlink, headers=self.headers)
        try:
            cont = urllib2.urlopen(req, timeout=5).read()
        except:
            try:
                cont = urllib2.urlopen(req, timeout=15).read()
            except:
                cont = urllib2.urlopen(req, timeout=25).read()

        soup = BeautifulSoup(cont, 'html.parser',
                             from_encoding='utf-8')
        source = soup.find('div',class_='p_arttopab clears').get_text().strip()
        hcont = soup.find('div',class_='p_cleftartbox')
        ps = hcont.find_all('p')
        content = '<div class_="cont">'
        for p in ps:
            content = content+str(p)

        content = content+'</div>'
        path = self.base_path+"\health_2_%d.html"%id
        f = open(path,'w')
        f.write('''
        <!DOCTYPE html>
        <html>
        <head>
        <meta charset="UTF-8"/>
        <title>%s</title>
        </head> '''% title.encode('utf-8'))

        f.write('''
        <body>
        %s
        </body></html>
        '''%(content))
        f.flush()
        f.close()
        self.insert_into_table(conn,cursor,title,source,desc,path,type_id)
        print 'craw id:%d,type_id:%d'%(id,type_id)


    def start(self):
        conn,cursor= self.use_database()
        list_id, list_title, list_desc, list_type_id, list_link = self.query_all_links(conn,cursor)
        for id in list_id:
          if id > 10809:
            self.parser_html(conn,cursor,id,list_title[id-1],list_desc[id-1],list_type_id[id-1],list_link[id-1])



spider = HealthHtml()
spider.start()


