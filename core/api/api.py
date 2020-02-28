# -*- coding: UTF-8 -*-
#author:Jacklanda
'''
getApi()方法提供了根据传入参数pos，以返回对应的url链接的功能，注意：传入的参数pos应为字符串str类型。
'''
    
def apiList():
    url_li = [
    'https://n.ustb.edu.cn/do-login',      #vpn登陆接口,pos=0
    'https://n.ustb.edu.cn/http-80/77726476706e69737468656265737421f5fb449d353e615e79469cbf8c576d30dd14c5990b/choose_courses/j_spring_security_check?vpn-12-o1-elearning.ustb.edu.cn',        #本科教学网登陆接口,pos=1
    'https://n.ustb.edu.cn/http-80/77726476706e69737468656265737421f5fb449d353e615e79469cbf8c576d30dd14c5990b/choose_courses/j_spring_security_logout',       #本科教学网登出接口,pos=2
    'https://n.ustb.edu.cn/http-80/77726476706e69737468656265737421f5fb449d353e615e79469cbf8c576d30dd14c5990b/choose_courses/information/singleStuInfo_singleStuInfo_loadSingleStuCxxfPage.action?vpn-12-o1-elearning.ustb.edu.cn',              #创新学分接口,pos=3
    'https://n.ustb.edu.cn/http-80/77726476706e69737468656265737421f5fb449d353e615e79469cbf8c576d30dd14c5990b/choose_courses/information/singleStuInfo_singleStuInfo_loadSingleStuScorePage.action?vpn-12-o1-elearning.ustb.edu.cn',             #课程成绩接口,pos=4
    'https://n.ustb.edu.cn/http-80/77726476706e69737468656265737421f5fb449d353e615e79469cbf8c576d30dd14c5990b/choose_courses/information/singleStuInfo_singleStuInfo_loadSingleStuTeachProgramPage.action?vpn-12-o1-elearning.ustb.edu.cn',      #教学计划接口,pos=5
    'https://n.ustb.edu.cn/http-80/77726476706e69737468656265737421f5fb449d353e615e79469cbf8c576d30dd14c5990b/choose_courses/information/singleStuInfo_singleStuInfo_loadSingleStuCetPage.action?vpn-12-o1-elearning.ustb.edu.cn',               #英语四六级接口,pos=6
    'https://n.ustb.edu.cn/http-80/77726476706e69737468656265737421f5fb449d353e615e79469cbf8c576d30dd14c5990b/choose_courses/information/singleStuInfo_singleStuInfo_loadSingleStuRankingInfoPage.action?vpn-12-o1-elearning.ustb.edu.cn',       #排名明细核对接口,pos=7
    'https://n.ustb.edu.cn/http-80/77726476706e69737468656265737421f5fb449d353e615e79469cbf8c576d30dd14c5990b/choose_courses/choosecourse/normalChooseCourse_chooseCourse_loadNormalNoticePage.action?vpn-12-o1-elearning.ustb.edu.cn&xsfl=normalFormal',        #选课须知接口,pos=8
    'https://n.ustb.edu.cn/http-80/77726476706e69737468656265737421f5fb449d353e615e79469cbf8c576d30dd14c5990b/choose_courses/choosecourse/normalChooseCourse_normalRequired_loadFormalNormalRequiredCoursesDisplay.action?vpn-12-o1-elearning.ustb.edu.cn&_dc=1581822439331&limit=5000&start=0&uid=41704215',     #必修课接口,pos=9
    'https://n.ustb.edu.cn/http-80/77726476706e69737468656265737421f5fb449d353e615e79469cbf8c576d30dd14c5990b/choose_courses/choosecourse/normalChooseCourse_normalMajorSelective_loadFormalNormalMajorSelectiveCourseDisplay.action?vpn-12-o1-elearning.ustb.edu.cn&_dc=1581822507396&limit=5000&start=0&uid=41704215',     #专选课接口,pos=10
    'https://n.ustb.edu.cn/http-80/77726476706e69737468656265737421f5fb449d353e615e79469cbf8c576d30dd14c5990b/choose_courses/choosecourse/normalChooseCourse_normalPublicSelective_loadFormalNormalPublicSelectiveCourses.action?vpn-12-o1-elearning.ustb.edu.cn&xqj=null&jc=null&kcm=&_dc=1581823171047&limit=5000&start=0&uid=41704215',    #公选课接口,pos=11
    'https://n.ustb.edu.cn/http-80/77726476706e69737468656265737421f5fb449d353e615e79469cbf8c576d30dd14c5990b/choose_courses/choosecourse/normalChooseCourse_normalKZYSelective_loadFormalNormalTeachingProgramsDisplay.action?vpn-12-o1-elearning.ustb.edu.cn&_dc=1581823300358&limit=25&page=1&start=0',        #跨选课接口,pos=12
    'https://n.ustb.edu.cn/http-80/77726476706e69737468656265737421f5fb449d353e615e79469cbf8c576d30dd14c5990b/choose_courses/choosecourse/commonChooseCourse_courseList_loadCodeTablesJson.action?vpn-12-o1-elearning.ustb.edu.cn&_dc=1581834524632',            #外选课接口,pos=13
    'https://n.ustb.edu.cn/http-80/77726476706e69737468656265737421f5fb449d353e615e79469cbf8c576d30dd14c5990b/choose_courses/choosecourse/commonChooseCourse_courseList_loadTermCourses.action?vpn-12-o1-elearning.ustb.edu.cn',                  #课程表接口,pos=14
    'https://n.ustb.edu.cn/http-80/77726476706e69737468656265737421f5fb449d353e615e79469cbf8c576d30dd14c5990b/choose_courses/choosecourse/normalChooseCourse_normalPublicSelective_addFormalNormalPublicSelectiveCourse.action?vpn-12-o1-elearning.ustb.edu.cn',  #选课接口,pos=15
    'https://n.ustb.edu.cn/http-80/77726476706e69737468656265737421f5fb449d353e615e79469cbf8c576d30dd14c5990b/choose_courses/choosecourse/normalChooseCourse_normalPublicSelective_removeFormalNormalPublicSelectiveCourse.action?vpn-12-o1-elearning.ustb.edu.cn',      #退课接口,pos=16
    'https://n.ustb.edu.cn/http/77726476706e69737468656265737421f5fb449d353e615e79469cbf8c576d30dd14c5990b/choose_courses/loginsucc.action'                   #本科教学网登陆成功验证接口,pos=17
    ]
    return url_li

if __name__ == '__main__':
    print('打印api接口ing')
    print(apiList())