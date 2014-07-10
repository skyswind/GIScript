# -*- coding: gbk -*-
#===================================
#矢量文件数据转SuperMap Udb格式
#ImportVectorFileToUDB.py
#运行环境Python2.7.6，Python3.x版本会有问题
#===================================

import sys
import os
import time
import getopt
from os.path import walk,join,normpath
import os.path as pth
import logging

class VectorFileToUDB():
    '''参数5个：
    filePath：转换文件路径；udbPath：UDB数据源路径；fileType：转换文件类型；
    datasourceName：保存转换结果的数据源；encodeType：结果数据集编码
    '''
    def __init__(self,filePath,udbPath,fileType,datasourceName,encodeType):
        self.filePath = filePath
        self.udbPath = udbPath
        self.fileType = fileType
        self.datasourceName = datasourceName
        self.encodeType = encodeType
        self.fileList = []
        self.importDataCount = 0  #记录成功导入的数据个数

    def SearchPath(self):
        #清空文件列表
        del self.fileList[:]
        #列出所选目录中的全部文件
        walk(self.filePath, self.visitFiles, 0)

    def visitFiles(self,arg,dirname,names):
        #当前目录中的所有文件列表
        curFileList = ()
        childFile = []
        for sfile in names:
            files = normpath(join(dirname,sfile))
            fileName = pth.split(files)[1]
            fileEx = pth.splitext(fileName)[1].upper()  # 获取扩展名
            if self.fileType == 'fileSHP' and fileEx == '.shp'.upper():
                childFile.append(files)
            elif self.fileType == 'fileMIF' and fileEx == '.mif'.upper():
                childFile.append(files)
            elif self.fileType == 'fileE00' and fileEx == '.e00'.upper():
                childFile.append(files)
            elif self.fileType == 'fileDWG' and fileEx == '.dwg'.upper():
                childFile.append(files)
            elif self.fileType == 'fileDXF' and fileEx == '.dxf'.upper():
                childFile.append(files)
            elif self.fileType == 'fileGDBVector' and fileEx == '.gdb'.upper():
                childFile.append(files)
            elif self.fileType == 'fileDGN' and fileEx == '.dgn'.upper():
                childFile.append(files)
            elif self.fileType == 'fileTAB' and fileEx == '.tab'.upper():
                childFile.append(files)
            elif self.fileType == 'fileAIBinCov' and fileEx == '.adf'.upper():
                childFile.append(files)
        if childFile:
            curFileList = (dirname,childFile)
            self.fileList.append(curFileList)

    def VectorFile2UDB(self):
        logging.info("初始化组件环境...")
        SuperMap.Init()
        self.SearchPath()
        datasourceAlias = ""
        datasources = {}
        datasetNames = {}
        engineType = 'sceUDB'

        logging.info("开始导入数据...")
        if len(self.fileList) > 0:
            for parent,files in self.fileList:
                if "None" == self.datasourceName:
                    L = parent.split("\\")
                    datasourceAlias = L[len(L) - 1]
                else:
                    datasourceAlias = self.datasourceName
                #创建数据源
                if not datasources.has_key(datasourceAlias):
                    if SuperMap.OpenDataSource(self.udbPath + '\\' + datasourceAlias + '.udb',"","",engineType,datasourceAlias) == 0:
                        isCreate = SuperMap.CreateDataSource(self.udbPath + "\\" + datasourceAlias,"","",engineType,datasourceAlias)
                        if isCreate == 1:
                            logging.info("创建数据源：[" + self.udbPath + '\\' + datasourceAlias + '.udb ' + "]成功。")
                        else:
                            logging.error("创建数据源：[" + self.udbPath + '\\' + datasourceAlias + '.udb ' + "]失败。")
                            SuperMap.Exit()
                            return
                    datasources[datasourceAlias] = datasourceAlias
                else:
                    SuperMap.CloseDataSource(datasourceAlias)
                    if SuperMap.OpenDataSource(self.udbPath + '\\' + datasourceAlias + '.udb',"","",engineType,datasourceAlias) == 0:
                        logging.info("打开数据源：[" + datasourceAlias + "]失败。")
                        SuperMap.Exit()
                        return
                #记录当前文件是否导入成功
                result = 0
                #导入shp数据
                for file in files:
                    fileName = pth.split(file)[1]
                    fileName = pth.splitext(fileName)[0]  # 获取不带扩展名的文件名
                    logging.info("开始导入数据：[" + file + "]...")
                    isImport = SuperMap.ImportVectorFile(datasourceAlias,fileName, self.encodeType,self.fileType, file, "GIS")
                    if isImport == 1:
                        logging.info("导入数据：[" + file + "]到数据源：[" + datasourceAlias + "]成功。")
                        self.importDataCount += 1
                    else:
                        logging.info("导入数据：[" + file + "]到数据源：[" + datasourceAlias + "]失败。")
                SuperMap.CloseDataSource(datasourceAlias)
        logging.info("导入操作完成。")
        logging.info("共有 " + str(self.importDataCount) + "个数据被成功导入为Udb格式。")
        SuperMap.Exit()

