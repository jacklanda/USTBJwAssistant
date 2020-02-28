# -*- coding: UTF-8 -*-
#author:Jacklanda

import re
from lxml import html

class courseInfo(object):
    
    def __init__(self, res):
        self.res = res
        self.coursesInfo()
    
    def selector(self):
        self.html_courseInfo = self.res.decode()
        selector = html.fromstring(self.html_courseInfo)
        return selector
    
    def getList(self, selector):
        self.title = selector.xpath('//title/text()')[0]
        #print(self.title)
        self.note1 = re.search('<caption>(.*?)</caption>', self.html_courseInfo).group(1)
        #print(self.note1)
        self.note2 = selector.xpath('//h5/span[@style="color: red"]/text()')[0]
        #print(self.note2)
        note3 = selector.xpath('//h5[2]')[0]
        self.note3 = note3.xpath('string(.)').strip()
        #print(self.note3)
        note4 = selector.xpath('//h5[3]')[0]
        self.note4 = note4.xpath('string(.)').strip()
        #print(self.note4)
        self.note5 = selector.xpath('//h5[4]/text()')[0]
        #print(self.note5)
        key = selector.xpath('//thead/tr/th/text()')
        #print(key)
        block = selector.xpath('//tbody/tr')
        li = []
        for each in block:
            info_dic = {}
            for i in range(len(key)):
                info_dic[key[i]] =each[i].text
            li.append(info_dic)
        #print(li)
        return li

    def coursesInfo(self):
        selector_ = self.selector()
        li = self.getList(selector_)
        dic = {
            'title': self.title,
            'note1': self.note1,
            'note2': self.note2,
            'note3': self.note3,
            'note4': self.note4,
            'note5': self.note5,
            'items': li
            }
        name = 'courseInfo'
        #print(name)
        #print(dic)
        return name, dic

if __name__ == '__main__':
    cou = courseInfo()