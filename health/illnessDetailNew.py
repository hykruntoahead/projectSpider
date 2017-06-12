#encoding=utf-8
import pymysql
import urllib2
from bs4 import BeautifulSoup

class IllnessDetail:
    def __init__(self):
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'
        self.headers = {'User-Agent': self.user_agent}

    def use_database(self):
        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', charset='UTF8')
        cursor = conn.cursor()
        cursor.execute("USE health")
        return conn, cursor;

    def query_all_items(self,conn,cursor):
        sql = '''
        select * from illness_new
        '''

        cursor.execute(sql)
        rows = cursor.fetchall()
        list_illness , list_link = [],[]
        for row in rows:
            list_illness.append(row[1])
            list_link.append(row[2])

        return  list_illness,list_link

    def insert_into_table(self, conn, cursor, illness, bingyin,zhengzhuang,zhiliao,yufang):
        sql = '''
           insert into illness_detail_new values(null,%s,%s,%s,%s,%s)
           ''' % ("'" + illness + "'", "'" + bingyin + "'", "'" + zhengzhuang + "'",
                  "'" + zhiliao + "'", "'" + yufang + "'")

        cursor.execute(sql)
        conn.commit()


    def parser_html(self,conn,cursor,illness,link):
        link_1 = link+'bingyin.html'
        link_2 = link+'zhengzhuang.html'
        link_3 = link+'zhiliao.html'
        link_4 = link+'yufang.html'

        req1 = urllib2.Request(link_1, headers=self.headers)
        try:
         cont1 = urllib2.urlopen(req1,timeout=30).read()
        except:
            cont1 = urllib2.urlopen(req1, timeout=20).read()
        soup1= BeautifulSoup(cont1.decode('gb2312', 'ignore').encode('utf-8'), 'html.parser',
                                 from_encoding='utf-8')
        bingyin = str(soup1.find('div',class_='d-js-cont2'))

        req2 = urllib2.Request(link_2, headers=self.headers)
        try:
         cont2 = urllib2.urlopen(req2,timeout=30).read()
        except:
            cont2 = urllib2.urlopen(req2, timeout=20).read()
        soup2 = BeautifulSoup(cont2.decode('gb2312', 'ignore').encode('utf-8'), 'html.parser',
                              from_encoding='utf-8')
        zhengzhuang = str(soup2.find('div',class_='d-js-cont2'))

        req3 = urllib2.Request(link_3, headers=self.headers)
        try:
         cont3 = urllib2.urlopen(req3,timeout=30).read()
        except:
            cont3 = urllib2.urlopen(req3, timeout=20).read()
        soup3 = BeautifulSoup(cont3.decode('gb2312', 'ignore').encode('utf-8'), 'html.parser',
                              from_encoding='utf-8')
        zhiliao =str(soup3.find('div',class_='d-js-cont2'))

        req4 = urllib2.Request(link_4, headers=self.headers)
        try:
         cont4 = urllib2.urlopen(req4,timeout=30).read()
        except:
            cont4 = urllib2.urlopen(req4, timeout=20).read()
        soup4 = BeautifulSoup(cont4.decode('gb2312', 'ignore').encode('utf-8'), 'html.parser',
                                  from_encoding='utf-8')
        yufang =str(soup4.find('div',class_='d-js-cont2'))


        while bingyin.find("'") != -1:
            bingyin = bingyin[:bingyin.index("'")] + '`' + bingyin[bingyin.index("'") + 1:]

        while zhengzhuang.find("'") != -1:
            zhengzhuang = zhengzhuang[:zhengzhuang.index("'")] + '`' + zhengzhuang[zhengzhuang.index("'") + 1:]

        while zhiliao.find("'") != -1:
            zhiliao = zhiliao[:zhiliao.index("'")] + '`' + zhiliao[zhiliao.index("'") + 1:]

        while yufang.find("'") != -1:
            yufang = yufang[:yufang.index("'")] + '`' + yufang[yufang.index("'") + 1:]

        self.insert_into_table(conn,cursor,illness.encode('utf-8'),bingyin,zhengzhuang,zhiliao,yufang)
        print 'craw illness:%s'% illness


    def start(self):
        conn,cursor = self.use_database()
        list_illness,list_link = self.query_all_items(conn,cursor)
        index =0
        for link in list_link:
              if index>41:
                self.parser_html(conn,cursor,list_illness[index],link)
              index+=1
              print 'craw index:%d'% index
spider = IllnessDetail()
spider.start()

