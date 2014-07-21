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
def initEnvironment():
        """ Initialize GIScript Environment,Load Library.
        """
        smlib_path = os.path.dirname(sys.path[0]+"/../smlib_python/")
        print "smlib path: ", smlib_path
        sys.path.append(smlib_path)

        smlib_so = smlib_path + "/7.1/Linux64/bin/"
        print "smlib_so path: ",smlib_so
        sys.path.append(smlib_so)

        smlib_ugc = "/media/supermap/Application/GeoScript/GIScript/lib/7.1/Linux64/ugc_710_64_x64_linux_gcc_Bin/"
        print "smlib_ugc path: ",smlib_ugc
        sys.path.append(smlib_ugc)

    
def testOpenUDB():
        print "UDB: " + udbpath
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
                print u"打开数据源失败"
                print u"UDB文件不存在：" + udbpath

        
help =u"----------------------------------------------------------\n\
说明:打开udb数据源，列出数据集名\n\
用法: CreateUDBDS.py      \n\
----------------------------------------------------------\n"

if __name__=='__main__':
        print "Test Open Datasource."
        #reload(sys)
        #sys.setdefaultencoding("utf-8")
        
        print "Init..."
        initEnvironment()
        #import smlib
        #smlib.load_smlib_ugc()
        #smlib.load_smlib()
        #import libSuBase
        #import libSuDataExchange
        #import smEngine
        import smu
        #testOpenUDB()
        sys.exit()
