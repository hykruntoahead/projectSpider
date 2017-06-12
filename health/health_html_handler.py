#encoding=utf-8

import pymysql
import urllib2
from bs4 import BeautifulSoup
import time
class healthHandler:
    def __init__(self):
        self.base_path='E:\health_new_html'
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'
        self.headers = {'User-Agent': self.user_agent}


    def use_databse(self):
        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', charset='UTF8')
        cursor = conn.cursor()
        cursor.execute("USE health")
        return conn, cursor;

    def query_all_item(self,conn,cursor):
        sql = '''
        select * from health_detail
        '''

        cursor.execute(sql)
        rows=cursor.fetchall()

        list_id=[]
        list_type_id=[]
        list_link=[]

        for row in rows:
            list_id.append(row[0])
            list_type_id.append(row[2])
            list_link.append(row[3])

        return list_id,list_type_id,list_link


    def insert_into_table(self,conn,cursor,title,source,desc,path,type_id,isnull):

        sql ='''
        insert into health_new_html values(null,%s,%s,%s,%s,%d,%d)
        '''%("'"+title.replace("'"," ")+"'","'"+source+"'","'"+desc.replace("'"," ")+"'","'"+path+"'",type_id,isnull)

        cursor.execute(sql)
        conn.commit()



    def parser_html(self,conn,cursor,id,type_id,url):
        # req =  urllib2.Request(url.encode('utf-8'), headers=self.headers)
        try:
            cont = urllib2.urlopen(url,timeout=5).read()
        except:
           try:
               cont = urllib2.urlopen(url,timeout=10).read()
           except:
            try:
               cont = urllib2.urlopen(url, timeout=20).read()
            except:
                cont = urllib2.urlopen(url, timeout=30).read()

        try:
            soup = BeautifulSoup(cont,'html.parser',from_encoding='utf-8')
        except:
            soup = BeautifulSoup(cont, 'html.parser', from_encoding='utf-8')

        main = soup.find('div',class_='main_left')
        hart_box = main.find('div',class_='border omanbg1 art_box')
        h1=hart_box.find('h1')
        title=h1.get_text().strip()
        hsource=hart_box.find('div',class_='date')
        source =hsource .get_text().strip()
        hsum = main.find('p',class_='summary')
        summary = hsum.get_text().strip()
        hcontent = main.find('div',class_="art_con",id='contentText')
        isnull = 0
        if(hcontent.get_text().strip()=='div>'):
            isnull = 1
        path = self.base_path+"\health_new_%d.html"%id
        fout = open(path, 'w')
        fout.write('<!DOCTYPE html>')
        fout.write("<html>")
        fout.write('''
                <head>
        		<meta charset="UTF-8">
        	    </head>
                ''')
        fout.write("<body>")
        fout.write('<div>')
        fout.write(str(h1))
        fout.write(str(hsource))
        fout.write(str(hsum))
        fout.write(str(hcontent))
        fout.write('</div>')
        fout.write("</body>")
        fout.write("</html>")
        fout.close()

        self.insert_into_table(conn,cursor,title,source,summary,path,type_id,isnull)
        print 'craw id;%d---title:%s---isnull:%d'%(id,title,isnull)


    def start(self):
        conn,cursor = self.use_databse()
        list_id,list_type_id,list_link = self.query_all_item(conn,cursor)
        for id in list_id:
           if id >109775:
            self.parser_html(conn,cursor,id,list_type_id[id-1],list_link[id-1])

spider = healthHandler()
spider.start()



