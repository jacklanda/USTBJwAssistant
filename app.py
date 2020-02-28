# -*- coding: UTF-8 -*-
#author:Jacklanda
'''
程序入口
'''
import sys, os
from core import main

if __name__ == '__main__':
    try:
        os.mkdir('./metadata')
    except:
        print('@该目录已存在，将默认使用之')
    main.ustbJwspider()
    sys.exit(0)