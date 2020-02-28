# -*- coding: UTF-8 -*-
#author:Jacklanda

import re
from lxml import html

class teachPlan(object):
    
    def __init__(self, res):
        self.res = res
        self.teachPlans()
    
    def selector(self):
        self.html_teachPlan = self.res.decode()
        selector = html.fromstring(self.html_teachPlan)
        return selector
    
    def getList(self, selector):
        self.title = selector.xpath('//title/text()')[0]
        #print(self.title)
        self.note1 = re.findall('<caption>(.*?)</caption>', self.html_teachPlan)
        #print(self.note1)
        self.note2 = selector.xpath('//h5/span[@style="color: red"]/text()')[0]
        #print(self.note2)
        self.note3 = selector.xpath('//h5[@id="jqpjnote"]/text()')[0]
        #print(self.note3)
        key_maj = selector.xpath('//table[1][@class="gridtable"]/thead/tr/th/text()')
        temp1 = key_maj[8]
        key_maj[8] = key_maj[13]
        key_maj[13] = temp1
        temp2 = key_maj[7]
        key_maj[7] = key_maj[12]
        key_maj.pop(12)
        key_maj.pop(12)
        key_maj.insert(9, '免修')
        #print(key_maj)
        key_pro = selector.xpath('//table[2][@class="gridtable"]/thead/tr/th/text()')
        #print(key_pro)
        key_pub = selector.xpath('//table[3][@class="gridtable"]/thead/tr/th/text()')
        #print(key_pub)
        block_maj = selector.xpath('//tbody[1]/tr')
        block_pro = selector.xpath('//tbody[2]/tr')
        block_pub = selector.xpath('//tbody[3]/tr')
        li1 = []
        for each in block_maj:        #将必修课信息写入字典
            info_dic = {}
            for i in range(len(key_maj)):
                try:
                    info_dic[key_maj[i]] = each[i].text
                except:
                    info_dic[key_maj[i]] = ''
            li1.append(info_dic)
        li2 = []
        for each in block_pro:        #将专选课信息写入字典
            info_dic = {}
            for i in range(len(key_pro)):
                try:
                    info_dic[key_pro[i]] = each[i].text
                except:
                    info_dic[key_pro[i]] = ''
            li2.append(info_dic)
        li3 = []
        for each in block_pub:        #将公选课信息写入字典
            info_dic = {}
            for i in range(len(key_pub)):
                try:
                    info_dic[key_pub[i]] = each[i].text
                except:
                    info_dic[key_pub[i]] = ''
            li3.append(info_dic)
        return (li1, li2, li3)

    def teachPlans(self):
        selector_ = self.selector()
        li = self.getList(selector_)
        dic = {
            'title': self.title,
            'note1': self.note1,
            'note2': self.note2,
            'note3': self.note3,
            self.note1[0]: li[0],
            self.note1[1]: li[1],
            self.note1[2]: li[2]
            }
        #print(dic)
        name = 'teachPlan'
        return name, dic

if __name__ == '__main__':
    cou = teachPlan()