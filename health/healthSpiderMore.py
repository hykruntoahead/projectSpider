#encoding=utf-8
import pymysql
import urllib2
from bs4 import BeautifulSoup
class healthSpiderMore:
    def __init__(self):
        self.base_url= 'http://laoren.ewsos.com'

    def use_database(self):
        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', charset='UTF8')
        cursor=conn.cursor()
        cursor.execute("USE health")
        return conn,cursor

    def query_type_links(self,conn,cursor):
        sql ='''
        select * from health_type
        '''

        cursor.execute(sql)
        rows = cursor.fetchall()
        list_id=[]
        list_link=[]
        for row in rows:
            list_id.append(row[0])
            list_link.append(row[2])

        return  list_id,list_link

    def insert_into_table(self,conn,cursor,title,t_id,local_link):
        sql='''
        insert into health_detail values (null,%s,%d,%s)
        '''%("'"+title+"'",t_id,"'"+local_link+"'")


        cursor.execute(sql)
        conn.commit()

    def parser_html(self,conn,cursor,id,link):
        cont = urllib2.urlopen(link)

        soup = BeautifulSoup(cont.read().decode('gb2312', 'ignore').encode('utf-8'), 'html.parser',
                             from_encoding='utf-8')


        lis = soup.find('div',class_='Con_L').find('div',class_='topic').find_all('li')
        index = 1;
        for li in lis:
            title = li.find_all('a')[-1].get_text()
            h_link = li.find_all('a')[-1].attrs['href']
            self.insert_into_table(conn,cursor,title,id,h_link)
            print 'craw type_id=%d ,page=%d,index=%d'% (id,1,index)
            index+=1

        page_as=soup.find('div',class_='art_page').find_all('a')
        str = page_as[-1].attrs['href'].strip()
        page_size = int(str[str.index('-')+1:str.index('.html')])
        print 'craw page_size:%d'%page_size
        for i in range(1,page_size):
            lk = link+"index-%d.html"% i
            ct = urllib2.urlopen(lk)

            soup = BeautifulSoup(ct.read().decode('gb2312', 'ignore').encode('utf-8'), 'html.parser',
                                 from_encoding='utf-8')

            lis = soup.find('div', class_='Con_L').find('div', class_='topic').find_all('li')
            index = 1
            for li in lis:
                title = li.find_all('a')[-1].get_text()
                h_link = li.find_all('a')[-1].attrs['href']
                self.insert_into_table(conn, cursor, title, id, h_link)
                print 'craw type_id=%d ,page=%d,index=%d' % (id, i+1, index)
                index += 1


    def start(self):
        conn,cursor = self.use_database()
        list_id,list_link = self.query_type_links(conn,cursor)
        for id in list_id:
            self.parser_html(conn,cursor,id,list_link[id-1])

spider = healthSpiderMore()
spider.start()



