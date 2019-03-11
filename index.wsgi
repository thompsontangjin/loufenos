   #coding:utf-8
import os
import tornado.wsgi
import sae
import tornado.database
import sae.const
from tornado.escape import json_encode
from sae.mail import send_mail
import math

import hashlib
import web
import time
import urllib2,json
from sae.mail import EmailMessage
import lxml
from lxml import etree
import sys


#数据库联结
SinaDatabase = tornado.database.Connection(
 "%s:%s"%(sae.const.MYSQL_HOST,str(sae.const.MYSQL_PORT)), 
 
 sae.const.MYSQL_DB, 
 sae.const.MYSQL_USER, 
 sae.const.MYSQL_PASS, 
 max_idle_time = 30
)
##############################################################################################################

#以下是专门处理GPS偏差。精度由原来的700至800米缩小至300米
#############################################################################################################

def transform(wgLat, wgLon):
     a = 6378245.0
     ee = 0.00669342162296594323
     pi = 3.14159265358979324

     if outofchina(wgLat, wgLon):
        return str(wgLat)+","+str(wgLon)
     else:
            
        
        dLat = transformlat(wgLat - 35.0,wgLon - 105.0)
        dLon = transformlon(wgLon - 105.0, wgLat - 35.0)
        radLat = wgLat / 180.0 * pi
        magic = math.sin(radLat)
        magic2 = 1 - ee * magic * magic
        sqrtMagic = math.sqrt(magic2)
        dLat1 = (dLat * 180.0) / ((a * (1 - ee)) / (magic2 * sqrtMagic) * pi)
        dLon1 = (dLon * 180.0) / (a / sqrtMagic * math.cos(radLat) * pi)
        mgLat = wgLat + dLat1
        mgLon = wgLon + dLon1
        return str(mgLat)+","+str(mgLon)


def outofchina(lat,lon):
     if lat>55.8271:
        return True
     elif lat<0.8293:
        return True
     elif lon>137.8347:
        return True
     elif lon<72.004:
        return True
     else:
        return False



def transformlat(x,y):
     pi = 3.14159265358979324
     ret=-100.0 + 2.0 * x + 3.0 * y + 0.2 * y * y + 0.1 * x * y + 0.2 * math.sqrt(abs(x))
     ret1=ret+(20.0 * math.sin(6.0 * x * pi) + 20.0 * math.sin(2.0 * x * pi)) * 2.0 / 3.0
     ret2=ret1+(20.0 * math.sin(x * pi) + 40.0 * math.sin(x / 3.0 * pi)) * 2.0 / 3.0
     ret3=ret2+(150.0 * math.sin(x / 12.0 * pi) + 300.0 * math.sin(x / 30.0 * pi)) * 2.0 / 3.0
     return ret3




def transformlon(x,y):
     pi = 3.14159265358979324


     ret = 300.0 + x + 2.0 * y + 0.1 * x * x + 0.1 * x * y + 0.1 * math.sqrt(abs(x));
     ret1 =ret+ (20.0 * math.sin(6.0 * x * pi) + 20.0 * math.sin(2.0 * x * pi)) * 2.0 / 3.0;
     ret2 =ret1+ (20.0 * math.sin(x * pi) + 40.0 * math.sin(x / 3.0 * pi)) * 2.0 / 3.0;
     ret3 =ret2+ (150.0 * math.sin(x / 12.0 * pi) + 300.0 * math.sin(x / 30.0 * pi)) * 2.0 / 3.0;
     return ret3

def altlatlon(x):
    latlon=x
    value=latlon.split(",")
    lat=value[0]
    lon=value[1]
    lonlat=lon+","+lat
    return lonlat

##############################################################################################################
#取出数据        
class GetValue(tornado.web.RequestHandler):
    def post(self):
        tag=self.get_argument('tag')
        value1=tag.strip('"')
        value=value1.split(",")
        tags=value[0]
        username=value[1]
        
        #send_mail("13779961531@139.com", "tag",tag,("smtp.139.com", 25, "13779961531@139.com", "tangjin7624" ,False))
        if tags=="username":
            
                    
             if SinaDatabase:
                            
                 d = SinaDatabase.query("SELECT * FROM usernamepw where username=%s",username);
                 if d:
                    self.set_header('Content-Type','application/json')
                    #tag=str(d[0]['username'])
                    password=str(d[0]['password'])
                    self.write(json_encode(["VALUE",tag,password]))   
                 else: self.write(json_encode(''))
        #elif tags=="whereismycar":
            

    def get(self):
         tag=self.get_argument('tag')
         self.write(str(tag))
