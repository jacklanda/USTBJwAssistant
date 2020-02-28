# -*- coding: UTF-8 -*-
#author:Jacklanda
import time
from pymongo import MongoClient

def cleanse():
    collection()[1].drop()
    col_old = collection()[0]
    col_new = collection()[1]
    agrigation = col_old.aggregate(condition())
    for each in agrigation:
        item = each['alternativeCourses']
        #print(item)
        dic = trans(item)
        col_new.insert_one(dic)
    
def collection():
    client = MongoClient()
    database = client['ustbJwspider']
    col_old = database['publicChoose']
    col_new = database['publicCourse']
    return col_old, col_new

def condition():
    con = [
        {'$unwind': '$alternativeCourses'},
        {'$project':
         {'_id':0, 'alternativeCourses': 1 }
         }
        ]
    return con

def trans(item):
    dic = {
        '选课id': item['ID'],
        '课程名': item['DYKCM'],
        '任课教师': item['JSM'][0]['JSM'],
        '学时': item['XS'],
        '学分': item['DYXF'],
        '选课人数': item['SKRS'],
        '容量': item['KRL'],
        '已选': item['SKRS'],
        '备注': item['BZ'],
        '课程类别': '公选课',
        '上课时间地点': item['SKSJDD'],
        '课程号': item['KCH'],
        '课序号': item['KXH'],
        '补选截止时间': item['TKJZRQ'],
        }
    return dic
        
if __name__ == '__main__':
    start = time.time()
    try:
        cleanse()
    except Exception as e:
        print(e)
    end = time.time()
    print(f'数据清洗花费的时间为：{end-start} 秒')
