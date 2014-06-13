# coding: utf-8
#===================================================
#影像成批导入SuperMap UDB / Oracle 工具.
#基本流程:
#1、扫描目录，或者根据经纬度按照块的高宽生成文件列表。
#2、扫描存在的文件，获取最大的坐标范围。
#3、扫描存在的文件，获取像素格式。
#4、遍历文件列表，对于存在的文件追加到打开的数据库UDB/Oracle中。
#5、创建金字塔索引，以加快显示速度。（可选的过程）
#===================================================

import sys
import string
import re
import os
import time
import smu
import smEngine

help =u"----------------------------------------------------------\n\
说明:创建udb数据源\n\
用法: CreateUDBDS.py path\n\
----------------------------------------------------------\n"
if __name__=='__main__':
    reload(sys)
    sys.setdefaultencoding("utf-8")
	
    if len(sys.argv) == 2:
		uds = smEngine.uds(sys.argv[1], u'uds') 
		uds.Create()
	
    else:
        print help
        sys.exit()