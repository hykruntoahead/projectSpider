#encoding=utf-8

import os


class  ExchangeHtml:
    def __init__(self):
        self.base_path= 'E:/health_html_1/health_html_1/'
        self.base_path2='E:/h_html/'
        self.head=''' <meta charset="UTF-8"/>
          <link type="text/css" href="../css/common.css" rel="stylesheet"/>
		  <script src="../js/common.js" type="text/javascript"></script>
        '''

    def query_all_file(self):
        files = os.listdir(self.base_path)
        for f in files:
          file = open(self.base_path+f,'r')
          cont = file.read()
          cont1 = cont.replace('<meta charset="UTF-8">', self.head)
          file.close()
          file1 = open(self.base_path+f,"w")
          file1.write(cont1)
          file1.flush()
          file1.close()
          print f



exchange = ExchangeHtml()
exchange.query_all_file()