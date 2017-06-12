#encoding=utf-8
import pymysql
import urllib2
from bs4 import BeautifulSoup

class healthSpiderHtmlHandler:
    def __init__(self):
        self.base_url='http://laoren.ewsos.com'
        self.base_path='E:\health_html'
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'
        self.headers = {'User-Agent': self.user_agent}

    def use_database(self):
        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', charset='UTF8')
        cursor = conn.cursor()
        cursor.execute("USE health")
        return conn,cursor

    def query_all_html(self,conn,cursor):
        sql = '''
        select * from health_detail
        '''

        cursor.execute(sql)
        rows=cursor.fetchall()

        list_id = []
        list_link =[]


        for row in rows:
            list_id.append(row[0])
            list_link.append(row[3])


        return list_id,list_link


    def insert_into_table(self,conn,cursor,title,source,desc,html_path,link_id):
        sql ='''
        insert into health_html values(null,%s,%s,%s,%s,%d)
        '''%("'"+title+"'","'"+source+"'","'"+desc+"'","'"+html_path+"'",link_id)

        cursor.execute(sql)
        conn.commit()


    def parser_html(self,conn,cursor,id ,link):
        request = urllib2.Request(link.encode('utf-8'), headers=self.headers)
        cont = urllib2.urlopen(request)
        soup = BeautifulSoup(cont.read().decode('gb2312', 'ignore').encode('utf-8'), 'html.parser',
                             from_encoding='utf-8')

        content = soup .find('div',class_='cont_left')
        h_title = content.find_all('h1')[0]
        title = h_title.get_text().strip()
        h_source = content.find('div',class_='art_box_guanzhu').find('li',class_='l1')
        source = h_source.get_text().strip()
        h_desc = content.find('div',class_='summary')
        desc = h_desc.find('p').get_text().strip()
        h_txt = content.find('div',class_='box_txt')

        path = self.base_path+'\health_laoren_%d.html'%id
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
        fout.write(str(h_title))
        fout.write('</div>')

        fout.write('<div>')
        fout.write('<ul>')
        fout.write(str(h_source))
        fout.write('</ul>')
        fout.write('</div>')

        fout.write(str(h_desc))
        fout.write(str(h_txt))
        fout.write("</body>")
        fout.write("</html>")

        fout.close()

        self.insert_into_table(conn,cursor,title,source,desc,path,id)
        print 'craw linkid;%d----path;%s'%(id,path)



    def startCraw(self):
        conn,cursor =self.use_database();
        list_id ,list_link = self.query_all_html(conn,cursor)

        for id in list_id:
          if id >281:
            self.parser_html(conn,cursor,id,list_link[id-1])



spider = healthSpiderHtmlHandler()
spider.startCraw()




