# coding: utf-8
#===================================================
#打开UDB数据源，UDB 路径 ./worldpy.udb
#基本流程:
#1、初始化默认字符编码环境（utf-8）
#2、加载 pylib 环境， import smEngine
#3、打开UDB数据源,，遍历数据集名
#4、关闭UDB数据源
#===================================================

import sys
import string
import os

udbpath=unicode(sys.path[0]+'/smlib_worldpy.udb',"utf-8")

# 初始化 pylib 环境
def initSMLib():
	""" Initialize GIScript Environment,Load Library.
	"""
	smlib_path=os.path.dirname(sys.path[0]+"/../smlib/")
	print "Load Library,smlib path: ", smlib_path
	sys.path.append(smlib_path)

def listDataset():
	if os.path.exists(udbpath):
		uds = smEngine.uds(udbpath, u'smlib_worldpy')
		bOpen = uds.Open()
		
		if bOpen == 1 or uds.GetDatasetCount()==0:
			dtNames=uds.GetAllDatasetName()
			print  u"数据集列表："
			for dtName in dtNames:
				print unicode(dtName)
		else:
			print u"打开数据源失败"
			
		uds.Close()
	else:
		print u"打开数据源失败,可能UDB文件不存在：" + udbpath

if __name__=='__main__':
	print "List Dataset of   Datasource."
	reload(sys)
	sys.setdefaultencoding("utf-8")
	initSMLib()
	import smlib
	smlib.load_smlib()
	import smEngine

	listDataset()