#存数据 
class StoreAValue(tornado.web.RequestHandler):
    def get(self):
        test=str(time.localtime(time.time()))

        self.set_header('Content-Type','application/json')
        self.write(json_encode(["STORED",test]))  

    def post(self):
        tag = self.get_argument('tag')
        value = self.get_argument('value')

                
        if tag=="longlat":
            value2=value.strip('"')
            value1=value2.split(",")
            phonenumber=value1[0]
            longtitude=value1[2]
            latitude=value1[1]
            latlong=transform(float(latitude),float(longtitude))
            if SinaDatabase:
                rec=SinaDatabase.query("SELECT * FROM traceinfo WHERE phonenumber=%s",phonenumber);
                if rec: 
                   SinaDatabase.execute("UPDATE traceinfo SET latlong=%s WHERE phonenumber=%s",latlong,phonenumber);
                   
                else:
                   self.set_header('Content-Type','application/json')
                   self.write(json_encode(''))
                   #SinaDatabase.execute("INSERT INTO traceinfo (phonenumber,latlong) VALUES (%s,%s)",phonenumber,latlong);
        elif tag=="goodtruck":
             value2=value.strip('"')
             value1=value2.split(",")
             gn=value1[0]
             dn=value1[1]
             if SinaDatabase:
                    rec=SinaDatabase.query("SELECT * FROM goodtraceinfo WHERE goodnumber=%s",gn);
                    if rec:
                        SinaDatabase.execute("UPDATE goodtraceinfo SET trucknumber=%s where goodnumber=%s",dn,gn);
                        
                    else:
                        SinaDatabase.execute("INSERT INTO goodtraceinfo (goodnumber,trucknumber) VALUES (%s,%s)",gn,dn);
             #send_mail("13779961531@139.com", tag,gn+dn,("smtp.139.com", 25, "13779961531@139.com", "tangjin7624" ,False))
        elif tag=="thompsonlonglat":
             value2=value.strip('"')
             value1=value2.split(",")
             phonenumber=value1[0]
             longtitude=value1[2]
             latitude=value1[1]
             latlong=transform(float(latitude),float(longtitude))
             if SinaDatabase:
                rec=SinaDatabase.query("SELECT * FROM traceinfo WHERE phonenumber=%s",phonenumber);
                if rec: 
                   SinaDatabase.execute("UPDATE traceinfo SET latlong=%s WHERE phonenumber=%s",latlong,phonenumber);
                   
                else:
                   
                   SinaDatabase.execute("INSERT INTO traceinfo (phonenumber,latlong) VALUES (%s,%s)",phonenumber,latlong);

        elif tag=="updatepassword":
             value2=value.strip('"')
             value1=value2.split(",")
             username=value1[0]
             password=value1[1]
             if SinaDatabase:
                    rec=SinaDatabase.query("SELECT * FROM usernamepw WHERE username=%s",username);
                    if rec:
                        SinaDatabase.execute("UPDATE usernamepw SET password=%s",password);
                    else:
                        pass
        elif tag=='gpsidaddv1':
            #send_mail("13779961531@139.com", tag,value,("smtp.139.com", 25, "13779961531@139.com", "tangjin7624" ,False))
            pv=value.strip('"')
            if SinaDatabase:
                   SinaDatabase.execute("INSERT INTO traceinfo (phonenumber,latlong) VALUES (%s,%s)",pv,'');
                   SinaDatabase.execute("INSERT INTO goodtraceinfo (goodnumber,trucknumber) VALUES (%s,%s)",pv,pv);
                   tag='gpsidaddmessage'
        elif tag=='gpsiddelv1':
            pv=value.strip('"')
            send_mail("13779961531@139.com", tag,value,("smtp.139.com", 25, "13779961531@139.com", "tangjin7624" ,False))
            SinaDatabase.execute("DELETE FROM traceinfo WHERE phonenumber=%s",pv);
        else:
            pass
            
        self.set_header('Content-Type','application/json')
        self.write(json_encode(["STORED",tag,value]))  
