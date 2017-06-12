#encoding=utf-8
import pymysql
import urllib2
import json

class TvState_Spider:

    def use_database(self):
        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', charset='UTF8')
        cursor = conn.cursor()
        cursor.execute("USE tv_state")
        return conn, cursor;

    def insert_into_table(self,conn,cursor,name,rel,link):
        sql = '''
        insert into tv values(null,%s,%s,%s)
        '''%("'"+name+"'","'"+rel+"'","'"+link+"'")

        cursor.execute(sql)
        conn.commit()


    def parser_json(self,conn,cursor,url):
        cont = urllib2.urlopen(url,timeout=20).read()

        js = json.loads(cont)

        results = js['result']
        for result in results:
            name= result['channelName']
            rel = result['rel']
            link = result['url']
            self.insert_into_table(conn,cursor,name,rel,link)
            print 'craw name:%s'% name

    def start(self):
        conn,cursor = self.use_database()
        for i in range(1,7):
            link = "http://japi.juhe.cn/tv/getChannel?pId=%d&key=8b56396d12cb1738614e1b347c1a03bf"% i
            self.parser_json(conn,cursor,link)
            print 'craw pId:%d'%i

spider = TvState_Spider()
spider.start()
