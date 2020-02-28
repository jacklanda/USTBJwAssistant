# -*- coding: UTF-8 -*-
#author:Jacklanda

import re
from lxml import html

class innoCredit(object):
    
    def __init__(self, res):
        self.res = res
        self.innoCredits()
    
    def selector(self):
        self.html_innoCredi = self.res.decode()
        selector = html.fromstring(self.html_innoCredi)
        return selector
    
    def getList(self, selector):
        self.title = selector.xpath('//title/text()')[0]
        #print(title)
        self.note1 = re.search('<caption>(.*?)</caption>', self.html_innoCredi).group(1)
        #print(note1)
        self.note2 = selector.xpath('//h5/span[@style="color: red"]/text()')[0]
        #print(note2)
        key = selector.xpath('//tr/th/text()')
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

    def innoCredits(self):
        selector_ = self.selector()
        li = self.getList(selector_)
        dic = {
            'title': self.title,
            'note1': self.note1,
            'note2': self.note2,
            'items': li
            }
        #print(dic)
        name = 'innoCredits'
        return name, dic
    
if __name__ == '__main__':
    cre = innoCredit()