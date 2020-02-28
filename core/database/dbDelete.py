# -*- coding: UTF-8 -*-
#author:Jacklanda

'''
删除传入的mongo集合对象
'''
from pymongo import MongoClient

def delete(col):
    col.drop