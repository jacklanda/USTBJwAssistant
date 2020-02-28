# -*- coding: UTF-8 -*-
#author:Jacklanda
'''
退课模块的实现逻辑：
*首先从课程表接口提取用户自己已选的公选课（先POST课程表接口---清洗---入库，再初始化MongoClient()）;
*聚合查询，将各已选课以字串形式（字串内容由字典抽出）打印，与用户交互（让用户知道：我目前已经选了哪些公选课）;
*让用户选择1/2/3，根据用户的选择脚本需要判断要退哪个课，然后再从字典中抽出信息，构造退课POST的FormData，之后将发送POST退课请求，并从请求返回的
 信息判断是否退课成功。不论退课成功or失败，都将结束模块返回至main.py文件中的userchoice();
'''
import re
from core.api import api
from core import mid
from pymongo import MongoClient

def showCourse(session, data_itm):
    choice = '12'
    try:
        res = session.post(api.apiList()[14], data=data_itm)
    except Exception as e:
        print(e)
    mid.infoExtract(choice, res.content)
    try:
        col = dbClient()
    except:
        print('mongo数据库初始化失败')
    con = condition()
    agrigation = col.aggregate(con)
    li = []
    print('你目前已选的课程有：')
    for pos, row in enumerate(agrigation):
        element = row['selectedCourses']
        li.append(element)
        each = transform(element).items()
        print(str(pos+1)+'.'+str(each))
    print('\n')
    return li
    
def dbClient():
    client = MongoClient()
    database = client['ustbJwspider']
    collection = database['couseTable']
    return collection

def condition():
    con = [
        {'$unwind': '$selectedCourses'},
        {'$match':
         {'$or':
          [
              {'selectedCourses.KCLBM': '公共选修'},
              {'selectedCourses.KCLBM': '人文素养'},
              {'selectedCourses.KCLBM': '科学素养'},
              {'selectedCourses.KCLBM': '创新创业课程'},
              {'selectedCourses.KCLBM': '外语'}
              ]
          }
         },
        {'$project':
         {'_id':0, 'selectedCourses.KCM':1,
          'selectedCourses.KCLBM':1,
          'selectedCourses.XF':1,
          'selectedCourses.DYKCH':1,
          'selectedCourses.KXH':1}
         }
        ]
    return con

def transform(ele):
    ele = str(ele)
    KCM = re.search("'KCM': '(.*?)',", ele).group(1)
    KCLB = re.search("'KCLBM': '(.*?)',", ele).group(1)
    XF = re.search("'XF': '(.*?)',", ele).group(1)
    KXH = re.search("'KXH': '(.*?)'", ele).group(1)
    ele_show = {
        '课程名': KCM,
        '课程类别': KCLB,
        '学分': XF,
        '课序号': KXH
        }
    return ele_show

def dropChoice(session, dics, account):
    while True:
        while True:
            choice = input('→请输入你想要退的课所对应的序号：')
            if choice == '':
                pass
            elif choice.isdigit():
                break
            else:
                print('----请输入一个纯数字序号----\n')
                pass
        if choice == '1':
            while True:
                confirm = input('→请再次确认本次退课请求[y/n]：')
                if confirm == 'y':
                    data = makeData(dics[0], account)
                    dropExecute(session, data)
                    break
                elif confirm == 'n':
                    break
                else:
                    print('你只能选y或者n,不能皮噢~')
                    pass
        elif choice == '2':
            while True:
                confirm = input('→请再次确认本次退课请求[y/n]：')
                if confirm == 'y':
                    data = makeData(dics[1], account)
                    dropExecute(session, data)
                    break
                elif confirm == 'n':
                    break
                else:
                    print('你只能选y或者n,不能皮噢~')
                    pass
        elif choice == '3':
            while True:
                confirm = input('→请再次确认本次退课请求[y/n]：')
                if confirm == 'y':
                    data = makeData(dics[2], account)
                    dropExecute(session, data)
                    break
                elif confirm == 'n':
                    break
                else:
                    print('你只能选y或者n,不能皮噢~')
                    pass
        else:
            print('\n你输入的数字序号超出索引范围了噢~')
        break

def dropExecute(session, data):
    #print(data)
    url = api.apiList()[16]
    res = session.post(url, data=data, verify=False)
    print(res.content.decode())
    print('yeah~退课成功咯~')
    
def makeData(dic, account):
    data = {
        'kch': dic['DYKCH'],
        'kxh': dic['KXH'],
        'xh': '',
        'uid': account
        }
    return data
    
def drop(session, data, account):
    dics = showCourse(session, data)
    dropChoice(session, dics, account)