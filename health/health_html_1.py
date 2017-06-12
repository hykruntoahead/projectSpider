#encoding=utf-8
import urllib2
import pymysql
from  bs4 import BeautifulSoup
import re

class HealthHtml:
    def __init__(self):
        self.base_path='E:\health_html_1'
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'
        self.headers = {'User-Agent': self.user_agent}
    def use_database(self):
        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', charset='UTF8')
        cursor = conn.cursor()
        cursor.execute("USE health")
        return conn, cursor;

    def query_all_items(self,conn,cursor):
        sql = '''
        select * from health_detail_1
        '''

        cursor.execute(sql)
        rows = cursor.fetchall()

        list_type_id, list_link=[],[]

        for row in rows:
            list_type_id.append(row[2])
            list_link.append(row[3])


        return list_type_id,list_link




    def insert_into_table(self,conn,cursor,title,source,desc,content,type_id):

        sql = '''
        insert into health_html_1 values(null,%s,%s,%s,%s,%d)
        '''%("'"+title+"'","'"+source+"'","'"+desc+"'","'"+content+"'",type_id)

        cursor.execute(sql)
        conn.commit()

    def parser_html(self,conn,cursor,id,type_id,link):

        print 'link:%s'% link
        req = urllib2.Request(link.encode('utf-8'), headers=self.headers)
        try:
            cont = urllib2.urlopen(link, timeout=5).read()
        except:
            try:
                cont = urllib2.urlopen(link, timeout=15).read()
            except:
                cont = urllib2.urlopen(link, timeout=25).read()

        soup = BeautifulSoup(cont.decode('gb2312', 'ignore').encode('utf-8'), 'html.parser',
                                 from_encoding='utf-8')

        try:
            abox = soup.find('div', id='art_box').find('div',class_='art_box')
            title = abox.find('h1').get_text().strip().encode('utf-8')
            source = abox.find('div', class_='date').get_text().strip().encode('utf-8')
        except:
          try:
            title = soup.find('title').get_text().strip().encode('utf-8')
            source = '时间未知 39健康网'
          except:
              abox = soup.find('div', id='art_box').find('div', class_='art_box')
              title = abox.find('h1').get_text().strip().encode('utf-8')
              source = abox.find('div', class_='date').get_text().strip().encode('utf-8')
            # abox = soup.find('div',id='artbox')
            # title = abox.find('h1').get_text().strip().encode('utf-8')
            # source = abox.find('div',class_='info').get_text().strip().encode('utf-8')
        try:
            desc = soup.find('p',class_='summary').get_text().strip().encode('utf-8')
            if desc.find('>') != -1:
                print 'desc'
                m = re.search(r'(.*?)</', desc)
                desc = m.group(1)
        except:
            desc = '暂无摘要'

        try :
            art_con= soup.find('div',class_='art_con',id='contentText');
            sc = art_con.find('div',class_='hzh_botleft')
            content = str(art_con).replace(str(sc),"")
        except:
          try:
              art_con = soup.find('div', class_='wrap');
              sc = art_con.find('div', class_='hzh_botleft')
              content = str(art_con).replace(str(sc), "")
          except:
              content = str(soup.find('div',class_='article'))

        path = self.base_path + "\health_new_%d.html" % id
        fout = open(path, 'w')
        fout.write('<!DOCTYPE html>')
        fout.write("<html>")
        fout.write('''
                        <head>
                		<meta charset="UTF-8">
                	    </head>
                        ''')
        fout.write("<body>")
        fout.write('<h1>'+title+'<br></h1>')
        fout.write(source+'<br>')
        fout.write('<h3>'+desc+'<br></h3>')
        fout.write(str(content))
        fout.write("</body>")
        fout.write("</html>")
        fout.close()

        self.insert_into_table(conn,cursor,title,source,desc,path,type_id)



    def start(self):
        conn,cursor = self.use_database()
        list_type_id, list_link= self.query_all_items(conn,cursor)
        index = 0
        for link in list_link:
          if index > 20970:
               self.parser_html(conn,cursor,index,list_type_id[index],link)
               print 'craw index:%d'% index
          index += 1

spider = HealthHtml()
spider.start()








