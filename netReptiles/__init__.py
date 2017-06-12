import urllib2,cookielib

cj=cookielib.CookieJar()

opener=urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

urllib2.install_opener(opener)

response=urllib2.urlopen("http://www.baidu.com")



print  response.read()