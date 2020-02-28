# -*- coding: UTF-8 -*-
#author:Jacklanda
'''
mid
'''
from core.database import db
from core.extractor import innoCredi as inno
from core.extractor import courseInfo as course
from core.extractor import rankInfo as rank
from core.extractor import teachPlan as teach
from core.extractor import majorCourse as maj
from core.extractor import publicChoose as pub
from core.extractor import crossChoose as cro
from core.extractor import proChoose as pro
from core.extractor import courseTable as table
from core.extractor import nonProchoose as nonPro

def infoExtract(choice, res):
    if choice == '1':
        print('******************创新学分信息清洗中******************\n')
        info = inno.innoCredit(res)       #类调用
        infos = info.innoCredits()        #类下的函数调用
        try:
            db.storer(infos[0], infos[1])
        except:
            print('数据已清洗完毕，但未能成功入库')
    if choice == '2':
        print('******************课程成绩信息清洗中******************\n')
        info = course.courseInfo(res)
        infos = info.coursesInfo()
        try:
            db.storer(infos[0], infos[1])
        except:
            print('数据已清洗完毕，但未能成功入库')
    if choice == '3':
        print('******************教学计划信息清洗中******************\n')
        info = teach.teachPlan(res)
        infos = info.teachPlans()
        try:
            db.storer(infos[0], infos[1])
        except:
            print('数据已清洗完毕，但未能成功入库')
    if choice == '4':
        print('******************英语四六级信息清洗中******************\n')
        print('本科教学网的英语四六级功能已作废，故脚本暂不提供该功能')
    if choice == '5':
        print('******************排名明细核对信息清洗中******************\n')
        info = rank.rankInfo(res)
        infos = info.ranksInfo()
        try:
            db.storer(infos[0], infos[1])
        except:
            print('数据已清洗完毕，但未能成功入库')
    if choice == '6':
        print('******************选课须知信息清洗中******************\n')
        print('由于选课须知的接口返回错误，故脚本暂时不提供该功能')
    if choice == '7':
        print('******************必修课信息清洗中******************\n')
        infos = maj.majorCourse(res)
        try:
            db.storer(infos[0], infos[1])
        except:
            print('数据已清洗完毕，但未能成功入库')
    if choice == '8':
        print('******************专业选修课信息清洗中******************\n')
        infos = pro.proChoose(res)
        try:
            db.storer(infos[0], infos[1])
        except:
            print('数据已清洗完毕，但未能成功入库')
    if choice == '9':
        print('******************公共选修课信息清洗中******************\n')
        infos = pub.publicChoose(res)
        try:
            db.storer(infos[0], infos[1])
        except:
            print('数据已清洗完毕，但未能成功入库')
    if choice == '10':
        print('******************跨专业选课信息清洗中******************\n')
        infos = cro.crossChoose(res)
        try:
            db.storer(infos[0], infos[1])
        except:
            print('数据已清洗完毕，但未能成功入库')
    if choice == '11':
        print('******************外专业选课信息清洗中******************\n')
        print('由于作者的账号并无外专业选课信息，故脚本暂不支持该功能')
    if choice == '12':
        print('******************课程表信息清洗中******************\n')
        infos = table.courseTable(res)
        try:
            db.storer(infos[0], infos[1])
        except:
            print('数据已清洗完毕，但未能成功入库')
            