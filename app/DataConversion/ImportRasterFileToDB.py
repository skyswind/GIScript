# -*- coding: gbk -*-
#===================================
#栅格文件数据入库
#ImportRasterFileToDB.py
#运行环境Python2.7.6，Python3.x版本会有问题
#===================================

import sys
import os
import time
import getopt
from os.path import walk,join,normpath
import os.path as pth
import logging
import re

class RasterFileToDB():
    '''参数14个，filePath：转换文件路径；isRasterFile：是栅格文件路径还是从文本读取文件(1栅格文件，0从文本读取)；
    fileType：转换文件类型；engineType：引擎类型(sceOraclePlus,sceSQLPlus,sceOracleSpatial,sceDB2,sceSybasePlus,sceKingBase)；
    dbServer：实例名(SQLServer数据库服务名)；dbName：数据库名称(Oracle传入空值)；dbUser：用户名；dbPassword：密码；
    datasetName：数据集名称；isGrid：数据集类型(0为影像，1为栅格)；encodeType：压缩编码类型；
    isBuildPyramid：是否创建影像金字塔；isSplicing：是否拼接影像；pixelFormat：像素格式'''
    def __init__(self,filePath,isRasterFile,fileType,engineType,dbServer,dbName,dbUser,dbPassword,
                 datasetName,isGrid,encodeType,isBuildPyramid,isSplicing,pixelFormat):
        self.filePath = filePath
        self.isRasterFile = int(isRasterFile)
        self.fileType = fileType
        self.engineType = engineType
        self.dbServer = dbServer
        self.dbName = dbName
        self.dbUser = dbUser
        self.dbPassword = dbPassword
        self.datasetName = datasetName
        self.isGrid = int(isGrid)
        self.encodeType = encodeType
        self.isBuildPyramid = int(isBuildPyramid)
        self.isSplicing = int(isSplicing)
        self.pixelFormat = pixelFormat
        self.fileList = []
        self.importDataCount = 0    #记录成功导入的数据个数

    def ToDB(self):
        logging.info("初始化组件环境...")
        SuperMap.Init()
        self.SearchPath()
        if self.isSplicing:
            self.RasterToDBAndMerge()
        else:
            self.RasterToDB()

    def SearchPath(self):
        #清空文件列表
        del self.fileList[:]
        #列出所选目录中的全部文件
        path = self.filePath
        if self.isRasterFile:
            walk(path, self.visitFiles, 0)
        else:
            ReadPathFromText(path)

    def visitFiles(self,arg,dirname,names):
        #当前目录中的所有文件列表
        curFileList = ()
        childFile = []
        for sfile in names:
            files = normpath(join(dirname,sfile))
            fileName = pth.split(files)[1]
            fileEx = pth.splitext(fileName)[1].upper()  # 获取扩展名
            if self.fileType == 'fileTIF' and (fileEx == '.tif'.upper() or fileEx == '.tiff'.upper()):
                childFile.append(files)
            elif self.fileType == 'fileIMG' and fileEx == '.img'.upper():
                childFile.append(files)
            elif self.fileType == 'fileArcInfoGrid' and fileEx == '.grd'.upper():
                childFile.append(files)
            elif self.fileType == 'fileSIT' and fileEx == '.sit'.upper():
                childFile.append(files)
            elif self.fileType == 'fileGDBRaster' and fileEx == '.gdb'.upper():
                childFile.append(files)
            elif self.fileType == 'fileBMP' and fileEx == '.bmp'.upper():
                childFile.append(files)
            elif self.fileType == 'fileJPG' and fileEx == '.jpg'.upper():
                childFile.append(files)
            elif self.fileType == 'fileRAW' and fileEx == '.raw'.upper():
                childFile.append(files)
        if childFile:
            curFileList = (dirname,childFile)
            self.fileList.append(curFileList)

    def ReadPathFromText(self,path):
            f = open(path,"r")
            demfiles = f.readlines()
            f.close()
            #当前目录中的所有文件列表
            curFileList = ()
            childFile = []
            if len(demfiles) > 0:
                for file in demfiles:
                    childFile.append(file[:-1])
                curFileList = ("",childFile)
                self.fileList.append(curFileList)
        
    def ProcessDtName(self,dtName):
        '''
        组成字段名称的字符可以为字母、汉字、数字和下划线，字段名称不可以用数字和下划线开头，如果用
        字母开头，也不可以是sm；数据集的名称目前实际上是限制在30个字符内
        '''
        if len(dtName) > 30:
            dtName = dtName[:30]
        if dtName[:2].upper() == "SM":
            dtName = "T" + dtName
        dtName = re.sub(ur"^[^a-zA-Z\u4E00-\u9FFFF]", ur"T" + dtName[0], dtName)
        return re.sub(ur"[^\w\u4E00-\u9FFFF]", ur"_", dtName)
            
    def RasterToDB(self):
        if len(self.fileList) > 0: 
            datasourceAlias = self.dbUser
            if SuperMap.OpenDataSource(self.dbServer,self.dbUser,self.dbPassword,self.engineType,datasourceAlias,self.dbName) == 0:
                if SuperMap.CreateDataSource(self.dbServer,self.dbUser,self.dbPassword,self.engineType,datasourceAlias):
                    logging.info("创建数据源：[" + datasourceAlias + "]成功。")
                else:
                    logging.error("打开或创建数据源：[" + datasourceAlias + "]失败。")
                    SuperMap.Exit()
                    return
            for parent,files in self.fileList:
                for rasterFile in files:
                    datasetName = pth.split(rasterFile)[1]
                    datasetName = pth.splitext(datasetName)[0]  # 获取不带扩展名的文件名
                    datasetName = self.ProcessDtName(datasetName)
                    logging.info("开始导入数据：[" + rasterFile + "]...")
                    if SuperMap.ImportRasterFile(datasourceAlias,datasetName,self.encodeType,self.fileType,rasterFile,self.isGrid):
                        logging.info("导入数据：[" + rasterFile + "]到数据源：[" + datasourceAlias + "]成功。")
                        self.importDataCount += 1
                    else:
                        logging.error("导入数据：[" + rasterFile + "]到数据源：[" + datasourceAlias + "]失败。")
            #创建影像金字塔
            if self.isBuildPyramid:
                datasetCount = SuperMap.GetDatasetCount(datasourceAlias)
                for datasetIndex in range(datasetCount):
                    datasetName = SuperMap.GetDatasetName(datasourceAlias,datasetIndex)
                    logging.info('数据集' + datasetName + '开始创建影像金字塔...')
                    if SuperMap.BuildPyramid(datasourceAlias,datasetName):
                        logging.info("数据源：[" + datasourceAlias + "] 数据集：[" + datasetName + "]创建影像金字塔成功。")
                    else:
                        logging.error("数据源：[" + datasourceAlias + "] 数据集：[" + datasetName + "]创建影像金字塔失败。")
            #关闭数据源
            SuperMap.CloseDataSource(datasourceAlias)
        logging.info("导入操作完成。")
        logging.info("共有 " + str(self.importDataCount) + " 个数据被成功导入为UDB格式。")
        SuperMap.Exit()
        
    def RasterToDBAndMerge(self):
        L = []
        left = []
        top = []
        right = []
        bottom = []
        ratiox = []
        ratioy = []
        if len(self.fileList) > 0:
            datasourceAlias = self.dbUser
            if SuperMap.OpenDataSource(self.dbServer,self.dbUser,self.dbPassword,self.engineType,datasourceAlias,self.dbName) == 0:
                if SuperMap.CreateDataSource(self.dbServer,self.dbUser,self.dbPassword,self.engineType,datasourceAlias):
                    logging.info("创建数据源：[" + datasourceAlias + "]成功。")
                else:
                    logging.error("打开或创建数据源：[" + datasourceAlias + "]失败。")
                    SuperMap.Exit()
                    return
            for parent,files in self.fileList:
                for rasterFile in files:
                    L = SuperMap.GetImageGeoRef(self.fileType,rasterFile)
                    l = float(L[0][0])
                    t = float(L[0][1])
                    r = float(L[0][2])
                    b = float(L[0][3])
                    w = int(L[1][0])
                    h = int(L[1][1])
                    x = (r - l) / w
                    y = (t - b) / h

                    left.append(l)
                    top.append(t)
                    right.append(r)
                    bottom.append(b)
                    ratiox.append(x)
                    ratioy.append(y)
                
            #获得Bounds
            dLeft = min(left)
            dRight = max(right)
            dTop = max(top)
            dBottom = min(bottom)
            
            #算出分辨率
            dRatioX = min(ratiox)
            dRatioY = min(ratioy)
            
            #算出长宽
            nWidth = int((dRight - dLeft) / dRatioX)
            nHeight = int((dTop - dBottom) / dRatioY)
            
            #重设Right和Bottom，以保证分辨率的正确性
            dRight = dLeft + dRatioX * nWidth
            dBottom = dTop - dRatioY * nHeight
            
            if SuperMap.OpenDataSource(self.dbServer,self.dbUser,self.dbPassword,self.engineType,datasourceAlias,self.dbName) == 0:
                if SuperMap.CreateDataSource(self.dbServer,self.dbUser,self.dbPassword,self.engineType,datasourceAlias):
                    logging.info("创建数据源：[" + datasourceAlias + "]成功。")
                else:
                    logging.error("创建数据源：[" + datasourceAlias + "]失败。")
                    SuperMap.Exit()
                    return
            #使用上面采集到的信息创建DEM或Grid数据集,最后一个参数标志数据集为压缩模式
            datasetType = "Grid" if self.isGrid == '0' else "Image"
            if SuperMap.CreateDatasetRaster(datasourceAlias,self.datasetName,datasetType,self.encodeType,self.pixelFormat,nWidth,nHeight,dLeft,dTop,dRight,dBottom,256):
                logging.info("创建数据集：[" + self.datasetName + "]成功。")
            else:
                logging.error("创建数据集：[" + self.datasetName + "]失败。")
                SuperMap.Exit()
                return
            #循环追加文件
            for parent,files in self.fileList:
                for rasterFile in files:
                    logging.info("开始导入数据：" + rasterFile + " ...")
                    if SuperMap.AppendRasterFile(datasourceAlias,self.datasetName,self.fileType,rasterFile):
                        logging.info("导入数据：[" + rasterFile + "] 到数据源：[" + datasourceAlias + "]成功。")
                        self.importDataCount += 1
                    else:
                        logging.error("导入数据：[" + rasterFile + "] 到数据源：[" + datasourceAlias + "]失败。")
            ##以下操作用于设置ClipRegion, 底层部分接口有问题
            #rgnDtName = "Rgn"
            #SuperMap. CreateDatasetVector(datasourceAlias,rgnDtName,"Region","encNONE")
            #for parent,files in self.fileList:
            #    for tifile in files:
            #        SuperMap.MakeBoundsRgn(tifile,fileType,datasourceAlias,rgnDtName)
            #nID = SuperMap.UnionRgnDt(datasourceAlias,rgnDtName)

            ##设置ClipRegion
            #if SuperMap.SetClipRegion(datasourceAlias,self.datasetName,datasourceAlias,rgnDtName,nID):
            #    logging.info("为影像数据集" + self.datasetName + "设置裁剪矩阵成功。")
            #else:
            #    logging.info("为影像数据集" + self.datasetName + "设置裁剪矩阵失败。")

            #创建影像金字塔
            if self.isBuildPyramid:
                logging.info('开始创建影像金字塔...')
                if SuperMap.BuildPyramid(datasourceAlias,self.datasetName):
                    logging.info("数据源：[" + datasourceAlias + "] 数据集：[" + self.datasetName + "]创建影像金字塔成功。")
                else:
                    logging.error("数据源：[" + datasourceAlias + "] 数据集：[" + self.datasetName + "]创建影像金字塔失败。")
            #关闭数据源
            SuperMap.CloseDataSource(datasourceAlias)
        logging.info("导入操作完成。")
        logging.info("共有 " + str(self.importDataCount) + " 个数据被成功导入为UDB格式。")
        SuperMap.Exit()

