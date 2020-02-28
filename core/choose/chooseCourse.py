# -*- coding: UTF-8 -*-
#author:Jacklanda

'''
该模块为spider主函数提供选课功能
*已实现功能：返回目前所有可选的课程列表（包括授课教师、讲台、课程类型、学分等信息）
 供用户做出实时选择，判断逻辑：课余量是否为零，不为零则列出
'''
import json, time
from core.mid import infoExtract
from core.api import api
from core.database import db
from core.database import dbDelete
from core.choose import courseList
from core.database import dataCleanse
from pymongo import MongoClient

type_li = ['公选课', '专选课', '必修课', '跨选课']

def inputName():                                            #以下错误仅针对于课序号不在索引范围内的情况，可能会出现：选错了讲台的情况,故在使用脚本选课后，要及时登录本科教学网核对所选课程
    course_name = input('请输入你想选择的课的课程名：')         #存在三种键入信息的错误情况：1.只有课程名错误；2.只有课序号错误；3.只有课程类别错误
    course_numb = input('请输入你想选择的课的课序号：')         #4.课程名和课序号同时输错；5.课程名和课程类别同时输错;6.课序号和课类别同时输错
    while True:                                                                                            #7.三者同时输错
        course_type = input('请输入你想选择的课的课程类别（tip：必修课、专选课、公选课、跨选课）：')         
        if course_type == '必修课':
            break
        elif course_type == '专选课':
            break
        elif course_type == '公选课':
            break
        elif course_type == '跨选课':
            break
        else:
            print('请输入正确的课程类型,不能皮噢~')
    return course_name, course_type, course_numb

def preparePost(session, type_name):        #向对应课程性质的API发送POST请求,自动获取实时的课容量&课余量并清洗入库                    #需增加对键入错误课程信息的判断,若错误，要求用户重新键入
    while True:                             #键入错误3、5、7将在preparePost中得到解决，直至用户输入正确的课程类型为止
        if type_name == '公选课':
            choice = '9'
            url = api.apiList()[11]
            res = session.get(url)
            infoExtract(choice, res.content)
            #print(type_name)
            break
        elif type_name == '专选课':
            print('脚本暂不提供专选课服务噢~')
            '''
            choice = '8'
            url = api.apiList()[10]
            res = session.get(url)
            infoExtract(choice, res)
            '''
            break
        elif type_name == '必修课':
            print('脚本暂不提供必修课服务噢~')
            '''
            choice = '7'
            url = api.apiList()[9]
            res = session.get(url)
            infoExtract(choice, res)
            type_name
            '''
            break
        elif type_name == '跨选课':
            print('脚本暂不提供跨选课服务噢~')
            '''
            choice = '10'
            url = api.apiList()[9]
            res = session.get(url)
            infoExtract(choice, res)
            '''
            break 
     
def dbClient(col_name):
    client = MongoClient()
    database = client['ustbJwspider']
    collection = database[col_name]
    return collection
        
                                           #在公选课、专选课、跨选课入库前，亦需进行数据清洗，须找出并删除包含学生个人信息的字典
