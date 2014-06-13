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

def getType(ext):
    if ext.lower() == 'tif':
        return u'fileTIF'
    elif ext.lower() == 'img':
        return u'fileIMG'
    
#匹配正则表达式，符合条件的append到datafiles，用于追加
def walkPath(type, path):
    print path
    datafiles = []
    reMatch = '[\d\D]*.tif$'
    if type=='img':
        reMath = '[\d\D]*.img$'
    for root, dirs, files in os.walk(path):
        for file in files:
            if (re.match(reMatch,file)):
                file=unicode(file,"utf-8")
#                print file
                datafiles.append(os.path.join(root, file))
    return datafiles

def calcDatasetInfo(type, datafiles):
    L=[]
    left=[]
    top=[]
    right=[]
    bottom=[]
    ratiox=[]
    ratioy=[]
    #获取每个影像文件的左右地理范围，保存到数组
    for file in datafiles:
        L= smu.GetImageGeoRef(type,file)
        print L
        l=float(L[0][0])
        t=float(L[0][1])
        r=float(L[0][2])
        b=float(L[0][3])
        w=int(L[1][0])
        h=int(L[1][1])
        x=(r-l)/w
        y=(t-b)/h
        left.append(l)
        right.append(r)
        top.append(t)
        bottom.append(b)
        ratiox.append(x)
        ratioy.append(y)
        #获取左右上下边界
        dLeft=min(left)
        dRight=max(right)
        dTop=max(top)
        dBottom=min(bottom)
        #获取分辨率，影像最小分辨率作为数据集分辨率
        dRatioX = min(ratiox)
        dRatioY = min(ratioy)
        #计算影像数据集宽度和高度
        nWidth = int((dRight-dLeft)/dRatioX)
        nHeight = int((dTop-dBottom)/dRatioY)
        #重新计算，保证分辨率正确
        dRight=dLeft+dRatioX*nWidth
        dBottom=dTop-dRatioY*nHeight
        L = [nWidth, nHeight, dLeft, dTop, dRight, dBottom]
    return L

def toDB(server, user, pwd, engType, fileType, path):
    files=[]
    files=walkPath(fileType, path)
    if len(files)>0:
        L=[]
        L = calcDatasetInfo(fileType, files)
        pixType = smu.GetImagePixelFormatName(fileType, files[0])

        odsAlias=u'test'
        if len(L)==6:
            nWidth=L[0]
            nHeight=L[1]
            dLeft=L[2]
            dTop=L[3]
            dRight=L[4]
            dBottom=L[5]
            dtName=u'test'
            isOpen=smu.OpenDataSource(server,user,pwd, engType, odsAlias)
            smu.DeleteDataset(odsAlias, dtName)
            bCreate = smu.CreateDatasetRaster(odsAlias,dtName, u'Image', u'encDCT', pixType,nWidth,nHeight, dLeft, dTop,dRight,dBottom,256)
            for file in files:
                smu.AppendRasterFile(odsAlias,dtName,fileType, file)
                
            smu.CloseDataSource(odsAlias)

#=====================================
def writeLog(logPath, tmpstr):
    time_str = time.strftime("%Y-%m-%d %H:%M:%S ",time.localtime())
    logstr = str(tmpstr) + time_str +'\n'
    print(logstr)
    f = open(logPath, "a")
    f.write(logstr)
    f.close()

help =u"----------------------------------------------------------\n\
说明:可导入udb或oracle引擎\n\
导入到UDB用法: AppendRasterFile.py tif c:/data\n\
导入到Oracle用法: AppendRasterFile.py server user pwd tif c:/data\n\
----------------------------------------------------------\n"
if __name__=='__main__':
    reload(sys)
    sys.setdefaultencoding("utf-8")
	
    if len(sys.argv) == 3:
        engType=u'sceUDB'
        fileType=sys.argv[1]
        fileType=getType(fileType)
        print fileType
        path=sys.argv[2]
        udb = unicode(path+'/test.udb',"utf-8")
        udd = unicode(path+'/test.udd',"utf-8")
        if os.path.exists(udb):
            os.remove(udb)
        if os.path.exists(udd):
            os.remove(udd)                
        toDB(udb, u'', u'', engType, fileType, path)
        smu.Exit()#清空环境，释放内存
    elif len(sys.argv) == 6:
        engType=u'sceOraclePlus'
        server=sys.argv[1]
        user=sys.argv[2]
        pwd=sys.argv[3]
        fileType=sys.argv[4]
        fileType=getType(fileType)
        path=sys.argv[5]
        toDB(server, user, pwd, engType, fileType, path)
        smu.Exit()#清空环境，释放内存
    else:
        print help
        sys.exit()