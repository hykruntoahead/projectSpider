#encoding=utf-8

import pymysql
import urllib2
from bs4 import BeautifulSoup

class HealthDetail:
    def __init__(self):
        self.base_url='http://www.fx120.net/'
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'
        self.headers = {'User-Agent': self.user_agent}

    def use_database(self):
        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', charset='UTF8')
        cursor = conn.cursor()
        cursor.execute("USE health")
        return conn, cursor;

    def query_all_items(self,conn,cursor):
        sql = '''
        select * from health_type_2
        '''

        cursor.execute(sql)
        rows = cursor.fetchall()
        list_type_id = []
        list_link = []
        list_page_size = []

        for row in rows :
            list_type_id.append(row[0])
            list_link.append(row[2])
            list_page_size.append(row[3])

        return  list_type_id,list_link,list_page_size


    def insert_into_table(self,conn,cursor,title,desc,link,type_id):
        conn.escape(desc)
        conn.escape(title)
        sql = '''
        insert into health_detail_2 values(null, %s,%s,%d,%s)
        '''%("'"+title+"'","'"+desc+"'",type_id,"'"+link+"'")

        cursor.execute(sql)
        conn.commit()

    def parser_html(self,conn,cursor,type_id,link,page_size):
        for page in range(page_size):
          if not (type_id==10 and page<144):
            new_link = link +'List_%d.html'%(page+1)

            print 'craw new_link:%s'% new_link
            req =  urllib2.Request(new_link.encode('utf-8'), headers=self.headers)
            try:
                cont = urllib2.urlopen(req,timeout=10).read()
            except:
                try:
                    cont = urllib2.urlopen(req,timeout=20).read()
                except:
                    try:
                        cont = urllib2.urlopen(req,timeout=30).read()
                    except Exception as e:
                        print e
                        continue

            soup = BeautifulSoup(cont, 'html.parser',
                                     from_encoding='utf-8')

            wfs = soup.find_all('div',class_='w_fl')
            print str(len(wfs))

            for wf in wfs:
                title = wf.find('h3').get_text().strip().encode('utf-8')
                item_link = self.base_url+wf.find('h3').find('a').attrs['href'].encode('utf-8')
                d = wf.find('p').get_text().strip()
                a = wf .find('p').find('a').get_text().strip()
                desc = d.replace(a,"").encode('utf-8')
                if title.find('"')!=-1:
                    title.replace('"','\\\"')
                if desc.find('"')!=-1:
                    desc = desc[:desc.index('"')] + '`' + desc[desc.index('"') + 1:]
                if title.find("'") != -1:
                    title.replace("'", "''")
                while desc.find("'") != -1:
                   desc =desc[:desc.index("'")] +'`'+desc[desc.index("'")+1:]


                self.insert_into_table(conn,cursor,title,desc,item_link,type_id)
                print 'craw page=%d,title:%s,type_id=%d'%(page,title,type_id)


    def start(self):
        conn,cursor = self.use_database()
        list_type_id,list_link,list_page_size = self.query_all_items(conn,cursor)

        index=0;
        for link in list_link:
            if index>8:
                self.parser_html(conn,cursor,list_type_id[index],link,list_page_size[index])
            index+=1
            print 'craw type_link:%s' % (link)

spider = HealthDetail()
spider.start()




