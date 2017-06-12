#encoding=utf-8
import json
import urllib2

import pymysql


class ListSpider:

    def __init__(self):
        self.base_url="http://api.avatardata.cn/Cook/List?key=8b01fc974ed0445cbe7e987879d9d830&id=%d&page=%d&rows=20"
        self.img_folder_path="E:\health_menu"

    def use_db(self):
        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', charset='UTF8')
        cursor = conn.cursor()
        cursor.execute("USE health_menu")
        return conn, cursor;

    def query_classify(self,conn,cursor):
        sql = '''
        select * from classify
        '''
        cursor.execute(sql)
        rows = cursor.fetchall()

        list_id =[]
        for row in rows:
            list_id.append(row[1])
        return list_id

    def insert_into_table(self,conn,cursor,item_id,name,food,keyword,description,img_path,classify_id):

        sql = '''
        insert into menu_list values(null,%d,%s,%s,%s,%s,%s,%d)
        '''%(item_id,"'"+name+"'","'"+food+"'","'"+keyword+"'","'"+description+"'", "'"+img_path+"'",classify_id)

        cursor.execute(sql)
        conn.commit()

    def parser_json(self,conn,cursor,url,classify_id):

        page =1;
        results = []
        while( page==1 or (len(results)>0 and  page>1)):
            print 'craw page=%d'%page
            if(not(page<49 and classify_id==68)):
               item =1;
               link = url%(classify_id,page)
               try:
                   cont = urllib2.urlopen(link, timeout=20).read()
               except:
                 try:
                   cont = urllib2.urlopen(link, timeout=20).read()
                 except:
                   cont = urllib2.urlopen(link, timeout=20).read()
               js = json.loads(cont)
               results = js['result']
               for result in results:
                   item_id = result['id']
                   # name = result['name']
                   # food = result['food']
                   # keyword = result['keywords']
                   # description = result['description']
                   path = self.img_folder_path+ ("\health_menu_item_%d" % item_id) + result['img'][-4:];
                   try:
                      content = urllib2.urlopen(result['img'],timeout=20).read()
                   except:
                       try:
                           content = urllib2.urlopen(result['img'],timeout=20).read()
                       except:
                           content = urllib2.urlopen(result['img'],timeout=20).read()
                   fout = file(path,'wb')
                   fout.write(content)
                   fout.flush()
                   fout.close()
                   # self.insert_into_table(conn,cursor,item_id,name,food,keyword,description,path,classify_id)
                   print ('craw classify=%d ;page =%d;item=%d'%(classify_id,page,item))
                   item+=1
            page+=1

    def start(self):
        conn,cursor=self.use_db()
        list_id = self.query_classify(conn,cursor)
        item =1
        for id in list_id:
            if(item>5):
             self.parser_json(conn,cursor,self.base_url,id);
            item+=1

spider= ListSpider()
spider.start();