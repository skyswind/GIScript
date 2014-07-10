# -*- coding: gbk -*-
#===================================
#矢量文件数据转SuperMap Udb格式
#ImportRasterFileToUDB.py
#运行环境Python2.7.6，Python3.x版本会有问题
#===================================

import sys
import os
import time
import getopt
from os.path import walk,join,normpath
import os.path as pth
import logging

class RasterFileToUDB():
    '''参数10个，filePath：转换文件路径；udbPath：UDB文件路径；fileType：转换文件类型；datasoruceName：数据源名称(None数据源以文件夹名称命名)；
    datasetName：数据集名称；isGrid：数据集类型(0为影像，1为栅格)；encodeType：压缩编码类型；
    isBuildPyramid：是否创建影像金字塔；isSplicing：是否拼接影像；pixelFormat：像素格式'''
    def __init__(self,filePath,udbPath,fileType,datasoruceName,datasetName,isGrid,encodeType,isBuildPyramid,isSplicing,pixelFormat):
        self.filePath = filePath
        self.udbPath = udbPath
        self.fileType = fileType
        self.datasourceName = datasoruceName
        self.datasetName = datasetName
        self.isGrid = int(isGrid)
        self.encodeType = encodeType
        self.isBuildPyramid = int(isBuildPyramid)
        self.isSplicing = int(isSplicing)
        self.pixelFormat = pixelFormat
        self.fileList = []
        self.importDataCount = 0    #记录成功导入的数据个数

    def ToUDB(self):
        logging.info("初始化组件环境...")
        SuperMap.Init()
        self.SearchPath()
        if self.isSplicing:
            self.RasterToUDBAndMerge()
        else:
            self.RasterToUDB()

    def SearchPath(self):
        #清空文件列表
        del self.fileList[:]
        #列出所选目录中的全部文件
        path = self.filePath
        walk(path, self.visitFiles, 0)

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
            
    def RasterToUDB(self):
        datasourceAlias = ""
        datasources = {}
        datasetNames = {}
        engineType = 'sceUDB'
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
                        if SuperMap.CreateDataSource(self.udbPath + "\\" + datasourceAlias,"","",engineType,datasourceAlias):
                            logging.info("创建数据源：[" + self.udbPath + '\\' + datasourceAlias + '.udb ' + "]成功。")
                        else:
                            logging.error("创建数据源：[" + self.udbPath + '\\' + datasourceAlias + '.udb ' + "]失败。")
                            SuperMap.Exit()
                            return
                    datasources[datasourceAlias] = datasourceAlias
                else:
                    SuperMap.CloseDataSource(datasourceAlias)
                    if SuperMap.OpenDataSource(self.udbPath + '\\' + datasourceAlias + '.udb',"","",engineType,datasourceAlias) == 0:
                        logging.error("打开数据源：[" + datasourceAlias + "]失败。")
                        SuperMap.Exit()
                        return
    
                for rasterFile in files:
                    datasetName = pth.split(rasterFile)[1]
                    datasetName = pth.splitext(datasetName)[0]  # 获取不带扩展名的文件名
                    #SuperMap数据集命名中不能出现'.'和'-',系统在执行导入操作时，自动将'.'替换为下划线'_'
                    datasetName = datasetName.replace('.', '_')
                    datasetName = datasetName.replace('-', '_')
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
        
    def RasterToUDBAndMerge(self):
        engineType = 'sceUDB'
        L = []
        left = []
        top = []
        right = []
        bottom = []
        ratiox = []
        ratioy = []
        if len(self.fileList) > 0:
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
            
            datasourceAlias = self.datasourceName
            if SuperMap.OpenDataSource(self.udbPath + '\\' + datasourceAlias + '.udb',"","",engineType,datasourceAlias) == 0:
                if SuperMap.CreateDataSource(self.udbPath + "\\" + datasourceAlias,"","",engineType,datasourceAlias):
                    logging.info("创建数据源：[" + self.udbPath + '\\' + datasourceAlias + '.udb ' + "]成功。")
                else:
                    logging.error("创建数据源：[" + self.udbPath + '\\' + datasourceAlias + '.udb ' + "]失败。")
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
            ##以下操作用于设置ClipRegion， 部分接口有问题，不能使用
            #rgnDtName = "Rgn"
            #logging.info("导入数据：[" + rasterFile + "] 到数据源：[" + datasourceAlias + "]成功。")
            #SuperMap.CreateDatasetVector(datasourceAlias,rgnDtName,"Region","encDWORD")
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
        '''共传入12个参数，0：脚本文件路径；1：SuperMap Python组件路径；2：转换文件路径；3：UDB文件路径；
        4：转换文件类型；5：数据源名称(None数据源以文件夹名称命名)；6：数据集名称；7：数据集类型(0为影像，1为栅格)
        8：压缩编码类型；9：是否创建影像金字塔；10：是否拼接影像；11：像素格式'''
        if (len(sys.argv) == 12):
            sys.path.append(sys.argv[1])  #将.net组件的路径添加到环境变量
            import smu as SuperMap        #导入SuperMap模块
            logPath = sys.argv[3] + r'\栅格数据转换.log'         #日志文件路径为数据源存放路径
            #定义日志文件路径，输出级别及其格式
            logging.basicConfig(filename=logPath,level=logging.DEBUG,format='%(asctime)s %(levelname)-8s %(message)s')
            #定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象
            #可以同时输出日志信息到文本文件和控制台，在C#程序中调用的时候可以获取到控制台程序输出
            console = logging.StreamHandler(sys.stdout)
            console.setLevel(logging.INFO)
            #日志信息开头加info:是为了和SuperMap组件输出的日志信息区别
            console.setFormatter(logging.Formatter('info:' '%(message)s'))
            logging.getLogger('').addHandler(console)
            objImport = RasterFileToUDB(sys.argv[2],sys.argv[3] ,sys.argv[4],sys.argv[5],sys.argv[6],
                                        sys.argv[7],sys.argv[8],sys.argv[9],sys.argv[10],sys.argv[11])
            objImport.ToUDB()
        else:
            print "执行脚本失败，脚本参数不正确。"
        #=========================================测试代码===============================================
        #objImport = RasterFileToUDB(r'E:\Data\数据转换测试数据\tif',r'E:\Data\数据转换测试数据\tif','fileTIF','栅格测试','Image',
        #                            '0','encDCT','1','1','IPF_RGB')
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
        #objImport.ToUDB()
        #=========================================测试代码===============================================
    except Exception,ex:
        print "执行脚本失败:" + ex.message
        sys.exit(2)

    
  