def retrieve(session, account):                     #如何根据选课名从mongo中调出其相应的'id'与'xf'呢?根据一个键值对返回其所在的字典
    try:
        dataCleanse.cleanse()
    except Exception as e:
        print(e)
    courseList.courseInfo()                #调用courseList()，返回目前可选的公选课信息
    times = 1
    info = inputName()                     #课程名：info[0], 课程类型：info[1], 课程号：info[2]
    while True:
        preparePost(session, info[1])      #传入已经经过了：两次模拟登陆---GET请求待选课嵌套数组后的session, info[1]为课程类型，用以构造选课请求的formdata
        if info[1] == '公选课':             #根据inputName()函数获取的选课类型来进入不同的控制流
            col_name = 'publicChoose'
            collection = dbClient(col_name)       #向dbClient()传入集合名，初始化mongo客户端---数据库---集合
            ver = verify(collection, info[0], info[2])     #传入mongo的集合对象、课程名和课序号，在verify函数中验证课余量是否为零
            if ver[0]:                     #根据verify()返回的布尔值来判断课程是否有余量，有则步进，无则打印“课余量不足”
                pos = 11
                typ = '公共选修课'
                data = makeDic(ver[1],account, typ)   #向makeDic()传入从数据库中调出的包含课程信息的字典、用户账号和完整的选课类型，返回选课时要提交的表单数据
                tri = trial(pos, session, data)    #通过trial()函数先POST对应课程类型的课总表接口，再POST用户的选课请求，尝试选课
                if tri[0] == True:    #选课成功
                    print(tri[1])
                    print(f'第{times}次尝试，选课成功咯~')
                    print('快打开本科教学网去探探自己心水已久的课程吧~')
                    break
                elif tri[0] == False:     #选课失败：此处失败的可能原因为：课余量充足，但自己已选满3门公选课，跳出尝试选课循环
                    print(tri[1])         
                    print(f'第{times}次尝试，选课失败咯~')
                    times = times+1
                    break
                elif tri[0] == '选课接口返回错误，请检查网络情况/提交的Form-Data':      #若出现此种情况，说明选课接口发生变化，需重新手动测试接口
                    print(f'第{times}次尝试，选课接口返回错误，请检查提交的Form-Data')
                    times = times+1
                    pass
            else:
                print(f'第{times}次尝试，课程余量不足，选课失败咯~')        #此后会设置延时，然后重新访问接口以更新数据库，重新尝试选课
                logRec('{"msg":"课程余量不足.","success":"false"}')
                try:
                    dbDelete.delete(collection)
                except Exception as e:
                    print(e)
                times = times+1
                time.sleep(10)
        
        if info[1] == '专选课':                                 #专选课的选课功能暂不可用
            print('脚本暂不提供专选课服务噢~')
            '''
            col_name = 'proChoose'
            collection = dbClient(col_name)       
            ver = verify(collection, info[0], info[2])     
            if ver[0]:                     
                pos = 10
                typ = '专业选修课'
                data = makeDic(ver[1],account, typ)   
                tri = trial(pos, session, data)    
                if tri[0] == True:    
                    print(tri[1])
                    print(f'第{times}次尝试，选课成功咯~')
                    print('快打开本科教学网去探探自己心水已久的课程吧~')
                    break
                elif tri[0] == False:     
                    print(tri[1])         
                    print(f'第{times}次尝试，选课失败咯~')
                    times = times+1
                    break
                elif tri[0] == '选课接口返回错误，请检查网络情况/提交的Form-Data':      
                    print(f'第{times}次尝试，选课接口返回错误，请检查提交的Form-Data')
                    times = times+1
                    pass
            else:
                print(f'第{times}次尝试，课程余量不足，选课失败咯~')        
                logRec('{"msg":"课程余量不足.","success":"false"}')
                try:
                    dbDelete.delete(collection)
                except Exception as e:
                    print(e)
                times = times+1
                time.sleep(10)
            '''
        
        if info[1] == '必修课':                                #必修课的选课功能暂不可用
            print('脚本暂不提供必修课服务噢~')
            '''
            col_name = 'majorCourse'
            collection = dbClient(col_name)       
            ver = verify(collection, info[0], info[2])     
            if ver[0]:                     
                pos = 10
                typ = '必修课'
                data = makeDic(ver[1],account, typ)   
                tri = trial(pos, session, data)    
                if tri[0] == True:    
                    print(tri[1])
                    print(f'第{times}次尝试，选课成功咯~')
                    print('快打开本科教学网去探探自己心水已久的课程吧~')
                    break
                elif tri[0] == False:     
                    print(tri[1])         
                    print(f'第{times}次尝试，选课失败咯~')
                    times = times+1
                    break
                elif tri[0] == '选课接口返回错误，请检查网络情况/提交的Form-Data':      
                    print(f'第{times}次尝试，选课接口返回错误，请检查提交的Form-Data')
                    times = times+1
                    pass
            else:
                print(f'第{times}次尝试，课程余量不足，选课失败咯~')        
                logRec('{"msg":"课程余量不足.","success":"false"}')
                try:
                    dbDelete.delete(collection)
                except Exception as e:
                    print(e)
                times = times+1
                time.sleep(10)
            '''
        if info[1] == '跨选课':                                    #跨选课的选课功能暂不可用
            print('脚本暂不提供跨选课服务噢~')
            '''
            col_name = 'crossChoose'
            collection = dbClient(col_name)       
            ver = verify(collection, info[0], info[2])     
            if ver[0]:                     
                pos = 10
                typ = '跨专业选修课'
                data = makeDic(ver[1],account, typ)   
                tri = trial(pos, session, data)    
                if tri[0] == True:    
                    print(tri[1])
                    print(f'第{times}次尝试，选课成功咯~')
                    print('快打开本科教学网去探探自己心水已久的课程吧~')
                    break
                elif tri[0] == False:     
                    print(tri[1])         
                    print(f'第{times}次尝试，选课失败咯~')
                    times = times+1
                    break
                elif tri[0] == '选课接口返回错误，请检查网络情况/提交的Form-Data':      
                    print(f'第{times}次尝试，选课接口返回错误，请检查提交的Form-Data')
                    times = times+1
                    pass
            else:
                print(f'第{times}次尝试，课程余量不足，选课失败咯~')        
                logRec('{"msg":"课程余量不足.","success":"false"}')
                try:
                    dbDelete.delete(collection)
                except Exception as e:
                    print(e)
                times = times+1
                time.sleep(10)
            '''
