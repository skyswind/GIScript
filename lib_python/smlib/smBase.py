#coding: utf-8
#基础类

import os
import sys
#import bin.smu as smu
import smu

#Rect2D
class rect:
    def __init__(self, left, top, right, bottom):
        self.left = left
        self.top = top
        self.right= right
        self.bottom = bottom
        self.width = right-left
        self.height = top-bottom
        self.area = self.width*self.height              #面积
        self.length = 2*(self.width+self.height)        #周长

#栅格文件信息
class imgFileInfo:
    def __init__(self):
        self.fileName = u''
        self.bounds = rect(0.0, 0.0, 0.0, 0.0)
        self.imgType = u'fileTIF'
        self.bandCount = 1
        self.pixelFormat = 8
        self.pixelFormatName = u'IPF_UNKNOWN'
        self.resX = 1.0
        self.resY = 1.0
        self.width = 0
        self.height = 0

    #输出影像信息
    def dump(self):
        print u'\n'
        print u'文件名：    ' + self.fileName
        print u'类型：      ' + self.imgType
        print u'波段数：    ' + str(self.bandCount)
        print u'像素位深：  ' + str(self.pixelFormat)
        print u'像素格式：  ' + self.pixelFormatName
        print u'宽度(像素)：' + str(self.width)
        print u'高度(像素)：' + str(self.height)
        print u'水平分辨率：' + str(self.resX)
        print u'垂直分辨率：' + str(self.resY)
        print u'范围        '
        print u'[左]：      ' + str(self.bounds.left)
        print u'[上]：      ' + str(self.bounds.top)
        print u'[右]：      ' + str(self.bounds.right)
        print u'[下]：      ' + str(self.bounds.bottom)
        print u'\n'

#下面是一些通用的函数

#根据栅格文件完整路径来获取文件的信息
def GetImgFileInfo(fileName,imgType):
    imgInfo = imgFileInfo()
    imgInfo.fileName = fileName
    imgInfo.imgType = imgType
    imgInfo.bandCount = smu.GetImageBandsCount(imgInfo.imgType,imgInfo.fileName)
    imgInfo.pixelFormat = smu.GetImagePixelFormat(imgInfo.imgType,imgInfo.fileName)
    imgInfo.pixelFormatName = smu.GetImagePixelFormatName(imgInfo.imgType,imgInfo.fileName)

    L = smu.GetImageGeoRef(imgInfo.imgType,imgInfo.fileName)
    imgInfo.bounds = rect(L[0][0], L[0][1],L[0][2],L[0][3])
    imgInfo.width = L[1][0];
    imgInfo.height = L[1][1];
    imgInfo.resX = imgInfo.bounds.width/float(imgInfo.width)
    imgInfo.resY = imgInfo.bounds.height/float(imgInfo.height)
    return imgInfo

#根据文件完整路径来获取文件类型（FileType）
def GetFileTypeByFileName(fileName):
    return smu.GetFileTypeByFileName(fileName)

#根据文件完整路径获取投影信息，并保存在文件中
#strType 文件类型;
#- fileTIF
#- fileIMG
#- fileBMP
#- fileJPG
#- fileGRD
#- fileRAW
#- fileUSGSGRID
#- fileSIT
#- fileArcinfoGrid
#- fileIDR
#strFilePath 输入文件全路径名;
#strPrjPath 输出文件全路径名;
def GetProjection(strType, strFilePath, strPrjPath):
    if smu.GetProjection(strType, strFilePath, strPrjPath):
        return True
    return False
    
#是否使用FME的转换能力; 如果安装了FME的插件、可选择使用FME进行数据转换.
#bUseFME 是否使用FME，0不使用，1作用;
def SetUseFME(bUseFME):
    smu.SetUseFME(bUseFME)