#---------------------------------------------------------------------------
if __name__ == '__main__':
    try:
        '''共传入16个参数，0：脚本文件路径；1：SuperMapPython组件路径；2：转换文件路径；3：是栅格文件路径还是从文本读取文件(1栅格文件，0从文本读取)；
        4：转换文件类型；5：引擎类型(sceOraclePlus,sceSQLPlus,sceOracleSpatial,sceDB2,sceSybasePlus,sceKingBase)；
        6：实例名(SQLServer数据库服务名)；7：数据库名称(Oracle传入空值)；8：用户名；9：密码；
        10：数据集名称；11：数据集类型(0为影像，1为栅格)；12：压缩编码类型；
        13：是否创建影像金字塔 14：是否拼接影像 15：像素格式'''
        if (len(sys.argv) == 16):
            sys.path.append(sys.argv[1])  #将.net组件的路径添加到环境变量
            import smu as SuperMap        #导入SuperMap模块
            logPath = sys.argv[2] + r'\栅格数据转换.log'         #日志文件路径为数据源存放路径
            #定义日志文件路径，输出级别及其格式
            logging.basicConfig(filename=logPath,level=logging.DEBUG,format='%(asctime)s %(levelname)-8s %(message)s')
            #定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象
            #可以同时输出日志信息到文本文件和控制台，在C#程序中调用的时候可以获取到控制台程序输出
            console = logging.StreamHandler(sys.stdout)
            console.setLevel(logging.INFO)
            #日志信息开头加info:是为了和SuperMap组件输出的日志信息区别
            console.setFormatter(logging.Formatter('info:' '%(message)s'))
            logging.getLogger('').addHandler(console)
            objImport = RasterFileToDB(sys.argv[2],sys.argv[3] ,sys.argv[4],sys.argv[5],sys.argv[6],sys.argv[7],sys.argv[8],
                                        sys.argv[9],sys.argv[10],sys.argv[11],sys.argv[12],sys.argv[13],sys.argv[14],sys.argv[15])
            objImport.ToDB()
        else:
            print "执行脚本失败，脚本参数不正确。"

        ##=========================================测试代码===============================================
        #objImport = RasterFileToDB(r'E:\Data\数据转换测试数据\tif','1','fileTIF','sceOraclePlus','172.16.10.60','smTest',
        #                            'smTest','sagis','Image','0','encDCT','1','1','IPF_RGB')
        #sys.path.append("E:\CodeSource\sgs_src\DataManager7.0\D-Process\Bin")  #将.net组件的路径添加到环境变量
        #import smu as SuperMap        #导入SuperMap模块
        #logPath = r'E:\Data\数据转换测试数据\tif\栅格数据转换.log'         #日志文件路径为数据源存放路径
        ##定义日志文件路径，输出级别及其格式
        #logging.basicConfig(filename=logPath,level=logging.DEBUG,format='%(asctime)s %(levelname)-8s %(message)s')
        ##定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象
        ##可以同时输出日志信息到文本文件和控制台，在C#程序中调用的时候可以获取到控制台程序输出
        #console = logging.StreamHandler(sys.stdout)
        #console.setLevel(logging.INFO)
        ##日志信息开头加info:是为了和SuperMap组件输出的日志信息区别
        #console.setFormatter(logging.Formatter('info:' '%(message)s'))
        #logging.getLogger('').addHandler(console)
        #objImport.ToDB()
        ##=========================================测试代码===============================================
    except Exception,ex:
        print "执行脚本失败:" + ex.message
        sys.exit(2)