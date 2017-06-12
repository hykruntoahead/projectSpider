#encoding=utf-8
import urllib2
from bs4 import BeautifulSoup
import pymysql


class HealthDetail:
    def __init__(self):
        self.tuple=(121,102,95,57,45,5,8,10)


    def use_database(self):
        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', charset='UTF8')
        cursor = conn.cursor()
        cursor.execute("USE health")
        return conn, cursor;

    def query_all_type(self,conn,cursor):
        sql = '''
        select * from health_type_1
        '''

        cursor.execute(sql)
        rows = cursor.fetchall()


        list_id = []
        list_link = []

        for row in rows:
            list_id.append(row[0])
            list_link.append(row[2])


        return  list_id,list_link



    def insert_into_table(self,conn,cursor,title,type_id,item_link):
         sql = '''
         insert into health_detail_1 values(null,%s,%d,%s)
         '''%("'"+title+"'",type_id,"'"+item_link+"'");

         cursor.execute(sql)
         conn.commit()



    def parser_html(self,conn,cursor,type_id,link):
        for page in range(self.tuple[type_id-1]):
            if (page==0):
                new_link = link+'index.html'
            else:
                new_link = link +"index_%d.html"% page
            print new_link
            try:
                    cont = urllib2.urlopen(new_link,timeout=5).read()
            except:
                  try:
                      cont = urllib2.urlopen(new_link, timeout=15).read()
                  except:
                      cont = urllib2.urlopen(new_link, timeout=25).read()

            soup = BeautifulSoup(cont.decode('gb2312', 'ignore').encode('utf-8'), 'html.parser',
                                 from_encoding='utf-8')

            list = soup.find('div',class_='listbox').find_all('li')
            index =1
            for li in list :
                title = li.find('a').get_text().strip()
                item_link = li.find('a').attrs['href']
                self.insert_into_table(conn,cursor,title,type_id,item_link)
                index+=1
                print 'craw type_id:%d,page:%d,item:%d '%(type_id,page,index)


    def start(self):
        conn,cursor = self.use_database()
        list_id ,list_link = self.query_all_type(conn,cursor)
        for id in list_id:
           if id >1:
            self.parser_html(conn,cursor,id,list_link[id-1])


spider = HealthDetail()
spider.start()


