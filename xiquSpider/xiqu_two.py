#encoding=utf-8

# sql = '''
# var xiqu5 = new SWFObject('/Player/cntvPlayer.swf?videoId=20101228100883&videoCenterId=2e638c5f80554f2090d3843b87ee3b19',
# 'SwfObject', '722', '400', '8', '#000000');
# xiqu5.addParam('allowScriptAccess', 'always');
# xiqu5.addParam('allowFullScreen', 'true');
# xiqu5.addParam('movie', '/Player/cntvPlayer.swf?videoId=20101228100883&videoCenterId=2e638c5f80554f2090d3843b87ee3b19');
# xiqu5.addParam('quality', 'high');xiqu5.addParam('bgcolor', '#000000');xiqu5.write('xiqu5flash');
# '''
#
#
# sobj=re.search( r'var xiqu5 = new SWFObject(.*?),(.*)',sql)
#
# print 'http://www.xiqu5.com/'+sobj.group(1)[2:-1]
import pymysql
import urllib2
from bs4 import BeautifulSoup
class XiquTwo:
    def __init__(self):
        self.base_url='http://www.xiqu5.com'

    def use_database(self):
        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', charset='UTF8')
        cursor = conn.cursor()
        cursor.execute("USE opera")
        return conn, cursor;

    def insert_to_table(self,conn,cursor,category,link):
        sql = '''
        insert into opera_new1 values(NULL ,%s,%s)
        '''% ("'"+category+"'","'"+link+"'")

        cursor.execute(sql)
        conn.commit()

    def parser_html(self,conn,cursor):
        cont = urllib2.urlopen(self.base_url)
        soup = BeautifulSoup(cont.read().decode('gb2312','ignore').encode('utf-8'),'html.parser',from_encoding='utf-8')
        accs= soup.find_all('div',class_='acc2')
        index=1
        for acc in accs:
            list_a = acc.find_all('a')
            i=1;
            for li in list_a:
                link=li.attrs['href'].strip()
                if(len(link)!=0):
                    self.insert_to_table(conn,cursor,li.get_text(),self.base_url+link)
                print 'craw div:%d,a:%d'%(index,i)
                i+=1
            index+=1


    def start(self):
        conn,cursor = self.use_database()
        self.parser_html(conn,cursor)

spider = XiquTwo()
spider.start()
