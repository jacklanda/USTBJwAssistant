# -*- coding: UTF-8 -*-
#author:Jacklanda

'''
由于API接口返回的是现成的json格式p数据，故此直接将json赋给dic对象，并将dic返回。
'''
import json

def nonProchoose():
    with open('./extractor/nonProchoose.txt', 'rb') as f:
        contents = f.read()
        dic = json.loads(contents)
        assert '.' not in dic.keys()[0]
        print(dic)
    name = 'nonProchoose'
    return name, dic

if __name__ == '__main__':
   nonProchoose()
