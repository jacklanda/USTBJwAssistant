# -*- coding: UTF-8 -*-
#author:Jacklanda

'''
由于API接口返回的是现成的json格式p数据，故此直接将json赋给dic对象，并将dic返回。
'''
import json

def publicChoose(res):
    contents = res.decode()
    dic = json.loads(contents)
    #print(dic)
    name = 'publicChoose'
    return name, dic

if __name__ == '__main__':
    publicChoose()
