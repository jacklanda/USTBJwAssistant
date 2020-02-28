# -*- coding: UTF-8 -*-
#author:Jacklanda
'''
数据存储模块使用MongoDB来进行数据的写入，更新（删除+插入）
数据入库前需要进行进一步地清洗：将各个键用其对应的中文含义替代
'''
from pymongo import MongoClient

def storer(name, dic):
    client = MongoClient()
    database = client['ustbJwspider']
    collection = database[name]        #先删除集合对象，再重新建立集合对象，避免历史数据堆积
    collection.drop()
    collection = database[name]
    collection.insert_one(dic)
    print(f'{name}已成功入库')

if __name__ == '__main__':
    name = 'collection_name'
    dic ={'key': 'value'}
    storer(name, dic)