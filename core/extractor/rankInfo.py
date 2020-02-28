# -*- coding: UTF-8 -*-
#author:Jacklanda
import re
from lxml import html

class rankInfo(object):
    
    def __init__(self, res):
        self.res = res
        self.ranksInfo()
    
    def selector(self):
        self.html_rankInfo = self.res.decode()
        selector = html.fromstring(self.html_rankInfo)
        return selector
    
    def getList(self, selector):
        re.sub(r'<!--\s+th>', r'<th>', self.html_rankInfo, count=0)         #以<!--\s+th>作为匹配目标的字串, '<th>',html_rankInfo为待匹配的字串，
        re.sub(r'</th>.*?>', r'</th>', self.html_rankInfo, count=0)       #通过re.sub方法将目标字串<!--  th>替换为<th>
        re.sub(r'<!--\s+td>', r'<td>', self.html_rankInfo, count=0)
        re.sub(r'</td>-->', r'</td>', self.html_rankInfo, count=0)
        #print(html_rankInfo)
        self.title = selector.xpath('//title/text()')[0]
        #print(self.title)
        self.note1 = re.search('<caption>(.*?)</caption>', self.html_rankInfo).group(1)
        #print(self.note1)
        self.note2 = selector.xpath('//body/h5/span[@style="color: red"]/text()')[0]
        #print(self.note2)
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

    def ranksInfo(self):
        selector_ = self.selector()
        li = self.getList(selector_)
        dic = {
            'title': self.title,
            'note1': self.note1,
            'note2': self.note2,
            'items': li
            }
        name = 'rankInfo'
        return name, dic
    
if __name__ == '__main__':
    rank = rankInfo()