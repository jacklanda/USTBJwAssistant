# -*- coding: UTF-8 -*-
#author:Jacklanda
'''
courseList()从经过清洗的publicChoose库中抽出实时可选的课列表（该课列表仅作为参考）
'''
import time
from pymongo import MongoClient

def courseInfo():
    col_cleaned = collection().find({}, {'_id':0})
    dics_li = sort(col_cleaned)
    print('\n>>>>>>>>>>下列为实时的可选课程，以供参考<<<<<<<<<<<<\n')
    intro(dics_li)
    print('\n>>>>>>>>>>以上为实时的可选课程，以供参考<<<<<<<<<<<<')

def sort(col):
    li = []
    for each in col:
        time_get = time.mktime(time.strptime(each['补选截止时间'], '%Y-%m-%d'))
        time_now = int(time.time())
        if int(each['选课人数']) < each['容量'] and time_now < time_get:
            li.append(each)
        else:
            pass
    return li
    
def intro(dics_li):
    num = 1
    for each in dics_li:
        id = each['选课id']
        cou_name = each['课程名']
        teacher = each['任课教师']
        credit = each['学分']
        cou_num = each['课程号']
        cou_ord = each['课序号']
        persons = each['选课人数']
        container = each['容量']
        end_time = each['补选截止时间']
        print('---------------------------------------------------------------------')
        print(f'{num}. 选课id：{id} |课程名:{cou_name} |任课教师:{teacher} |学分:{credit}|\n \t课程号:{cou_num} |课序号:{cou_ord} |选课人数:{persons} |容量:{container} |补选截止时间:{end_time}')
        num = num+1

def collection():
    client = MongoClient()
    database = client['ustbJwspider']
    col_new = database['publicCourse']
    return col_new
        
if __name__ == '__main__':
    courseInfo()
