# -*- coding: UTF-8 -*-
#author:Jacklanda

'''该脚本为依赖于requests库的北京科技大学本科教学网（VPN情况下的）教务系统选课辅助脚本，
   脚本启动后须人为键入北科校园网账号(学生学号)、密码以及学号所对应的本科教学网登陆密码，
   登陆成功后需要用户选择键入需要获取信息之对应标号，方能驱动脚本抓取对应的信息，
   其后，脚本将开始自动抓取并将抓取的数据存入脚本所在路径下的「metadata」中，若用户安装了MongoDB，则数据将清洗入库
'''
#脚本尚待完善处：1、对抓取数据进行键名清洗并导入数据库；源码中的许多处代码显得十分繁冗，有待重构；
#              2、对入库的数据进行数据可视化分析，如生成课程云图、学生成绩云图、课程成绩区段分析等；
#重要的事情说三遍: 脚本不提供各请求所涉及的任何api，请自行获取！！！
#                脚本不提供各请求所涉及的任何api，请自行获取！！！
#                脚本不提供各请求所涉及的任何api，请自行获取！！！
import requests, json, re, os
from lxml import html
from PIL import Image
from random import randint
from core import mid
from core.api import api
from core.drop import dropCourse
from core.choose import chooseCourse

print('******************信息键入******************')
account = input('→请输入你的校园网登陆账号：')
password = input('→请输入你的校园网登陆密码：')
password_b = input('→请接着输入你的本科教学网登录密码：')
title_li = ['创新学分', '课程成绩', '教学计划', '英语四六级', '排名明细核对', '选课须知', '必修课信息', '专业选修课', '公共选修课', '跨专业选课', '外专业选课', '我的课程表']
data_vpn = {'auth_type':'local', 'username':account, 'sms_code':'', 'password':password,
            'captcha':'', 'needCaptcha':'', 'captcha_id':''}
data_edu = {'j_username':account+',undergraduate','j_password':password_b}
data_uid = {'uid':account}
data_itm = {'listXnxq':'2019-2020-2',
            'uid':account
            }
            
