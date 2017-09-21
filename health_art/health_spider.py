# encoding=utf-8
import urllib2
from bs4 import BeautifulSoup
import pymysql

# form http://www.cndzys.com
class Health:
    def __init__(self):
        self.base_url = "http://www.cndzys.com"
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'
        self.headers = {'User-Agent': self.user_agent}

    def use_database(self):
        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', charset='UTF8')
        cursor = conn.cursor()
        cursor.execute("USE health")
        return conn, cursor;

    def insert_into_table(self, conn, cursor, title, source,
                          description, type_id, body):
        sql = '''
        insert into health_yangseng values(null,%s,%s,%s,%d,%s)
        ''' % ("'" + title + "'", "'" + source + "'", "'" + description + "'", + type_id, "'" + body + "'")

        cursor.execute(sql)
        conn.commit()

    def parser_html(self, conn, cursor, link, page):
        req = urllib2.Request(link, headers=self.headers)
        try:
            cont = urllib2.urlopen(req, timeout=25).read()
        except:
            try:
                cont = urllib2.urlopen(req, timeout=35).read()
            except:
                try:
                    cont = urllib2.urlopen(req, timeout=45).read()
                except:
                    print "error: ";

        soup = BeautifulSoup(cont, 'html.parser', from_encoding='utf-8')

        news = soup.find_all('div', class_='news')
        index = 0
        for new in news:
            if index > 14:
                title = new.find('div', class_='news_title').find('h4').find('a').get_text().strip()
                description = new.find('p').get_text().strip()
                lk = new.find('h4').find('a').attrs['href']
                url = self.base_url + lk;
                source, body = self.parser_detail(url)
                self.insert_into_table(conn, cursor, title, source,
                                       description, 5, body)
                print "page:%s,new_index:%d\n\rhtml:%s\n\rtitle:%s"\
                      % (page, index, url,title)
            index += 1;

    def parser_detail(self,url):
        req = urllib2.Request(url, headers=self.headers)

        try:
            cont = urllib2.urlopen(req, timeout=25).read()
        except:
            try:
                cont = urllib2.urlopen(req, timeout=25).read()
            except:
                print "error: ";

        soup = BeautifulSoup(cont, 'html.parser', from_encoding='utf-8')
        sos = soup.find('div', class_='info').find_all('span')
        source = sos[-1].find('a').get_text().strip()
        body = soup.find('div', class_='content_text')

        str_body =  unicode(str(body), "utf-8")

        while str_body.find("'") != -1:
            str_body = str_body[:str_body.index("'")] + '`' + str_body[str_body.index("'") + 1:]
        return source,str_body;

    def start(self):
        conn, cursor = self.use_database()
        for i in range(10):
            if (i == 0):
                continue
            elif i == 1:
                link = self.base_url +"/renqun/laoren/index.html"
            else:
                link = self.base_url+"/renqun/laoren/index%d.html" % i
            if i > 8:
                print "link--%s"% link
                self.parser_html(conn, cursor, link, i)


spider = Health()
spider.start()
