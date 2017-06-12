#encoding=utf-8
import pymysql
import urllib2
from bs4 import BeautifulSoup

class HealthDetail:
    def __init__(self):
        self.base_url='http://laoren.jiankangzu.com'
    def use_databse(self):
        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', charset='UTF8')
        cursor = conn.cursor()
        cursor.execute("USE health")
        return conn, cursor;

    def query_all_type(self,conn,cursor):
        sql = '''
        select * from health_new_type
        '''
        cursor.execute(sql)
        rows = cursor.fetchall()

        list_id = []
        list_link = []

        for row in rows:
            list_id.append(row[0])
            list_link.append(row[2])


        return list_id,list_link



    def insert_into_table(self,conn,cursor,title,type_id,link):
        sql = '''
        insert into health_detail values (null,%s,%d,%s)
        '''%("'"+title.replace("'"," ")+"'",type_id,"'"+link+"'")

        try:
            cursor.execute(sql)
            conn.commit()
        except:
            print  'insert_error'
            conn.rollback()


    def parser_html(self,conn,cursor,id,link):
        cont = urllib2.urlopen(link)
        soup = BeautifulSoup(cont.read(),'html.parser',from_encoding='utf-8')
        pagesize = int(soup.find('div',id='page').find_all('a')[-1].get_text())
        lis=soup.find('div',class_='mainl_list ').find_all('li')
        flag=1
        if id !=8:
            for li in lis:
                a=li.find('a').attrs['href']
                title = li.find('a').get_text().strip()
                self.insert_into_table(conn,cursor,title,id,a)
                print 'craw type:%d,page:1,index:%d'%(id,flag)
                flag+=1

        for page in range(1,pagesize):
          if not (id ==8 and page<=2):
            new_link = link[:-2]+str(page+1)
            ct = urllib2.urlopen(new_link)
            sp = BeautifulSoup(ct.read(),'html.parser',from_encoding='utf-8')
            lis = sp.find('div', class_='mainl_list ').find_all('li')
            index = 1
            for li in lis:
                a = li.find('a').attrs['href']
                title = li.find('a').get_text().strip()
                self.insert_into_table(conn, cursor, title, id, a)
                print 'craw type:%d,page:%d,index:%d' % (id,(page+1),index)
                index += 1


    def start(self):
        conn,cursor = self.use_databse()
        list_id,list_link = self.query_all_type(conn,cursor)
        for id in list_id:
            if id>7:
                self.parser_html(conn,cursor,id,list_link[id-1])


spider = HealthDetail()
spider.start()





