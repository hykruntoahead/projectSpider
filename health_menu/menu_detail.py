#encoding=utf-8
import json

import pymysql
import urllib2

class menuDetail:
    def __init__(self):
        self.base_path = 'E:\health_detail'
        self.base_url = 'http://www.tngou.net/api/cook/show?id=%d'
        self.base_img = 'http://tnfs.tngou.net/image'

    def use_db(self):
        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', charset='UTF8')
        cursor = conn.cursor()
        cursor.execute("USE health_menu")
        return conn, cursor;

    def query_list(self,conn,cursor):

        sql = '''
        select * from menu_list
        '''
        cursor.execute(sql)
        rows=cursor.fetchall()

        list_id = []
        for row in rows:
            list_id.append(row[1])

        return  list_id


    def insert_into_table(self,conn,cursor,item_id,name,food,keywords,description,message,img_path):
        sql ='''
        insert into menu_detail values(null,%d,%s,%s,%s,%s,%s,%s)
        '''%(item_id,"'"+name+"'","'"+food+"'","'"+keywords+"'","'"+description+"'","'"+message+"'","'"+img_path+"'")

        cursor.execute(sql)
        conn.commit()

    def parse_json(self,conn,cursor,url,id,item):
        link = url % (id)
        try:
            cont = urllib2.urlopen(link,timeout=20).read()
        except:
          try:
            cont = urllib2.urlopen(link,timeout=20).read()
          except:
            cont =urllib2.urlopen(link,timeout=20).read()

        print  cont;
        result = json.loads(cont);

        item_id = result['id']
        img = self.base_img+result['img']
        path = self.base_path+('\health_menu_detail_%d'%id)+img[-4:];
        try:
            content = urllib2.urlopen(img, timeout=20).read()
        except:
            try:
                content = urllib2.urlopen(img, timeout=20).read()
            except:
                try:
                    content = urllib2.urlopen(img, timeout=20).read()
                except:
                    content = urllib2.urlopen('http://tse4.mm.bing.net/th?id=OIP.M031e557ee9d07e20ea6e2af2a775592do0&w=216&h=147&c=7&rs=1&qlt=90&o=4&pid=1.1', timeout=20).read()
        fout = file(path, 'wb')
        fout.write(content)
        fout.flush()
        fout.close()

        print ('craw item= %d  item_id=%d' % (item,item_id))

    def start(self):
       conn,cursor = self.use_db();
       list_id = self.query_list(conn,cursor);
       item =1;
       for id in list_id:
           if item>4020:
            self.parse_json(conn,cursor,self.base_url,id,item)
           item+=1

spider = menuDetail()
spider.start()