#---------------------------------------------------------------------------
if __name__ == '__main__':
    try:
        '''共传入7个参数，0：脚本文件路径；1：SuperMap Python组件路径；2：转换文件路径
        3：UDB文件路径；4：转换文件类型；5：数据源名称(None数据源以文件夹名称命名)；6：压缩编码类型'''
        if (len(sys.argv) == 7):
            sys.path.append(sys.argv[1])  #将.net组件的路径添加到环境变量
            import smu as SuperMap        #导入SuperMap模块
            logPath = sys.argv[3] + r'\矢量数据转换.log'         #日志文件路径为数据源存放路径
            #定义日志文件路径，输出级别及其格式
            logging.basicConfig(filename=logPath,level=logging.DEBUG,format='%(asctime)s %(levelname)-8s %(message)s')
            logging.basicConfig(filename=logPath,level=logging.DEBUG,format='%(asctime)s %(levelname)-8s %(message)s')
            #定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象
            #可以同时输出日志信息到文本文件和控制台，在C#程序中调用的时候可以获取到控制台程序输出
            console = logging.StreamHandler(sys.stdout)
            console.setLevel(logging.INFO)
            #日志信息开团加info:是为了和SuperMap组件输出的日志信息区别
            console.setFormatter(logging.Formatter('info:' '%(message)s'))
            logging.getLogger('').addHandler(console)
            objImport = VectorFileToUDB(sys.argv[2],sys.argv[3] ,sys.argv[4],sys.argv[5],sys.argv[6])
            objImport.VectorFile2UDB()
        else:
            print "执行脚本失败，脚本参数不正确。"
    except Exception,ex:
        print "执行脚本失败:" + ex.message
        sys.exit(2)
    #=========================================测试代码===============================================
    #测试数据源以文件夹名
    #objImport = VectorFileToUDB(r"E:\Data\数据转换测试数据\SHP",r"E:\Data\数据转换测试数据\SHP" ,"fileSHP","None","encNONE")
    #logPath = r'E:\Data\数据转换测试数据\SHP\log.log'
    #logging.basicConfig(filename=logPath,level=logging.DEBUG,format='%(asctime)s %(levelname)-8s %(message)s')
    ##定义一个Handler打印INFO及以上级别的日志到sys.stdout
    ##可以同时输出日志信息到文本文件和控制台，在C#程序中调用的时候可以获取到控制台程序输出
    #console = logging.StreamHandler(sys.stdout)
    #console.setLevel(logging.INFO)
    ##日志信息开团加info:是为了和SuperMap组件输出的日志信息区别
    #console.setFormatter(logging.Formatter('info:' '%(message)s'))
    #logging.getLogger('').addHandler(console)
    #sys.path.append(r"E:\CodeSource\sgs_src\DataManager7.0\D-Process\Bin")  #将.net组件的路径添加到环境变量
    #import smu as SuperMap #导入SuperMap模块
    #objImport.VectorFileToUDB()
    #=========================================测试代码===============================================