##########################################################################################################################
class Adlg(tornado.web.RequestHandler):
    def get(self):

        self.render("adming.html")
        
    def post(self):
        username=self.get_argument("username")
        pw=self.get_argument("password")
        #content="IP地址："+self.request.remote_ip+"用户名："+username+"密码：" +pw 
        #self.write(pw)
        if username=="thompson201":
           if pw=="sfc5698232":
              self.render("admin.html")
           else:
              self.write("密码错误")
        else:
           self.write("非法用户,你的IP已被记录：")
           self.write(self.request.remote_ip)
           
           send_mail("13779961531@139.com", "lufeng系统非法用户闯入，IP地址见邮件正文。",username+self.request.remote_ip+pw,("smtp.139.com", 25, "13779961531@139.com", "tangjin7624" ,False))


#########################################################################################################################                                                                           
#管理员入口 
class Admin(tornado.web.RequestHandler):

 
            
    def post(self):
        
        gpsid=self.get_argument('gpsid')
        phonenumber='%'+gpsid+'%'
        recordmount=0
        self.write('<center><h1> The list:</h1></center><br><br><div style="margin=auto ,width:60%"')
        
        if SinaDatabase:
           rec=SinaDatabase.query("select * from traceinfo  where phonenumber like %s ORDER BY id DESC ",phonenumber);
        
           if rec:
              for recsign in rec:
                self.write('<br><center>')
                self.write('<font color="red"><strong>record id:&nbsp </strong></font>')
                self.write(str(recsign['id']))
                self.write('<font color="red"><strong>&nbsp &nbsp &nbsp  &nbsp  &nbsp GPSID:&nbsp </strong></font>')
                self.write(recsign['phonenumber'])
                self.write('<font color="red"><strong>&nbsp &nbsp &nbsp  &nbsp  &nbsp  经纬度：&nbsp </strong></font>')
                self.write(recsign['latlong'])
                self.write('<font color="red"><strong>&nbsp &nbsp &nbsp  &nbsp  &nbsp date:&nbsp </strong></font>')
                self.write(str(recsign['date']))
                self.write('</center><br>')
                recordmount=recordmount+1

           else:
                self.write('sorry ,no anyone')
        self.write('<p><center><h3>You have found &nbsp ')
        self.write(str(recordmount))
        self.write('&nbsp records</h3></center></p>')
        self.write('<div>')
#########################################################################################################################
class Delete(tornado.web.RequestHandler):
            
    def post(self):
        
        gpsid=self.get_argument('gpsid')
        
        #self.write('<center><h1> The list:</h1></center><br><br><div style="margin=auto ,width:60%"')
        
        if SinaDatabase:
           rec=SinaDatabase.query("select * from traceinfo  where id=%s",gpsid);
        
           if rec:
              for recsign in rec:
                SinaDatabase.execute("DELETE FROM traceinfo WHERE id=%s",gpsid);
                self.write("<center><h3>delete is done</h3></center>")

           else:
                self.write('<center>sorry ,no the rec</center>')
 
        #self.write('<div>')
####################################################################################################
class Admingn(tornado.web.RequestHandler):
            
    def post(self):
        
        rgoodnumber=self.get_argument('goodnumber')
        goodnumber='%'+rgoodnumber+'%'
        recordmount=0
        self.write('<center><h1> The list:</h1></center><br><br><div style="margin=auto ,width:60%"')
        
        if SinaDatabase:
           rec=SinaDatabase.query("select * from goodtraceinfo  where goodnumber like %s ORDER BY id DESC ",goodnumber);
        
           if rec:
              for recsign in rec:
                self.write('<br><center>')
                self.write('<font color="red"><strong>record id:&nbsp </strong></font>')
                self.write(str(recsign['id']))
                self.write('<font color="red"><strong>&nbsp &nbsp &nbsp  &nbsp  &nbsp 货号:&nbsp </strong></font>')
                self.write(recsign['goodnumber'])
                self.write('<font color="red"><strong>&nbsp &nbsp &nbsp  &nbsp  &nbsp  GPSID:&nbsp </strong></font>')
                self.write(recsign['trucknumber'])
                self.write('<font color="red"><strong>&nbsp &nbsp &nbsp  &nbsp  &nbsp date:&nbsp </strong></font>')
                self.write(str(recsign['date']))
                self.write('</center><br>')
                recordmount=recordmount+1

           else:
                self.write('sorry ,no anyone')
        self.write('<p><center><h3>You have found &nbsp ')
        self.write(str(recordmount))
        self.write('&nbsp records</h3></center></p>')
        self.write('<div>')
      
