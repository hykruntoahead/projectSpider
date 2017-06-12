#encoding=utf-8
import pymysql
import urllib2
from bs4 import BeautifulSoup

class IllnessDetail:

    def use_database(self):
        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', charset='UTF8')
        cursor = conn.cursor()
        cursor.execute("USE health")
        return conn, cursor;

    def query_all_items(self,conn,cursor):
        sql = '''
        select * from illness
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
           insert into illness_detail values(null,%s,%s,%s,%s,%s)
           ''' % ("'" + illness + "'", "'" + bingyin + "'", "'" + zhengzhuang + "'",
                  "'" + zhiliao + "'", "'" + yufang + "'")

        cursor.execute(sql)
        conn.commit()


    def parser_html(self,conn,cursor,link):
        link_1 = link.replace('jieshao','bingyin')
        link_2 = link.replace('jieshao','zhengzhuang')
        link_3 = link.replace('jieshao','zhiliao')
        link_4 = link.replace('jieshao','yufang')


        cont1 = urllib2.urlopen(link_1,timeout=20).read()
        soup1= BeautifulSoup(cont1.decode('gb2312', 'ignore').encode('utf-8'), 'html.parser',
                                 from_encoding='utf-8')
        bingyins = soup1.find('div',class_='contArticle').find_all('p')
        bingyin = ''
        for p in bingyins:
            bingyin = bingyin+p.get_text().strip()+'/n/r'


        illness = soup1.find('div',class_='topic').find('h2').get_text().strip()
        label = soup1.find('div',class_='topic').find('label')
        if(label!= None):
            illness = illness + label.get_text().strip()


        cont2 = urllib2.urlopen(link_2, timeout=20).read()
        soup2 = BeautifulSoup(cont2.decode('gb2312', 'ignore').encode('utf-8'), 'html.parser',
                              from_encoding='utf-8')
        zhengzhuangs = soup2.find('div', class_='contArticle').find_all('p')
        zhengzhuang = ''
        for p in zhengzhuangs:
            zhengzhuang = zhengzhuang + p.get_text().strip() + '/n/r'


        cont3 = urllib2.urlopen(link_3, timeout=20).read()
        soup3 = BeautifulSoup(cont3.decode('gb2312', 'ignore').encode('utf-8'), 'html.parser',
                              from_encoding='utf-8')
        zhiliaos = soup3.find('div', class_='contArticle').find_all('p')
        zhiliao = ''
        for p in zhiliaos:
            zhiliao = zhiliao + p.get_text().strip() + '/n/r'


        cont4 = urllib2.urlopen(link_4, timeout=20).read()
        soup4 = BeautifulSoup(cont4.decode('gb2312', 'ignore').encode('utf-8'), 'html.parser',
                                  from_encoding='utf-8')
        yufangs = soup4.find('div', class_='contArticle').find_all('p')
        yufang = ''
        for p in yufangs:
            yufang = yufang + p.get_text().strip() + '/n/r'

        while bingyin.find("'") != -1:
            bingyin = bingyin[:bingyin.index("'")] + '`' + bingyin[bingyin.index("'") + 1:]

        while zhengzhuang.find("'") != -1:
            zhengzhuang = zhengzhuang[:zhengzhuang.index("'")] + '`' + zhengzhuang[zhengzhuang.index("'") + 1:]

        while zhiliao.find("'") != -1:
            zhiliao = zhiliao[:zhiliao.index("'")] + '`' + zhiliao[zhiliao.index("'") + 1:]

        while yufang.find("'") != -1:
            yufang = yufang[:yufang.index("'")] + '`' + yufang[yufang.index("'") + 1:]

        self.insert_into_table(conn,cursor,illness,bingyin,zhengzhuang,zhiliao,yufang)
        print 'craw illness:%s'% illness


    def start(self):
        conn,cursor = self.use_database()
        list_illness,list_link = self.query_all_items(conn,cursor)
        index =0
        for link in list_link:
            self.parser_html(conn,cursor,link)
            index+=1
spider = IllnessDetail()
spider.start()