class ustbJwspider(object):
    
    def __init__(self):
        self.welcome()
        self.session = requests.Session()
        '''                                        #若使用完整的headers，则发送请求后接口不能正常返回，原因不明
        self.session.headers = {
            'accept':'*/*',
            'accept-encoding':'gzip, deflate, br',
            'accept-language':'zh-CN,zh;q=0.8',
            'content-length':'84',
            'content-type':'application/x-www-form-urlencoded; charset=UTF-8',
            'origin':'',
            'referer':'',
            'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0',
            'x-requested-with':'XMLHttpRequest'
            }
        '''                
        self.autoLogin()
        self.userChoice()
        
    def welcome(self):
        Reset="\033[0m"
        cor = ["\033[1;33m","\033[1;34m","\033[1;30m","\033[1;36m","\033[1;31m","\033[35m","\033[95m","\033[96m","\033[39m","\033[38;5;82m","\033[38;5;198m","\033[38;5;208m","\033[38;5;167m","\033[38;5;91m","\033[38;5;210m","\033[38;5;165m","\033[38;5;49m","\033[38;5;160m","\033[38;5;51m","\033[38;5;13m","\033[38;5;162m","\033[38;5;203m","\033[38;5;113m","\033[38;5;14m"]
        colors = cor[randint(0,15)]
        print(colors + """
           .'\   /`.
         .'.-.`-'.-.`.
    ..._:   .-. .-.   :_...
  .'    '-.(o ) (o ).-'    `.
 :  _    _ _`~(_)~`_ _    _  :
:  /:   ' .-=_   _=-. `   ;\  :
:   :|-.._  '     `  _..-|:   :
 :   `:| |`:-:-.-:-:'| |:'   :
  `.   `.| | | | | | |.'   .'
    `.   `-:_| | |_:-'   .'     - Welcome~!
      `-._   ````    _.-'
          ``-------''
    """)
    
    def headers(self):
        Headers ={
            'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36 SE 2.X MetaSr 1.0'
            }
        return Headers
    
    def userChoice(self):
        while True:
            print('*******************服务选择*******************\n')
            while True:
                choice = input('请输入你想要获取的信息所对应的序号：\n 1.创新学分/2.课程成绩/3.教学计划/4.英语四六级/5.排名明细核对/6.选课须知 \n 7.必修课/8.专业选修课/9.公共选修课/10.跨专业选课/11.外专业选修课/12.课程表/ \n13.尝试选课/14.尝试退课/15.获取以上的全部内容 \n\n')
                if choice == '':
                    pass
                if choice.isdigit():
                    break
                else:
                    print('----请输入一个纯数字序号----\n')
                    pass
            if int(choice) <= 15 and int(choice) >=1:
                pass
            elif choice.isdigit():
                print('----所选服务的序号超出索引范围----\n')
                continue
            #try:
            self.infocrawl(choice)
            '''
            except Exception as e:
                print(e)
                print('程序里有bug噢，你要好好检查哟~')
            finally:
                print('----信息抽取完毕并已保存至本地----')
            '''
            run = str(input('键入任意键继续，键入n退出程序[y/n]：'))
            if run == 'n':
                break
        print(self.autoLogout())
                
    def autoLogin(self):
        while True:
            try:
                print('******************vpn登陆中******************')
                url_vpn = api.apiList()[0]
                log_vpn = self.session.post(url_vpn, data=data_vpn, headers=self.headers())           #当...条件出现，判断登陆成功。
                try:
                    if 'captcha' in log_vpn.text:
                        message = self.getMsg(log_vpn)                        #当VPN首次登陆失败时，服务器将要求进行验证码验证，
                    else:
                        pass
                except Exception as e:
                    print(e)
                if '近期访问' in log_vpn.text:
                    #print(log_vpn.text)
                    print('vpn登陆成功√')
                    break
                else:
                    print(message)
                    account = input('→请重新输入你的校园网登陆账号：')
                    password = input('→请重新输入你的校园网登陆密码：')
                    self.getParam(log_vpn)
                    data_vpn['username'] = account
                    data_vpn['password'] = password
                    data_edu['j_username'] = account+',undergraduate'
            except Exception as e:
                print(e)
        while True:
            try:
                print('******************本科教学网登陆中******************')
                url_edu = api.apiList()[1]
                url_suc = api.apiList()[17]
                log_edu = self.session.post(url_edu, data=data_edu, headers=self.headers())
                log_suc = self.session.get(url_suc, headers=self.headers())
                #print(log_edu.request.headers)
                if 'success:true' in log_suc.text:
                    print('本科教学网登陆成功√')
                    break
                if 'Ext.Msg.alert' in log_edu.text:
                    print('---------该账号的登陆频率受限，请稍后重试---------')
                    while True:
                        wait = input('------去泡杯茶吧*^▽^*（键入y可尝试重新登陆）------\n')
                        if wait == '':
                            pass
                        if wait == 'y':
                            break
                        else :
                            pass     
                    password_b = input('→请重新输入你的本科教学网登录密码：')
                    data_edu['j_password'] = password_b
                else:
                    print('本科教学网登陆密码错误')
                    password_b = input('→请重新输入你的本科教学网登录密码：')
                    data_edu['j_password'] = password_b
            except Exception as e:
                print(e)
    
    def autoLogout(self):
        url_out = api.apiList()[2]
        log_out = self.session.post(url_out)
        #print(log_out.text)
        tip = '\n******************你已成功退出登陆了噢******************'
        return tip
    
    def getMsg(self, log_vpn):
        selector = html.fromstring(log_vpn.content.decode())
        msg = selector.xpath('//div[@class="msg"]/text()')[0]
        li = re.findall('[\u4e00-\u9fa5]', msg)
        mat = ''.join(li)
        msg = f'!!!!!!错误提示：{mat}!!!!!!'
        return msg
    
    def getParam(self, log_vpn):
        selector = html.fromstring(log_vpn.content.decode())
        block = selector.xpath('//div[@class="el-input code-input"]')[0]
        judge = block.xpath('input/@value')[0]
        data_vpn['needCaptcha'] = judge
        captcha_id = block.xpath('div/input/@value')[0]
        data_vpn['captcha_id'] = captcha_id
        self.getCaptcha(captcha_id)
    
    def getCaptcha(self, captcha_id):
        res = requests.post('https://****/captcha/'+captcha_id+'.png')
        with open(f'./captcha_id:{captcha_id}.png', 'wb') as f:
            f.write(res.content)
        try:
            img = Image.open(f'./captcha_id:{captcha_id}.png')
            img.show()
        except Exception as e:
            print(e)
        num = input('→请输入验证码：')
        data_vpn['captcha'] = num

    def infocrawl(self, choice):
        if choice == '1':
            print('******************创新学分信息抓取中******************\n')
            pos = int(choice)
            res = self.session.post(api.apiList()[3], data=data_uid, headers=self.headers())
            #print(res.content.decode())
            title = title_li[0]
            self.infoStore(title, res.content)
            mid.infoExtract(choice, res.content)
        elif choice == '2':
            print('******************课程成绩信息抓取中******************\n')
            pos = int(choice)
            res = self.session.post(api.apiList()[4], data=data_uid, headers=self.headers())
            #print(res.content.decode())
            title = title_li[1]
            self.infoStore(title, res.content)
            mid.infoExtract(choice, res.content)
        elif choice == '3':
            print('******************教学计划信息抓取中******************\n')
            pos = int(choice)
            res = self.session.post(api.apiList()[5], data=data_uid, headers=self.headers())
            #print(res.content.decode())
            title = title_li[2]
            self.infoStore(title, res.content)
            mid.infoExtract(choice, res.content)
        elif choice == '4':
            print('******************英语四六级信息抓取中******************\n')
            pos = int(choice)
            res = self.session.post(api.apiList()[6], data=data_uid, headers=self.headers())
            #print(res.content.decode())
            title = title_li[3]
            self.infoStore(title, res.content)
            mid.infoExtract(choice, res.content)
        elif choice == '5':
            print('******************排名明细核对信息抓取中******************\n')
            pos = int(choice)
            res = self.session.post(api.apiList()[7], data=data_uid, headers=self.headers())
            #print(res.content.decode())
            title = title_li[4]
            self.infoStore(title, res.content)
            mid.infoExtract(choice, res.content)
        elif choice == '6':
            print('******************选课须知信息抓取中******************\n')
            pos = int(choice)
            res = ''
            #print(res.content.decode())
            #title = title_li[5]
            mid.infoExtract(choice, res)
            #self.infoStore(title, res)
        elif choice == '7':
            print('******************必修课信息抓取中******************\n')
            pos = int(choice)
            res = self.session.get(api.apiList()[9])
            #print(res.content.decode())
            title = title_li[6]
            self.infoStore(title, res.content)
            mid.infoExtract(choice, res.content)
        elif choice == '8':
            print('******************专业选修课信息抓取中******************\n')
            pos = int(choice)
            res = self.session.get(api.apiList()[10])
            #print(res.text)
            title = title_li[7]
            self.infoStore(title, res.content)
            mid.infoExtract(choice, res.content)
        elif choice == '9':
            print('******************公共选修课信息抓取中******************\n')
            pos = int(choice)
            res = self.session.get(api.apiList()[11])
            #print(res.content.decode())
            title = title_li[8]
            self.infoStore(title, res.content)
            mid.infoExtract(choice, res.content)
        elif choice == '10':
            print('******************跨专业选课信息抓取中******************\n')
            pos = int(choice)
            res = self.session.get(api.apiList()[12])
            #print(res.content.decode())
            title = title_li[9]
            self.infoStore(title, res.content)
            mid.infoExtract(choice, res.content)
        elif choice == '11':
            print('******************外专业选修课信息抓取中******************\n')
            pos = int(choice)
            res = self.session.get(api.apiList()[13])
            #print(res.content.decode())
            title = title_li[10]
            self.infoStore(title, res.content)
            mid.infoExtract(choice, res.content)
        elif choice == '12':
            print('******************课程表信息抓取中******************\n')
            pos = int(choice)
            res = self.session.post(api.apiList()[14], data=data_itm)
            #print(res.content.decode())
            title = title_li[11]
            self.infoStore(title, res.content)
            mid.infoExtract(choice, res.content)
        
        elif choice == '13':                #选课功能
            print('>>>>>>>>>>尝试选课中<<<<<<<<<<\n')
            chooseCourse.retrieve(self.session, account)

        elif choice == '14':                #退课功能
            print('>>>>>>>>>>尝试退课中<<<<<<<<<<\n')
            dropCourse.drop(self.session, data_itm, account)
        
        elif choice == '15':
            print('******************全部信息抓取中******************\n')
            url_li = api.apiList()[3:15]      #创新学分获取——排名明细获取   
            for pos, url in enumerate(url_li):
                if pos <=4:
                    res = self.session.post(url, data=data_uid)
                    title = title_li[pos]
                    mid.infoExtract(str(pos+1), res.content)
                    self.infoStore(title, res.content)
                else:
                    break
            for pos, url in enumerate(url_li[6:10]):     #必修课获取——跨选课获取
                res = self.session.get(url)
                title = title_li[pos+6]
                mid.infoExtract(str(pos+7), res.content)
                self.infoStore(title, res.content)
            res = self.session.post(url_li[11], data=data_itm)
            #print(res.content.decode())
            title = title_li[11]
            mid.infoExtract('12', res.content)
            self.infoStore(title, res.content)
                    
    def infoStore(self, choice, res):
        with open(f'./metadata/{choice}.md', 'w') as f:
            f.write(res.decode())
            print(f'.md文件写入完毕')

if __name__ == '__main__':
    try:
        os.mkdir('../metadata')
    except:
        pass
    spider = ustbJwspider()