####################################################################################################
class Username(tornado.web.RequestHandler):
            
    def post(self):
        
        rusername=self.get_argument('username')
        username='%'+rusername+'%'
        recordmount=0
        self.write('<center><h1> The list of username:</h1></center><br><br><div style="margin=auto ,width:60%"')
        
        if SinaDatabase:
           rec=SinaDatabase.query("select * from usernamepw  where username like %s ORDER BY id DESC ",username);
        
           if rec:
              for recsign in rec:
                self.write('<br><center>')
                self.write('<font color="red"><strong>record id:&nbsp </strong></font>')
                self.write(str(recsign['id']))
                self.write('<font color="red"><strong>&nbsp &nbsp &nbsp  &nbsp  &nbsp 用户名:&nbsp </strong></font>')
                self.write(recsign['username'])
                self.write('<font color="red"><strong>&nbsp &nbsp &nbsp  &nbsp  &nbsp  密码:&nbsp </strong></font>')
                self.write(recsign['password'])
                self.write('<font color="red"><strong>&nbsp &nbsp &nbsp  &nbsp  &nbsp 日期:&nbsp </strong></font>')
                self.write(str(recsign['date']))
                self.write('</center><br>')
                recordmount=recordmount+1

           else:
                self.write('sorry ,no anyone')
        self.write('<p><center><h3>You have found &nbsp ')
        self.write(str(recordmount))
        self.write('&nbsp records</h3></center></p>')
        self.write('<div>')
####################################################################################################
class Usernameadd(tornado.web.RequestHandler):
            
    def post(self):
        
        username=self.get_argument('username')
        password=self.get_argument('password')
       
        if SinaDatabase:
             rec=SinaDatabase.query("select * from usernamepw  where username=%s",username);
             if rec:
                self.write('<center><h3>用户名已存在</h3></center>')
             else:
                SinaDatabase.execute("INSERT INTO usernamepw (username,password) VALUES (%s,%s)",username,password);
                self.write('<center><h3>new username is added </h3></center>')
        else:
                self.write('sorry ,some wrong with database')

        self.write('<div>')
#########################################################################################################################
class Usernamedelete(tornado.web.RequestHandler):
            
    def post(self):
        
        uid=self.get_argument('usernameid')
        
        #self.write('<center><h1> The list:</h1></center><br><br><div style="margin=auto ,width:60%"')
        
        if SinaDatabase:
           rec=SinaDatabase.query("select * from usernamepw  where id=%s",uid);
        
           if rec:
              for recsign in rec:
                SinaDatabase.execute("DELETE FROM usernamepw WHERE id=%s",uid);
                self.write("<center><h3>delete is done</h3></center>")

           else:
               self.write('<center>sorry ,no the rec</center>')
#########################################################################################################################
class Deletegn(tornado.web.RequestHandler):
            
    def post(self):
        
        gnid=self.get_argument('gnid')
        
        #self.write('<center><h1> The list:</h1></center><br><br><div style="margin=auto ,width:60%"')
        
        if SinaDatabase:
           rec=SinaDatabase.query("select * from goodtraceinfo  where id=%s",gnid);
        
           if rec:
              for recsign in rec:
                SinaDatabase.execute("DELETE FROM goodtraceinfo WHERE id=%s",gnid);
                self.write("<center><h3>delete is done</h3></center>")

           else:
               self.write('<center>sorry ,no the rec</center>')