def condiction(cou_name, cou_numb):         #mongo中记录的查询条件
    dic = {
        "alternativeCourses":
        {"$elemMatch":
         {"DYKCM":cou_name,"KXH":cou_numb}
         }
        }
    return dic

def verify(col, cou_name, cou_numb):
    while True:
        try:
            retri = col.find_one(condiction(cou_name, cou_numb), {'_id':0, 'alternativeCourses.$':1})    #如何从{[],[],[{},{},...,{}]}的数据结构中提取出一个内层字典
            if retri is not None:
                break
            else:
                print('可能是你键入的课程名/课序号错误了，要仔细检查噢~')      #键入错误1、2、4、6将在verify()中得到解决
                rekey = inputName()
                cou_name = rekey[0]
                cou_numb = rekey[2]
        except Exception as e:
            print('mongo数据库检索错误：'+e)
    li = retri['alternativeCourses']
    try:
        for each in li:
            dic = each
            break
    except Exception as e:
        print(e)
    #print(dic)
    num = dic['SKRS']                                                     #返回字段：{'_id': 0, 'SKRS': 1, 'KRL': 1}
    maxi = dic['KRL']
    if int(num) < int(maxi):
        ver = True
    else:
        ver = False
    return ver, dic

def makeDic(result, account, typ):         #构造FormData，注意：字典内的元素是有顺序的
    dic = {}
    dic['id'] = str(result.pop('ID'))
    dic['uid'] = account
    dic['xf'] = result.pop('XF')
    dic['xkfs'] = typ
    dic['xh'] = ''
    #print(dic)
    return dic

def trial(pos, session, data):
    url = api.apiList()[15]
    res_pre = session.get(api.apiList()[pos])
    res = session.post(url, data=data, verify=False)
    con = res.content.decode()
    #print(con)
    while True:
        try:
            dic = json.loads(con)
            #print(dic)
            break
        except Exception as e:
            print(e)
    if dic['success'] == 'false':           #根据选课接口返回的提示信息判断是否选课成功
        msg = dic['msg']
        logRec(con)
        return False, msg
    elif dic['success'] == 'true':
        msg = dic['msg']
        logRec(con)
        return True, msg
    else :
        warn = '选课接口返回错误，请检查网络情况/提交的Form-Data'
        return warn

def logRec(message):                       #记录选课日志
    time_stamp = int(time.time())
    #print(time_stamp)
    time_present = time.localtime(time_stamp)
    time_f = time.strftime('%Y-%m-%d %H:%M:%S', time_present)
    with open('./Log.md','a') as f:
        f.write(message)
        f.write('|'+time_f)
        f.write('\n')