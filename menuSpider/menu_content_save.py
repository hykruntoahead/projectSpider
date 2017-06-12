# encoding=utf-8
import pymysql
import urllib2
from bs4 import BeautifulSoup

class MenuContent:

    def __init__(self):
        self.base_path='E:\html'
        self.user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'
        self.headers = {'User-Agent': self.user_agent}


    def init_database(self):
        conn = pymysql.connect(host='localhost', port=3306, user='root', passwd='123456', charset='UTF8');
        cursor = conn.cursor();

        cursor.execute("use spider")
        return conn, cursor;

    def get_link_list(self, conn, cursor):

        links = []

        sql = '''
        select * from menu
        '''

        try:
            cursor.execute(sql)
            rows = cursor.fetchall()
        except:
            conn.rollback()
            print "select menu is failed"

        for row in rows:
            links.append(row[3])

        return links;

    def create_new_table(self,conn,cursor):

        sql='''create table MENU_CONT(
         ID INT(200) NOT NULL ,
         OLD_LINK TEXT,
         HTML_PATH TEXT ,
         PRIMARY KEY (ID)
         )
        '''

        try:
           cursor.execute(sql)
           conn.commit()
        except:
            conn.rollback()
            print "create table is failed"

        return  conn,cursor;



    def parser_group(self,link,index):

        request = urllib2.Request(link.encode('utf-8'), headers=self.headers)
        # response = urllib2.urlopen(request)

        response=urllib2.urlopen(link.encode('utf-8'))

        # soup=BeautifulSoup(response.read(),'html.parser',from_encoding='utf-8')
        # head=soup.find('head')
        # c_left=soup.find(class_='space_left')
        # # is used
        # user_top=c_left.find(class_='userTop clear')
        # recip_detail=c_left.find(class_='recipDetail')
        # # is used
        # r_d_imgBox=recip_detail.find(class_='recipe_De_imgBox')
        # block_txt=recip_detail.find(class_='block_txt')
        #
        # mt20s=recip_detail.find_all(class_='mo mt20')
        # print str(mt20s)
        # r_s_r_clear=recip_detail.find(class_='recipeCategory_sub_R clear')
        # r_s_r_mt30_clear=recip_detail.find(class_='recipeCategory_sub_R mt30 clear')
        #
        # # mt20 2 所在
        #
        # recipe_step=recip_detail.find(class_='recipeStep')
        # mo=recip_detail.find(class_='mo')
        # recipe_tip=recip_detail.find(class_='recipeTip')
        #
        # recipe_mt16=recip_detail.find(class_='recipeTip mt16')
        #
        path= self.base_path+'\menu_cont_%d.html'% (index)

        fout = open(path, 'w')
        #
        # fout.write('<html>')
        # fout.write(str(head))
        # fout.write('<body>')
        # fout.write('<div>')
        # fout.write(str(user_top))
        # fout.write('<div>')
        # fout.write(str(r_d_imgBox))
        # fout.write(str(block_txt))
        #
        # # fout.write(str(mt20s[0]))
        # fout.write('<div class="mo mt20"><h3>食材明细</h3></div>')
        # fout.write(str(r_s_r_clear))
        # fout.write(str(r_s_r_mt30_clear))
        # # fout.write(str(mt20s[1]))
        # fout.write('<div class="mo mt20"><h3>｛素食｝只需5分钟的快手家常小炒 麻香娃娃菜的做法步骤</h3></div>')
        # fout.write(str(recipe_step))
        # fout.write(str(mo))
        # fout.write(str(recipe_tip))
        # fout.write(str(recipe_mt16))
        # fout.write('</div>')
        # fout.write('</div>')
        # fout.write('</body>')
        html='''


<!doctype html>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>【图文】鸡丝金针菇的做法_鸡丝金针菇的家常做法_鸡丝金针菇怎么做好吃_做法步骤,视频_鸡丝金针菇-美食天下</title>
<meta name="keywords" content="鸡丝金针菇,鸡丝金针菇的做法,鸡丝金针菇的家常做法,鸡丝金针菇怎么做,鸡丝金针菇的做法步骤,鸡丝金针菇的最正宗做法,鸡丝金针菇怎么做好吃,鸡丝金针菇" />
<meta name="description" content="美食天下通过图文并茂的方式，手把手教你鸡丝金针菇如何做才美味，并详细说明鸡丝金针菇烹制所用佐料时间和窍门，包括鸡丝金针菇营养价值和最适宜食用方法等揭秘。" />
<meta name="renderer" content="webkit">
<meta http-equiv="mobile-agent" content="format=xhtml; url=http://m.meishichina.com/recipe/70281/">
<link rel="shortcut icon" href="http://static.meishichina.com/v6/img/lib/f.ico"/>
<link rel="apple-touch-icon" href="http://static.meishichina.com/v6/img/lib/wapico.png" />
<link rel="stylesheet" type="text/css" href="http://static.meishichina.com/v6/css/lib/all.css?a=7">
<link rel="stylesheet" type="text/css" href="http://static.meishichina.com/v6/css/app/newrecipe/recipe2.css?a=2016-08-04">

<link rel="stylesheet" type="text/css" href="http://static.meishichina.com/v6/css/lib/comment.css?a=2015-07-16">
<script type="text/javascript" src="http://static.meishichina.com/v6/js/lib/dfp-content-7.js"></script>
</head>
<body>
 <div class="space_left">

<div class="userTop clear">
<h1 class="recipe_De_title"><a href="http://home.meishichina.com/recipe-70281.html" id="recipe_title" title="鸡丝金针菇">鸡丝金针菇</a></h1>
<a title="neo1124" href="http://home.meishichina.com/space-761377.html#utm_source=recipe_last_tuijian_space" target="_blank" class="uright">
<img src="http://i3.meishichina.com/data/avatar/000/76/13/77_avatar_small.jpg" />
<span class="userName" id="recipe_username">neo1124</span>
</a>
</div>


				<div class="space_box_home">

					<div class="recipDetail">


						<div class="recipe_De_imgBox" id="recipe_De_imgBox">
							<a class="J_photo" title="鸡丝金针菇的做法"><span></span><img src="http://i3.meishichina.com/attachment/r/2012/06/10/p800_20120610190709688566502.jpg" alt="鸡丝金针菇的做法"> </a>

						</div>


<div class="mo mt20">
<h3>食材明细</h3>
</div>



<div class="recipeCategory_sub_R clear">
<ul>
				  				  <li>
					<span class="category_s1">
														<a target="_blank" href="http://www.meishichina.com/YuanLiao/JiXiongRou/" title="鸡胸肉的做法"  ><b>鸡胸肉</b></a>
												</span>
				  					<span class="category_s2">1块</span>
				  				  </li>
				  				  <li>
					<span class="category_s1">
														<a target="_blank" href="http://www.meishichina.com/YuanLiao/JinZhenGu/" title="金针菇的做法"  ><b>金针菇</b></a>
												</span>
				  					<span class="category_s2">1把</span>
				  				  </li>
				  				  <li>
					<span class="category_s1">
														<a target="_blank" href="http://www.meishichina.com/YuanLiao/HuangHuaCai/" title="黄花菜的做法"  ><b>黄花菜</b></a>
												</span>
				  					<span class="category_s2">数朵</span>
				  				  </li>
				  				  <li>
					<span class="category_s1">
														<a target="_blank" href="http://www.meishichina.com/YuanLiao/DaSuan/" title="大蒜的做法"  ><b>大蒜</b></a>
												</span>
				  					<span class="category_s2">1</span>
				  				  </li>
				  				  <li>
					<span class="category_s1">
														<a target="_blank" href="http://www.meishichina.com/YuanLiao/HuaJiaoHuaJiao/" title="花椒的做法"  ><b>花椒</b></a>
												</span>
				  					<span class="category_s2">数粒</span>
				  				  </li>
				  				  <li>
					<span class="category_s1">
														<a target="_blank" href="http://www.meishichina.com/YuanLiao/BaJiao/" title="八角的做法"  ><b>八角</b></a>
												</span>
				  					<span class="category_s2">1</span>
				  				  </li>

</ul>
</div>

<div class="recipeCategory_sub_R mt30 clear">
<ul>

<li>
<span class="category_s1">
		<a title="怪味" href="http://home.meishichina.com/recipe-type-do-cuisine-view-25.html" target="_blank">怪味</a>
	</span>
<span class="category_s2">口味</span>
</li>

<li>
<span class="category_s1">
							<a title="拌" href="http://home.meishichina.com/recipe-type-do-technics-view-8.html" target="_blank">拌</a>
						</span>
<span class="category_s2">工艺</span>
</li>

<li>
<span class="category_s1">
							<a title="半小时" href="http://home.meishichina.com/recipe-type-do-during-view-3.html" target="_blank">半小时</a>
						</span>
<span class="category_s2">耗时</span>
</li>

<li>
<span class="category_s1">
							<a title="简单" href="http://home.meishichina.com/recipe-type-do-level-view-1.html" target="_blank">简单</a>
						</span>
<span class="category_s2">难度</span>
</li>


</ul>
</div>





<div class="mo mt20">
<h3>鸡丝金针菇的做法步骤</h3>
</div>




           <div class="recipeStep">
            <ul>
				              <li>
			  			  <div class="recipeStep_img">
				  <img src="http://i3.meishichina.com/attachment/recipe/201206/p320_201206101910221339907513.JPG" alt="鸡丝金针菇的做法步骤：1">
			                   </div>
								<div class="recipeStep_word"><div class="recipeStep_num">1</div>干货黄花菜要先泡一泡</div>
				              </li>
			                <li>
			  			  <div class="recipeStep_img">
				  <img src="http://i3.meishichina.com/attachment/recipe/201206/p320_201206101917351339588364.JPG" alt="鸡丝金针菇的做法步骤：2">
			                   </div>
								<div class="recipeStep_word"><div class="recipeStep_num">2</div>把泡好的黄花菜，金针菇，鸡胸肉陆续的煮熟。鸡胸肉煮的时候要加姜片和八角 煮到熟就好金针菇最好是弄弄开 这样吃起来比较方便</div>
				              </li>
			                <li>
			  			  <div class="recipeStep_img">
				  <img src="http://i3.meishichina.com/attachment/recipe/201206/p320_201206101913561339796035.JPG" alt="鸡丝金针菇的做法步骤：3">
			                   </div>
								<div class="recipeStep_word"><div class="recipeStep_num">3</div>趁煮的时候 切点蒜蓉 依个人喜好准备 Neo是爱吃蒜 嘿嘿</div>
				              </li>
			                <li>
			  			  <div class="recipeStep_img">
				  <img src="http://i3.meishichina.com/attachment/recipe/201206/p320_201206101917511339743701.JPG" alt="鸡丝金针菇的做法步骤：4">
			                   </div>
								<div class="recipeStep_word"><div class="recipeStep_num">4</div>把花椒粒在热油粒煸煸 变成花椒油 在趁热倒入刚刚装蒜蓉的碗里 依序加入生抽，鸡精，黑醋，糖糖只是调味只要一点点就好了哦！</div>
				              </li>
			                <li>
			  			  <div class="recipeStep_img">
				  <img src="http://i3.meishichina.com/attachment/recipe/201206/p320_201206101918361339585950.jpg" alt="鸡丝金针菇的做法步骤：5">
			                   </div>
								<div class="recipeStep_word"><div class="recipeStep_num">5</div>把煮好的金针菇，黄花菜和撕好的鸡丝好好的拌拌 再放入冰箱 吃的时候再拿出来 夏天胃口不好 吃凉菜可下饭啦~</div>
				              </li>
			              </ul>
          </div>

<div class="recipeTip mt16">
使用的厨具：煮锅
</div>
  </div>
  </div></body></html>'''
        fout.write(html)

        return path


    def insert_into_menu_cont(self,conn,cursor,id,link,path):

        sql='''
        INSERT INTO MENU_CONT VALUES (
        %d,%s,%s)''' % (id, "'" + link + "'", "'" + path + "'")

        try:
            cursor.execute(sql)
            conn.commit()
        except:
            conn.rollback()
            print 'insert to table failed'




    def start(self):
        conn,cursor=self.init_database()
        list=self.get_link_list(conn,cursor)
        conn,cursor=self.create_new_table(conn,cursor)

        index=1;

        for li in list:
            if(index==70281):
                path=self.parser_group(li,index)
                self.insert_into_menu_cont(conn,cursor,index,li,path)
                print 'craw id=%d and path=%s' % (index,path)
            index+=1


menu_cont=MenuContent()
menu_cont.start()