#以下是微信专用模块 
#####################################################################################################
#####################################################################################################
class WeixinInterface(tornado.web.RequestHandler):
    
    
    
    def get(self):
   
        #获取输入参数
        signature = self.get_argument('signature')
        timestamp = self.get_argument('timestamp')
        nonce = self.get_argument('nonce')
        echostr=self.get_argument('echostr')
        #sefl.write(signature)
        #自己的token
        token='lufengnetwork' #这里改写你在微信公众平台里输入的token
        #字典序排序
        list=[token,timestamp,nonce]
        list.sort()
        sha1=hashlib.sha1()
        map(sha1.update,list)
        hashcode=sha1.hexdigest()
       
        #如果是来自微信的请求，则回复echostr
        if hashcode == signature:
           self.write(echostr)
      
    def post(self):
        str_xml=self.request.body
        
        xml = etree.fromstring(str_xml)#进行XML解析
        tracenumber=xml.find("Content").text#取得用户所输入的内容

                
        msgType=xml.find("MsgType").text
        
      
        
        fromUser=xml.find("FromUserName").text
        toUser=xml.find("ToUserName").text
        create_time=int(time.time())
        
        self.set_header('Content-Type','application/xml')
        if xml.find("MsgType").text=='text':
           if SinaDatabase:
                rec=SinaDatabase.query("SELECT * FROM goodtraceinfo WHERE goodnumber=%s",tracenumber);                                                                                                                                                                                                                                                                                                                                                                     
                if rec:
                    trucknumber=rec[0]['trucknumber']
                    
                    rec2=SinaDatabase.query("SELECT * FROM traceinfo WHERE phonenumber=%s",trucknumber);
                    if rec2:

                        content="http://4.tangjinfirstapp.applinzi.com/location?latlon="+rec2[0]['latlong']                                                                                                                                                                                                                                                                                                                                                                                                                        
            
                        self.render("reply_traceinfo.xml",toUser=fromUser,fromUser=toUser,create_time=create_time,msgtype="news",title1="当前查询位置--高德交通图",description1="点击查看全文，您查询的位置将以高德地图显示.",url1=content+"&map=1",title2="当前查询位置--谷歌照片图",description2="点击查看全文，您查询的位置将以谷歌地图航空照片形式显示，个别网络会无法显示谷歌地图.",url2=content+"&map=2",title3="当前查询位置--谷歌大图",description3="点击查看全文，您查询的位置将以谷歌大地图显示，个别网络会无法显示谷歌地图.",url3=content+"&map=3")
                       
                       
                        
                    else:
                        self.render("reply_text.xml",toUser=fromUser,fromUser=toUser,create_time=create_time,msgtype="text",content="没有车号记录，谢谢。")
                else:
                                      
                    self.render("reply_text.xml",toUser=fromUser,fromUser=toUser,create_time=create_time,msgtype="text",content="没有此号记录，谢谢。")
           else:
                self.render("reply_text.xml",toUser=fromUser,fromUser=toUser,create_time=create_time,msgtype="text",content="系统正在建设中，敬请期待。谢谢,唐进。")
        elif xml.find("MsgType").text=='image':
           self.render("reply_text.xml",toUser=fromUser,fromUser=toUser,create_time=create_time,msgtype="text",content="系统正在建设中，感谢您的图片。谢谢,唐进。")
        
        elif xml.find("Event").text=='subscribe':
        
           
           self.render("reply_text.xml",toUser=fromUser,fromUser=toUser,create_time=create_time,msgtype='text',content="欢迎订阅唐进的订阅号。")
        else :
            pass
       
       
       
       

#####################################################################################################
 
###定位地图##############################################################################################
        
class Location(tornado.web.RequestHandler):
    def get(self):
        latlon = self.get_argument('latlon')
        maps=self.get_argument('map')
        lonlat=altlatlon(latlon)
        if int(maps)==1:
            self.render("location1.html",lonlat=lonlat)
        elif int(maps)==2:
            self.render("location2.html",latlon=latlon)
        elif int(maps)==3:
            self.render("location3.html",latlon=latlon)
        else:
            pass
        
#########################################################################################################################
###动态网页输出：
#########################################################################################################################
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        
        self.render("static/index.html")
        
        
        
        
class Contact(tornado.web.RequestHandler):
    def get(self):
        
        self.render("static/contact.html")
        
        
                    
app = tornado.wsgi.WSGIApplication([
    ( '/',MainHandler), 
    ('/contact',Contact),
    (r'/storeavalue', StoreAValue),
    (r'/getvalue', GetValue), 
    (r'/weixin',WeixinInterface),
    (r'/location',Location),
    (r'/admin',Admin),
    (r'/delete',Delete),
    (r'/admingn',Admingn),
    (r'/deletegn',Deletegn),
    (r'/username',Username),
    (r'/usernameadd',Usernameadd),
    (r'/usernamedelete',Usernamedelete),
    (r'/adlg',Adlg),
  
    
])
    
application = sae.create_wsgi_app(app)
